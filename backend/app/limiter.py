from fastapi import Request
from slowapi import Limiter


def _get_real_ip(request: Request) -> str:
    """Return the client's real IP, honouring X-Forwarded-For behind proxies.

    C-4: using request.client.host alone gives the proxy IP when running behind
    Docker Compose or a cloud load-balancer, collapsing all users into one rate
    limit bucket.  X-Forwarded-For is set by trusted infrastructure (nginx,
    Railway, Vercel) and contains the original client IP as the first entry.
    """
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


limiter = Limiter(key_func=_get_real_ip)
