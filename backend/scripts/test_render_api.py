"""
Test seed API on Render
Script để test API seed trên production
"""
import requests
import json
import time

BASE_URL = "https://apartment-backend-rdcs.onrender.com"

def test_health():
    """Test main health endpoint"""
    print("🔌 Testing main health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=60)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Backend is healthy!")
            return True
        else:
            print(f"   ⚠️  Backend returned: {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        print("   ⏰ Timeout - Backend may be cold starting...")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_seed_health():
    """Test seed API health"""
    print("\n🌱 Testing seed API health...")
    try:
        response = requests.get(f"{BASE_URL}/api/seed/health", timeout=30)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Seed API is ready!")
            print(f"   Available endpoints:")
            for endpoint in data.get('endpoints', []):
                print(f"      - {endpoint}")
            return True
        else:
            print(f"   ⚠️  Seed API returned: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def seed_real_data():
    """Seed realistic data"""
    print("\n🚀 Seeding realistic data...")
    try:
        response = requests.post(f"{BASE_URL}/api/seed/real-data", timeout=60)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ {data.get('message')}")
            if data.get('status') == 'success':
                print(f"   Created:")
                print(f"      - Apartments: {data.get('apartments_created', 0)}")
                print(f"      - Users: {data.get('users_created', 0)}")
            elif data.get('status') == 'skipped':
                print(f"   Existing:")
                print(f"      - Apartments: {data.get('apartments', 0)}")
                print(f"      - Users: {data.get('users', 0)}")
            return True
        else:
            print(f"   ❌ Failed: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def force_seed_data(secret="render-seed-2026"):
    """Force seed data with clearing"""
    print("\n⚠️  Force seeding (will clear existing data)...")
    confirm = input("   Are you sure? (yes/no): ").lower().strip()
    
    if confirm != "yes":
        print("   ❌ Cancelled")
        return False
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/seed/force-real-data?secret={secret}",
            timeout=60
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ {data.get('message')}")
            if 'deleted' in data:
                print(f"   Deleted:")
                print(f"      - Apartments: {data['deleted'].get('apartments', 0)}")
                print(f"      - Users: {data['deleted'].get('users', 0)}")
            if 'created' in data:
                print(f"   Created:")
                print(f"      - Apartments: {data['created'].get('apartments', 0)}")
                print(f"      - Users: {data['created'].get('users', 0)}")
            return True
        elif response.status_code == 403:
            print(f"   ❌ Invalid secret key")
            return False
        else:
            print(f"   ❌ Failed: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_api_docs():
    """Check if API docs are accessible"""
    print("\n📚 Testing API documentation...")
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=30)
        if response.status_code == 200:
            print(f"   ✅ API docs available at: {BASE_URL}/docs")
            return True
        else:
            print(f"   ⚠️  API docs returned: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 70)
    print("  TESTING SEED API ON RENDER")
    print("=" * 70)
    print(f"\n🌐 Backend URL: {BASE_URL}")
    print()
    
    # Test 1: Main health
    health_ok = test_health()
    if not health_ok:
        print("\n⚠️  Backend is cold starting. Waiting 30 seconds...")
        time.sleep(30)
        health_ok = test_health()
        if not health_ok:
            print("\n❌ Backend is not responding. Please check Render dashboard.")
            return
    
    # Test 2: Seed health
    seed_health_ok = test_seed_health()
    if not seed_health_ok:
        print("\n❌ Seed API is not available. Make sure you deployed the latest code.")
        return
    
    # Test 3: API docs
    test_api_docs()
    
    # Ask what to do
    print("\n" + "=" * 70)
    print("  WHAT DO YOU WANT TO DO?")
    print("=" * 70)
    print("1. Seed data (skip if exists)")
    print("2. Force seed data (clear & recreate)")
    print("3. Exit")
    print()
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == "1":
        seed_real_data()
    elif choice == "2":
        force_seed_data()
    else:
        print("\n👋 Goodbye!")
        return
    
    # Final summary
    print("\n" + "=" * 70)
    print("  TEST COMPLETED!")
    print("=" * 70)
    print("\n📝 Next steps:")
    print(f"   1. Visit: {BASE_URL}/docs")
    print(f"   2. Test login with: manager / 123456")
    print("   3. Check Supabase dashboard for data")
    print()

if __name__ == "__main__":
    main()
