# 🎯 HƯỚNG DẪN NHANH - ĐĂNG NHẬP & IMPORT DỮ LIỆU

## 📌 TÓM TẮT NHANH

Bạn đã deploy app lên Render. Giờ cần:
1. ✅ Biết thông tin đăng nhập cho 4 roles
2. ✅ Import dữ liệu căn hộ/người dùng với tên thực tế  

---

## 🔐 THÔNG TIN ĐĂNG NHẬP 4 ROLES

### Mật khẩu mặc định: `123456`

| Role | Username | Họ tên | Quyền hạn |
|------|----------|--------|-----------|
| **Manager** | `manager` | Đỗ Minh Quân | Toàn quyền hệ thống |
| **Accountant** | `accountant` | Phạm Thu Hằng | Quản lý hóa đơn, tài chính |
| **Receptionist** | `receptionist` | Vũ Thanh Hà | Xử lý phản ánh, thông báo |
| **User** | `hanh.nguyen` | Nguyễn Thị Hạnh | Xem hóa đơn, gửi phản ánh |

👉 **Xem chi tiết:** [LOGIN_CREDENTIALS.md](LOGIN_CREDENTIALS.md)

---

## 🏢 DỮ LIỆU CĂN HỘ MẪU

Script đã tạo 3 tòa nhà với tên có ý nghĩa:

### 🌅 Tòa Sunrise (5 căn hộ)
- SR101, SR102, SR201, SR202, SR301
- Đặc điểm: Tầng thấp, giá phải chăng

### 🌙 Tòa Moonlight (5 căn hộ)
- ML101, ML102, ML201, ML202, ML301
- Đặc điểm: Tầng trung, view đẹp

### 🌊 Tòa Ocean View (3 căn hộ)
- OV101, OV201, OV301
- Đặc điểm: Cao cấp, view biển

### 👥 Cư dân mẫu (tên thực tế)
- Nguyễn Thị Hạnh (SR101)
- Lê Minh Đức (SR102)
- Trần Thúy Lan (SR201)
- Phạm Đình Khoa (SR202)
- Vũ Thị Mai (ML101)
- Hoàng Anh Tuấn (ML102)
- Nguyễn Khánh Linh (ML201)
- Đỗ Hải Phong (ML301)
- Lê Thị Dung (OV101)
- Trần Quốc Minh (OV201)

---

## 🚀 CÁCH CHẠY TRÊN RENDER

### Option 1: Dữ liệu mới (Khuyến nghị) ⭐

**Nếu bạn muốn dữ liệu hoàn toàn mới:**

```bash
# Vào Render Dashboard > Your Backend Service > Shell
cd backend

# Xóa dữ liệu cũ (CẢNH BÁO: Mất hết dữ liệu hiện tại!)
python -m scripts.reset_db

# Import dữ liệu mới với tên thực tế
python -m scripts.seed_real_data
```

### Option 2: Giữ dữ liệu cũ + Thêm mới

**Nếu muốn giữ cả dữ liệu cũ:**

Hiện tại script tự động bỏ qua nếu đã có data. Bạn có thể:
- Login với users hiện tại (manager/123456)
- Tạo thủ công thêm căn hộ/users qua giao diện Admin

### Option 3: Chạy local rồi push lên

```powershell
# Windows PowerShell - Local
cd backend
$env:DATABASE_URL = "postgresql://..."  # Lấy từ Render
python -m scripts.seed_real_data
```

👉 **Xem chi tiết:** [SEED_ON_RENDER.md](SEED_ON_RENDER.md)

---

## ✅ KIỂM TRA SAU KHI SEED

### 1. Test đăng nhập qua Web
```
URL: https://[your-app].onrender.com
```

**Test 4 roles:**
- ✓ Manager: `manager/123456` → Vào được Admin Dashboard
- ✓ Accountant: `accountant/123456` → Quản lý Bills
- ✓ Receptionist: `receptionist/123456` → Xử lý Tickets
- ✓ User: `hanh.nguyen/123456` → Xem hóa đơn căn SR101

### 2. Test qua script (local)
```bash
cd backend
python -m scripts.test_real_data
```

Kết quả mong đợi:
```
✅ Database Connection
✅ Users Data (13 users)
✅ Apartments Data (13 apartments)
✅ Login Credentials
✅ Data Relationships
```

---

## 🎯 CHECKLIST HOÀN THÀNH

Đánh dấu vào các bước đã làm:

- [ ] ✅ App đã deploy và chạy trên Render
- [ ] ✅ Đã chạy script seed_real_data trên Render
- [ ] ✅ Đăng nhập được với Manager
- [ ] ✅ Đăng nhập được với Accountant  
- [ ] ✅ Đăng nhập được với Receptionist
- [ ] ✅ Đăng nhập được với User (cư dân)
- [ ] ✅ Xem được danh sách apartments (3 tòa)
- [ ] ✅ Xem được danh sách users (13 người)

---

## 📂 CÁC FILE LIÊN QUAN

| File | Mô tả |
|------|-------|
| [LOGIN_CREDENTIALS.md](LOGIN_CREDENTIALS.md) | Chi tiết tất cả accounts đăng nhập |
| [SEED_ON_RENDER.md](SEED_ON_RENDER.md) | Hướng dẫn chi tiết chạy trên Render |
| [seed_real_data.py](backend/scripts/seed_real_data.py) | Script seed dữ liệu thực tế |
| [test_real_data.py](backend/scripts/test_real_data.py) | Script test dữ liệu |

---

## ⚠️ LƯU Ý QUAN TRỌNG

### Về Mật khẩu
- ⚠️ Mật khẩu mặc định `123456` CHỈ dùng cho DEV/TESTING
- 🔒 Đổi ngay khi deploy production
- 🔐 Nên dùng mật khẩu mạnh: ít nhất 8 ký tự, có chữ hoa, số, ký tự đặc biệt

### Về Dữ liệu
- 💾 Backup database trước khi reset
- 🚫 Script `reset_db` sẽ XÓA TẤT CẢ dữ liệu
- ✅ Script `seed_real_data` tự động skip nếu đã có data

### Về Naming
- ✅ DÙNG: Tên có ý nghĩa (Nguyễn Thị Hạnh, Lê Minh Đức)
- ❌ TRÁNH: Tên giả (Nguyễn Văn A, John Smith)

---

## 🆘 GẶP VẤN ĐỀ?

### Lỗi: "User not found"
```bash
# Solution: Chạy lại seed users
cd backend
python -m scripts.seed_real_data
```

### Lỗi: "Database connection failed"
```bash
# Check DATABASE_URL trong Render Environment Variables
# Verify database service đang chạy (Supabase/PostgreSQL)
```

### Lỗi: "Already exists"
Script tự động skip. Nếu muốn thay thế:
```bash
python -m scripts.reset_db
python -m scripts.seed_real_data
```

---

## 📞 SUPPORT

Nếu cần hỗ trợ:
1. Check Render Logs: Dashboard > Logs
2. Check Database: Supabase Dashboard  
3. Test API: `https://[app].onrender.com/health`
4. Test locally: `python -m scripts.test_real_data`

---

**Cập nhật:** 13/02/2026  
**Version:** 1.0
