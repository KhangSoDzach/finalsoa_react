"""
Seed API Routes - For seeding data remotely on Render
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select, delete
from app.core.database import get_session
from app.models.user import User, UserRole, OccupierType
from app.models.apartment import Apartment, ApartmentStatus
from app.core.security import get_password_hash
from datetime import datetime
from typing import Dict, Any

router = APIRouter()

@router.get("/health")
async def seed_health():
    """Check if seed endpoint is available"""
    return {
        "status": "healthy",
        "message": "Seed API is ready",
        "endpoints": [
            "GET /seed/health - This endpoint",
            "POST /seed/real-data - Seed realistic data (without clearing)",
            "POST /seed/force-real-data?secret=YOUR_SECRET - Force seed (clear & recreate)"
        ]
    }

@router.post("/real-data")
async def seed_real_data(session: Session = Depends(get_session)) -> Dict[str, Any]:
    """
    Seed realistic data (apartments + users)
    Skips if data already exists
    """
    try:
        # Check if data exists
        existing_apartments = session.exec(select(Apartment)).first()
        existing_users = session.exec(select(User)).first()
        
        if existing_apartments and existing_users:
            return {
                "status": "skipped",
                "message": "Data already exists. Use /seed/force-real-data to override.",
                "apartments": len(session.exec(select(Apartment)).all()),
                "users": len(session.exec(select(User)).all())
            }
        
        # Seed apartments if not exists
        apartments_created = 0
        if not existing_apartments:
            apartments_created = _seed_apartments(session)
        
        # Seed users if not exists
        users_created = 0
        if not existing_users:
            users_created = _seed_users(session)
        
        return {
            "status": "success",
            "message": "Realistic data seeded successfully",
            "apartments_created": apartments_created,
            "users_created": users_created
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Seed failed: {str(e)}")

@router.post("/force-real-data")
async def force_seed_real_data(
    secret: str,
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    Force seed realistic data (clear existing and recreate)
    Requires secret parameter for security
    Secret should be set in environment variable SEED_SECRET
    """
    import os
    expected_secret = os.getenv("SEED_SECRET", "render-seed-2026")
    
    if secret != expected_secret:
        raise HTTPException(status_code=403, detail="Invalid secret")
    
    try:
        # Clear existing data
        deleted_apartments = session.exec(delete(Apartment)).rowcount
        
        # Delete users (keep manager for safety)
        users_to_delete = session.exec(
            select(User).where(User.role != UserRole.MANAGER)
        ).all()
        
        deleted_users = 0
        for user in users_to_delete:
            try:
                session.delete(user)
                deleted_users += 1
            except:
                pass
        
        session.commit()
        
        # Seed new data
        apartments_created = _seed_apartments(session)
        users_created = _seed_users(session)
        
        return {
            "status": "success",
            "message": "Data cleared and reseeded successfully",
            "deleted": {
                "apartments": deleted_apartments,
                "users": deleted_users
            },
            "created": {
                "apartments": apartments_created,
                "users": users_created
            }
        }
        
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Force seed failed: {str(e)}")

def _seed_apartments(session: Session) -> int:
    """Internal function to seed apartments"""
    apartments_data = [
        # Tòa Sunrise
        {"apartment_number": "SR101", "building": "Sunrise", "floor": 1, "area": 68.0, 
         "bedrooms": 2, "bathrooms": 2, "status": ApartmentStatus.OCCUPIED,
         "description": "Căn góc view vườn hoa, thoáng mát"},
        {"apartment_number": "SR102", "building": "Sunrise", "floor": 1, "area": 72.5,
         "bedrooms": 2, "bathrooms": 2, "status": ApartmentStatus.OCCUPIED,
         "description": "Thiết kế hiện đại, ban công rộng"},
        {"apartment_number": "SR201", "building": "Sunrise", "floor": 2, "area": 68.0,
         "bedrooms": 2, "bathrooms": 2, "status": ApartmentStatus.OCCUPIED,
         "description": "Tầng cao, view đẹp"},
        {"apartment_number": "SR202", "building": "Sunrise", "floor": 2, "area": 85.0,
         "bedrooms": 3, "bathrooms": 2, "status": ApartmentStatus.OCCUPIED,
         "description": "3 phòng ngủ rộng rãi"},
        {"apartment_number": "SR301", "building": "Sunrise", "floor": 3, "area": 95.0,
         "bedrooms": 3, "bathrooms": 3, "status": ApartmentStatus.AVAILABLE,
         "description": "Penthouse mini, sân thượng riêng"},
        
        # Tòa Moonlight
        {"apartment_number": "ML101", "building": "Moonlight", "floor": 1, "area": 75.0,
         "bedrooms": 2, "bathrooms": 2, "status": ApartmentStatus.OCCUPIED,
         "description": "Nhà mới xây, nội thất cao cấp"},
        {"apartment_number": "ML102", "building": "Moonlight", "floor": 1, "area": 70.0,
         "bedrooms": 2, "bathrooms": 2, "status": ApartmentStatus.OCCUPIED,
         "description": "Thiết kế thông minh"},
        {"apartment_number": "ML201", "building": "Moonlight", "floor": 2, "area": 82.0,
         "bedrooms": 3, "bathrooms": 2, "status": ApartmentStatus.OCCUPIED,
         "description": "3 phòng ngủ view hồ bơi"},
        {"apartment_number": "ML202", "building": "Moonlight", "floor": 2, "area": 75.0,
         "bedrooms": 2, "bathrooms": 2, "status": ApartmentStatus.AVAILABLE,
         "description": "Căn hộ mẫu"},
        {"apartment_number": "ML301", "building": "Moonlight", "floor": 3, "area": 100.0,
         "bedrooms": 4, "bathrooms": 3, "status": ApartmentStatus.OCCUPIED,
         "description": "Duplex 2 tầng"},
        
        # Tòa Ocean View
        {"apartment_number": "OV101", "building": "Ocean View", "floor": 1, "area": 88.0,
         "bedrooms": 3, "bathrooms": 2, "status": ApartmentStatus.OCCUPIED,
         "description": "View trực diện biển"},
        {"apartment_number": "OV201", "building": "Ocean View", "floor": 2, "area": 92.0,
         "bedrooms": 3, "bathrooms": 3, "status": ApartmentStatus.OCCUPIED,
         "description": "Căn góc 270 độ view biển"},
        {"apartment_number": "OV301", "building": "Ocean View", "floor": 3, "area": 120.0,
         "bedrooms": 4, "bathrooms": 4, "status": ApartmentStatus.AVAILABLE,
         "description": "Penthouse cao cấp, jacuzzi riêng"},
    ]
    
    for apt_data in apartments_data:
        apartment = Apartment(**apt_data)
        session.add(apartment)
    
    session.commit()
    return len(apartments_data)

def _seed_users(session: Session) -> int:
    """Internal function to seed users"""
    default_password = "123456"
    
    users_data = [
        # Management
        {"username": "manager", "email": "manager@skyresidence.com",
         "full_name": "Đỗ Minh Quân", "phone": "0901234567",
         "role": UserRole.MANAGER, "apartment_number": None, "building": None},
        {"username": "accountant", "email": "accountant@skyresidence.com",
         "full_name": "Phạm Thu Hằng", "phone": "0902345678",
         "role": UserRole.ACCOUNTANT, "apartment_number": None, "building": None},
        {"username": "receptionist", "email": "receptionist@skyresidence.com",
         "full_name": "Vũ Thanh Hà", "phone": "0903456789",
         "role": UserRole.RECEPTIONIST, "apartment_number": None, "building": None},
        
        # Residents
        {"username": "hanh.nguyen", "email": "hanh.nguyen@gmail.com",
         "full_name": "Nguyễn Thị Hạnh", "phone": "0904567890",
         "role": UserRole.USER, "occupier": OccupierType.OWNER,
         "apartment_number": "SR101", "building": "Sunrise"},
        {"username": "duc.le", "email": "duc.le@gmail.com",
         "full_name": "Lê Minh Đức", "phone": "0905678901",
         "role": UserRole.USER, "occupier": OccupierType.OWNER,
         "apartment_number": "SR102", "building": "Sunrise"},
        {"username": "lan.tran", "email": "lan.tran@yahoo.com",
         "full_name": "Trần Thúy Lan", "phone": "0906789012",
         "role": UserRole.USER, "occupier": OccupierType.RENTER,
         "apartment_number": "SR201", "building": "Sunrise"},
        {"username": "khoa.pham", "email": "khoa.pham@outlook.com",
         "full_name": "Phạm Đình Khoa", "phone": "0907890123",
         "role": UserRole.USER, "occupier": OccupierType.OWNER,
         "apartment_number": "SR202", "building": "Sunrise"},
        {"username": "mai.vu", "email": "mai.vu@gmail.com",
         "full_name": "Vũ Thị Mai", "phone": "0908901234",
         "role": UserRole.USER, "occupier": OccupierType.OWNER,
         "apartment_number": "ML101", "building": "Moonlight"},
        {"username": "tuan.hoang", "email": "tuan.hoang@gmail.com",
         "full_name": "Hoàng Anh Tuấn", "phone": "0909012345",
         "role": UserRole.USER, "occupier": OccupierType.RENTER,
         "apartment_number": "ML102", "building": "Moonlight"},
        {"username": "linh.nguyen", "email": "linh.nguyen@yahoo.com",
         "full_name": "Nguyễn Khánh Linh", "phone": "0910123456",
         "role": UserRole.USER, "occupier": OccupierType.OWNER,
         "apartment_number": "ML201", "building": "Moonlight"},
        {"username": "phong.do", "email": "phong.do@gmail.com",
         "full_name": "Đỗ Hải Phong", "phone": "0911234567",
         "role": UserRole.USER, "occupier": OccupierType.OWNER,
         "apartment_number": "ML301", "building": "Moonlight"},
        {"username": "dung.le", "email": "dung.le@outlook.com",
         "full_name": "Lê Thị Dung", "phone": "0912345678",
         "role": UserRole.USER, "occupier": OccupierType.OWNER,
         "apartment_number": "OV101", "building": "Ocean View"},
        {"username": "minh.tran", "email": "minh.tran@gmail.com",
         "full_name": "Trần Quốc Minh", "phone": "0913456789",
         "role": UserRole.USER, "occupier": OccupierType.OWNER,
         "apartment_number": "OV201", "building": "Ocean View"},
    ]
    
    for user_data in users_data:
        user = User(
            **user_data,
            hashed_password=get_password_hash(default_password),
            is_active=True,
            created_at=datetime.now()
        )
        session.add(user)
    
    session.commit()
    return len(users_data)
