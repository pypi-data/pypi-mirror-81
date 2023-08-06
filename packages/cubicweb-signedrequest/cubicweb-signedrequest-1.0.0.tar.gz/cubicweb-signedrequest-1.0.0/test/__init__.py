# copyright 2013-2017 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import hmac
from email.utils import formatdate
from operator import itemgetter
import time

from cubicweb.web.controller import Controller
import cubicweb.devtools  # noqa
from cubicweb_signedrequest import includeme
from cubicweb_signedrequest.tools import HEADERS_TO_SIGN


class TestController(Controller):
    __regid__ = "testauth"

    def publish(self, rset):
        if self._cw.user.login == self._cw.form.get("expected", "admin"):
            return b"VALID"
        else:
            return b"INVALID"


class SignedRequestBaseTC(object):
    test_db_id = "signedresquest"

    def includeme(self, config):
        includeme(config)

    def setup_database(self):
        with self.admin_access.repo_cnx() as cnx:
            with cnx.security_enabled(False, False):
                cnx.execute(
                    'INSERT AuthToken T: T token "my precious", '
                    "                    T token_for_user U, "
                    '                    T id "admin", '
                    "                    T enabled True"
                    ' WHERE U login "admin"'
                )
                cnx.commit()

    def _assert_auth(self, req, result):
        raise NotImplementedError()

    def _assert_auth_failed(self, req, result):
        raise NotImplementedError()

    def _build_string_to_sign(self, request):
        raise NotImplementedError()

    def _build_signature(self, id, string_to_sign):
        with self.admin_access.client_cnx() as cnx:
            rset = cnx.execute("Any K WHERE T id %(id)s, T token K", {"id": id})
            assert rset
            return hmac.new(
                rset[0][0].encode("utf-8"), string_to_sign, digestmod="sha512"
            ).hexdigest()

    def _test_header_format(
        self,
        method,
        login,
        http_method="GET",
        signature=None,
        headers=None,
        content=None,
        url="/testauth",
        **params,
    ):
        raise NotImplementedError()

    def get_valid_authdata(self, headers=None):
        if headers is None:
            headers = {}
        headers.setdefault(
            "Content-SHA512",
            "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13"
            "c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e",
        )
        headers.setdefault("Content-Type", "application/xhtml+xml")
        headers.setdefault("Date", formatdate(usegmt=True))
        return headers

    def test_login(self):
        result, req = self._test_header_format(
            method="Cubicweb",
            login="admin",
        )
        self._assert_auth(req, result)

    def test_bad_date(self):
        for date in (
            formatdate(time.time() + 1000, usegmt=True),
            formatdate(time.time() - 1000, usegmt=True),
            "toto",
        ):
            headers = {"Date": date}

            result, req = self._test_header_format(
                method="Cubicweb", login="admin", headers=headers
            )
            self._assert_auth_failed(req, result)

    def test_bad_http_auth_method(self):
        signature = self._build_signature("admin", b"")
        result, req = self._test_header_format(
            method="AWS", login="admin", signature=signature
        )
        self._assert_auth_failed(req, result)

    def test_bad_signature(self):
        result, req = self._test_header_format(
            method="Cubicweb", login="admin", signature="YYY"
        )
        self._assert_auth_failed(req, result)

    def test_deactivated_token(self):
        with self.admin_access.repo_cnx() as cnx:
            cnx.execute(
                "SET T enabled False WHERE " "T token_for_user U, U login %(l)s",
                {"l": "admin"},
            )
            cnx.commit()
        result, req = self._test_header_format(method="Cubicweb", login="admin")
        self._assert_auth_failed(req, result)

    def test_bad_signature_url(self):
        def bad_build_string_to_sign(req):
            get_headers = itemgetter(*HEADERS_TO_SIGN)
            return "".join(get_headers(req.headers))

        orig = self._build_string_to_sign
        self._build_string_to_sign = bad_build_string_to_sign
        try:
            result, req = self._test_header_format(
                method="Cubicweb", login="admin", signature="YYY"
            )
            self._assert_auth_failed(req, result)
        finally:
            self._build_string_to_sign = orig

    def test_post_http_request_signature(self):
        headers = {
            "Content-SHA512": "f1bb758ab06b3b4e6c5b0545d827cbc4958c2b0d0b242bdcae2562a517220"
            "0f1c603b69964b99c108ca04a3e4f670f8bba2c4cb8f1490112f33438520ea5e3f7",
            "Content-Type": "application/x-www-form-urlencoded",
            "Date": formatdate(usegmt=True),
        }
        result, req = self._test_header_format(
            method="Cubicweb", login="admin", http_method="POST", headers=headers
        )
        self._assert_auth(req, result)

    def test_post_http_request_signature_with_multipart(self):
        date = formatdate(usegmt=True)
        headers = {
            "Content-SHA512": "28a505eb101c411f40a36b19d24c008b7f8d4945ec30e17b7fd6d60fd0b27fbf80bb"
            "69039ab64e6940f09bf293901b363650195a9437c110ab8825381f1ae9cf",
            "Content-Type": "multipart/form-data; "
            "boundary=a71da6eca73a45459439dd288f8185a4",
            "Date": date,
        }
        # string_to_sign = ('POSThttp://testing.fr/cubicweb/testauth?'
        #                   'key1=value1f47787068b27ee123d28392f2d21cf70'
        #                   'multipart/form-data; '
        #                   'boundary=a71da6eca73a45459439dd288f8185a4%s'%date)
        body = (
            "--a71da6eca73a45459439dd288f8185a4\r\n"
            "Content-Disposition: form-data; "
            'name="datak1"\r\n\r\nsome content\r\n'
            "--a71da6eca73a45459439dd288f8185a4\r\n"
            'Content-Disposition: form-data; name="filename"; '
            'filename="filename"\r\n'
            "Content-Type: application/octet-stream\r\n\r\nabc\r\n"
            "--a71da6eca73a45459439dd288f8185a4--\r\n"
        ).encode("utf-8")
        result, req = self._test_header_format(
            method="Cubicweb",
            login="admin",
            content=body,
            http_method="POST",
            headers=headers,
            url="/testauth?key1=value1",
        )
        self._assert_auth(req, result)

    def test_post_http_request_signature_with_data(self):
        date = formatdate(usegmt=True)
        headers = {
            "Content-SHA512": "65c256c639bd6dd483be341831c19a3996954901bb2a07f79593f3e3af569"
            "2559bdb124d099c2b92ced7e59b7ed02d3b7f42d50740d999bebd91983db2842762",
            "Date": date,
        }
        # string_to_sign = ('POSThttp://testing.fr/cubicweb/testauth?'
        #                 'key1=value19893532233caff98cd083a116b013c0b%s'%date)
        body = b"some content"
        result, req = self._test_header_format(
            method="Cubicweb",
            login="admin",
            content=body,
            http_method="POST",
            headers=headers,
            url="/testauth?key1=value1",
        )
        self._assert_auth(req, result)

    def test_deactivated_user(self):
        with self.admin_access.repo_cnx() as cnx:
            user = cnx.find("CWUser", login="admin").one()
            flowable = user.cw_adapt_to("IWorkflowable")

            flowable.fire_transition("deactivate")
            cnx.commit()

            result, req = self._test_header_format(method="Cubicweb", login="admin")
            self._assert_auth_failed(req, result)

            flowable.fire_transition("activate")
            cnx.commit()

            result, req = self._test_header_format(method="Cubicweb", login="admin")
            self._assert_auth(req, result)
