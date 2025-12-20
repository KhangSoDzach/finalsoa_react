"""
Test suite for password hashing migration from SHA256 to bcrypt.

Tests:
- Dual-mode verification (SHA256 legacy + bcrypt new)
- Password hash detection
- Backward compatibility
- Migration safety
"""
import pytest
import hashlib
from app.core.security import (
    verify_password,
    get_password_hash,
    needs_password_rehash
)


class TestPasswordHashingMigration:
    """Test password hashing migration functionality."""
    
    def test_bcrypt_password_creation(self):
        """Test that new passwords use bcrypt."""
        password = "TestPassword123!"
        hashed = get_password_hash(password)
        
        # Bcrypt hashes start with $2b$
        assert hashed.startswith("$2b$") or hashed.startswith("$2a$")
        # Bcrypt hashes are 60 characters (fixed length)
        assert len(hashed) == 60
    
    def test_bcrypt_password_verification(self):
        """Test bcrypt password verification."""
        password = "SecurePassword456!"
        hashed = get_password_hash(password)
        
        # Correct password should verify
        assert verify_password(password, hashed) is True
        
        # Incorrect password should fail
        assert verify_password("WrongPassword", hashed) is False
    
    def test_legacy_sha256_verification(self):
        """Test that legacy SHA256 passwords still work (backward compatibility)."""
        password = "LegacyPassword789"
        # Simulate old SHA256 hash
        legacy_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Should still verify with legacy method
        assert verify_password(password, legacy_hash) is True
        
        # Wrong password should fail
        assert verify_password("WrongPassword", legacy_hash) is False
    
    def test_needs_rehash_detection_sha256(self):
        """Test detection of SHA256 hashes that need migration."""
        legacy_password = "OldPassword"
        legacy_hash = hashlib.sha256(legacy_password.encode()).hexdigest()
        
        # SHA256 hash should be detected as needing rehash
        assert needs_password_rehash(legacy_hash) is True
        assert len(legacy_hash) == 64  # SHA256 length
    
    def test_needs_rehash_detection_bcrypt(self):
        """Test that bcrypt hashes are not flagged for rehash."""
        new_password = "NewSecurePassword"
        bcrypt_hash = get_password_hash(new_password)
        
        # Bcrypt hash should NOT need rehash
        assert needs_password_rehash(bcrypt_hash) is False
    
    def test_password_hash_uniqueness(self):
        """Test that same password generates different bcrypt hashes (salt)."""
        password = "SamePassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # Different hashes due to different salts
        assert hash1 != hash2
        
        # But both should verify correctly
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True
    
    def test_migration_scenario_user_login(self):
        """
        Simulate real migration scenario:
        1. User has SHA256 hash
        2. User logs in (verification works)
        3. On next password change, gets bcrypt hash
        """
        password = "UserPassword123"
        
        # Step 1: User has old SHA256 hash
        old_hash = hashlib.sha256(password.encode()).hexdigest()
        assert needs_password_rehash(old_hash) is True
        
        # Step 2: User logs in - should still work
        assert verify_password(password, old_hash) is True
        
        # Step 3: User changes password - gets bcrypt
        new_password = "NewUserPassword456"
        new_hash = get_password_hash(new_password)
        assert needs_password_rehash(new_hash) is False
        assert verify_password(new_password, new_hash) is True
    
    def test_empty_password_handling(self):
        """Test handling of empty passwords."""
        with pytest.raises(ValueError):
            # Bcrypt should reject empty passwords
            pwd_context = __import__('passlib.context', fromlist=['CryptContext']).CryptContext(
                schemes=["bcrypt"]
            )
            pwd_context.hash("")
    
    def test_long_password_support(self):
        """Test that bcrypt handles long passwords (up to 72 bytes)."""
        # Bcrypt has a 72-byte limit
        long_password = "A" * 70 + "!@"  # 72 characters
        hashed = get_password_hash(long_password)
        
        assert verify_password(long_password, hashed) is True
    
    def test_special_characters_in_password(self):
        """Test passwords with special characters."""
        special_passwords = [
            "Pass@word#123",
            "Pāsswørd™",  # Unicode
            "P@$$w0rd!",
            "密碼123",  # Chinese characters
        ]
        
        for password in special_passwords:
            hashed = get_password_hash(password)
            assert verify_password(password, hashed) is True
            assert verify_password("WrongPassword", hashed) is False


class TestSecurityImprovements:
    """Test security improvements over SHA256."""
    
    def test_timing_attack_resistance(self):
        """Test that verification time is consistent (timing attack resistance)."""
        import time
        
        password = "TestPassword"
        hashed = get_password_hash(password)
        
        # Time correct password
        start = time.perf_counter()
        verify_password(password, hashed)
        time_correct = time.perf_counter() - start
        
        # Time incorrect password
        start = time.perf_counter()
        verify_password("WrongPassword", hashed)
        time_incorrect = time.perf_counter() - start
        
        # Times should be similar (within 50% variance)
        # Bcrypt is designed to have consistent timing
        ratio = time_correct / time_incorrect if time_incorrect > 0 else 1
        assert 0.5 < ratio < 2.0, "Timing variance too large"
    
    def test_computational_cost(self):
        """Test that bcrypt is computationally expensive (brute-force resistance)."""
        import time
        
        password = "TestPassword123"
        
        # Bcrypt should take noticeable time (> 50ms typically)
        start = time.perf_counter()
        hashed = get_password_hash(password)
        duration = time.perf_counter() - start
        
        # Should take at least 10ms (bcrypt default work factor)
        assert duration > 0.01, f"Bcrypt too fast: {duration*1000:.2f}ms"
        
        # Verify is also slow
        start = time.perf_counter()
        verify_password(password, hashed)
        verify_duration = time.perf_counter() - start
        
        assert verify_duration > 0.01


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
