# 🗄️ Quick Database Viewer Setup

## ⚡ Fastest Way (2 Steps)

### Step 1: Create Admin Account
```bash
cd Helmet-Numberplate-Speed-Detection
python manage.py createsuperuser
```

Enter:
```
Username: admin
Password: (choose password)
```

### Step 2: Access in Browser
```bash
python manage.py runserver
```

Open: **http://localhost:8000/admin/**

**Done!** You can now view all tables! ✅

---

## 📊 What You'll See

### Tables Available:

1. **CustomUser** - All users with license & phone
2. **RegisteredUser** - Vehicle registrations  
3. **UserViolation** - Traffic violations detected

---

## 🎯 Alternative Tools

### Desktop App (Recommended):
**DB Browser for SQLite**
- Download: https://sqlitebrowser.org/
- Open file: `mydatabase`
- Browse visually

### VS Code Extension:
Search: **"SQLite Viewer"**
- Right-click database → Open

---

## 📁 Database Location

```
c:\Users\kidg2\OneDrive\Desktop\miniproject\Helmet-Numberplate-Speed-Detection\mydatabase
```

---

## 🔧 Already Created For You:

✅ **admin.py** - Updated with all tables registered  
✅ **create_admin.bat** - Quick admin creation script  
✅ **DATABASE_VIEWER_GUIDE.md** - Complete guide  

---

## ✨ Current Data

**Users:** 2  
**Vehicles:** 2  
**Violations:** Check in admin panel!

---

**Choose Django Admin for easiest access!** 🎉
