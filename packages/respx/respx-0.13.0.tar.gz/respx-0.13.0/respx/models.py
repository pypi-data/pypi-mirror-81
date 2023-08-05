import inspect
import json as jsonlib
import re
from functools import partial
from typing import (
    Any,
    AsyncIterator,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Pattern,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)
from unittest import mock
from urllib.parse import urljoin, urlparse

import httpx  # TODO: Drop usage
from httpcore import AsyncByteStream, SyncByteStream
from httpx import Headers as HTTPXHeaders  # TODO: Drop usage

URL = Tuple[bytes, bytes, Optional[int], bytes]
Headers = List[Tuple[bytes, bytes]]
Request = Tuple[
    bytes,  # http method
    URL,
    Headers,
    Union[SyncByteStream, AsyncByteStream],
]
SyncResponse = Tuple[
    int,  # status code
    Headers,
    SyncByteStream,  # body
    dict,  # ext
]
AsyncResponse = Tuple[
    int,  # status code
    Headers,
    AsyncByteStream,  # body
    dict,  # ext
]
Response = Union[SyncResponse, AsyncResponse]

HeaderTypes = Union[
    HTTPXHeaders,
    Dict[str, str],
    Dict[bytes, bytes],
    Sequence[Tuple[str, str]],
    Sequence[Tuple[bytes, bytes]],
]

DefaultType = TypeVar("DefaultType", bound=Any)

Regex = type(re.compile(""))
Kwargs = Dict[str, Any]
URLPatternTypes = Union[str, Pattern[str], URL]
ContentDataTypes = Union[bytes, str, List, Dict, Callable, Exception]

istype = lambda t, o: isinstance(o, t)
isregex = partial(istype, Regex)


def build_request(request: Request) -> Union[httpx.Request, Request]:
    """
    Try to re-build a httpx request from httpcore request args
    """
    try:
        from httpx import Request as _Request
    except ImportError:  # pragma: no cover
        return request
    else:
        method, url, headers, stream = request
        return _Request(method, url, headers=headers, stream=stream)


def build_response(
    response: Optional[Response], request: Union[httpx.Request, Request]
) -> Optional[Union[httpx.Response, Response]]:
    """
    Try to re-build a httpx response from httpcore response
    """
    if response is None:
        return None
    if not isinstance(request, httpx.Request):  # pragma: no cover
        return response
    try:
        from httpx import Response as _Response
    except ImportError:  # pragma: no cover
        return response
    else:
        status_code, headers, stream, ext = response
        httpx_response = _Response(
            status_code,
            headers=headers,
            stream=stream,
            ext=ext,
            request=request,
        )

        # Pre-read response stream, but only if mocked, not pass-through
        if isinstance(stream, ContentStream):
            httpx_response.read()

        return httpx_response


class ContentStream(AsyncByteStream, SyncByteStream):
    def __init__(self, content: bytes) -> None:
        self._content = content
        self.close_func = None
        self.aclose_func = None

    def __iter__(self) -> Iterator[bytes]:
        yield self._content

    async def __aiter__(self) -> AsyncIterator[bytes]:
        yield self._content


class ResponseTemplate:
    def __init__(
        self,
        status_code: Optional[int] = None,
        headers: Optional[HeaderTypes] = None,
        content: Optional[ContentDataTypes] = None,
        content_type: Optional[str] = None,
        context: Optional[Kwargs] = None,
    ) -> None:
        self.http_version = 1.1
        self.status_code = status_code or 200
        self.context = context if context is not None else {}
        self._content = content if content is not None else b""
        self._headers = HTTPXHeaders(headers) if headers else HTTPXHeaders()
        if content_type:
            self._headers["Content-Type"] = content_type

    def clone(self, context: Optional[Kwargs] = None) -> "ResponseTemplate":
        return ResponseTemplate(
            self.status_code, self._headers, self._content, context=context
        )

    @property
    def headers(self) -> HTTPXHeaders:
        if "Content-Type" not in self._headers:
            self._headers["Content-Type"] = "text/plain"
        return self._headers

    @property
    def content(self) -> bytes:
        return self.encode_content(self._content)

    @content.setter
    def content(self, content: ContentDataTypes) -> None:
        self._content = content

    @property
    async def acontent(self) -> bytes:
        content: ContentDataTypes = self._content

        # Pre-handle async content callbacks
        if callable(content) and inspect.iscoroutinefunction(content):
            content = await content(**self.context)

        return self.encode_content(content)

    def encode_content(self, content: ContentDataTypes) -> bytes:
        if callable(content):
            content = content(**self.context)

        if isinstance(content, Exception):
            raise content

        if isinstance(content, bytes):
            return content

        if isinstance(content, (list, dict)):
            content = jsonlib.dumps(content)
            if "Content-Type" not in self._headers:
                self._headers["Content-Type"] = "application/json"

        assert isinstance(content, str), "Invalid type of content"
        content = content.encode("utf-8")  # TODO: Respect charset

        return content

    @property
    def raw(self):
        stream = ContentStream(self.content)
        return (
            self.status_code,
            self.headers.raw,
            stream,
            {"http_version": f"HTTP/{self.http_version}".encode("ascii")},
        )

    @property
    async def araw(self):
        stream = ContentStream(await self.acontent)
        return (
            self.status_code,
            self.headers.raw,
            stream,
            {"http_version": f"HTTP/{self.http_version}".encode("ascii")},
        )


class RequestPattern:
    def __init__(
        self,
        method: Union[str, Callable],
        url: Optional[URLPatternTypes],
        response: Optional[ResponseTemplate] = None,
        pass_through: bool = False,
        alias: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        self._match_func: Optional[Callable] = None

        if callable(method):
            self.method = None
            self.url = None
            self.pass_through = None
            self._match_func = method
        else:
            self.method = method
            self.set_url(url, base=base_url)
            self.pass_through = pass_through

        self.response = response or ResponseTemplate()
        self.alias = alias
        self.stats = mock.MagicMock()

    @property
    def called(self):
        return self.stats.called

    @property
    def call_count(self):
        return self.stats.call_count

    @property
    def calls(self):
        return [
            (request, response) for (request, response), _ in self.stats.call_args_list
        ]

    def get_url(self) -> Optional[URLPatternTypes]:
        return self._url

    def set_url(
        self, url: Optional[URLPatternTypes], base: Optional[str] = None
    ) -> None:
        url = url or None
        if url is None:
            url = base
        elif isinstance(url, str):
            url = url if base is None else urljoin(base, url)
            parsed_url = urlparse(url)
            if not parsed_url.path:
                url = parsed_url._replace(path="/").geturl()
        elif isinstance(url, tuple):
            url = self.build_url(url)
        elif isregex(url):
            url = url if base is None else re.compile(urljoin(base, url.pattern))
        else:
            raise ValueError(
                "Request url pattern must be str or compiled regex, got {}.".format(
                    type(url).__name__
                )
            )
        self._url = url

    url = property(get_url, set_url)

    def build_url(self, parts: URL) -> str:
        scheme, host, port, full_path = parts
        port_str = (
            ""
            if not port or port == {b"https": 443, b"http": 80}[scheme]
            else f":{port}"
        )
        return f"{scheme.decode()}://{host.decode()}{port_str}{full_path.decode()}"

    def match(self, request: Request) -> Optional[Union[Request, ResponseTemplate]]:
        """
        Matches request with configured pattern;
        custom matcher function or http method + url pattern.

        Returns None for a non-matching pattern, mocked response for a match,
        or input request for pass-through.
        """
        matches = False
        url_params: Kwargs = {}
        _request = build_request(request)

        if self.pass_through:
            return request

        if self._match_func:
            response = self.response.clone(context={"request": _request})
            result = self._match_func(_request, response)
            if result == _request:  # Detect pass through
                result = request
            return result

        request_method, _request_url, *_ = request
        if self.method != request_method.decode():
            return None

        request_url = self.build_url(_request_url)
        if not self._url:
            matches = True
        elif isinstance(self._url, str):
            matches = self._url == request_url
        else:
            match = self._url.match(request_url)
            if match:
                matches = True
                url_params = match.groupdict()

        if matches:
            return self.response.clone(context={"request": _request, **url_params})

        return None
