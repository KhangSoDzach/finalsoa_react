# 🚀 HƯỚNG DẪN SEED DỮ LIỆU LÊN RENDER

## 📌 URL Backend của bạn
```
https://apartment-backend-rdcs.onrender.com
```

---

## ✅ CÁCH 1: SEED QUA API (KHUYẾN NGHỊ - DỄ NHẤT)

### Bước 1: Đợi backend khởi động
Render free tier có cold start (tắt sau 15 phút không dùng). Truy cập để đánh thức:
```
https://apartment-backend-rdcs.onrender.com/health
```
Đợi 30-60 giây nếu thấy lỗi 503.

### Bước 2: Kiểm tra Seed API
```
https://apartment-backend-rdcs.onrender.com/api/v1/seed/health
```

### Bước 3: Seed dữ liệu

**Option A: Seed tự động (không xóa data cũ)**
```bash
# PowerShell
Invoke-WebRequest -Uri "https://apartment-backend-rdcs.onrender.com/api/v1/seed/real-data" -Method POST
```

Hoặc dùng browser/Postman:
```
POST https://apartment-backend-rdcs.onrender.com/api/v1/seed/real-data
```

**Option B: Force Seed (xóa & tạo mới)**
```bash
# PowerShell
Invoke-WebRequest -Uri "https://apartment-backend-rdcs.onrender.com/api/v1/seed/force-real-data?secret=render-seed-2026" -Method POST
```

Hoặc:
```
POST https://apartment-backend-rdcs.onrender.com/api/v1/seed/force-real-data?secret=render-seed-2026
```

### Bước 4: Kiểm tra kết quả
Truy cập Swagger UI để xem:
```
https://apartment-backend-rdcs.onrender.com/docs
```

---

## ✅ CÁCH 2: SEED QUA RENDER SHELL

### Bước 1: Vào Render Dashboard
```
https://dashboard.render.com
```

### Bước 2: Mở Shell
1. Chọn service **apartment-backend-rdcs**
2. Click tab **Shell** bên trái
3. Đợi shell khởi động (~30 giây)

### Bước 3: Chạy lệnh seed

**Seed tự động (skip nếu có data):**
```bash
cd backend
python -m scripts.seed_real_data
```

**Force seed (xóa & tạo mới):**
```bash
cd backend
python -m scripts.force_seed_real_data
# Gõ "yes" khi được hỏi
```

---

## ✅ CÁCH 3: SEED TỪ LOCAL

Nếu có DATABASE_URL:

```powershell
# Lấy DATABASE_URL từ Render Environment Variables
# Dashboard > apartment-backend-rdcs > Environment > DATABASE_URL

cd backend
$env:DATABASE_URL = "postgresql://user:pass@host:5432/db"
python -m scripts.seed_real_data
```

---

## 🗄️ DATABASE MIỄN PHÍ TỐT NHẤT

### 🏆 Top 3 Khuyến Nghị:

#### 1. **Supabase** (⭐ BEST CHOICE)
**✅ Ưu điểm:**
- 500MB database miễn phí
- PostgreSQL chuẩn
- Dashboard đẹp, dễ dùng
- Tốc độ cao
- Auto-backup hàng ngày
- API tự động
- Không sleep (luôn online)

**📝 Đăng ký:**
```
https://supabase.com
```

**🔧 Setup:**
1. Create new project
2. Lấy connection string: Settings > Database > URI
3. Thêm vào Render Environment: `DATABASE_URL`

**💰 Free Plan:**
- 500MB database
- Unlimited API requests
- 50,000 monthly active users
- 2GB file storage

---

#### 2. **Neon** (⭐ RUNNER-UP)
**✅ Ưu điểm:**
- 0.5GB storage miễn phí
- Serverless PostgreSQL
- Auto-pause khi không dùng (tiết kiệm)
- Branching database (như Git)
- Rất nhanh

**📝 Đăng ký:**
```
https://neon.tech
```

**💰 Free Plan:**
- 0.5GB storage
- 1 project
- 10 branches
- Unlimited queries

---

#### 3. **Railway** (⭐ GOOD OPTION)
**✅ Ưu điểm:**
- $5 credit miễn phí/tháng
- PostgreSQL + Redis
- Deploy App + DB cùng chỗ
- CI/CD tự động

**📝 Đăng ký:**
```
https://railway.app
```

**💰 Free Plan:**
- $5/month credit
- ~500MB database
- 100GB bandwidth

---

### 📊 So Sánh:

| Feature | Supabase | Neon | Railway |
|---------|----------|------|---------|
| **Storage** | 500MB | 512MB | ~500MB |
| **Uptime** | 100% | 100% | 100% |
| **Sleep/Pause** | ❌ No | ✅ Auto | ❌ No |
| **Backup** | ✅ Auto | ✅ Auto | ❌ Manual |
| **Dashboard** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Speed** | Nhanh | Rất nhanh | Nhanh |
| **Dễ dùng** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

### 🎯 Khuyến Nghị:

**Cho project của bạn: SUPABASE** ⭐
- Không giới hạn requests
- Luôn online (không sleep)
- Dashboard tuyệt vời
- Đủ space cho project nhỏ/vừa

---

## 🔧 SETUP DATABASE TRÊN SUPABASE

### Bước 1: Tạo project
1. Vào https://supabase.com
2. Sign up (dùng GitHub)
3. Click **New Project**
4. Nhập:
   - Name: `apartment-system`
   - Password: `your-strong-password`
   - Region: **Singapore** (gần VN nhất)
5. Đợi ~2 phút để setup

### Bước 2: Lấy database URL
1. Vào **Settings** > **Database**
2. Scroll xuống **Connection string**
3. Chọn tab **URI**
4. Copy string (dạng: `postgresql://...`)

### Bước 3: Thêm vào Render
1. Vào Render Dashboard
2. Service **apartment-backend-rdcs**
3. Tab **Environment**
4. Edit **DATABASE_URL**
5. Paste connection string từ Supabase
6. Save changes
7. Render sẽ tự động redeploy

### Bước 4: Chờ deploy xong (~2 phút)
Check logs:
```
Dashboard > Logs
```

### Bước 5: Seed dữ liệu
```bash
# Qua API
POST https://apartment-backend-rdcs.onrender.com/api/seed/real-data

# Hoặc qua Shell
python -m scripts.seed_real_data
```

---

## ✅ KIỂM TRA SAU KHI SEED

### 1. Kiểm tra qua Supabase Dashboard
1. Vào Supabase Dashboard
2. Tab **Table Editor**
3. Xem bảng:
   - `user` (13 users)
   - `apartment` (13 apartments)

### 2. Kiểm tra qua API
```
GET https://apartment-backend-rdcs.onrender.com/api/users
```

### 3. Đăng nhập qua Frontend
```
Username: manager
Password: 123456
```

---

## 📋 CHECKLIST

- [ ] Backend đang chạy OK (check /health)
- [ ] Database đã setup (Supabase recommended)
- [ ] DATABASE_URL đã thêm vào Render env
- [ ] Seed API đã chạy thành công
- [ ] Có 13 apartments (3 tòa)
- [ ] Có 13 users (3 staff + 10 residents)
- [ ] Đăng nhập được với manager/123456

---

## 🆘 XỬ LÝ LỖI

### Lỗi: 503 Service Unavailable
- **Nguyên nhân:** Cold start (Render free tier)
- **Giải pháp:** Đợi 30-60 giây, refresh lại

### Lỗi: Database connection failed
- **Nguyên nhân:** DATABASE_URL sai hoặc database chưa ready
- **Giải pháp:** 
  1. Check DATABASE_URL trong Render env
  2. Test connect từ Supabase dashboard
  3. Kiểm tra IP whitelist (nếu có)

### Lỗi: Already exists
- **Nguyên nhân:** Data đã tồn tại
- **Giải pháp:** Dùng force-seed với secret

### Lỗi: Migration failed
- **Nguyên nhân:** Database schema chưa đúng
- **Giải pháp:**
```bash
# Qua Render Shell
alembic upgrade head
```

---

## 💡 TIPS

### Giữ Render app luôn chạy (không cold start)
Dùng UptimeRobot hoặc Cron-job để ping mỗi 10 phút:
```
https://uptimerobot.com (free)
Ping: https://apartment-backend-rdcs.onrender.com/health
```

### Backup database định kỳ
Supabase tự backup hàng ngày. Muốn backup thủ công:
```bash
# Supabase Dashboard > Settings > Database > Download backup
```

### Monitor usage
```
Supabase Dashboard > Reports
```

---

**Cập nhật:** 13/02/2026  
**Backend URL:** https://apartment-backend-rdcs.onrender.com  
**Khuyến nghị DB:** Supabase (https://supabase.com)
