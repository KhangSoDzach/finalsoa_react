# 🔧 XỬ LÝ LỖI 500 KHI SEED

## ❌ Lỗi đang gặp:
```
POST https://apartment-backend-rdcs.onrender.com/api/v1/seed/real-data
→ 500 Internal Server Error
```

---

## 🔍 NGUYÊN NHÂN & GIẢI PHÁP

### 1️⃣ Database chưa được cấu hình (PHỔ BIẾN NHẤT)

**Kiểm tra:**
1. Vào Render Dashboard: https://dashboard.render.com
2. Chọn service **apartment-backend-rdcs**
3. Tab **Environment**
4. Tìm biến `DATABASE_URL`

**Nếu CHƯA CÓ hoặc SAI:**

#### Setup Supabase (2 phút):

**A. Tạo Supabase database:**
```
1. Vào https://supabase.com
2. Sign up with GitHub
3. New Project:
   - Name: apartment-system
   - Password: [your-password]
   - Region: Singapore
4. Đợi 2 phút để setup
```

**B. Lấy connection string:**
```
Supabase Dashboard
→ Settings
→ Database
→ Connection String
→ Tab "URI"
→ Copy: postgresql://postgres.[xxx]@[host].supabase.co:5432/postgres
```

**C. Thêm vào Render:**
```
Render Dashboard
→ apartment-backend-rdcs
→ Environment tab
→ Add Environment Variable:
   Key: DATABASE_URL
   Value: [paste Supabase URI]
→ Save Changes
```

**D. Đợi Render redeploy (~2 phút)**

Check progress trong tab **Events**

---

### 2️⃣ Kiểm tra Render Logs

```
Render Dashboard
→ apartment-backend-rdcs
→ Logs tab
→ Xem error messages màu đỏ
```

**Các lỗi thường gặp:**

#### Lỗi: "Could not connect to database"
```
❌ could not connect to server: Connection refused
```
**Giải pháp:** DATABASE_URL chưa đúng, check lại

#### Lỗi: "relation does not exist"
```
❌ relation "user" does not exist
```
**Giải pháp:** Chạy migration
```bash
# Qua Render Shell:
alembic upgrade head
```

#### Lỗi: "No module named 'xxx'"
```
❌ ModuleNotFoundError: No module named 'sqlmodel'
```
**Giải pháp:** Dependencies chưa cài đủ (hiếm gặp với Render)

---

### 3️⃣ Chạy lại deployment

Sau khi fix DATABASE_URL:

**Cách 1: Auto (khuyến nghị)**
```
Render tự động redeploy khi thay đổi environment
→ Đợi ~2 phút
→ Check tab Events
```

**Cách 2: Manual redeploy**
```
Render Dashboard
→ apartment-backend-rdcs
→ Manual Deploy
→ Deploy latest commit
```

---

## ✅ SAU KHI FIX

### Bước 1: Đợi deploy xong
```
Events tab → Thấy "Live" với checkmark xanh
```

### Bước 2: Test API health
```
https://apartment-backend-rdcs.onrender.com/api/v1/seed/health
```

Phải thấy:
```json
{
  "status": "healthy",
  "message": "Seed API is ready",
  "endpoints": [...]
}
```

### Bước 3: Seed dữ liệu
```powershell
Invoke-WebRequest -Uri "https://apartment-backend-rdcs.onrender.com/api/v1/seed/real-data" -Method POST
```

Hoặc mở trong browser:
```
https://apartment-backend-rdcs.onrender.com/api/v1/seed/real-data
```
(Lưu ý: Browser dùng GET nên có thể báo lỗi 405, dùng PowerShell POST thay thế)

---

## 🗄️ SETUP SUPABASE CHI TIẾT

### Tại sao Supabase?
✅ **500MB miễn phí**  
✅ **Luôn online** (không sleep)  
✅ **Dashboard đẹp**  
✅ **PostgreSQL chuẩn**  
✅ **Auto backup hàng ngày**  

### Các bước setup:

**1. Tạo account:**
```
https://supabase.com
→ Continue with GitHub
```

**2. Tạo organization (nếucần):**
```
Organization name: YourName
→ Create organization
```

**3. Tạo project:**
```
New Project
  Name: apartment-system
  Database Password: [strong password - save it!]
  Region: Southeast Asia (Singapore)
  Pricing Plan: Free
→ Create new project
→ Đợi ~2 phút
```

**4. Lấy database URL:**
```
Project Dashboard
→ Settings (⚙️ icon bên trái)
→ Database
→ Scroll xuống "Connection string"
→ Chọn tab "URI"
→ Mode: "Session"
→ Copy toàn bộ chuỗi (bắt đầu với postgresql://)
```

Example:
```
postgresql://postgres.abcdefghijk:password@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres
```

**5. Thêm vào Render:**
```
https://dashboard.render.com
→ Chọn service: apartment-backend-rdcs
→ Environment tab (bên trái)
→ Click "+ Add Environment Variable"
→ Key: DATABASE_URL
→ Value: [paste connection string từ Supabase]
→ Click "Add"
→ Click "Save Changes" (góc trên phải)
```

**6. Kiểm tra deployment:**
```
Tab "Events":
→ Thấy "Deploy started"
→ Đợi ~2 phút
→ Thấy "Live" với checkmark xanh ✅
```

**7. Test connection:**
```
Tab "Logs":
→ Không thấy error về database
→ Thấy "Application startup complete"
```

---

## 🧪 TEST TỪNG BƯỚC

### Test 1: Backend có chạy không?
```
https://apartment-backend-rdcs.onrender.com/
```
**Kỳ vọng:** `{"message":"Apartment Management API is running"}`

### Test 2: API docs có không?
```
https://apartment-backend-rdcs.onrender.com/docs
```
**Kỳ vọng:** Trang Swagger UI hiển thị

### Test 3: Seed health check
```
https://apartment-backend-rdcs.onrender.com/api/v1/seed/health
```
**Kỳ vọng:** `{"status":"healthy",...}`

### Test 4: Seed data (qua PowerShell)
```powershell
Invoke-WebRequest -Uri "https://apartment-backend-rdcs.onrender.com/api/v1/seed/real-data" -Method POST
```
**Kỳ vọng:** Status 200, response JSON với "success"

---

## 📋 CHECKLIST FIX LỖI 500

- [ ] Supabase project đã tạo xong
- [ ] Database password đã lưu lại
- [ ] Connection string đã copy đúng (bắt đầu với postgresql://)
- [ ] DATABASE_URL đã thêm vào Render Environment
- [ ] Render đã redeploy xong (check Events tab)
- [ ] Test / endpoint → thấy API message
- [ ] Test /docs endpoint → thấy Swagger UI
- [ ] Test /api/v1/seed/health → thấy "healthy"
- [ ] POST /api/v1/seed/real-data → Status 200

---

## 🆘 VẪN GẶP LỖI?

### Check Render Logs chi tiết:
```
Render Dashboard
→ apartment-backend-rdcs
→ Logs tab
→ Tìm dòng màu đỏ cuối cùng
→ Copy error message
```

### Common errors:

#### "could not translate host name"
```
❌ could not translate host name "xxx" to address
```
→ DNS issue, đợi 5 phút và thử lại

#### "password authentication failed"
```
❌ password authentication failed for user "postgres"
```
→ Password trong DATABASE_URL sai, check lại

#### "SSL connection required"
```
❌ server requires SSL
```
→ Thêm `?sslmode=require` vào cuối DATABASE_URL

#### "too many connections"
```
❌ FATAL: too many connections
```
→ Supabase free tier bị limit, restart database hoặc tăng plan

---

## 💡 PRO TIPS

### Tip 1: Test database connection trực tiếp
Trong Supabase Dashboard:
```
SQL Editor
→ New query
→ Chạy: SELECT version();
→ Phải thấy PostgreSQL version
```

### Tip 2: View tables trong Supabase
```
Table Editor
→ Xem bảng: user, apartment, bill, etc.
```

### Tip 3: Monitor Render logs real-time
```
Logs tab → Để tab này mở
→ Chạy seed command
→ Xem logs real-time
```

---

**Cập nhật:** 13/02/2026  
**Khuyến nghị database:** Supabase (https://supabase.com)  
**Support:** Check Render Logs trước khi hỏi
