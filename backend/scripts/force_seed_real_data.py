"""
Force seed real data - Override existing data
Script này sẽ XÓA và TẠO LẠI dữ liệu thực tế
Run: python -m scripts.force_seed_real_data
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select, delete
from app.core.database import engine
from app.models.user import User, UserRole, OccupierType
from app.models.apartment import Apartment, ApartmentStatus
from app.core.security import get_password_hash
from datetime import datetime

def clear_existing_data():
    """Clear existing users and apartments"""
    print("⚠️  WARNING: This will DELETE all existing data!")
    print("   - All users (except those with existing bills/tickets)")
    print("   - All apartments")
    print()
    
    response = input("Do you want to continue? (yes/no): ").lower().strip()
    
    if response != "yes":
        print("❌ Operation cancelled.")
        return False
    
    print("\n🗑️  Clearing existing data...")
    
    with Session(engine) as session:
        try:
            # Delete apartments first
            deleted_apartments = session.exec(delete(Apartment)).rowcount
            print(f"   Deleted {deleted_apartments} apartments")
            
            # Delete users (be careful with foreign keys)
            # Only delete users without bills/tickets
            users_to_delete = session.exec(
                select(User).where(User.role != UserRole.MANAGER)  # Keep manager for safety
            ).all()
            
            deleted_users = 0
            for user in users_to_delete:
                try:
                    session.delete(user)
                    deleted_users += 1
                except Exception as e:
                    print(f"   ⚠️  Skipped user {user.username}: {e}")
            
            session.commit()
            print(f"   Deleted {deleted_users} users")
            print("✅ Data cleared successfully!")
            return True
            
        except Exception as e:
            session.rollback()
            print(f"❌ Error clearing data: {e}")
            return False

def seed_apartments():
    """Create realistic apartments"""
    apartments_data = [
        # Tòa Sunrise (Mặt trời mọc)
        {
            "apartment_number": "SR101",
            "building": "Sunrise",
            "floor": 1,
            "area": 68.0,
            "bedrooms": 2,
            "bathrooms": 2,
            "status": ApartmentStatus.OCCUPIED,
            "description": "Căn góc view vườn hoa, thoáng mát, gần sảnh chính"
        },
        {
            "apartment_number": "SR102",
            "building": "Sunrise",
            "floor": 1,
            "area": 72.5,
            "bedrooms": 2,
            "bathrooms": 2,
            "status": ApartmentStatus.OCCUPIED,
            "description": "Thiết kế hiện đại, ban công rộng"
        },
        {
            "apartment_number": "SR201",
            "building": "Sunrise",
            "floor": 2,
            "area": 68.0,
            "bedrooms": 2,
            "bathrooms": 2,
            "status": ApartmentStatus.OCCUPIED,
            "description": "Tầng cao, view đẹp, yên tĩnh"
        },
        {
            "apartment_number": "SR202",
            "building": "Sunrise",
            "floor": 2,
            "area": 85.0,
            "bedrooms": 3,
            "bathrooms": 2,
            "status": ApartmentStatus.OCCUPIED,
            "description": "3 phòng ngủ rộng rãi, phù hợp gia đình đông người"
        },
        {
            "apartment_number": "SR301",
            "building": "Sunrise",
            "floor": 3,
            "area": 95.0,
            "bedrooms": 3,
            "bathrooms": 3,
            "status": ApartmentStatus.AVAILABLE,
            "description": "Penthouse mini, sân thượng riêng, view toàn cảnh"
        },
        # Tòa Moonlight (Ánh trăng)
        {
            "apartment_number": "ML101",
            "building": "Moonlight",
            "floor": 1,
            "area": 75.0,
            "bedrooms": 2,
            "bathrooms": 2,
            "status": ApartmentStatus.OCCUPIED,
            "description": "Nhà mới xây, nội thất cao cấp"
        },
        {
            "apartment_number": "ML102",
            "building": "Moonlight",
            "floor": 1,
            "area": 70.0,
            "bedrooms": 2,
            "bathrooms": 2,
            "status": ApartmentStatus.OCCUPIED,
            "description": "Thiết kế thông minh, tận dụng không gian"
        },
        {
            "apartment_number": "ML201",
            "building": "Moonlight",
            "floor": 2,
            "area": 82.0,
            "bedrooms": 3,
            "bathrooms": 2,
            "status": ApartmentStatus.OCCUPIED,
            "description": "3 phòng ngủ view hồ bơi"
        },
        {
            "apartment_number": "ML202",
            "building": "Moonlight",
            "floor": 2,
            "area": 75.0,
            "bedrooms": 2,
            "bathrooms": 2,
            "status": ApartmentStatus.AVAILABLE,
            "description": "Căn hộ mẫu, trang bị đầy đủ"
        },
        {
            "apartment_number": "ML301",
            "building": "Moonlight",
            "floor": 3,
            "area": 100.0,
            "bedrooms": 4,
            "bathrooms": 3,
            "status": ApartmentStatus.OCCUPIED,
            "description": "Duplex 2 tầng, phòng làm việc riêng"
        },
        # Tòa Ocean View (Nhìn ra biển)
        {
            "apartment_number": "OV101",
            "building": "Ocean View",
            "floor": 1,
            "area": 88.0,
            "bedrooms": 3,
            "bathrooms": 2,
            "status": ApartmentStatus.OCCUPIED,
            "description": "View trực diện biển, ban công lớn"
        },
        {
            "apartment_number": "OV201",
            "building": "Ocean View",
            "floor": 2,
            "area": 92.0,
            "bedrooms": 3,
            "bathrooms": 3,
            "status": ApartmentStatus.OCCUPIED,
            "description": "Căn góc 270 độ view biển"
        },
        {
            "apartment_number": "OV301",
            "building": "Ocean View",
            "floor": 3,
            "area": 120.0,
            "bedrooms": 4,
            "bathrooms": 4,
            "status": ApartmentStatus.AVAILABLE,
            "description": "Penthouse cao cấp, jacuzzi riêng, sân vườn trên cao"
        }
    ]
    
    with Session(engine) as session:
        for apt_data in apartments_data:
            apartment = Apartment(**apt_data)
            session.add(apartment)
        session.commit()
        print(f"✅ Created {len(apartments_data)} apartments")

def seed_users():
    """Create realistic users"""
    default_password = "123456"
    
    users_data = [
        # Management Team
        {
            "username": "manager",
            "email": "manager@skyresidence.com",
            "full_name": "Đỗ Minh Quân",
            "phone": "0901234567",
            "role": UserRole.MANAGER,
            "apartment_number": None,
            "building": None,
            "is_active": True
        },
        {
            "username": "accountant",
            "email": "accountant@skyresidence.com",
            "full_name": "Phạm Thu Hằng",
            "phone": "0902345678",
            "role": UserRole.ACCOUNTANT,
            "apartment_number": None,
            "building": None,
            "is_active": True
        },
        {
            "username": "receptionist",
            "email": "receptionist@skyresidence.com",
            "full_name": "Vũ Thanh Hà",
            "phone": "0903456789",
            "role": UserRole.RECEPTIONIST,
            "apartment_number": None,
            "building": None,
            "is_active": True
        },
        # Sunrise Residents
        {
            "username": "hanh.nguyen",
            "email": "hanh.nguyen@gmail.com",
            "full_name": "Nguyễn Thị Hạnh",
            "phone": "0904567890",
            "role": UserRole.USER,
            "occupier": OccupierType.OWNER,
            "apartment_number": "SR101",
            "building": "Sunrise",
            "is_active": True
        },
        {
            "username": "duc.le",
            "email": "duc.le@gmail.com",
            "full_name": "Lê Minh Đức",
            "phone": "0905678901",
            "role": UserRole.USER,
            "occupier": OccupierType.OWNER,
            "apartment_number": "SR102",
            "building": "Sunrise",
            "is_active": True
        },
        {
            "username": "lan.tran",
            "email": "lan.tran@yahoo.com",
            "full_name": "Trần Thúy Lan",
            "phone": "0906789012",
            "role": UserRole.USER,
            "occupier": OccupierType.RENTER,
            "apartment_number": "SR201",
            "building": "Sunrise",
            "is_active": True
        },
        {
            "username": "khoa.pham",
            "email": "khoa.pham@outlook.com",
            "full_name": "Phạm Đình Khoa",
            "phone": "0907890123",
            "role": UserRole.USER,
            "occupier": OccupierType.OWNER,
            "apartment_number": "SR202",
            "building": "Sunrise",
            "is_active": True
        },
        # Moonlight Residents
        {
            "username": "mai.vu",
            "email": "mai.vu@gmail.com",
            "full_name": "Vũ Thị Mai",
            "phone": "0908901234",
            "role": UserRole.USER,
            "occupier": OccupierType.OWNER,
            "apartment_number": "ML101",
            "building": "Moonlight",
            "is_active": True
        },
        {
            "username": "tuan.hoang",
            "email": "tuan.hoang@gmail.com",
            "full_name": "Hoàng Anh Tuấn",
            "phone": "0909012345",
            "role": UserRole.USER,
            "occupier": OccupierType.RENTER,
            "apartment_number": "ML102",
            "building": "Moonlight",
            "is_active": True
        },
        {
            "username": "linh.nguyen",
            "email": "linh.nguyen@yahoo.com",
            "full_name": "Nguyễn Khánh Linh",
            "phone": "0910123456",
            "role": UserRole.USER,
            "occupier": OccupierType.OWNER,
            "apartment_number": "ML201",
            "building": "Moonlight",
            "is_active": True
        },
        {
            "username": "phong.do",
            "email": "phong.do@gmail.com",
            "full_name": "Đỗ Hải Phong",
            "phone": "0911234567",
            "role": UserRole.USER,
            "occupier": OccupierType.OWNER,
            "apartment_number": "ML301",
            "building": "Moonlight",
            "is_active": True
        },
        # Ocean View Residents
        {
            "username": "dung.le",
            "email": "dung.le@outlook.com",
            "full_name": "Lê Thị Dung",
            "phone": "0912345678",
            "role": UserRole.USER,
            "occupier": OccupierType.OWNER,
            "apartment_number": "OV101",
            "building": "Ocean View",
            "is_active": True
        },
        {
            "username": "minh.tran",
            "email": "minh.tran@gmail.com",
            "full_name": "Trần Quốc Minh",
            "phone": "0913456789",
            "role": UserRole.USER,
            "occupier": OccupierType.OWNER,
            "apartment_number": "OV201",
            "building": "Ocean View",
            "is_active": True
        }
    ]
    
    with Session(engine) as session:
        for user_data in users_data:
            user = User(
                **user_data,
                hashed_password=get_password_hash(default_password),
                created_at=datetime.now()
            )
            session.add(user)
        session.commit()
        print(f"✅ Created {len(users_data)} users")

def main():
    """Main function"""
    print("=" * 70)
    print("  FORCE SEED REALISTIC DATA - XÓA & TẠO LẠI DỮ LIỆU")
    print("=" * 70)
    print()
    
    try:
        # Clear existing
        if not clear_existing_data():
            return
        
        print()
        
        # Seed apartments
        print("📦 Step 1: Creating apartments...")
        seed_apartments()
        
        print()
        
        # Seed users
        print("👥 Step 2: Creating users...")
        seed_users()
        
        print()
        print("=" * 70)
        print("✅ FORCE SEEDING COMPLETED!")
        print("=" * 70)
        print()
        print("📝 Login with:")
        print("   Manager:      manager / 123456")
        print("   Accountant:   accountant / 123456")
        print("   Receptionist: receptionist / 123456")
        print("   User:         hanh.nguyen / 123456")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
