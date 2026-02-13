"""
Quick test script to verify real data seeding works
Chạy test nhanh trước khi deploy lên Render
Run: python -m scripts.test_real_data
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select
from app.core.database import engine
from app.models.user import User, UserRole
from app.models.apartment import Apartment

def test_database_connection():
    """Test database connectivity"""
    print("🔌 Testing database connection...")
    try:
        with Session(engine) as session:
            result = session.exec(select(User).limit(1)).first()
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_users_data():
    """Test if users data exists"""
    print("\n👥 Checking users data...")
    with Session(engine) as session:
        # Count by role
        total = session.exec(select(User)).all()
        managers = session.exec(select(User).where(User.role == UserRole.MANAGER)).all()
        accountants = session.exec(select(User).where(User.role == UserRole.ACCOUNTANT)).all()
        receptionists = session.exec(select(User).where(User.role == UserRole.RECEPTIONIST)).all()
        users = session.exec(select(User).where(User.role == UserRole.USER)).all()
        
        print(f"   Total users: {len(total)}")
        print(f"   - Managers: {len(managers)}")
        print(f"   - Accountants: {len(accountants)}")
        print(f"   - Receptionists: {len(receptionists)}")
        print(f"   - Regular users: {len(users)}")
        
        if len(total) == 0:
            print("   ⚠️  No users found! Run: python -m scripts.seed_real_data")
            return False
        
        # Show sample users
        print("\n   📋 Sample users:")
        for user in total[:5]:
            building_info = f" ({user.building}-{user.apartment_number})" if user.apartment_number else ""
            print(f"      - {user.username}: {user.full_name}{building_info} [{user.role}]")
        
        return True

def test_apartments_data():
    """Test if apartments data exists"""
    print("\n🏢 Checking apartments data...")
    with Session(engine) as session:
        apartments = session.exec(select(Apartment)).all()
        
        if len(apartments) == 0:
            print("   ⚠️  No apartments found! Run: python -m scripts.seed_real_data")
            return False
        
        # Group by building
        buildings = {}
        for apt in apartments:
            if apt.building not in buildings:
                buildings[apt.building] = []
            buildings[apt.building].append(apt)
        
        print(f"   Total apartments: {len(apartments)}")
        for building, apts in buildings.items():
            print(f"   - {building}: {len(apts)} apartments")
        
        # Show sample apartments
        print("\n   📋 Sample apartments:")
        for apt in apartments[:5]:
            status_icon = "🟢" if apt.status == "OCCUPIED" else "⚪"
            print(f"      {status_icon} {apt.building}-{apt.apartment_number}: "
                  f"{apt.area}m², {apt.bedrooms}BR, {apt.bathrooms}BA")
        
        return True

def test_login_credentials():
    """Test if default login credentials work"""
    print("\n🔑 Testing login credentials...")
    
    test_accounts = [
        ("manager", "Manager"),
        ("accountant", "Accountant"),
        ("receptionist", "Receptionist"),
        ("hanh.nguyen", "Regular User")
    ]
    
    with Session(engine) as session:
        all_passed = True
        for username, role_name in test_accounts:
            user = session.exec(select(User).where(User.username == username)).first()
            if user:
                # Verify password hash exists
                if user.hashed_password:
                    print(f"   ✅ {role_name} ({username}): Ready")
                else:
                    print(f"   ❌ {role_name} ({username}): No password hash")
                    all_passed = False
            else:
                print(f"   ❌ {role_name} ({username}): User not found")
                all_passed = False
        
        return all_passed

def test_data_relationships():
    """Test if user-apartment relationships are correct"""
    print("\n🔗 Checking data relationships...")
    with Session(engine) as session:
        users_with_apartments = session.exec(
            select(User).where(User.apartment_number.isnot(None))
        ).all()
        
        print(f"   Users with apartments: {len(users_with_apartments)}")
        
        # Check if apartments exist for users
        issues = []
        for user in users_with_apartments:
            apartment = session.exec(
                select(Apartment).where(
                    Apartment.apartment_number == user.apartment_number,
                    Apartment.building == user.building
                )
            ).first()
            
            if not apartment:
                issues.append(f"{user.username} -> {user.building}-{user.apartment_number} (apartment not found)")
            else:
                print(f"   ✅ {user.username} -> {apartment.building}-{apartment.apartment_number}")
        
        if issues:
            print("\n   ⚠️  Issues found:")
            for issue in issues:
                print(f"      - {issue}")
            return False
        
        return True

def main():
    """Run all tests"""
    print("=" * 70)
    print("  TESTING REAL DATA SEEDING - KIỂM TRA DỮ LIỆU")
    print("=" * 70)
    print()
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Users Data", test_users_data),
        ("Apartments Data", test_apartments_data),
        ("Login Credentials", test_login_credentials),
        ("Data Relationships", test_data_relationships)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ Test '{test_name}' failed with error: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 70)
    print("  TEST SUMMARY - TỔNG KẾT")
    print("=" * 70)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        icon = "✅" if result else "❌"
        print(f"{icon} {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! You can now deploy to Render.")
        print("\n📝 Next steps:")
        print("   1. Push code to Git: git push")
        print("   2. Deploy to Render (automatic)")
        print("   3. Run: python -m scripts.seed_real_data (in Render Shell)")
        print("   4. Login with credentials from LOGIN_CREDENTIALS.md")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues before deploying.")
        print("\n🔧 Troubleshooting:")
        print("   1. Run: python -m scripts.seed_real_data")
        print("   2. Check database connection")
        print("   3. Re-run this test: python -m scripts.test_real_data")

if __name__ == "__main__":
    main()
