from collections import defaultdict, deque
from collections.abc import Awaitable, Callable
from threading import Lock
from time import monotonic

from fastapi import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_429_TOO_MANY_REQUESTS


class InMemoryRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._buckets: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def is_allowed(self, key: str) -> bool:
        now = monotonic()
        threshold = now - self.window_seconds

        with self._lock:
            bucket = self._buckets[key]
            while bucket and bucket[0] <= threshold:
                bucket.popleft()

            if len(bucket) >= self.max_requests:
                return False

            bucket.append(now)
            return True


def get_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


async def rate_limit_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable],
    limiter: InMemoryRateLimiter,
    route_limiters: dict[str, InMemoryRateLimiter] | None = None,
):
    
    if request.url.path == "/":
        return await call_next(request)

    path = request.url.path
    selected_limiter = route_limiters.get(path, limiter) if route_limiters else limiter

    client_ip = get_client_ip(request)
    key = f"{path}:{client_ip}"
    if not selected_limiter.is_allowed(key):
        return JSONResponse(
            status_code=HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Too many requests. Please try again shortly."},
        )

    return await call_next(request)
