# Copyright 2020, Boling Consulting Solutions
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
from twisted.internet import defer
from twisted.cred import error as credError
from twisted.cred.credentials import IUsernamePassword, IUsernameHashedPassword, \
    DigestedCredentials, UsernamePassword
from twisted.cred.checkers import ICredentialsChecker
from twisted.conch.checkers import UNIXPasswordDatabase, verifyCryptedPassword
from zope.interface import implementer

# TODO: Add the anonymous (anyone) credentials checker


@implementer(ICredentialsChecker)
class PasswordDictChecker:
    """ Credential checker that validates a username and password against a dictionary """
    credentialInterfaces = (IUsernamePassword, IUsernameHashedPassword,)

    def __init__(self, users_db, passwords_db):
        """
        a dict-like object mapping user names to passwords

        :param users_db:     (dict) 'username' -> 'full name'
        :param passwords_db: (dict) 'username' -> 'password' (plain text)
        """
        self._passwords = copy.deepcopy(passwords_db)
        self._users = copy.deepcopy(users_db)

    @property
    def users(self):
        """ Return a copy of the username -> fullname database """
        return copy.deepcopy(self._users)

    def requestAvatarId(self, credentials):              # pylint: disable=invalid-name
        """
        Validate credentials and produce an avatar ID.

        @param credentials: something which implements one of the interfaces in
        C{credentialInterfaces}.

        @return: a L{Deferred} which will fire with a L{bytes} that identifies
        an avatar, an empty tuple to specify an authenticated anonymous user
        (provided as L{twisted.cred.checkers.ANONYMOUS}) or fail with
        L{UnauthorizedLogin}. Alternatively, return the result itself.

        @see: L{twisted.cred.credentials}
        """
        username = credentials.username

        if username in self._passwords:
            if isinstance(credentials, DigestedCredentials):
                # Digest Authentications
                if credentials.checkPassword(self._passwords[username]):
                    return defer.succeed(username)

                return defer.fail(credError.UnauthorizedLogin("Bad password"))

            if isinstance(credentials, UsernamePassword):
                # Basic Authentication
                if credentials.password == self._passwords[username]:
                    return defer.succeed(username)

                return defer.fail(credError.UnauthorizedLogin("Bad password"))

        return defer.fail(credError.UnauthorizedLogin("No such user"))


@implementer(ICredentialsChecker)
class CryptedPasswordDictChecker:
    """ Similar to the PasswordDictChecker, but passwords are one-way encrypted"""
    credentialInterfaces = (IUsernamePassword, IUsernameHashedPassword,)

    def __init__(self, users_db, passwords_db):
        """
        a dict-like object mapping user names to passwords

        :param users_db:     (dict) 'username' -> 'full name'
        :param passwords_db: (dict) 'username' -> 'password' (encrpyted)
        """
        self._passwords = copy.deepcopy(passwords_db)
        self._users = copy.deepcopy(users_db)

    @property
    def users(self):
        """ Return a copy of the username -> fullname database """
        return copy.deepcopy(self._users)

    def requestAvatarId(self, credentials):              # pylint: disable=invalid-name
        """
        Validate credentials and produce an avatar ID.

        @param credentials: something which implements one of the interfaces in
        C{credentialInterfaces}.

        @return: a L{Deferred} which will fire with a L{bytes} that identifies
        an avatar, an empty tuple to specify an authenticated anonymous user
        (provided as L{twisted.cred.checkers.ANONYMOUS}) or fail with
        L{UnauthorizedLogin}. Alternatively, return the result itself.

        @see: L{twisted.cred.credentials}
        """
        username = credentials.username

        if username in self._passwords:
            if verifyCryptedPassword(self._passwords[username], credentials.password):
                return defer.succeed(username)

            return defer.fail(credError.UnauthorizedLogin("Bad password"))

        return defer.fail(credError.UnauthorizedLogin("No such user"))


@implementer(ICredentialsChecker)
class UNIXPasswordDatabaseChecker(UNIXPasswordDatabase):
    """ Uses Unix username/password."""
    credentialInterfaces = (IUsernamePassword, IUsernameHashedPassword,)

    def __init__(self):
        """passwords: a dict-like object mapping user names to passwords"""
        super().__init__()

    @property
    def users(self):
        """ Provide users property for realm control """
        # TODO: Future -> Return dict of username->full-usernames for tracing/log purposes
        return None

    def requestAvatarId(self, credentials):         # pylint: disable=invalid-name
        """
        Validate credentials and produce an avatar ID.

        @param credentials: something which implements one of the interfaces in
        C{credentialInterfaces}.

        @return: a L{Deferred} which will fire with a L{bytes} that identifies
        an avatar, an empty tuple to specify an authenticated anonymous user
        (provided as L{twisted.cred.checkers.ANONYMOUS}) or fail with
        L{UnauthorizedLogin}. Alternatively, return the result itself.

        @see: L{twisted.cred.credentials}
        """
        # Get from wrapped checker.  Later will tie this into an access logger that
        # I would like to provide in a future release

        if isinstance(credentials, UsernamePassword):
            avatar = super().requestAvatarId(credentials)

        elif isinstance(credentials, DigestedCredentials):
            username = credentials.username
            # TODO: Need to decode credentials..  Work in progress
            password = 'something'

            avatar = super().requestAvatarId(UsernamePassword(username, password))

        else:
            return defer.fail(credError.UnauthorizedLogin("unable to validate credentials"))

        def successful(username):
            # TODO: Add anything extra here
            return username

        def unauthorized(reason):
            # TODO: Add anything extra here
            if isinstance(reason, credError.UnauthorizedLogin):
                return reason

            return defer.fail(credError.UnauthorizedLogin("Access denied: {}".format(reason)))

        return avatar.addCallbacks(successful, unauthorized)
