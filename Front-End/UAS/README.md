# Frontend UAS - MotoSpare Mart

A frontend e-commerce interface for browsing spare parts. This is a **read-only display application** that shows products from the database.

## Important Notice

**This Frontend is Display-Only**

- You CAN: View products, search, browse by category, add to cart, checkout
- You CANNOT: Add, edit, or delete products from this frontend
- All product data is **read-only** from the shared database
- No CRUD operations are allowed in this frontend version

## Product Management

### For Adding, Editing, or Deleting Products:

Use the **Backend UAS Application** instead:

**Location:** `Back-End/UAS/`

**Available Options:**
- `app_sqlite.py` - Local SQLite database
- `app_mysql.py` - MySQL backend (remote database)
- `app_mongo.py` - MongoDB backend

### Backend Features:
- **Add Products** - Insert new items to catalog
- **Edit Products** - Update product details
- **Delete Products** - Remove items from catalog
- **Upload Images** - Add product images
- **Admin Dashboard** - Manage all products

---

## How to Use Backend for CRUD

### Step 1: Navigate to Backend

```bash
cd Back-End/UAS
```

### Step 2: Install Dependencies

```bash
# For MySQL
pip install flask mysql-connector-python

# For MongoDB
pip install flask pymongo

# For SQLite
pip install flask
```

### Step 3: Run Backend Application

```bash
# SQLite (Local database)
python app_sqlite.py

# MySQL (Remote database)
python app_mysql.py

# MongoDB
python app_mongo.py
```

### Step 4: Access Admin Dashboard

Open browser and navigate to:

```
http://localhost:5000/admin/login
```

**Default Credentials:**
- Username: `admin`
- Password: `admin123`

> Change these in production!

### Step 5: Manage Products

From the admin dashboard you can:

1. **Add New Product**
   - Click "Tambah Produk" (Add Product)
   - Fill in product details:
     - Name (Nama Produk)
     - Category (Kategori)
     - Price (Harga)
     - Description (Deskripsi)
     - Upload image or reference existing image
   - Click "Simpan" (Save)

2. **Edit Existing Product**
   - Click "Edit" button on product row
   - Modify product details
   - Upload new image if needed
   - Click "Perbarui" (Update)

3. **Delete Product**
   - Click "Hapus" (Delete) button
   - Confirm deletion

---

## Available Categories

The system supports these product categories:

- **Oli** (Oil)
- **Rem** (Brakes)
- **Ban** (Tires)
- **Mesin** (Engine)
- **Kelistrikan** (Electrical)
- **Rantai** (Chain)

---

## Database Configuration

### MySQL Setup

Set environment variables before running:

```bash
# Windows PowerShell
$env:MYSQL_HOST="your-host"
$env:MYSQL_PORT="3306"
$env:MYSQL_USER="testuser"
$env:MYSQL_PASSWORD="testpass"
$env:MYSQL_DB="testdb"

python app_mysql.py
```

### MongoDB Setup

```bash
$env:MONGO_URI="mongodb://connection-string"
$env:MONGO_DB="testdb"
$env:MONGO_COLLECTION="products"

python app_mongo.py
```

### SQLite Setup

```bash
# No configuration needed - uses local stokumkm.db
python app_sqlite.py
```

---

## Seed Data

To populate the database with sample data:

**SQL Database:**
```sql
-- Import from: Back-End/UAS/JSON/Seeq.sql
-- Copy and run SQL commands in your database client
```

**MongoDB:**
```bash
mongoimport --db testdb --collection products --file Back-End/UAS/JSON/Seeq.json
```

---

---

## Data Flow

```
┌─────────────────────────────────────────┐
│   Shared MySQL/SQLite/MongoDB Database  │
└──────────────┬──────────────────────────┘
               │
        ┌──────┴──────┐
        │             │
    READ       WRITE/UPDATE/DELETE
    (Frontend)   (Backend UAS)
        │             │
   Display UI    Manage CRUD
```

---

## Support

For issues or questions:
1. Check Backend UAS README: `Back-End/UAS/README.md`
2. Verify database connection settings
3. Ensure Backend application is running when making admin changes

---

## License

Project for educational purposes - SP3/SPS3.1 Course Material

