#!/usr/bin/env python3
""" Methods for interacting with GUS.

    Originally from bin/chatter.py

    Author Ankush Gulati
    Original Authors Philip Bergen, Richard Rak
"""
import ast
import codecs
import json
import os
import sys
import requests

from re import sub
from urllib.parse import quote


class GUS(object):
    AUTH_CACHE = None
    HOST = 'https://gus.my.salesforce.com'
    API = 'services/%s'

    def __init__(self, host=HOST, api=API):
        # TODO Enable HTTPS verification
        try:
            requests.packages.urllib3.disable_warnings()
        except AttributeError:
            pass
        self._url = host + '/' + api

    def __call__(self, target, method='GET', headers=None, body=None, **params):
        req = requests.request(method,
                               self._url % target,
                               headers=headers,
                               data=body,
                               params=params)
        req.raise_for_status()
        if 204 == req.status_code:
            return req.status_code
        return req.json()

    def __check_py_tls12(self):
        from sys import platform as _platform
        if _platform == "darwin":
            import ssl
            if not hasattr(ssl, 'PROTOCOL_TLSv1_2'):
                print('*** INFO: BLT Chatter setup for mac is currently BROKEN.         ')
                print('*** INFO: The BLT team is working on a fix: http://sfdc.co/cunkl0')
                raise ssl.SSLError

    def __get_auth_cache(self):
        auth_cache = os.environ['HOME'] + '/.chatter'
        if not os.path.exists(auth_cache):
            print('*** ERROR: Missing ' + auth_cache)
            print('           Please run the following command to setup chatter:')
            print('               Gus --setup')
            sys.exit(1)
        return auth_cache

    def __read_auth_cache(self):
        if not self.AUTH_CACHE:
            self.AUTH_CACHE = json.load(open(self.__get_auth_cache()))
        return self.AUTH_CACHE

    def __get_oauth(self, request_input, force=False):
        """Returns cached oauth objects. Force refreshes the token in the cache."""
        auth_cache = self.__get_auth_cache()

        def store_cache(data):
            with open(auth_cache, 'w') as fout:
                os.chmod(auth_cache, 0o600)
                json.dump(data, fout)

            self.AUTH_CACHE = data

        if 'username' not in request_input or request_input['username'] is None:
            request_input['username'] = self.gus_resolve_username()

        if not request_input['username'].endswith('@gus.com'):
            request_input['username'] = request_input['username'] + '@gus.com'

        cache = request_input['cache']
        self.username = request_input['username']
        if not force and request_input['username'] in cache:
            return cache[request_input['username']]

        if 'client' not in cache:
            print('*** ERROR: Missing content in ' + auth_cache + '.')

        if 'password' not in request_input or request_input['password'] is None:
            request_input['password'] = self.gus_resolve_password()

        cache['client']['username'] = request_input['username']
        pw = cache['client']['password']
        if pw != '-':
            if isinstance(request_input['password'], str):
                request_input['password'] = request_input['password'].encode(
                    sys.stdin.encoding or sys.getdefaultencoding())
            cache['client']['password'] = codecs.encode(
                codecs.encode(request_input['password'], 'bz2'), 'base64')

        params = {
            'username': request_input['username'],
            'password': request_input['password'],
            'grant_type': 'password',
            'client_id': cache['client']['id'],
            'client_secret': cache['client']['secret']
        }

        try:
            cache[request_input['username']] = self('oauth2/token', 'POST', **params)
        except requests.exceptions.HTTPError as e:
            if 400 == e.response.status_code and 'invalid_grant' == ast.literal_eval(
                    e.response.text)['error']:
                # Password is invalid
                print('*** ERROR: Request failed. ', str(e).split('=')[0] + '\n')
                print('           Password is deleted from',
                      auth_cache + '. Set a new password with')
                print('               Gus --setup force')
                del cache['client']['password']
                store_cache(cache)
                sys.exit(1)
            else:
                raise e
        # no need to store password after obtaining oauth token
        cache['client']['password'] = '-'
        store_cache(cache)
        return cache[request_input['username']]

    def __set_username_password(self, request, username=None, password=None, strict=False):
        """
        Resolves the GUS user and password, updating the request_input structure

        :param request: the request object to resolve the username and password into
        :param username: the username to use, instead of the cached value
        :param password: the password to use, instead of the cached value
        :param strict: if strict, password is not used or cached
        :return: a tuple containing the username, unencoded password and encoded password
                that was set for the gus user
        """
        raw_password = password
        encoded_password = None
        request['cache'] = self.__read_auth_cache()

        if not username:
            username = self.gus_resolve_username()
        if not raw_password:
            raw_password = self.gus_resolve_password(strict)

        if raw_password != '-':
            encoded_password = codecs.encode(
                codecs.encode(raw_password.encode(sys.stdin.encoding or sys.getdefaultencoding()),
                              'bz2'), 'base64')

        request['cache']['client']['username'] = username
        request['cache']['client']['password'] = encoded_password
        return username, raw_password, encoded_password

    def gus_resolve_username(self):
        """
        Resolves the gus username using the auth cache, or if not available,
        the results of 'whoami'@gus.com is returned.

        :return: the GUS username to send to the server
        """
        cache = self.__read_auth_cache()

        if cache and 'client' in cache and cache['client'].get('username'):
            username = cache['client']['username']
        else:
            username = os.popen('whoami').read().strip() + '@gus.com'

        return username

    def gus_resolve_password(self, strict=False):
        """
        Resolves the gus password using the auth cache
        :return: the GUS password to send to the server
        """

        raw_password = None

        cache = self.__read_auth_cache()
        encoded_password = cache['client'].get('password')
        if encoded_password:
            if encoded_password == '-' and strict:
                return '-'
            elif encoded_password != '-':
                try:
                    # use bytes and decode back to string
                    if not isinstance(encoded_password, bytes):
                        encoded_password = encoded_password.encode(sys.stdin.encoding or
                                                                   sys.getdefaultencoding())
                    raw_password = codecs.decode(codecs.decode(encoded_password, 'base64'),
                                                 'bz2').decode(sys.stdin.encoding or
                                                               sys.getdefaultencoding())
                except IOError:
                    print('*** WARNING: Could not decode password from ~/.chatter, ignored')

        if raw_password is None:
            # Password is invalid
            import getpass
            print('*** INFO: Fetching new GUS token, please enter your network password.')
            return getpass.getpass(prompt='SSO Password:').rstrip()
            # Temporarily do not fail
            # TODO: use pass to fetch n/w password
            # print '*** ERROR: Request failed. \n'
            # print '    OAuth token invalid in', self.__get_auth_cache() + '. Get a new token with'
            # print '               Gus --setup force'
            # sys.exit(1)
        return raw_password

    def gus_execute_request(self, request):
        """
        Executes the given request object (obtained via a call to gus_create_request) against the server.  If
        the server responds with a 401 response code, a single attempt will be made to retrieve a new oauth token.
        All non-okay exit codes (not within the range 200 - 299) will result in debug output and a return of None.
        :return: an object containing the results of JSON decoding the response from the GUS service for all
        okay exit codes (within the range 200 - 299) except for exit code 204 which has no response body.
        """

        def gus_response():
            headers = {
                'Authorization': 'OAuth ' + token['access_token'],
                'Content-type': 'application/json'
            }
            return self(target=request['path'],
                        method=request['method'],
                        headers=headers,
                        body=None if request['body'] is None else json.dumps(request['body']),
                        **({} if request['params'] is None else request['params']))

        try:
            self.__check_py_tls12()
            token = self.__get_oauth(request)
            resp = gus_response()
        except requests.exceptions.HTTPError as e:
            if 401 == e.response.status_code:
                try:
                    token = self.__get_oauth(request, True)
                    resp = gus_response()
                except requests.exceptions.HTTPError as e:
                    if 401 == e.response.status_code:
                        print(f'*** ERROR: Request failed, OAuth is broken: {e}\n'
                              f'          for {e.request.url}\n')
                        return None
                    else:
                        raise e
            else:
                raise e

        if request['debug']:
            request['response'] = resp
            print("*** INFO: " + json.dumps(request, indent=4, separators=(',', ': ')))
        return resp

    def gus_execute(self,
                    method,
                    path,
                    body=None,
                    params=None,
                    username=None,
                    password=None,
                    debug=False,
                    strict=True):
        """
        Executes a request again the GUS service.

        :param method: the HTTP method to pass.
        :param path: the URI path to pass to the server
        :param body: the message body to send to the server
        :param params: params to send to the server
        :param username: the username to use when communicating with the server (default is use OAuth cached credentials)
        :param password: the password to use when communicating with the server (default is use OAuth cached credentials)
        :param debug: whether or not to enable debug output
        :param strict: if strict, password is not used to get/post to GUS
        :return: an object containing the JSON decoded response from the GUS service.
        """
        request = {'method': method, 'path': path, 'body': body, 'params': params, 'debug': debug}
        self.__set_username_password(request, username, password, strict)
        return self.gus_execute_request(request)

    def gus_query(self, query_string, debug=False):
        """
        Executes the given query string against gus, returning the results as json.  If there is an
        error executing the query, the request and response will be dumped and the program will exit.

        :param query_string: the query string to execute
        :param debug: whether or not to enable debug output
        :return: the json result from the server
        """
        encoded_query_string = quote(sub("\s+", " ", query_string))
        query_url = "data/v29.0/query?q=" + encoded_query_string
        return self.gus_execute('GET', query_url, debug=debug)

    def gus_get_record(self, record_type, record_id, debug=False):
        """
        Retrieves a single record from GUS with the given record_type and record_id.  If there is an
        error retrieving the record, the request and response will be dumped and the program will exit.

        :param record_type: the GUS record type to retrieve
        :param record_id: the GUS record id to retrieve
        :param debug: whether or not to enable debug output
        :return: the json result from the server
        """
        query_url = "data/v29.0/sobjects/%s/%s" % (record_type, record_id)
        return self.gus_execute('GET', query_url, debug=debug)
