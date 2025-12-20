import hashlib
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt as bcrypt_lib
from app.core.config import settings

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash with dual-mode support.
    Supports both legacy SHA256 (for backward compatibility) and bcrypt.
    """
    # Try bcrypt first (recommended method)
    try:
        if bcrypt_lib.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8')):
            return True
    except Exception:
        # Not a valid bcrypt hash, try legacy method
        pass
    
    # Fallback to legacy SHA256 for existing users
    legacy_hash = hashlib.sha256(plain_password.encode()).hexdigest()
    return legacy_hash == hashed_password

def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt (secure method).
    All new passwords will use bcrypt.
    """
    salt = bcrypt_lib.gensalt()
    hashed = bcrypt_lib.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def needs_password_rehash(hashed_password: str) -> bool:
    """
    Check if a password hash needs migration to bcrypt.
    SHA256 hashes are exactly 64 characters long.
    """
    return len(hashed_password) == 64  # SHA256 length

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_token(token: str):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None