import os

from requests import Response
from requests.sessions import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


from argus_api._validators import validate_http_response

try:
    from argus_cli.settings import settings
except ImportError:
    settings = {}

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, timeout=30, **kwargs):
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


package_version = version("argus-api")


class ArgusAPISession:

    SUPPORTED_METHODS = ("get", "post", "put", "delete")
    USER_AGENT = f"ArgusAPI/{package_version}"
    DEFAULT_TIMEOUT = 30  # seconds
    # retry strategy defaults
    DEFAULT_RETRY_MAX = 3
    DEFAULT_RETRY_STATUSES = [500, 503]
    DEFAULT_RETRY_METHODS = ["GET", "PUT", "DELETE", "POST"]
    # Used to calculate sleep time between retries. backoff sleep time formula:
    # {backoff factor} * (2 ** ({number of total retries} - 1))
    DEFAULT_RETRY_BACKOFF_FACTOR = 0

    def __init__(self):
        self.user_agent = self.USER_AGENT
        self.api_key = settings.get("api", {}).get("api_key")
        self.base_url = settings.get("api", {}).get(
            "api_url", "https://api.mnemonic.no"
        )

        self._session = Session()
        # set default timeout and retry strategy
        self.default_timeout = self.DEFAULT_TIMEOUT
        self.retry_strategy = Retry(
            total=self.DEFAULT_RETRY_MAX,
            status_forcelist=self.DEFAULT_RETRY_STATUSES,
            method_whitelist=self.DEFAULT_RETRY_METHODS,
            raise_on_redirect=False,
            backoff_factor=self.DEFAULT_RETRY_BACKOFF_FACTOR,
            raise_on_status=False,
        )
        adapter = TimeoutHTTPAdapter(
            timeout=self.default_timeout, max_retries=self.retry_strategy
        )
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)
        # set headers
        self._session.headers.update(
            {"User-Agent": self.USER_AGENT, "content": "application/json"}
        )
        if self.api_key:
            self._session.headers.update({"Argus-API-Key": self.api_key})

    def _request(self, method, _route, *args, **kwargs) -> Response:
        """
        
        _route should have a leading /
        """

        # build destination URL
        base_url = self.base_url
        if kwargs.get("server_url"):
            base_url = kwargs["server_url"]
        url = f"{base_url}{_route}"

        # allow auth header override
        headers_override = {}
        if kwargs.get("apiKey"):
            headers_override["Argus-Api-Key"] = kwargs["apiKey"]
        elif kwargs.get("authentication"):
            authentication = kwargs["authentication"]
            if isinstance(authentication, dict):
                headers_override["Argus-Api-Key"] = None
                headers_override.update(authentication)
            elif callable(authentication):
                headers_override["Argus-Api-Key"] = None
                headers_override.update(authentication(url))

        # update request-specific headers
        if headers_override:
            if "headers" not in kwargs:
                kwargs["headers"] = {}
            kwargs["headers"].update(headers_override)

        # emulate previous behavior, where the verify parameter would be ignored
        # if a CA bundle is defined.
        kwargs["verify"] = os.getenv(
            "REQUESTS_CA_BUNDLE",
            os.getenv("CURL_CA_BUNDLE", kwargs.get("verify", True)),
        )

        # clean kwargs before passing them down to requests
        for arg in ("apiKey", "authentication", "server_url"):
            if arg in kwargs:
                del kwargs[arg]

        # perform the request
        response = getattr(self._session, method)(url, *args, **kwargs)

        # check the status code for errors
        validate_http_response(response)

        return response

    def get(self, _route, *args, **kwargs):
        return self._request("get", _route, *args, **kwargs)

    def post(self, _route, *args, **kwargs):
        return self._request("post", _route, *args, **kwargs)

    def put(self, _route, *args, **kwargs):
        return self._request("put", _route, *args, **kwargs)

    def delete(self, _route, *args, **kwargs):
        return self._request("delete", _route, *args, **kwargs)


session = ArgusAPISession()
