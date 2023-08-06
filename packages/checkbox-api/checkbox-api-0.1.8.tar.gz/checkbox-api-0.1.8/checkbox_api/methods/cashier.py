import base64
import datetime

from httpx import Response

from checkbox_api.methods.base import BaseMethod, HTTPMethod
from checkbox_api.storage.simple import SessionStorage

URI_PREFIX = "cashier/"


class _SignInMixin:
    method = HTTPMethod.POST

    def parse_response(self, storage: SessionStorage, response: Response):
        result = response.json()
        storage.token = result["access_token"]
        return result


class SignIn(_SignInMixin, BaseMethod):
    uri = URI_PREFIX + "signin"

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password

    @property
    def payload(self):
        return {"login": self.login, "password": self.password}


class SignInPinCode(_SignInMixin, BaseMethod):
    uri = SignIn.uri + "PinCode"

    def __init__(self, pin_code: str):
        self.pin_code = pin_code

    @property
    def payload(self):
        return {"pin_code": self.pin_code}


class SignInSignature(_SignInMixin, BaseMethod):
    uri = SignIn.uri + "Signature"

    def __init__(self, signature: bytes):
        self.signature = signature

    @property
    def payload(self):
        signature = base64.standard_b64encode(self.signature).decode()
        return {"signature": signature}


class GetMe(BaseMethod):
    method = HTTPMethod.GET
    uri = URI_PREFIX + "me"

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        storage.cashier = result
        return result


class SignOut(BaseMethod):
    method = HTTPMethod.POST
    uri = URI_PREFIX + "signout"

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)

        storage.shift = None
        storage.cashier = None
        storage.token = None

        return result


class GetActiveShift(BaseMethod):
    uri = URI_PREFIX + "shift"

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        storage.shift = result
        return result


class AskOfflineCodes(BaseMethod):
    uri = URI_PREFIX + "ask-offline-codes"

    def __init__(self, count: int = 2000, sync: bool = False):
        self.count = count
        self.sync = sync

    @property
    def query(self):
        query = super().query
        query.update({"count": self.count, "sync": self.sync})
        return query


class GetOfflineCodes(BaseMethod):
    uri = URI_PREFIX + "get-offline-codes"

    def __init__(self, count: int = 2000):
        self.count = count

    @property
    def query(self):
        query = super().query
        query.update({"count": self.count})
        return query


class GoOnline(BaseMethod):
    uri = URI_PREFIX + "go-online"
    method = HTTPMethod.POST


class GoOffline(BaseMethod):
    uri = URI_PREFIX + "go-offline"
    method = HTTPMethod.POST

    def __init__(self, go_offline_date: datetime.datetime, fiscal_code: str):
        self.go_offline_date = go_offline_date
        self.fiscal_code = fiscal_code

    @property
    def payload(self):
        payload = super().payload
        payload.update(
            {"go_offline_date": self.go_offline_date.isoformat(), "fiscal_code": self.fiscal_code}
        )
        return payload
