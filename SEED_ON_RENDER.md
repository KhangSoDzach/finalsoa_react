# 🚀 HƯỚNG DẪN CHẠY DỮ LIỆU THỰC TẾ TRÊN RENDER

## 📋 TỔNG QUAN

File này hướng dẫn cách import dữ liệu thực tế (tên người và căn hộ có ý nghĩa) vào hệ thống đã deploy trên Render.

---

## ✅ BƯỚC 1: KIỂM TRA ỨNG DỤNG TRÊN RENDER

### 1.1. Đảm bảo app đang chạy
```
https://[your-app-name].onrender.com/health
```
Kết quả phải là: `{"status": "healthy"}`

### 1.2. Kiểm tra database connection
Vào Render Dashboard:
- Services > Your Backend App > Logs
- Kiểm tra không có lỗi database connection

---

## 🔧 BƯỚC 2: CHẠY SCRIPT SEED DỮ LIỆU

### Phương án A: Sử dụng Render Shell (Khuyến nghị) ⭐

1. **Vào Render Dashboard**
   ```
   https://dashboard.render.com
   ```

2. **Mở Shell cho backend service**
   - Chọn service backend của bạn
   - Click vào tab "Shell" ở menu bên trái
   - Đợi shell khởi động (có thể mất 30-60 giây)

3. **Chạy lệnh seed**
   ```bash
   # Di chuyển vào thư mục backend
   cd backend
   
   # Chạy script seed dữ liệu thực tế
   python -m scripts.seed_real_data
   ```

4. **Kiểm tra kết quả**
   - Bạn sẽ thấy output:
     ```
     ✅ Created 13 realistic apartments
     ✅ Created 13 realistic users
     🔑 Default password for all users: 123456
     ```

### Phương án B: Sử dụng Local Script với Remote Database

1. **Tạo file .env.production** (nếu chưa có)
   ```env
   DATABASE_URL=postgresql://user:pass@host:5432/dbname
   ```
   ⚠️ Lấy DATABASE_URL từ Render Dashboard > Backend Service > Environment

2. **Chạy script local**
   ```bash
   # Windows PowerShell
   cd backend
   $env:DATABASE_URL = "postgresql://..."  # Thay bằng URL thực
   python -m scripts.seed_real_data
   
   # Linux/Mac
   cd backend
   export DATABASE_URL="postgresql://..."
   python -m scripts.seed_real_data
   ```

### Phương án C: Tạo API Endpoint Seed (Nâng cao)

Nếu muốn seed qua API, thêm endpoint vào backend:

```python
# app/api/routes/seed.py
from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.models.user import User, UserRole
from scripts.seed_real_data import main as seed_real_data

router = APIRouter(prefix="/seed", tags=["Seed"])

@router.post("/real-data")
async def seed_data(current_user: User = Depends(get_current_user)):
    # Chỉ manager mới được seed
    if current_user.role != UserRole.MANAGER:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    try:
        seed_real_data()
        return {"status": "success", "message": "Seeded realistic data"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

Sau đó gọi API:
```bash
curl -X POST https://[your-app].onrender.com/api/seed/real-data \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📊 BƯỚC 3: XÁC NHẬN DỮ LIỆU ĐÃ IMPORT

### 3.1. Kiểm tra qua web interface

1. **Đăng nhập với Manager**
   - Username: `manager`
   - Password: `123456`
   
2. **Kiểm tra Users**
   - Vào menu Users Management
   - Phải thấy các user mới: `hanh.nguyen`, `duc.le`, `lan.tran`, ...

3. **Kiểm tra Apartments**
   - Vào menu Apartments Management
   - Phải thấy các tòa: `Sunrise`, `Moonlight`, `Ocean View`

### 3.2. Kiểm tra qua Database (Supabase/PostgreSQL)

```sql
-- Kiểm tra users
SELECT username, full_name, apartment_number, building, role 
FROM users 
ORDER BY created_at DESC 
LIMIT 15;

-- Kiểm tra apartments
SELECT apartment_number, building, floor, area, status 
FROM apartments 
ORDER BY building, floor;

-- Kiểm tra mapping
SELECT u.full_name, u.apartment_number, a.building, a.area, a.monthly_fee
FROM users u
LEFT JOIN apartments a ON u.apartment_number = a.apartment_number
WHERE u.role = 'USER'
ORDER BY a.building, u.apartment_number;
```

---

## 🧪 BƯỚC 4: TEST 4 ROLES

### Test 1: Manager (Quản lý)
```
URL: https://[your-app].onrender.com/login
Username: manager
Password: 123456

Kiểm tra:
✓ Vào được Admin Dashboard
✓ Xem được tất cả users
✓ Xem được tất cả apartments
✓ Tạo/sửa/xóa được dữ liệu
```

### Test 2: Accountant (Kế toán)
```
Username: accountant
Password: 123456

Kiểm tra:
✓ Vào được Accountant Dashboard
✓ Xem được Bills
✓ Tạo được hóa đơn
✓ Xem báo cáo tài chính
✗ Không xem được Users Management
```

### Test 3: Receptionist (Lễ tân)
```
Username: receptionist
Password: 123456

Kiểm tra:
✓ Vào được Receptionist Dashboard
✓ Xem được Tickets/Phản ánh
✓ Trả lời phản ánh được
✓ Gửi thông báo được
✗ Không xem được Bills
```

### Test 4: User (Cư dân)
```
Username: hanh.nguyen
Password: 123456
Căn hộ: SR101

Kiểm tra:
✓ Vào được User Dashboard
✓ Xem được hóa đơn của căn SR101
✓ Gửi phản ánh được
✓ Xem thông tin căn hộ
✗ Không xem được hóa đơn căn khác
```

---

## 🗑️ XÓA DỮ LIỆU CŨ (NẾU CẦN)

### Cảnh báo: ⚠️ Thao tác này sẽ xóa TẤT CẢ dữ liệu!

```bash
# Qua Render Shell
cd backend
python -m scripts.reset_db

# Hoặc qua SQL (Supabase Dashboard)
TRUNCATE TABLE users CASCADE;
TRUNCATE TABLE apartments CASCADE;
TRUNCATE TABLE bills CASCADE;
TRUNCATE TABLE tickets CASCADE;
TRUNCATE TABLE vehicles CASCADE;
TRUNCATE TABLE notifications CASCADE;
```

Sau đó chạy lại seed:
```bash
python -m scripts.seed_real_data
```

---

## 📝 DỮ LIỆU MẪU ĐÃ TẠO

### 🏢 3 Tòa nhà:
1. **Sunrise** (Mặt trời mọc) - 5 căn
   - Tầng thấp, giá phải chăng (2.8M - 4.2M/tháng)
   - SR101, SR102, SR201, SR202, SR301

2. **Moonlight** (Ánh trăng) - 5 căn
   - Tầng trung, view đẹp (2.95M - 4.8M/tháng)
   - ML101, ML102, ML201, ML202, ML301

3. **Ocean View** (Nhìn ra biển) - 3 căn
   - Cao cấp nhất (4.1M - 6.5M/tháng)
   - OV101, OV201, OV301

### 👥 13 Người dùng:

**Ban quản lý (3):**
- Đỗ Minh Quân (Manager)
- Phạm Thu Hằng (Accountant)
- Vũ Thanh Hà (Receptionist)

**Cư dân Sunrise (4):**
- Nguyễn Thị Hạnh - SR101 (Chủ hộ)
- Lê Minh Đức - SR102 (Chủ hộ)
- Trần Thúy Lan - SR201 (Người thuê)
- Phạm Đình Khoa - SR202 (Chủ hộ)

**Cư dân Moonlight (4):**
- Vũ Thị Mai - ML101 (Chủ hộ)
- Hoàng Anh Tuấn - ML102 (Người thuê)
- Nguyễn Khánh Linh - ML201 (Chủ hộ)
- Đỗ Hải Phong - ML301 (Chủ hộ)

**Cư dân Ocean View (2):**
- Lê Thị Dung - OV101 (Chủ hộ)
- Trần Quốc Minh - OV201 (Chủ hộ)

---

## ❓ XỬ LÝ LỖI

### Lỗi: "Table does not exist"
```bash
# Chạy migration
cd backend
alembic upgrade head

# Hoặc chạy init script
python -m scripts.reset_db
python -m scripts.seed_real_data
```

### Lỗi: "User/Apartment already exists"
```
⚠️ Users already exist. Skipping user seeding...
```
Giải pháp: Script tự động skip nếu data đã tồn tại. Muốn seed lại:
1. Xóa dữ liệu cũ (xem phần "XÓA DỮ LIỆU CŨ")
2. Chạy lại script

### Lỗi: "Connection refused"
- Kiểm tra DATABASE_URL đúng chưa
- Kiểm tra Render service đã deploy xong chưa
- Kiểm tra IP whitelist trong Supabase (nếu dùng Supabase)

---

## 🎯 CHECKLIST HOÀN THÀNH

- [ ] App chạy thành công trên Render
- [ ] Database connection OK
- [ ] Chạy script seed_real_data thành công
- [ ] Đăng nhập được với Manager
- [ ] Đăng nhập được với Accountant
- [ ] Đăng nhập được với Receptionist
- [ ] Đăng nhập được với User (cư dân)
- [ ] Xem được danh sách apartments
- [ ] Xem được danh sách users
- [ ] Tạo được bills/tickets mẫu

---

## 📞 LIÊN HỆ HỖ TRỢ

Nếu gặp vấn đề:
1. Check Render logs: Dashboard > Logs
2. Check Database: Supabase Dashboard
3. Check API: `/health`, `/docs` endpoints

**Cập nhật:** 13/02/2026
