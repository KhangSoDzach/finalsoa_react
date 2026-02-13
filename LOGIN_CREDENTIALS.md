# 🔐 THÔNG TIN ĐĂNG NHẬP HỆ THỐNG

## 📋 4 ROLES TRONG HỆ THỐNG

### 1️⃣ MANAGER (Quản lý)
- **Username:** `manager`
- **Password:** `123456`
- **Quyền hạn:** Toàn quyền quản lý hệ thống, xem tất cả dữ liệu, phê duyệt, quản lý người dùng

### 2️⃣ ACCOUNTANT (Kế toán)
- **Username:** `accountant`
- **Password:** `123456`
- **Quyền hạn:** Quản lý hóa đơn, thanh toán, báo cáo tài chính, xem dữ liệu căn hộ

### 3️⃣ RECEPTIONIST (Lễ tân)
- **Username:** `receptionist`
- **Password:** `123456`
- **Quyền hạn:** Tiếp nhận phản ánh, quản lý thông báo, xem thông tin cư dân

### 4️⃣ USER (Cư dân)
- **Username:** `user_a101`
- **Password:** `123456`
- **Căn hộ:** A101
- **Quyền hạn:** Xem hóa đơn cá nhân, gửi phản ánh, quản lý thông tin cá nhân

---

## 🏢 DANH SÁCH CƯ DÂN KHÁC (Tất cả mật khẩu: 123456)

### Tòa A
- `user_a101` - Căn A101 (Chủ hộ)
- `user_a102` - Căn A102 (Người thuê)
- `user_a201` - Căn A201 (Chủ hộ)
- `user_a202` - Căn A202 (Người thuê)
- `user_a301` - Căn A301 (Chủ hộ)

### Tòa B
- `user_b101` - Căn B101 (Người thuê)
- `user_b102` - Căn B102 (Chủ hộ)
- `user_b201` - Căn B201 (Người thuê)
- `user_b202` - Căn B202 (Chủ hộ)

### Tòa C
- `user_c101` - Căn C101 (Chủ hộ)
- `user_c201` - Căn C201 (Chủ hộ)

---

## 🚀 CÁCH SỬ DỤNG TRÊN RENDER

### Bước 1: Truy cập trang web
```
https://[your-app-name].onrender.com
```

### Bước 2: Đăng nhập
1. Nhập username và password tương ứng
2. Hệ thống sẽ tự động chuyển đến dashboard phù hợp với role

### Bước 3: Seed dữ liệu (nếu chưa có)

#### Cách 1: Qua Render Shell
```bash
# Vào Render Dashboard > Your App > Shell
cd backend
python -m scripts.seed_users
python -m scripts.seed_apartments
python -m scripts.seed_real_data  # Dữ liệu thực tế
```

#### Cách 2: Qua API endpoint (nếu có)
```bash
curl -X POST https://[your-app-name].onrender.com/api/seed/all
```

---

## 📊 TEST CASES THEO ROLE

### Test Manager
1. Đăng nhập với `manager/123456`
2. Kiểm tra xem tất cả menu (Users, Bills, Apartments, Analytics)
3. Thử tạo/sửa/xóa user
4. Xem báo cáo tổng quan hệ thống

### Test Accountant  
1. Đăng nhập với `accountant/123456`
2. Vào Bills Management
3. Tạo hóa đơn mới cho căn hộ
4. Đánh dấu thanh toán
5. Xem báo cáo doanh thu

### Test Receptionist
1. Đăng nhập với `receptionist/123456`
2. Vào Tickets/Notifications
3. Xem danh sách phản ánh từ cư dân
4. Trả lời và xử lý phản ánh
5. Gửi thông báo chung

### Test User
1. Đăng nhập với `user_a101/123456`
2. Xem hóa đơn của căn hộ A101
3. Gửi phản ánh mới
4. Cập nhật thông tin cá nhân
5. Xem thông báo

---

## ⚠️ LƯU Ý QUAN TRỌNG

1. **Đổi mật khẩu ngay** sau khi triển khai production
2. **Không dùng mật khẩu mặc định** `123456` ở môi trường thực tế
3. **Backup database** trước khi seed dữ liệu mới
4. **Kiểm tra database connection** trước khi chạy scripts

---

## 🔧 XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi: "User not found"
- Chạy lại script `seed_users.py`
- Kiểm tra database connection

### Lỗi: "Invalid credentials"
- Đảm bảo username và password chính xác
- Kiểm tra user có active không

### Lỗi: "Apartment not found"
- Chạy script `seed_apartments.py`
- Kiểm tra dữ liệu đã được seed chưa

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề, kiểm tra:
1. Render logs: `Logs` tab trong Render Dashboard
2. Database: Kết nối qua Supabase Dashboard
3. API Health: `https://[your-app-name].onrender.com/health`

---

**Cập nhật lần cuối:** 13/02/2026
