# ⚠️ BACKEND VS FRONTEND - HƯỚNG DẪN QUAN TRỌNG

## 🔴 VẤN ĐỀ BẠN ĐANG GẶP

### 1️⃣ Backend URL chỉ trả về JSON, không phải website
```
https://apartment-backend-rdcs.onrender.com/
→ {"message":"Apartment Management API is running"}
```

**✅ ĐÂY LÀ ĐÚNG!** Backend là API server, chỉ trả về JSON cho frontend gọi.

### 2️⃣ API endpoint cần có `/v1` trong URL
```
❌ SAI: /api/seed/real-data
✅ ĐÚNG: /api/v1/seed/real-data
```

---

## 🎯 SEED DỮ LIỆU NGAY (URL CẬP NHẬT)

### ✅ Các endpoint ĐÚNG:

**1. Health check:**
```
https://apartment-backend-rdcs.onrender.com/api/v1/seed/health
```

**2. Seed data:**
```
https://apartment-backend-rdcs.onrender.com/api/v1/seed/real-data
```

**3. Force seed:**
```
https://apartment-backend-rdcs.onrender.com/api/v1/seed/force-real-data?secret=render-seed-2026
```

### 🚀 Cách seed nhanh nhất:

**Mở trong Browser:**
```
https://apartment-backend-rdcs.onrender.com/api/v1/seed/real-data
```

Bạn sẽ thấy response JSON như:
```json
{
  "status": "success",
  "message": "Realistic data seeded successfully",
  "apartments_created": 13,
  "users_created": 13
}
```

**Hoặc dùng PowerShell:**
```powershell
Invoke-WebRequest -Uri "https://apartment-backend-rdcs.onrender.com/api/v1/seed/real-data" -Method POST
```

---

## 🌐 XEM WEBSITE THẬT - DEPLOY FRONTEND

Backend (API) và Frontend (Website) là 2 services riêng:

### 📍 Backend (Đã có):
```
https://apartment-backend-rdcs.onrender.com
→ API server (chỉ JSON, không có giao diện)
```

### 📍 Frontend (Cần deploy):
```
Cần deploy lên Vercel/Netlify
→ Website có giao diện cho người dùng
```

---

## 🚀 DEPLOY FRONTEND LÊN VERCEL (5 PHÚT)

### Lựa chọn 1: Deploy qua Vercel Dashboard (DỄ NHẤT)

**Bước 1: Truy cập Vercel**
```
https://vercel.com
→ Sign up with GitHub
```

**Bước 2: Import Project**
```
1. Click "Add New" > "Project"
2. Chọn repository: finalsoa_react
3. Click "Import"
```

**Bước 3: Configure Build**
```
Framework Preset: Vite
Root Directory: ./
Build Command: npm run build
Output Directory: dist
Install Command: npm install
```

**Bước 4: Thêm Environment Variable**
```
Click "Environment Variables"

Add:
  Name: VITE_API_URL
  Value: https://apartment-backend-rdcs.onrender.com/api/v1
```

**Bước 5: Deploy**
```
Click "Deploy"
→ Đợi 2-3 phút
```

**Bước 6: Lấy URL**
Sau khi deploy xong, bạn sẽ có URL dạng:
```
https://your-app-name.vercel.app
```

---

### Lựa chọn 2: Deploy qua Vercel CLI (NHANH HƠN)

```powershell
# 1. Cài Vercel CLI
npm install -g vercel

# 2. Login
vercel login

# 3. Deploy từ thư mục root project
cd E:\Code\KTHDV\Final\FinalSOA-React
vercel

# Trả lời các câu hỏi:
# ? Set up and deploy? Y
# ? Which scope? [Your account]
# ? Link to existing project? N
# ? What's your project's name? apartment-frontend
# ? In which directory is your code located? ./
# ? Want to override the settings? N

# 4. Thêm environment variable
vercel env add VITE_API_URL

# Nhập value:
# https://apartment-backend-rdcs.onrender.com/api/v1

# 5. Deploy production
vercel --prod
```

---

## 📋 SAU KHI DEPLOY FRONTEND

### ✅ Bạn sẽ có 2 URLs:

**Backend API:**
```
https://apartment-backend-rdcs.onrender.com
→ Không vào đây bằng browser
→ Chỉ dùng cho API calls từ frontend
```

**Frontend Website:**
```
https://your-app.vercel.app
→ VÀO ĐÂY để xem website
→ Đây là giao diện người dùng
```

### 🔐 Test Login:
```
URL: https://your-app.vercel.app
Username: manager
Password: 123456
```

---

## 🔧 KIỂM TRA CẤU HÌNH API

Frontend đã được cấu hình đúng trong `src/services/api.ts`:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'
```

Chỉ cần set environment variable `VITE_API_URL` là OK!

---

## ⚡ CÁCH NHANH NHẤT - DÙNG VERCEL

### 1. Tạo file `.env` trong root project:
```env
VITE_API_URL=https://apartment-backend-rdcs.onrender.com/api/v1
```

### 2. Commit và push:
```powershell
git add .env
git commit -m "Add production API URL"
git push origin main
```

### 3. Deploy Vercel:
- Vào Vercel Dashboard
- Import GitHub repo
- Auto-detect config
- Deploy!

**✅ XONG!**

---

## 🎯 TÓM TẮT

| Service | URL | Mục đích |
|---------|-----|----------|
| **Backend** | https://apartment-backend-rdcs.onrender.com | API server (JSON only) |
| **Frontend** | https://[your-app].vercel.app | Website (UI) |
| **Seed API** | .../api/v1/seed/real-data | Seed dữ liệu |
| **API Docs** | .../docs | Xem tất cả endpoints |

### ⚠️ LƯU Ý:
- Backend URL = API, không có giao diện web
- Frontend URL = Website có giao diện
- Cần deploy cả 2 để hệ thống hoạt động đầy đủ

---

## 📞 CÁC LỆNH QUAN TRỌNG

```powershell
# Seed dữ liệu backend
Invoke-WebRequest -Uri "https://apartment-backend-rdcs.onrender.com/api/v1/seed/real-data" -Method POST

# Test API
https://apartment-backend-rdcs.onrender.com/docs

# Deploy frontend
vercel --prod

# Check logs
vercel logs [deployment-url]
```

---

**Cập nhật:** 13/02/2026  
**Backend:** https://apartment-backend-rdcs.onrender.com (✅ API ready)  
**Frontend:** Cần deploy lên Vercel  
**Database:** Supabase (khuyến nghị)
