# gemato: OpenPGP verification support
# vim:fileencoding=utf-8
# (c) 2017-2020 Michał Górny
# Licensed under the terms of 2-clause BSD license

import base64
import datetime
import email.utils
import errno
import hashlib
import logging
import os
import os.path
import shutil
import subprocess
import tempfile
import urllib.parse
import warnings

from gemato.exceptions import (
    OpenPGPNoImplementation,
    OpenPGPVerificationFailure,
    OpenPGPExpiredKeyFailure,
    OpenPGPRevokedKeyFailure,
    OpenPGPKeyImportError,
    OpenPGPKeyListingError,
    OpenPGPKeyRefreshError,
    OpenPGPUnknownSigFailure,
    OpenPGPUntrustedSigFailure,
    OpenPGPSigningFailure,
    )

try:
    import requests
except ImportError:
    requests = None

try:
    import pgpy
except ImportError:
    pgpy = None


GNUPG = os.environ.get('GNUPG', 'gpg')
GNUPGCONF = os.environ.get('GNUPGCONF', 'gpgconf')


class OpenPGPSignatureData:
    __slots__ = ['fingerprint', 'timestamp', 'expire_timestamp',
                 'primary_key_fingerprint']

    def __init__(self, fingerprint, timestamp, expire_timestamp,
                 primary_key_fingerprint):
        self.fingerprint = fingerprint
        self.timestamp = timestamp
        self.expire_timestamp = expire_timestamp
        self.primary_key_fingerprint = primary_key_fingerprint


ZBASE32_TRANSLATE = bytes.maketrans(
    b'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567',
    b'ybndrfg8ejkmcpqxot1uwisza345h769')


def get_wkd_url(email):
    localname, domain = email.split('@', 1)
    b32 = (
        base64.b32encode(
            hashlib.sha1(localname.encode('utf8').lower()).digest())
        .translate(ZBASE32_TRANSLATE).decode('ASCII'))
    return (f'https://{domain.lower()}/.well-known/openpgpkey/hu/'
            f'{b32}?l={urllib.parse.quote(localname)}')


class SystemGPGEnvironment:
    """
    OpenPGP environment class that uses the global OpenPGP environment
    (user's home directory or GNUPGHOME).
    """

    __slots__ = ['debug']

    def __init__(self, debug=False, proxy=None):
        self.debug = debug

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_cb):
        pass

    def close(self):
        pass

    def import_key(self, keyfile, trust=True):
        """
        Import a public key from open file @keyfile. The file should
        be open for reading in binary mode, and oriented
        at the beginning.
        """

        raise NotImplementedError(
            'import_key() is not implemented by this OpenPGP provider')

    def refresh_keys(self, allow_wkd=True, keyserver=None):
        """
        Update the keys from their assigned keyservers. This should be called
        at start of every execution in order to ensure that revocations
        are respected. This action requires network access.

        @allow_wkd specifies whether WKD can be used to fetch keys. This is
        experimental but usually is more reliable than keyservers.  If WKD
        fails to fetch *all* keys, gemato falls back to keyservers.

        @keyserver may be used to force an alternate keyserver. If its present,
        it should specify a keyserver URL.
        """

        raise NotImplementedError(
            'refresh_keys() is not implemented by this OpenPGP provider')

    def _parse_gpg_ts(self, ts):
        """
        Parse GnuPG status timestamp that can either be time_t value
        or ISO 8601 timestamp.
        """
        # that's how upstream tells us to detect this
        if 'T' in ts:
            # TODO: is this correct for all cases? is it localtime?
            return datetime.datetime.strptime(ts, '%Y%m%dT%H%M%S')
        elif ts == '0':
            # no timestamp
            return None
        else:
            return datetime.datetime.utcfromtimestamp(int(ts))

    def verify_file(self, f):
        """
        Perform an OpenPGP verification of Manifest data in open file @f.
        The file should be open in text mode and set at the beginning
        (or start of signed part). Raises an exception if the verification
        fails.
        """

        exitst, out, err = self._spawn_gpg(
            [GNUPG, '--batch', '--status-fd', '1', '--verify'],
            f.read().encode('utf8'),
            raise_on_error=OpenPGPVerificationFailure)

        is_good = False
        is_trusted = False
        sig_data = None

        # process the output of gpg to find the exact result
        for line in out.splitlines():
            if line.startswith(b'[GNUPG:] GOODSIG'):
                is_good = True
            elif line.startswith(b'[GNUPG:] EXPKEYSIG'):
                raise OpenPGPExpiredKeyFailure(
                    err.decode('utf8', errors='backslashreplace'))
            elif line.startswith(b'[GNUPG:] REVKEYSIG'):
                raise OpenPGPRevokedKeyFailure(
                    err.decode('utf8', errors='backslashreplace'))
            elif line.startswith(b'[GNUPG:] VALIDSIG'):
                spl = line.split(b' ')
                assert len(spl) >= 12
                fp = spl[2].decode('utf8')
                ts = self._parse_gpg_ts(spl[4].decode('utf8'))
                expts = self._parse_gpg_ts(spl[5].decode('utf8'))
                pkfp = spl[11].decode('utf8')

                sig_data = OpenPGPSignatureData(fp, ts, expts, pkfp)
            elif line.startswith(b'[GNUPG:] TRUST_'):
                spl = line.split(b' ', 2)
                if spl[1] in (b'TRUST_MARGINAL',
                              b'TRUST_FULL',
                              b'TRUST_ULTIMATE'):
                    is_trusted = True

        # require both GOODSIG and VALIDSIG
        if not is_good or sig_data is None:
            raise OpenPGPUnknownSigFailure(
                err.decode('utf8', errors='backslashreplace'))
        if not is_trusted:
            raise OpenPGPUntrustedSigFailure(
                err.decode('utf8', errors='backslashreplace'))
        return sig_data

    def clear_sign_file(self, f, outf, keyid=None):
        """
        Create an OpenPGP cleartext signed message containing the data
        from open file @f, and writing it into open file @outf.
        Both files should be open in text mode and set at the appropriate
        position. Raises an exception if signing fails.

        Pass @keyid to specify the key to use. If not specified,
        the implementation will use the default key.
        """

        args = []
        if keyid is not None:
            args += ['--local-user', keyid]
        exitst, out, err = self._spawn_gpg(
            [GNUPG, '--batch', '--clearsign'] + args,
            f.read().encode('utf8'),
            raise_on_error=OpenPGPSigningFailure)

        outf.write(out.decode('utf8'))

    def _spawn_gpg(self, argv, stdin='', env_override={},
                   raise_on_error=None):
        env = os.environ.copy()
        env['TZ'] = 'UTC'
        env.update(env_override)

        try:
            p = subprocess.Popen(argv,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 env=env)
        except FileNotFoundError:
            raise OpenPGPNoImplementation('install gpg')

        out, err = p.communicate(stdin)
        if raise_on_error is not None and p.wait() != 0:
            raise raise_on_error(
                err.decode('utf8', errors='backslashreplace'))
        return (p.wait(), out, err)


def _rmtree_error_handler(func, path, exc_info):
    # ignore ENOENT -- it probably means a race condition between
    # us and gpg-agent cleaning up after itself
    # also non-empty directory due to races, and EBUSY for NFS:
    # https://bugs.gentoo.org/684172
    if (not isinstance(exc_info[1], OSError)
            or exc_info[1].errno not in (errno.ENOENT,
                                         errno.ENOTEMPTY,
                                         errno.EEXIST,
                                         errno.EBUSY)):
        raise exc_info[1]


class IsolatedGPGEnvironment(SystemGPGEnvironment):
    """
    An isolated environment for OpenPGP routines. Used to get reliable
    verification results independently of user configuration.

    Remember to close() in order to clean up the temporary directory,
    or use as a context manager (via 'with').
    """

    __slots__ = ['_home', 'proxy']

    def __init__(self, debug=False, proxy=None):
        super().__init__(debug=debug)
        self.proxy = proxy
        self._home = tempfile.mkdtemp(prefix='gemato.')

        with open(os.path.join(self._home, 'dirmngr.conf'), 'w') as f:
            f.write(f'''# autogenerated by gemato

# honor user's http_proxy setting
honor-http-proxy

# enable debugging, in case we needed it
log-file {os.path.join(self._home, 'dirmngr.log')}
debug-level guru
''')
        with open(os.path.join(self._home, 'gpg.conf'), 'w') as f:
            f.write('''# autogenerated by gemato

# we set validity directly on keys
trust-model direct
''')
        with open(os.path.join(self._home, 'gpg-agent.conf'), 'w') as f:
            f.write(f'''# autogenerated by gemato

# avoid any smartcard operations, we are running in isolation
disable-scdaemon

# enable debugging, in case we needed it
log-file {os.path.join(self._home, 'gpg-agent.log')}
debug-level guru
''')

    def __exit__(self, exc_type, exc_value, exc_cb):
        if self._home is not None:
            self.close()

    def clone(self):
        return IsolatedGPGEnvironment(debug=self.debug, proxy=self.proxy)

    def close(self):
        if self._home is not None:
            ret, sout, serr = self._spawn_gpg(
                [GNUPGCONF, '--kill', 'all'])
            if ret != 0:
                logging.warning(
                    f'{GNUPGCONF} --kill failed:\n'
                    f'{serr.decode("utf8", errors="backslashescape")}')
            if not self.debug:
                # we need to loop due to ENOTEMPTY potential
                while os.path.isdir(self._home):
                    shutil.rmtree(self._home,
                                  onerror=_rmtree_error_handler)
            else:
                logging.debug(f'GNUPGHOME left for debug purposes: '
                              f'{self._home}')
            self._home = None

    def import_key(self, keyfile, trust=True):
        exitst, out, err = self._spawn_gpg(
            [GNUPG, '--batch', '--import', '--status-fd', '1'],
            keyfile.read(),
            raise_on_error=OpenPGPKeyImportError)

        if trust:
            fprs = set()
            for line in out.splitlines():
                if line.startswith(b'[GNUPG:] IMPORT_OK'):
                    fprs.add(line.split(b' ')[3].decode('ASCII'))

            ownertrust = ''.join(f'{fpr}:6:\n' for fpr in fprs).encode('utf8')
            exitst, out, err = self._spawn_gpg(
                [GNUPG, '--batch', '--import-ownertrust'],
                ownertrust,
                raise_on_error=OpenPGPKeyImportError)

    def list_keys(self):
        """
        List fingerprints and UIDs of all keys in keyring

        Returns a mapping from fingerprint (as a string) to an iterable
        of UIDs.
        """

        exitst, out, err = self._spawn_gpg(
            [GNUPG, '--batch', '--with-colons', '--list-keys'],
            raise_on_error=OpenPGPKeyListingError)

        prev_pub = None
        fpr = None
        ret = {}

        for line in out.splitlines():
            # were we expecting a fingerprint?
            if prev_pub is not None:
                if line.startswith(b'fpr:'):
                    fpr = line.split(b':')[9].decode('ASCII')
                    if not fpr.endswith(prev_pub):
                        raise OpenPGPKeyListingError(
                            f'Incorrect fingerprint {fpr} for key '
                            f'{prev_pub}')
                    logging.debug(
                        f'list_keys(): fingerprint: {fpr}')
                    ret[fpr] = []
                    prev_pub = None
                else:
                    raise OpenPGPKeyListingError(
                        f'No fingerprint in GPG output, instead got: '
                        f'{line}')
            elif line.startswith(b'pub:'):
                # wait for the fingerprint
                prev_pub = line.split(b':')[4].decode('ASCII')
                logging.debug(f'list_keys(): keyid: {prev_pub}')
            elif line.startswith(b'uid:'):
                if fpr is None:
                    raise OpenPGPKeyListingError(
                        f'UID without key in GPG output: {line}')
                uid = line.split(b':')[9]
                _, addr = email.utils.parseaddr(
                    uid.decode('utf8', errors='replace'))
                if '@' in addr:
                    logging.debug(f'list_keys(): UID: {addr}')
                    ret[fpr].append(addr)
                else:
                    logging.debug(
                        f'list_keys(): ignoring UID without mail: '
                        f'{uid!r}')

        return ret

    def refresh_keys_wkd(self):
        """
        Attempt to fetch updated keys using WKD.  Returns true if *all*
        keys were successfully found.  Otherwise, returns false.
        """
        if requests is None:
            logging.debug('refresh_keys_wkd(): failing because requests'
                          'module is missing')
            return False

        # list all keys in the keyring
        keys = self.list_keys()
        if not keys:
            logging.debug('refresh_keys_wkd(): no keys found')
            return False
        addrs = set()
        for key, uids in keys.items():
            if not uids:
                logging.debug(
                    f'refresh_keys_wkd(): failing due to no UIDs on '
                    f'key {key}')
                return False
            addrs.update(uids)
        keys = set(keys)

        data = b''
        proxies = {}
        if self.proxy is not None:
            proxies = {
                'http': self.proxy,
                'https': self.proxy,
            }
        for a in addrs:
            url = get_wkd_url(a)
            try:
                resp = requests.get(url, proxies=proxies)
                resp.raise_for_status()
            except (requests.exceptions.ConnectionError,
                    requests.exceptions.HTTPError,
                    ) as e:
                logging.debug(f'refresh_keys_wkd(): failing due to failed '
                              f'request for {url}: {e}')
                return False
            data += resp.content

        exitst, out, err = self._spawn_gpg(
            [GNUPG, '--batch', '--import', '--status-fd', '1'],
            data,
            raise_on_error=OpenPGPKeyRefreshError)

        # we need to explicitly ensure all keys were fetched
        for line in out.splitlines():
            if line.startswith(b'[GNUPG:] IMPORT_OK'):
                fpr = line.split(b' ')[3].decode('ASCII')
                logging.debug(
                    f'refresh_keys_wkd(): import successful for key: {fpr}')
                if fpr in keys:
                    keys.remove(fpr)
                else:
                    # we need to delete unexpected keys
                    exitst, out, err = self._spawn_gpg(
                        [GNUPG, '--batch', '--delete-keys', fpr],
                        raise_on_error=OpenPGPKeyRefreshError)
        if keys:
            logging.debug(
                f'refresh_keys_wkd(): failing due to non-updated keys: '
                f'{keys}')
            return False

        return True

    def refresh_keys_keyserver(self, keyserver=None):
        ks_args = []
        if keyserver is not None:
            ks_args = ['--keyserver', keyserver]

        exitst, out, err = self._spawn_gpg(
            [GNUPG, '--batch', '--refresh-keys'] + ks_args,
            raise_on_error=OpenPGPKeyRefreshError)

    def refresh_keys(self, allow_wkd=True, keyserver=None):
        logging.debug(f'refresh_keys(allow_wkd={allow_wkd}, '
                      f'keyserver={keyserver}) called')

        if allow_wkd and self.refresh_keys_wkd():
            return

        self.refresh_keys_keyserver(keyserver=keyserver)

    @property
    def home(self):
        assert self._home is not None
        return self._home

    def _spawn_gpg(self, *args, **kwargs):
        env_override = {'GNUPGHOME': self.home}
        if self.proxy is not None:
            env_override['http_proxy'] = self.proxy
        assert 'env_override' not in kwargs
        kwargs['env_override'] = env_override
        return super()._spawn_gpg(*args, **kwargs)


class PGPyEnvironment:
    """Stand-alone environment using pgpy library"""

    __slots__ = ['debug', 'keyring', 'proxy']

    def __init__(self, debug=False, proxy=None):
        if pgpy is None:
            raise OpenPGPNoImplementation('install PGPy')
        self.debug = debug
        self.keyring = pgpy.PGPKeyring()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_cb):
        pass

    def close(self):
        pass

    def import_key(self, keyfile):
        with warnings.catch_warnings(record=True) as warns:
            try:
                key_res = pgpy.PGPKey.from_blob(keyfile.read())
            except ValueError as e:
                raise OpenPGPKeyImportError(
                    f'OpenPGP key import failed: {e}')
        fprs = []
        for k in key_res[1].values():
            fprs.extend(self.keyring.load(k))

        for w in warns:
            if str(w.message) == 'Incorrect crc24':
                raise OpenPGPKeyImportError(
                    f'OpenPGP key import failed: {w.message}')

        for fpr in fprs:
            with self.keyring.key(fpr) as k:
                if k.parent is not None:
                    try:
                        verifies = k.parent.verify(k)
                    except pgpy.errors.PGPError:
                        logging.debug(
                            f'Rejecting subkey {fpr} due to missing sig')
                        self.keyring.unload(k)
                    else:
                        if not verifies:
                            logging.debug(
                                f'Rejecting subkey {fpr} since parent '
                                f'key signature does not check out')
                            self.keyring.unload(k)
                for uid in k.userids:
                    if uid.selfsig is None:
                        raise OpenPGPKeyImportError(
                            f'Self-signature on {uid} missing')
                    if not k.verify(uid):
                        raise OpenPGPKeyImportError(
                            f'Self-signature on {uid} does not verify')

    def verify_file(self, f):
        msg = pgpy.PGPMessage.from_blob(f.read())
        assert msg.is_signed
        assert len(msg.signatures) == 1
        assert len(msg.signers) == 1

        signer, = msg.signers
        try:
            with self.keyring.key(signer) as k:
                pk = k
                if k.parent is not None:
                    pk = k.parent
                assert pk.parent is None

                vr = k.verify(msg)
                if not vr:
                    raise OpenPGPVerificationFailure(
                        f'Bad signature made by key {k.fingerprint}')
                now = datetime.datetime.utcnow()
                sig_expire = msg.signatures[0].expires_at
                if sig_expire is not None and sig_expire < now:
                    raise OpenPGPVerificationFailure(
                        f'Signature expired at {msg.signatures[0].expires_at}')
                if k.expires_at is not None and k.expires_at < now:
                    raise OpenPGPExpiredKeyFailure(
                        f'Key {k.fingerprint} expired at {k.expires_at}')
                if pk.expires_at is not None and pk.expires_at < now:
                    raise OpenPGPExpiredKeyFailure(
                        f'Primary key {pk.fingerprint} expired '
                        f'at {k.expires_at}')
                if list(k.revocation_signatures):
                    raise OpenPGPRevokedKeyFailure(
                        f'Key {pk.fingerprint} was revoked')
                if list(pk.revocation_signatures):
                    raise OpenPGPRevokedKeyFailure(
                        f'Primary key {pk.fingerprint} was revoked')
                return OpenPGPSignatureData(
                    k.fingerprint,
                    msg.signatures[0].created,
                    msg.signatures[0].expires_at,
                    pk.fingerprint)
        except KeyError:
            raise OpenPGPVerificationFailure(
                f'Key {signer} not in keyring')


OpenPGPSystemEnvironment = SystemGPGEnvironment
OpenPGPEnvironment = IsolatedGPGEnvironment
