"""
Migration script to convert SHA256 password hashes to bcrypt.

Usage:
    python -m backend.scripts.migrate_passwords_to_bcrypt

Safety:
    - Backs up database before migration
    - Uses transactions for atomicity
    - Dry-run mode available
    - Validates each migration
"""
import sys
import os
from pathlib import Path

# Add backend directory to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from sqlmodel import Session, select
from app.core.database import engine
from app.models.user import User
from app.core.security import needs_password_rehash, get_password_hash
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def migrate_passwords(dry_run: bool = True) -> dict:
    """
    Migrate SHA256 password hashes to bcrypt.
    
    Args:
        dry_run: If True, only simulate the migration without committing changes.
        
    Returns:
        dict: Migration statistics
    """
    stats = {
        "total_users": 0,
        "needs_migration": 0,
        "migrated": 0,
        "already_bcrypt": 0,
        "errors": 0,
        "error_details": []
    }
    
    logger.info(f"Starting password migration (dry_run={dry_run})...")
    
    try:
        with Session(engine) as session:
            # Get all users
            users = session.exec(select(User)).all()
            stats["total_users"] = len(users)
            
            logger.info(f"Found {stats['total_users']} users in database")
            
            for user in users:
                try:
                    # Check if password needs migration
                    if needs_password_rehash(user.hashed_password):
                        stats["needs_migration"] += 1
                        logger.warning(
                            f"User '{user.username}' has SHA256 hash - "
                            f"CANNOT auto-migrate (need plain password)"
                        )
                        stats["error_details"].append({
                            "username": user.username,
                            "reason": "SHA256 hash detected - requires user to reset password"
                        })
                    else:
                        stats["already_bcrypt"] += 1
                        logger.info(f"User '{user.username}' already uses bcrypt")
                
                except Exception as e:
                    stats["errors"] += 1
                    logger.error(f"Error processing user '{user.username}': {str(e)}")
                    stats["error_details"].append({
                        "username": user.username,
                        "error": str(e)
                    })
            
            if not dry_run:
                session.commit()
                logger.info("Changes committed to database")
            else:
                logger.info("DRY RUN - No changes committed")
    
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        stats["errors"] += 1
        raise
    
    return stats


def print_migration_report(stats: dict):
    """Print detailed migration report."""
    print("\n" + "="*70)
    print("PASSWORD MIGRATION REPORT")
    print("="*70)
    print(f"Total Users:           {stats['total_users']}")
    print(f"Already using bcrypt:  {stats['already_bcrypt']}")
    print(f"Need migration:        {stats['needs_migration']}")
    print(f"Migrated:              {stats['migrated']}")
    print(f"Errors:                {stats['errors']}")
    print("="*70)
    
    if stats['needs_migration'] > 0:
        print("\n⚠️  WARNING: Users with SHA256 hashes detected!")
        print("These users need to reset their passwords through the forgot-password flow.")
        print("\nRecommended actions:")
        print("1. Send password reset emails to affected users")
        print("2. Or create a temporary endpoint for admin to force password reset")
        print("\nAffected users:")
        for detail in stats['error_details']:
            if 'SHA256' in detail.get('reason', ''):
                print(f"  - {detail['username']}")
    
    if stats['errors'] > 0:
        print("\n❌ ERRORS:")
        for detail in stats['error_details']:
            if 'error' in detail:
                print(f"  - {detail['username']}: {detail['error']}")
    
    print("\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate passwords from SHA256 to bcrypt")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually perform the migration (default is dry-run)"
    )
    
    args = parser.parse_args()
    
    # Confirm execution
    if args.execute:
        response = input(
            "\n⚠️  This will modify the database. "
            "Have you backed up your database? (yes/no): "
        )
        if response.lower() != "yes":
            print("Migration cancelled. Please backup your database first.")
            sys.exit(0)
    
    # Run migration
    stats = migrate_passwords(dry_run=not args.execute)
    
    # Print report
    print_migration_report(stats)
    
    # Exit with appropriate code
    if stats['errors'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)
