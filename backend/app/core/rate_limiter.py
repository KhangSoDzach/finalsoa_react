"""
Rate limiting configuration using SlowAPI.

Implements rate limiting for API endpoints to prevent:
- Brute force attacks
- DDoS attacks  
- API abuse

Usage:
    from app.core.rate_limiter import limiter
    
    @router.post("/login")
    @limiter.limit("5/minute")
    async def login(...):
        ...
"""
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
import logging

logger = logging.getLogger(__name__)

def get_client_ip(request: Request) -> str:
    """
    Extract client IP address from request.
    Handles X-Forwarded-For header for proxies (Vercel, etc.)
    """
    # Try to get IP from X-Forwarded-For header (proxy/load balancer)
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # X-Forwarded-For can be comma-separated, take first IP
        return forwarded.split(",")[0].strip()
    
    # Fallback to direct client IP
    return get_remote_address(request)


# Initialize limiter with in-memory storage
# For production with multiple instances, consider Redis backend
limiter = Limiter(
    key_func=get_client_ip,
    default_limits=["100/minute"],  # Default rate limit for all endpoints
    storage_uri="memory://",  # Use in-memory storage (fallback to Redis if available)
    strategy="fixed-window",  # Fixed window strategy
    headers_enabled=True,  # Include rate limit headers in response
)


async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """
    Custom handler for rate limit exceeded errors.
    Returns JSON response with retry information.
    """
    # Log rate limit violation
    logger.warning(
        f"Rate limit exceeded: {get_client_ip(request)} - "
        f"Path: {request.url.path} - Method: {request.method}"
    )
    
    # Extract retry-after from exception if available
    retry_after = getattr(exc, "retry_after", None)
    
    response_data = {
        "error": "rate_limit_exceeded",
        "message": "Too many requests. Please try again later.",
        "detail": "You have exceeded the rate limit for this endpoint."
    }
    
    if retry_after:
        response_data["retry_after_seconds"] = int(retry_after)
    
    return JSONResponse(
        status_code=HTTP_429_TOO_MANY_REQUESTS,
        content=response_data,
        headers={
            "Retry-After": str(int(retry_after)) if retry_after else "60",
            "X-RateLimit-Limit": str(exc.limit) if hasattr(exc, "limit") else "unknown",
            "X-RateLimit-Remaining": "0",
            "X-RateLimit-Reset": str(int(retry_after)) if retry_after else "60"
        }
    )


def is_admin_ip(request: Request) -> bool:
    """
    Check if request comes from admin IP (optional whitelist).
    Can be used to exclude certain IPs from rate limiting.
    """
    # Example: whitelist local development IPs
    admin_ips = ["127.0.0.1", "::1", "localhost"]
    client_ip = get_client_ip(request)
    return client_ip in admin_ips


# Rate limit presets for different endpoint types
RATE_LIMITS = {
    "auth_login": "5/minute",           # Login endpoint: 5 attempts per minute
    "auth_register": "10/hour",         # Register: 10 per hour
    "auth_forgot_password": "3/hour",   # Forgot password: 3 per hour
    "auth_reset_password": "5/hour",    # Reset password: 5 per hour
    "api_default": "100/minute",        # Default API endpoints
    "api_heavy": "30/minute",           # Heavy operations (reports, exports)
    "api_create": "20/minute",          # Create operations
    "api_update": "50/minute",          # Update operations
    "api_delete": "10/minute",          # Delete operations
}


def get_rate_limit(limit_type: str) -> str:
    """
    Get rate limit string for a specific endpoint type.
    
    Args:
        limit_type: Type of rate limit (e.g., 'auth_login', 'api_default')
        
    Returns:
        Rate limit string (e.g., '5/minute')
    """
    return RATE_LIMITS.get(limit_type, RATE_LIMITS["api_default"])
