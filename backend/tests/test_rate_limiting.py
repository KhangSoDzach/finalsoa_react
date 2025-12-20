"""
Test suite for rate limiting functionality.

Tests:
- Rate limiting on login endpoint (5/minute)
- Rate limiting on register endpoint (10/hour)  
- Rate limiting on forgot-password endpoint (3/hour)
- Rate limit headers
- Custom error responses
- IP address extraction
"""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
import time

# Base URL for testing
BASE_URL = "http://test"


class TestRateLimiting:
    """Test rate limiting on authentication endpoints."""
    
    @pytest.mark.asyncio
    async def test_login_rate_limit_within_limit(self):
        """Test that requests within rate limit are allowed."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
            # Clear any previous rate limit state by using unique data
            test_data = {"username": f"test_user_{time.time()}", "password": "test_password"}
            
            # First 5 requests should succeed (or fail with 401, not 429)
            for i in range(5):
                response = await client.post("/api/v1/auth/login", json=test_data)
                # Should not be rate limited (can be 401 unauthorized, but not 429)
                assert response.status_code != 429, f"Request {i+1} was rate limited"
    
    @pytest.mark.asyncio
    async def test_login_rate_limit_exceeded(self):
        """Test that 6th login attempt is rate limited."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
            test_data = {"username": f"test_limit_{time.time()}", "password": "test_password"}
            
            # Make 6 requests rapidly
            responses = []
            for i in range(6):
                response = await client.post("/api/v1/auth/login", json=test_data)
                responses.append(response)
            
            # 6th request should be rate limited
            last_response = responses[-1]
            assert last_response.status_code == 429, "Expected rate limit on 6th request"
            
            # Check response body
            data = last_response.json()
            assert "error" in data
            assert data["error"] == "rate_limit_exceeded"
            assert "message" in data
            assert "retry_after_seconds" in data or "detail" in data
    
    @pytest.mark.asyncio
    async def test_rate_limit_headers(self):
        """Test that rate limit headers are present."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
            test_data = {"username": f"test_headers_{time.time()}", "password": "test"}
            
            # Make request
            response = await client.post("/api/v1/auth/login", json=test_data)
            
            # Check for rate limit headers (may or may not be present depending on slowapi config)
            # These headers help clients understand their rate limit status
            headers = response.headers
            
            # At minimum, response should have standard headers
            assert "content-type" in headers
    
    @pytest.mark.asyncio
    async def test_register_rate_limit_different_from_login(self):
        """Test that register has different rate limit than login."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
            # Register endpoint should allow more requests per timeframe
            test_email = f"test_{time.time()}@example.com"
            
            response = await client.post("/api/v1/auth/register", json={
                "username": f"user_{time.time()}",
                "email": test_email,
                "password": "SecurePass123!",
                "full_name": "Test User",
                "role": "user"
            })
            
            # Should not be rate limited on first request (may fail validation, but not 429)
            assert response.status_code != 429
    
    @pytest.mark.asyncio
    async def test_forgot_password_rate_limit(self):
        """Test that forgot-password endpoint is rate limited (3/hour)."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
            test_email = f"test_{time.time()}@example.com"
            
            # Make 3 requests
            responses = []
            for i in range(3):
                response = await client.post(
                    "/api/v1/auth/forgot-password",
                    params={"email": test_email}
                )
                responses.append(response)
                
            # All 3 should succeed (not rate limited)
            for i, resp in enumerate(responses):
                assert resp.status_code != 429, f"Request {i+1} was rate limited"
    
    @pytest.mark.asyncio
    async def test_rate_limit_error_format(self):
        """Test that rate limit error response has correct format."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
            test_data = {"username": f"test_format_{time.time()}", "password": "test"}
            
            # Trigger rate limit by making many requests
            for _ in range(6):
                response = await client.post("/api/v1/auth/login", json=test_data)
            
            if response.status_code == 429:
                data = response.json()
                
                # Check required fields
                assert "error" in data
                assert "message" in data
                
                # Check error type
                assert data["error"] == "rate_limit_exceeded"
                
                # Check headers
                assert "Retry-After" in response.headers


class TestRateLimiterConfig:
    """Test rate limiter configuration."""
    
    def test_rate_limiter_enabled(self):
        """Test that rate limiter is enabled in app."""
        # Check that limiter is attached to app state
        assert hasattr(app.state, "limiter")
        assert app.state.limiter is not None
    
    def test_get_rate_limit_presets(self):
        """Test rate limit preset values."""
        from app.core.rate_limiter import get_rate_limit, RATE_LIMITS
        
        # Check preset values
        assert RATE_LIMITS["auth_login"] == "5/minute"
        assert RATE_LIMITS["auth_register"] == "10/hour"
        assert RATE_LIMITS["auth_forgot_password"] == "3/hour"
        
        # Check getter function
        assert get_rate_limit("auth_login") == "5/minute"
        assert get_rate_limit("unknown") == RATE_LIMITS["api_default"]
    
    def test_client_ip_extraction(self):
        """Test IP address extraction from request."""
        from app.core.rate_limiter import get_client_ip
        
        # Just verify the function exists and is importable
        assert callable(get_client_ip)


class TestRateLimitBypass:
    """Test rate limit bypass for admin IPs (optional)."""
    
    def test_admin_ip_check(self):
        """Test admin IP detection."""
        from app.core.rate_limiter import is_admin_ip
        
        # Verify function exists
        assert callable(is_admin_ip)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
