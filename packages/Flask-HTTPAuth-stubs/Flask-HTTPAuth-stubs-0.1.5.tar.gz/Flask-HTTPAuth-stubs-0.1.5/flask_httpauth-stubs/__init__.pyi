from typing import (
    Callable,
    Optional,
    Tuple,
    Union,
)
from werkzeug.datastructures import Authorization

class HTTPAuth:
    def __init__(
        self,
        scheme: Optional[str] = ...,
        realm: Optional[str] = ...,
        header: Optional[str] = ...,
    ) -> None:
        self.scheme = scheme
        self.realm = realm or "Authentication Required"
        self.header = header
        self.get_password_callback = None
        self.get_user_roles_callback = None
        self.auth_error_callback = None
        def default_get_password(username):
            return None
        def default_auth_error(status):
            return "Unauthorized Access", status
        self.get_password(default_get_password)
        self.error_handler(default_auth_error)
    def authenticate_header(self) -> str: ...
    def authorize(
        self,
        role: Optional[Union[Tuple[str, str], Tuple[Tuple[str, str]], str]],
        user: Union[str, bool],
        auth: Optional[Authorization],
    ) -> Optional[bool]: ...
    def current_user(self) -> Optional[str]: ...
    def error_handler(self, f: Callable) -> Callable: ...
    def get_auth(self) -> Optional[Authorization]: ...
    def get_auth_password(self, auth: Optional[Authorization]) -> Optional[str]: ...
    def get_password(self, f: Callable) -> Callable: ...
    def get_user_roles(self, f: Callable) -> Callable: ...
    def login_required(
        self,
        f: Optional[Callable] = ...,
        role: Optional[Union[Tuple[str, str], Tuple[Tuple[str, str]], str]] = ...,
        optional: Optional[bool] = ...,
    ) -> Callable: ...
    def username(self) -> str: ...
    def auth_error_callback(self, status: int=200): ...

class HTTPBasicAuth(HTTPAuth):
    def __init__(self, scheme: None = ..., realm: Optional[str] = ...) -> None:
        super(HTTPBasicAuth, self).__init__(scheme or "Basic", realm)

        self.hash_password_callback = None
        self.verify_password_callback = None
    def authenticate(
        self, auth: Optional[Authorization], stored_password: Optional[str]
    ) -> Optional[Union[str, bool]]: ...
    def get_auth(self) -> Optional[Authorization]: ...
    def hash_password(self, f: Callable) -> Callable: ...
    def verify_password(self, f: Callable) -> Callable: ...

class HTTPDigestAuth(HTTPAuth):
    def __init__(
        self, scheme: None = ..., realm: Optional[str] = ..., use_ha1_pw: bool = ...
    ) -> None:
        super(HTTPDigestAuth, self).__init__(scheme or "Digest", realm)
        self.use_ha1_pw = use_ha1_pw
        self.random = SystemRandom()
        try:
            self.random.random()
        except NotImplementedError:  # pragma: no cover
            self.random = Random()

        self.generate_nonce_callback = None
        self.verify_nonce_callback = None
        self.generate_opaque_callback = None
        self.verify_opaque_callback = None
        def _generate_random():
            return md5(str(self.random.random()).encode("utf-8")).hexdigest()
        def default_generate_nonce():
            session["auth_nonce"] = _generate_random()
            return session["auth_nonce"]
        def default_verify_nonce(nonce):
            session_nonce = session.get("auth_nonce")
            if nonce is None or session_nonce is None:
                return False
            return safe_str_cmp(nonce, session_nonce)
        def default_generate_opaque():
            session["auth_opaque"] = _generate_random()
            return session["auth_opaque"]
        def default_verify_opaque(opaque):
            session_opaque = session.get("auth_opaque")
            if opaque is None or session_opaque is None:  # pragma: no cover
                return False
            return safe_str_cmp(opaque, session_opaque)
        self.generate_nonce(default_generate_nonce)
        self.generate_opaque(default_generate_opaque)
        self.verify_nonce(default_verify_nonce)
        self.verify_opaque(default_verify_opaque)
    def authenticate(
        self, auth: Optional[Authorization], stored_password_or_ha1: Optional[str]
    ) -> bool: ...
    def authenticate_header(self) -> str: ...
    def generate_ha1(self, username: str, password: str) -> str: ...
    def generate_nonce(self, f: Callable) -> Callable: ...
    def generate_opaque(self, f: Callable) -> Callable: ...
    def get_nonce(self) -> str: ...
    def get_opaque(self) -> str: ...
    def verify_nonce(self, f: Callable) -> Callable: ...
    def verify_opaque(self, f: Callable) -> Callable: ...

class HTTPTokenAuth(HTTPAuth):
    def __init__(
        self, scheme: str = ..., realm: Optional[str] = ..., header: Optional[str] = ...
    ) -> None:
        super(HTTPTokenAuth, self).__init__(scheme, realm, header)
        self.verify_token_callback = None
    def authenticate(
        self, auth: Optional[Authorization], stored_password: None
    ) -> Optional[Union[str, bool]]: ...
    def verify_token(self, f: Callable) -> Callable: ...

class MultiAuth:
    def __init__(self, main_auth: HTTPBasicAuth, *args) -> None:
        self.main_auth = main_auth
        self.additional_auth = args
    def current_user(self) -> Optional[str]: ...
    def login_required(
        self, f: Optional[Callable] = ..., role: Optional[str] = ...
    ) -> Callable: ...
