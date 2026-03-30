# 🗄️ Database Viewer Guide - View Your Tables

## 📊 Your Database Location

**File:** `c:\Users\kidg2\OneDrive\Desktop\miniproject\Helmet-Numberplate-Speed-Detection\mydatabase`

**Type:** SQLite (Relational Database)

---

## 🎯 Method 1: Django Admin Panel (EASIEST!) ⭐

### Why Use This?
✅ Web-based interface  
✅ Already configured in your project  
✅ Can view, search, filter, and edit data  
✅ No software installation needed  

### Step 1: Create Admin Account

**Windows:**
```bash
cd Helmet-Numberplate-Speed-Detection
create_admin.bat
```

**Manual:**
```bash
cd Helmet-Numberplate-Speed-Detection
python manage.py createsuperuser
```

You'll be prompted:
```
Username: admin
Email address: (leave blank)
Password: ********
Password (again): ********
Superuser created successfully!
```

### Step 2: Start Server
```bash
python manage.py runserver
```

### Step 3: Access Admin Panel
Open browser: **http://localhost:8000/admin/**

Login with your credentials!

### What You'll See:

#### **CustomUser Table**
- All registered users
- Search by license/phone/name
- Filter by age
- Edit user details

#### **RegisteredUser Table**
- All registered vehicles
- Search by vehicle number or phone
- Filter by active status
- See registration dates

#### **UserViolation Table**
- All detected violations
- Search by plate number
- Filter by type (helmet/speed)
- Filter by severity
- View timestamps

---

## 🖥️ Method 2: DB Browser for SQLite (Desktop App)

### Download & Install

**Get it here:** https://sqlitebrowser.org/

![DB Browser Screenshot](https://sqlitebrowser.org/wp-content/uploads/2017/01/dbbrowser4.png)

### How to Use:

1. **Open DB Browser**
2. **Click "Open Database"**
3. **Navigate to:**
   ```
   c:\Users\kidg2\OneDrive\Desktop\miniproject\Helmet-Numberplate-Speed-Detection\mydatabase
   ```
4. **Browse Data Tab** → Select table to view

### Features:
- ✅ View all tables visually
- ✅ Execute SQL queries
- ✅ Export to CSV/JSON
- ✅ Edit data directly
- ✅ Import from CSV
- ✅ Free & Open Source

---

## 🔧 Method 3: VS Code Extensions

### If You Use VS Code:

#### Extension A: SQLite Viewer

1. **Install Extension:**
   - Open VS Code
   - Press `Ctrl+Shift+X`
   - Search: **"SQLite Viewer"**
   - Install by Florian Klampfer

2. **Usage:**
   - Right-click `mydatabase` file
   - Click "Open Database"
   - View tables in sidebar

#### Extension B: SQLite

1. **Install:** Search **"SQLite"** by alexcvzz

2. **Features:**
   - Run SQL queries
   - View results inline
   - Export capabilities

---

## 💻 Method 4: Command Line Tools

### Option A: SQLite CLI

```bash
# Install on Windows (via Chocolatey)
choco install sqlite

# Or download from: https://sqlite.org/download.html
```

**Usage:**
```bash
cd Helmet-Numberplate-Speed-Detection
sqlite3 mydatabase

# Now you're in SQLite shell:
.tables
SELECT * FROM CustomUser;
SELECT * FROM RegisteredUser;
SELECT * FROM UserViolation;
.quit
```

### Option B: Django Shell (Already Have!)

```bash
cd Helmet-Numberplate-Speed-Detection
python manage.py shell
```

```python
from app.models import CustomUser, RegisteredUser, UserViolation

# View all users
print("=== USERS ===")
for user in CustomUser.objects.all():
    print(f"{user.license_number} | {user.phone} | {user.first_name} {user.last_name}")

# View all vehicles
print("\n=== VEHICLES ===")
for vehicle in RegisteredUser.objects.all():
    print(f"{vehicle.vehicle_number} | {vehicle.phone_number}")

# View all violations
print("\n=== VIOLATIONS ===")
for v in UserViolation.objects.all():
    print(f"{v.plate_number} | {v.violation_type} | {v.severity}")
```

---

## 🌐 Method 5: Online SQLite Viewers

### SQLite Viewer Online
**Website:** https://inloop.github.io/sqlite-viewer/

**How to use:**
1. Copy your `mydatabase` file
2. Upload to website
3. View tables in browser

⚠️ **Warning:** Only use for development databases, not production!

---

## 📱 Method 6: Mobile Apps

### Android: SQLite Editor
- Download from Play Store
- Open database file
- Browse tables

### iOS: SQLite Database Browser
- Download from App Store
- Import database via cloud storage
- View tables

---

## 🎯 Comparison Table

| Method | Ease | Features | Cost | Best For |
|--------|------|----------|------|----------|
| **Django Admin** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Free | Quick web access |
| **DB Browser** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Free | Desktop power users |
| **VS Code Ext** | ⭐⭐⭐⭐ | ⭐⭐⭐ | Free | Developers |
| **Command Line** | ⭐⭐⭐ | ⭐⭐⭐⭐ | Free | Scripting |
| **Online Viewer** | ⭐⭐⭐⭐ | ⭐⭐ | Free | Quick look |

---

## 🚀 Recommended Workflow

### For Daily Use:
**Use Django Admin Panel** (Method 1)

Why?
- Always accessible via browser
- Integrated with your authentication
- Can test while developing
- No extra software needed

### For Deep Analysis:
**Use DB Browser for SQLite** (Method 2)

Why?
- Better visualization
- Advanced SQL queries
- Export capabilities
- Data manipulation tools

### For Quick Checks:
**Use Django Shell** (Method 4B)

Why?
- Already running your server
- Quick Python commands
- No context switching

---

## 📋 Current Database Contents

Based on earlier check, you have:

### CustomUser Table (2 users)
```
License: 5147          | Phone: 885236971   | Name: k ag
License: kl25k         | Phone: 8157968294  | Name: Kailas A J
```

### RegisteredUser Table (2 vehicles)
```
Vehicle: DL 2S G 5988  | Phone: 9876543210
Vehicle: DL 2S G 5989  | Phone: 8157968294
```

### UserViolation Table
```
(Check with: python manage.py shell)
```

---

## 🔧 Setup Instructions

### Quick Setup (5 minutes):

1. **Create admin account:**
   ```bash
   cd Helmet-Numberplate-Speed-Detection
   python manage.py createsuperuser
   # Username: admin
   # Password: (choose strong password)
   ```

2. **Start server:**
   ```bash
   python manage.py runserver
   ```

3. **Open browser:**
   ```
   http://localhost:8000/admin/
   ```

4. **Login and browse!**

### Alternative Setup (DB Browser):

1. Download: https://sqlitebrowser.org/
2. Install
3. Open `mydatabase` file
4. Browse "Browse Data" tab

---

## 🎨 Admin Panel Screenshots Preview

When you access `/admin/`, you'll see:

### Main Admin Page:
```
Authentication and Authorization
├─ Users (2)              ← Your CustomUser model

Traffic Monitor
├─ Custom users (2)       ← Same as above
├─ Registered users (2)   ← Vehicle registrations
└─ User violations (?)    ← Detected violations
```

### CustomUser Detail View:
```
License Number: kl25k
Phone Number: 8157968294
First Name: Kailas
Last Name: A J
Age: 25
Address: ...
```

With search and filter options!

---

## 💡 Pro Tips

### Django Admin Tips:
1. **Enable dark mode** - Click moon icon in footer
2. **Use search** - Fast lookup by license/phone
3. **Use filters** - Filter violations by type/date
4. **Export data** - Use actions menu
5. **Edit inline** - Click to modify any field

### DB Browser Tips:
1. **Execute SQL** tab for custom queries
2. **Export** button to save as CSV/JSON
3. **Copy** button to duplicate rows
4. **Filter** button to search quickly

### VS Code Tips:
1. **Right-click** table → "View Top 100 Rows"
2. **Drag** database file to sidebar
3. **Run query** from command palette

---

## 🆘 Troubleshooting

### Issue: Can't access /admin/

**Solution:**
```bash
# Make sure server is running
python manage.py runserver

# Check URL is correct
http://localhost:8000/admin/
```

### Issue: Forgot admin password

**Solution:**
```bash
python manage.py changepassword admin
```

### Issue: Tables not showing in admin

**Solution:**
Check `admin.py` has all models registered (already done!)

### Issue: DB Browser won't open file

**Solution:**
- Make sure file path is correct
- Check file isn't locked by another process
- Try copying file and opening copy

---

## 📊 Example SQL Queries

If using DB Browser or command line:

### Get all users:
```sql
SELECT * FROM CustomUser;
```

### Get violations for specific vehicle:
```sql
SELECT * FROM UserViolation WHERE plate_number = 'DL 2S G 5988';
```

### Count violations by type:
```sql
SELECT violation_type, COUNT(*) 
FROM UserViolation 
GROUP BY violation_type;
```

### Get recent violations:
```sql
SELECT * FROM UserViolation 
ORDER BY detected_at DESC 
LIMIT 10;
```

---

## ✅ Summary

### Best Options:

1. **For daily use:** Django Admin Panel (`/admin/`)
2. **For analysis:** DB Browser for SQLite (desktop app)
3. **For quick checks:** Django Shell

### Files Created:
- ✅ `create_admin.bat` - Quick admin creation script
- ✅ Updated `admin.py` - All tables registered
- ✅ This guide - Complete instructions

### Next Steps:
1. Run `create_admin.bat`
2. Start server
3. Access `http://localhost:8000/admin/`
4. View all your tables!

---

**You now have multiple ways to view your database tables!** 🎉🗄️

Choose the method that works best for you. The Django Admin panel is recommended since it's already integrated into your project and accessible from any browser!
