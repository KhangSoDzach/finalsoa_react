"""
Script to seed realistic data with meaningful names for apartments and users
Dữ liệu thực tế với tên có ý nghĩa, tránh tên giả
Run: python -m scripts.seed_real_data
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select
from app.core.database import engine
from app.models.user import User, UserRole, OccupierType
from app.models.apartment import Apartment, ApartmentStatus
from app.core.security import get_password_hash
from decimal import Decimal
from datetime import datetime

def seed_real_apartments():
    """Create realistic apartments with meaningful data"""
    
    apartments_data = [
        # Tòa Sunrise (Mặt trời mọc) - Tầng thấp, giá phải chăng
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
        
        # Tòa Moonlight (Ánh trăng) - Tầng trung, view đẹp
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
        
        # Tòa Ocean View (Nhìn ra biển) - Cao cấp nhất
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
        # Check existing apartments
        existing = session.exec(select(Apartment)).first()
        if existing:
            print("⚠️  Apartments already exist. Skipping apartment seeding...")
            return
        
        # Add all apartments
        for apt_data in apartments_data:
            apartment = Apartment(**apt_data)
            session.add(apartment)
        
        session.commit()
        print(f"✅ Created {len(apartments_data)} realistic apartments")
        print(f"   - Sunrise Building: {len([a for a in apartments_data if a['building'] == 'Sunrise'])}")
        print(f"   - Moonlight Building: {len([a for a in apartments_data if a['building'] == 'Moonlight'])}")
        print(f"   - Ocean View Building: {len([a for a in apartments_data if a['building'] == 'Ocean View'])}")
        print(f"   - Occupied: {len([a for a in apartments_data if a['status'] == ApartmentStatus.OCCUPIED])}")
        print(f"   - Available: {len([a for a in apartments_data if a['status'] == ApartmentStatus.AVAILABLE])}")

def seed_real_users():
    """Create realistic users with meaningful names"""
    
    # Default password for all users
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
        
        # Sunrise Building Residents
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
        
        # Moonlight Building Residents
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
        
        # Ocean View Building Residents (Premium)
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
        # Check if users already exist
        existing = session.exec(select(User)).first()
        if existing:
            print("⚠️  Users already exist. Skipping user seeding...")
            return
        
        # Add all users
        created_count = 0
        for user_data in users_data:
            # Check if user already exists
            existing_user = session.exec(
                select(User).where(User.username == user_data["username"])
            ).first()
            
            if not existing_user:
                user = User(
                    **user_data,
                    hashed_password=get_password_hash(default_password),
                    created_at=datetime.now()
                )
                session.add(user)
                created_count += 1
        
        session.commit()
        print(f"✅ Created {created_count} realistic users")
        print(f"   - Manager: {len([u for u in users_data if u['role'] == UserRole.MANAGER])}")
        print(f"   - Accountant: {len([u for u in users_data if u['role'] == UserRole.ACCOUNTANT])}")
        print(f"   - Receptionist: {len([u for u in users_data if u['role'] == UserRole.RECEPTIONIST])}")
        print(f"   - Regular Users: {len([u for u in users_data if u['role'] == UserRole.USER])}")
        print(f"   - Owners: {len([u for u in users_data if u.get('occupier') == OccupierType.OWNER])}")
        print(f"   - Renters: {len([u for u in users_data if u.get('occupier') == OccupierType.RENTER])}")
        print(f"\n🔑 Default password for all users: {default_password}")

def main():
    """Main function to seed all realistic data"""
    print("=" * 70)
    print("  SEEDING REALISTIC DATA - DỮ LIỆU THỰC TẾ")
    print("=" * 70)
    print()
    
    try:
        # Seed apartments first
        print("📦 Step 1: Creating realistic apartments...")
        seed_real_apartments()
        print()
        
        # Then seed users
        print("👥 Step 2: Creating realistic users...")
        seed_real_users()
        print()
        
        print("=" * 70)
        print("✅ SEEDING COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print()
        print("📝 Login Credentials:")
        print("   Manager:      manager / 123456")
        print("   Accountant:   accountant / 123456")
        print("   Receptionist: receptionist / 123456")
        print("   User Example: hanh.nguyen / 123456 (Căn SR101)")
        print()
        print("🏢 Buildings:")
        print("   - Sunrise (Mặt trời mọc): Tầng thấp, giá phải chăng")
        print("   - Moonlight (Ánh trăng): Tầng trung, view đẹp")
        print("   - Ocean View (Nhìn ra biển): Cao cấp nhất")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
