from flask import (
    Flask,
    request,
    redirect,
    url_for,
    session,
    flash,
    get_flashed_messages,
    send_from_directory,
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from pathlib import Path
from datetime import datetime
import sqlite3
from html import escape

# ============================================================
# MILLA GROCERIES STORE
# COMPLETE ONE-FILE SYSTEM
# ============================================================

app = Flask(__name__)
app.secret_key = "milla-groceries-complete-2026"

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "milla_groceries.db"
IMAGE_DIR = BASE_DIR / "images"

# Automatically create images folder
IMAGE_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp",
    "gif"
}


# ============================================================
# DESIGN
# ============================================================

CSS = r"""
@import url(
'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800;900&family=Playfair+Display:wght@700&display=swap'
);

:root{
    --navy:#171d38;
    --navy-2:#232a4a;
    --purple:#6852d9;
    --purple-dark:#4e3bb6;
    --lavender:#eeeaff;
    --coral:#ee7967;
    --coral-dark:#c95b4a;
    --gold:#f2c35b;
    --cream:#fff8ed;
    --ivory:#fffdf9;
    --text:#24283a;
    --muted:#72778a;
    --line:#e7e1d7;
    --white:#ffffff;
    --danger:#d94b4b;
    --success:#29956b;
    --shadow:0 20px 55px rgba(29,31,53,.10);
}

*{
    box-sizing:border-box;
}

html{
    scroll-behavior:smooth;
}

body{
    margin:0;
    min-height:100vh;
    font-family:"DM Sans",Segoe UI,Arial,sans-serif;
    color:var(--text);

    background:
        radial-gradient(
            circle at 5% 8%,
            rgba(104,82,217,.16),
            transparent 22%
        ),
        radial-gradient(
            circle at 96% 10%,
            rgba(238,121,103,.16),
            transparent 21%
        ),
        radial-gradient(
            circle at 88% 87%,
            rgba(242,195,91,.14),
            transparent 18%
        ),
        linear-gradient(
            135deg,
            #fffdf9 0%,
            #f6f0fa 48%,
            #eef0ff 100%
        );
}

body:before{
    content:"";
    position:fixed;
    width:260px;
    height:260px;
    left:-130px;
    bottom:8%;
    border-radius:50%;
    border:55px solid rgba(238,121,103,.06);
    pointer-events:none;
}

body:after{
    content:"";
    position:fixed;
    width:300px;
    height:300px;
    right:-145px;
    top:35%;
    border-radius:50%;
    border:55px solid rgba(104,82,217,.06);
    pointer-events:none;
}

a{
    text-decoration:none;
    color:inherit;
}

/* ============================================================
   NAVIGATION
   ============================================================ */

.topbar{
    position:sticky;
    top:0;
    z-index:100;
    background:
        linear-gradient(
            110deg,
            var(--navy),
            var(--navy-2)
        );
    border-bottom:4px solid var(--gold);
    box-shadow:
        0 12px 35px rgba(23,29,56,.20);
}

.navbar{
    width:min(1280px,94%);
    min-height:82px;
    margin:auto;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:20px;
}

.brand{
    display:flex;
    align-items:center;
    gap:12px;
    color:#fff;
    font-weight:900;
    font-size:20px;
    white-space:nowrap;
}

.brand-icon{
    width:45px;
    height:45px;
    display:grid;
    place-items:center;
    border-radius:14px;
    background:
        linear-gradient(
            145deg,
            var(--gold),
            #ffe08a
        );
    color:var(--navy);
    box-shadow:
        0 8px 20px rgba(242,195,91,.20);
}

.nav-links{
    display:flex;
    align-items:center;
    justify-content:flex-end;
    flex-wrap:wrap;
    gap:5px;
}

.nav-links a{
    color:#e7eaf4;
    font-size:12px;
    font-weight:800;
    padding:10px 12px;
    border-radius:10px;
    border:1px solid transparent;
    transition:.18s ease;
}

.nav-links a:hover{
    color:var(--navy);
    background:var(--gold);
    border-color:var(--gold);
    transform:translateY(-1px);
}

.cart-count{
    display:inline-flex;
    align-items:center;
    justify-content:center;
    min-width:21px;
    padding:2px 7px;
    border-radius:999px;
    background:var(--coral);
    color:#fff;
    font-size:10px;
    margin-left:4px;
}

/* ============================================================
   PAGE
   ============================================================ */

.page{
    width:min(1280px,94%);
    margin:35px auto 80px;
    position:relative;
    z-index:1;
}

.page-title{
    margin-bottom:24px;
}

.page-title h1{
    margin:0 0 7px;
    color:var(--navy);
    font-size:38px;
}

.page-title p{
    margin:0;
    color:var(--muted);
}

/* ============================================================
   HERO
   ============================================================ */

.hero{
    min-height:510px;
    position:relative;
    overflow:hidden;
    border-radius:36px;
    padding:70px;
    display:flex;
    align-items:center;

    background:
        radial-gradient(
            circle at 88% 18%,
            rgba(242,195,91,.22),
            transparent 13%
        ),
        radial-gradient(
            circle at 80% 84%,
            rgba(238,121,103,.18),
            transparent 16%
        ),
        linear-gradient(
            125deg,
            #191d39,
            #34336b 52%,
            #6752d9
        );

    color:#fff;

    box-shadow:
        0 35px 80px rgba(38,34,82,.24);
}

.hero:before{
    content:"";
    position:absolute;
    right:-185px;
    top:-180px;
    width:530px;
    height:530px;
    border-radius:50%;
    border:95px solid rgba(255,255,255,.055);
}

.hero:after{
    content:"";
    position:absolute;
    right:80px;
    bottom:-155px;
    width:280px;
    height:280px;
    border-radius:50%;
    border:36px solid rgba(242,195,91,.07);
}

.hero-content{
    max-width:790px;
    position:relative;
    z-index:3;
}

.hero-label{
    display:inline-block;
    padding:8px 14px;
    border-radius:999px;
    background:rgba(242,195,91,.12);
    border:1px solid rgba(242,195,91,.35);
    color:#ffe6a0;
    font-size:11px;
    font-weight:900;
    letter-spacing:2px;
}

.hero h1{
    font-family:"Playfair Display",Georgia,serif;
    font-size:63px;
    line-height:1.02;
    margin:18px 0;
    letter-spacing:-1.3px;
}

.hero p{
    max-width:700px;
    font-size:18px;
    line-height:1.75;
    color:rgba(255,255,255,.82);
    margin:0;
}

.hero-actions{
    display:flex;
    flex-wrap:wrap;
    gap:12px;
    margin-top:29px;
}

/* ============================================================
   BUTTONS
   ============================================================ */

.btn{
    display:inline-flex;
    align-items:center;
    justify-content:center;
    gap:7px;
    min-height:44px;
    padding:11px 16px;
    border:0;
    border-radius:12px;
    font:inherit;
    font-size:13px;
    font-weight:900;
    cursor:pointer;
    transition:.18s ease;
}

.btn:hover{
    transform:translateY(-2px);
}

.btn-purple{
    background:var(--purple);
    color:#fff;
}

.btn-purple:hover{
    background:var(--purple-dark);
}

.btn-coral{
    background:var(--coral);
    color:#fff;
}

.btn-coral:hover{
    background:var(--coral-dark);
}

.btn-gold{
    background:var(--gold);
    color:var(--navy);
}

.btn-white{
    background:#fff;
    color:var(--navy);
}

.btn-soft{
    background:var(--lavender);
    color:var(--purple-dark);
}

.btn-danger{
    background:#fff0ee;
    color:#ae3f35;
}

.btn-small{
    min-height:36px;
    padding:8px 11px;
    font-size:12px;
}

.btn-full{
    width:100%;
}

/* ============================================================
   STAT CARDS
   ============================================================ */

.stats{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:18px;
}

.stat{
    position:relative;
    overflow:hidden;
    background:rgba(255,253,249,.97);
    border:1px solid var(--line);
    border-radius:21px;
    padding:22px;
    box-shadow:var(--shadow);
}

.stat:nth-child(1){
    border-top:5px solid var(--purple);
}

.stat:nth-child(2){
    border-top:5px solid var(--gold);
}

.stat:nth-child(3){
    border-top:5px solid var(--coral);
}

.stat:nth-child(4){
    border-top:5px solid #54a7df;
}

.stat-top{
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.stat-label{
    color:var(--muted);
    font-size:11px;
    font-weight:900;
    letter-spacing:.8px;
}

.stat-icon{
    width:43px;
    height:43px;
    display:grid;
    place-items:center;
    border-radius:13px;
    background:#f3eefc;
    font-size:20px;
}

.stat-value{
    margin-top:11px;
    font-size:31px;
    font-weight:900;
    color:var(--navy);
}

/* ============================================================
   SECTION
   ============================================================ */

.section-head{
    display:flex;
    justify-content:space-between;
    align-items:flex-end;
    gap:20px;
    margin:38px 0 17px;
}

.section-head h2{
    margin:0;
    font-size:29px;
    color:var(--navy);
}

.section-head p{
    margin:5px 0 0;
    color:var(--muted);
}

/* ============================================================
   PRODUCTS
   ============================================================ */

.products-grid{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:19px;
}

.product-card{
    position:relative;
    overflow:hidden;
    padding:12px;
    background:rgba(255,253,249,.97);
    border:1px solid var(--line);
    border-radius:22px;
    box-shadow:
        0 13px 35px rgba(28,31,53,.065);
    transition:.22s ease;
}

.product-card:hover{
    transform:translateY(-7px);
    box-shadow:var(--shadow);
}

.product-card:after{
    content:"";
    position:absolute;
    left:18px;
    right:18px;
    bottom:0;
    height:4px;
    border-radius:999px;
    background:
        linear-gradient(
            90deg,
            var(--purple),
            var(--gold),
            var(--coral)
        );
}

.product-image{
    position:relative;
    height:185px;
    overflow:hidden;
    display:flex;
    align-items:center;
    justify-content:center;
    border-radius:18px;
    background:#efeafd;
}

.product-image:before{
    content:"";
    position:absolute;
    width:145px;
    height:145px;
    border-radius:50%;
    background:rgba(255,255,255,.53);
}

.product-image img{
    position:relative;
    z-index:2;
    width:100%;
    height:100%;
    object-fit:cover;
    display:block;
}

.product-fallback{
    position:absolute;
    z-index:1;
    font-size:74px;
}

.product-info{
    padding:11px 4px 7px;
}

.product-category{
    color:var(--muted);
    font-size:10px;
    font-weight:900;
    letter-spacing:.8px;
}

.product-info h3{
    margin:5px 0;
    color:var(--navy);
    font-size:17px;
}

.product-row{
    display:flex;
    justify-content:space-between;
    align-items:end;
    gap:10px;
}

.price{
    color:var(--purple-dark);
    font-size:20px;
    font-weight:900;
}

.stock{
    color:var(--muted);
    font-size:11px;
    margin-top:3px;
}

/* ============================================================
   PANELS / FORMS
   ============================================================ */

.panel{
    background:rgba(255,253,249,.97);
    border:1px solid var(--line);
    border-radius:21px;
    padding:23px;
    margin-bottom:22px;
    box-shadow:var(--shadow);
}

.form-grid{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:12px;
    align-items:end;
}

label{
    display:block;
    margin-bottom:6px;
    color:#5b6070;
    font-size:12px;
    font-weight:900;
}

input,
select{
    width:100%;
    padding:12px 13px;
    border:1px solid #ddd6c8;
    border-radius:11px;
    background:#fff;
    color:var(--text);
    font:inherit;
    outline:none;
}

input:focus,
select:focus{
    border-color:var(--purple);
    box-shadow:
        0 0 0 4px rgba(104,82,217,.09);
}

.searchbar{
    display:grid;
    grid-template-columns:1fr auto;
    gap:10px;
}

/* ============================================================
   TABLES
   ============================================================ */

.table-wrap{
    overflow:auto;
}

.table-wrap table{
    width:100%;
    min-width:780px;
    border-collapse:collapse;
}

th,
td{
    padding:13px 11px;
    border-bottom:1px solid #ebe5db;
    text-align:left;
}

th{
    background:#f8f3e9;
    color:#6d6a63;
    font-size:11px;
    text-transform:uppercase;
    letter-spacing:.7px;
}

td{
    font-size:14px;
}

/* ============================================================
   BADGES
   ============================================================ */

.badge{
    display:inline-flex;
    align-items:center;
    padding:6px 9px;
    border-radius:999px;
    font-size:11px;
    font-weight:900;
}

.badge-good{
    background:#e4f6ed;
    color:#1a7551;
}

.badge-low{
    background:#fff1d2;
    color:#95670e;
}

.badge-out{
    background:#ffe7e5;
    color:#aa3830;
}

/* ============================================================
   LOGIN / REGISTER
   ============================================================ */

.auth-wrap{
    width:min(455px,100%);
    margin:55px auto;
}

.auth-card{
    padding:33px;
    background:rgba(255,253,249,.98);
    border:1px solid var(--line);
    border-radius:26px;
    box-shadow:
        0 28px 65px rgba(27,31,54,.12);
}

.auth-logo{
    width:57px;
    height:57px;
    display:grid;
    place-items:center;
    border-radius:17px;
    background:
        linear-gradient(
            145deg,
            var(--gold),
            #ffe49a
        );
    color:var(--navy);
    font-size:26px;
}

.auth-card h1{
    font-family:"Playfair Display",Georgia,serif;
    color:var(--navy);
    font-size:39px;
    margin:17px 0 5px;
}

/* ============================================================
   QUICK ACTIONS
   ============================================================ */

.quick-grid{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:15px;
}

.quick-card{
    padding:20px;
    border-radius:18px;
    background:#fff;
    border:1px solid var(--line);
    box-shadow:var(--shadow);
    transition:.18s ease;
}

.quick-card:hover{
    transform:translateY(-3px);
}

.quick-icon{
    display:block;
    font-size:28px;
    margin-bottom:9px;
}

/* ============================================================
   ALERT
   ============================================================ */

.alert{
    padding:12px 14px;
    margin-bottom:9px;
    border-radius:12px;
    font-weight:700;
}

.alert.success{
    background:#e4f6ed;
    color:#177049;
}

.alert.warning{
    background:#fff1d2;
    color:#95660e;
}

.alert.danger{
    background:#ffe7e5;
    color:#aa3830;
}

/* ============================================================
   EMPTY
   ============================================================ */

.empty{
    padding:70px 20px;
    text-align:center;
}

.empty-icon{
    font-size:58px;
}

/* ============================================================
   FOOTER
   ============================================================ */

footer{
    text-align:center;
    padding:32px 10px;
    color:#868996;
    font-size:12px;
}

/* ============================================================
   MOBILE
   ============================================================ */

@media(max-width:1100px){

    .products-grid{
        grid-template-columns:repeat(3,1fr);
    }

    .stats{
        grid-template-columns:repeat(2,1fr);
    }

    .quick-grid{
        grid-template-columns:repeat(2,1fr);
    }

    .form-grid{
        grid-template-columns:repeat(2,1fr);
    }
}

@media(max-width:760px){

    .navbar{
        flex-direction:column;
        align-items:flex-start;
        padding:15px 0;
    }

    .nav-links{
        width:100%;
    }

    .hero{
        min-height:430px;
        padding:45px 28px;
    }

    .hero h1{
        font-size:44px;
    }

    .products-grid{
        grid-template-columns:repeat(2,1fr);
    }
}

@media(max-width:540px){

    .page{
        width:94%;
        margin-top:21px;
    }

    .products-grid,
    .stats,
    .form-grid,
    .quick-grid{
        grid-template-columns:1fr;
    }

    .hero{
        padding:35px 22px;
    }

    .hero h1{
        font-size:35px;
    }

    .hero p{
        font-size:15px;
    }

    .hero-actions .btn{
        width:100%;
    }
}
"""


# ============================================================
# PRODUCT ICONS
# ============================================================

PRODUCT_ICONS = {
    "Rice": "🍚",
    "Noodles": "🍜",
    "Beverages": "☕",
    "Cooking": "🫗",
    "Canned": "🥫",
    "Bakery": "🍞",
    "Drinks": "🥤",
    "Grocery": "🍬",
    "Snacks": "🍪",
    "Vegetables": "🥬",
    "Fruits": "🍌",
    "Dairy": "🥚",
}


# ============================================================
# DATABASE
# ============================================================

def get_db():
    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_db()

    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        full_name TEXT NOT NULL,

        role TEXT NOT NULL DEFAULT 'User',

        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP

    );

    CREATE TABLE IF NOT EXISTS products(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        code TEXT UNIQUE NOT NULL,

        name TEXT NOT NULL,

        category TEXT NOT NULL,

        price REAL NOT NULL DEFAULT 0,

        stock INTEGER NOT NULL DEFAULT 0,

        unit TEXT NOT NULL DEFAULT 'pcs',

        image TEXT DEFAULT ''

    );

    CREATE TABLE IF NOT EXISTS customers(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        customer_name TEXT NOT NULL,

        phone TEXT,

        email TEXT,

        address TEXT,

        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP

    );

    CREATE TABLE IF NOT EXISTS sales(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        customer TEXT NOT NULL,

        total REAL NOT NULL DEFAULT 0,

        payment TEXT NOT NULL DEFAULT 'Cash',

        sale_date TEXT NOT NULL

    );
    """)

    # ---------------- ADMIN ----------------

    admin = conn.execute(
        """
        SELECT id
        FROM users
        WHERE username='admin'
        """
    ).fetchone()

    if admin is None:

        conn.execute(
            """
            INSERT INTO users
            (username,password,full_name,role)
            VALUES(?,?,?,?)
            """,
            (
                "admin",
                generate_password_hash("admin123"),
                "System Administrator",
                "Admin"
            )
        )

    # ---------------- PRODUCTS ----------------

    if conn.execute(
        """
        SELECT COUNT(*) AS c
        FROM products
        """
    ).fetchone()["c"] == 0:

        conn.executemany(
            """
            INSERT INTO products
            (code,name,category,price,stock,unit,image)
            VALUES(?,?,?,?,?,?,?)
            """,
            [

                (
                    "P001",
                    "Premium Rice",
                    "Rice",
                    65,
                    50,
                    "kg",
                    "P001.jpg"
                ),

                (
                    "P002",
                    "Instant Noodles",
                    "Noodles",
                    15,
                    80,
                    "pcs",
                    "P002.jpg"
                ),

                (
                    "P003",
                    "Coffee",
                    "Beverages",
                    12,
                    60,
                    "sachet",
                    "P003.jpg"
                ),

                (
                    "P004",
                    "Cooking Oil",
                    "Cooking",
                    95,
                    30,
                    "bottle",
                    "P004.jpg"
                ),

                (
                    "P005",
                    "Canned Goods",
                    "Canned",
                    45,
                    25,
                    "can",
                    "P005.jpg"
                ),

                (
                    "P006",
                    "Bread",
                    "Bakery",
                    55,
                    20,
                    "loaf",
                    "P006.jpg"
                ),

                (
                    "P007",
                    "Soft Drinks",
                    "Drinks",
                    40,
                    35,
                    "bottle",
                    "P007.jpg"
                ),

                (
                    "P008",
                    "Sugar",
                    "Grocery",
                    70,
                    40,
                    "kg",
                    "P008.jpg"
                ),

                (
                    "P009",
                    "Snacks",
                    "Snacks",
                    25,
                    45,
                    "pack",
                    "P009.jpg"
                ),

                (
                    "P010",
                    "Fresh Vegetables",
                    "Vegetables",
                    85,
                    18,
                    "bundle",
                    "P010.jpg"
                ),
            ]
        )

    # ---------------- CUSTOMERS ----------------

    if conn.execute(
        """
        SELECT COUNT(*) AS c
        FROM customers
        """
    ).fetchone()["c"] == 0:

        conn.executemany(
            """
            INSERT INTO customers
            (customer_name,phone,email,address)
            VALUES(?,?,?,?)
            """,
            [

                (
                    "Juan Dela Cruz",
                    "09170000001",
                    "juan@example.com",
                    "Bacolod City"
                ),

                (
                    "Maria Santos",
                    "09170000002",
                    "maria@example.com",
                    "Bacolod City"
                ),

                (
                    "Pedro Reyes",
                    "09170000003",
                    "pedro@example.com",
                    "Talisay City"
                ),
            ]
        )

    conn.commit()

    conn.close()


# ============================================================
# HELPERS
# ============================================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


def login_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:

            flash(
                "Please log in first.",
                "warning"
            )

            return redirect(
                url_for("login")
            )

        return function(
            *args,
            **kwargs
        )

    return wrapper


def admin_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:

            flash(
                "Please log in first.",
                "warning"
            )

            return redirect(
                url_for("login")
            )

        if session.get("role") != "Admin":

            flash(
                "Admin access only.",
                "danger"
            )

            return redirect(
                url_for("dashboard")
            )

        return function(
            *args,
            **kwargs
        )

    return wrapper


def get_cart():

    return session.get(
        "cart",
        {}
    )


def cart_data():

    cart = get_cart()

    conn = get_db()

    items = []

    total = 0

    count = 0

    for product_id, quantity in cart.items():

        product = conn.execute(
            """
            SELECT *
            FROM products
            WHERE id=?
            """,
            (
                int(product_id),
            )
        ).fetchone()

        if product:

            quantity = int(
                quantity
            )

            subtotal = (
                product["price"]
                * quantity
            )

            items.append(
                (
                    product,
                    quantity,
                    subtotal
                )
            )

            total += subtotal

            count += quantity

    conn.close()

    return (
        items,
        total,
        count
    )


def product_card(
    product,
    show_button=True
):

    icon = PRODUCT_ICONS.get(
        product["category"],
        "🛒"
    )

    image = product["image"]

    button = ""

    if show_button:

        if product["stock"] > 0:

            button = f"""
            <form
                method="post"
                action="/cart/add/{product['id']}"
            >

                <button
                    class="btn btn-purple btn-small"
                >
                    🛒 Add
                </button>

            </form>
            """

        else:

            button = """
            <span class="badge badge-out">
                Out of stock
            </span>
            """

    image_url = url_for(
        "product_image",
        filename=image
    )

    return f"""
    <article class="product-card">

        <div class="product-image">

            <span class="product-fallback">
                {icon}
            </span>

            <img
                src="{image_url}"
                alt="{escape(product['name'])}"
                onerror="this.style.display='none';"
            >

        </div>

        <div class="product-info">

            <div class="product-category">
                {escape(product["category"]).upper()}
            </div>

            <h3>
                {escape(product["name"])}
            </h3>

            <div class="product-row">

                <div>

                    <div class="price">
                        ₱{product["price"]:,.2f}
                    </div>

                    <div class="stock">
                        {product["stock"]}
                        {escape(product["unit"])}
                        available
                    </div>

                </div>

                {button}

            </div>

        </div>

    </article>
    """


def layout(
    title,
    body
):

    _, _, cart_count = cart_data()

    nav = ""

    nav += '<a href="/">🏠 Home</a>'

    nav += '<a href="/products">🛍️ Products</a>'

    if session.get("user_id"):

        nav += f"""
        <a href="/cart">
            🛒 Cart
            <span class="cart-count">
                {cart_count}
            </span>
        </a>
        """

        nav += """
        <a href="/dashboard">
            📊 Dashboard
        </a>
        """

        if session.get("role") == "Admin":

            nav += """
            <a href="/sales">
                💰 Sales
            </a>

            <a href="/inventory">
                📦 Inventory
            </a>

            <a href="/customers">
                👥 Customers
            </a>

            <a href="/users">
                👤 Users
            </a>
            """

        nav += """
        <a href="/contact">
            📞 Contact
        </a>

        <a href="/logout">
            🚪 Logout
        </a>
        """

    else:

        nav += """
        <a href="/contact">
            📞 Contact
        </a>

        <a href="/login">
            🔐 Login
        </a>

        <a href="/register">
            ✨ Register
        </a>
        """

    alerts = ""

    for category, message in get_flashed_messages(
        with_categories=True
    ):

        alerts += f"""
        <div class="alert {escape(category)}">
            {escape(message)}
        </div>
        """

    return f"""
    <!DOCTYPE html>

    <html lang="en">

    <head>

        <meta charset="UTF-8">

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0"
        >

        <title>
            {escape(title)}
            | Milla Groceries Store
        </title>

        <style>
            {CSS}
        </style>

    </head>

    <body>

        <header class="topbar">

            <div class="navbar">

                <a
                    class="brand"
                    href="/"
                >

                    <span class="brand-icon">
                        🛒
                    </span>

                    Milla Groceries Store

                </a>

                <nav class="nav-links">
                    {nav}
                </nav>

            </div>

        </header>

        <main class="page">

            {alerts}

            {body}

        </main>

        <footer>
            🛒 Milla Groceries Store
            · Fresh shopping made simple
            · 2026
        </footer>

    </body>

    </html>
    """


# ============================================================
# IMAGE ROUTE
# ============================================================

@app.route(
    "/images/<path:filename>"
)
def product_image(filename):

    return send_from_directory(
        IMAGE_DIR,
        filename
    )


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    conn = get_db()

    products = conn.execute(
        """
        SELECT *
        FROM products
        ORDER BY id DESC
        LIMIT 8
        """
    ).fetchall()

    conn.close()

    cards = ""

    for product in products:

        cards += product_card(
            product,
            show_button=False
        )

    body = f"""

    <section class="hero">

        <div class="hero-content">

            <span class="hero-label">
                ✦ FRESH • LOCAL • CONVENIENT
            </span>

            <h1>
                Your everyday grocery,
                made beautiful.
            </h1>

            <p>
                Welcome to Milla Groceries Store —
                a modern grocery management system
                for shopping, products, inventory,
                customers, and sales.
            </p>

            <div class="hero-actions">

                <a
                    href="/products"
                    class="btn btn-gold"
                >
                    🛍️ Explore Products
                </a>

                <a
                    href="/register"
                    class="btn btn-white"
                >
                    ✨ Create Account
                </a>

            </div>

        </div>

    </section>

    <div class="section-head">

        <div>

            <h2>
                Fresh Picks
            </h2>

            <p>
                Everyday essentials from Milla Groceries.
            </p>

        </div>

    </div>

    <section class="products-grid">

        {cards}

    </section>

    """

    return layout(
        "Home",
        body
    )


# ============================================================
# REGISTER
# ============================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        full_name = request.form.get(
            "full_name",
            ""
        ).strip()

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        confirm = request.form.get(
            "confirm",
            ""
        )

        if (
            not full_name
            or not username
            or not password
        ):

            flash(
                "Please complete all required fields.",
                "warning"
            )

        elif password != confirm:

            flash(
                "Passwords do not match.",
                "danger"
            )

        else:

            conn = get_db()

            try:

                conn.execute(
                    """
                    INSERT INTO users
                    (
                        username,
                        password,
                        full_name,
                        role
                    )
                    VALUES(?,?,?,'User')
                    """,
                    (
                        username,
                        generate_password_hash(
                            password
                        ),
                        full_name
                    )
                )

                conn.commit()

                flash(
                    "Account created successfully.",
                    "success"
                )

                return redirect(
                    url_for("login")
                )

            except sqlite3.IntegrityError:

                flash(
                    "Username already exists.",
                    "danger"
                )

            finally:

                conn.close()

    body = """

    <div class="auth-wrap">

        <div class="auth-card">

            <div class="auth-logo">
                ✨
            </div>

            <h1>
                Join Milla
            </h1>

            <p class="muted">
                Create your grocery store account.
            </p>

            <form method="post">

                <label>
                    Full name
                </label>

                <input
                    name="full_name"
                    placeholder="Your full name"
                    required
                >

                <label>
                    Username
                </label>

                <input
                    name="username"
                    placeholder="Choose a username"
                    required
                >

                <label>
                    Password
                </label>

                <input
                    type="password"
                    name="password"
                    placeholder="Create password"
                    required
                >

                <label>
                    Confirm password
                </label>

                <input
                    type="password"
                    name="confirm"
                    placeholder="Repeat password"
                    required
                >

                <br>

                <button
                    class="btn btn-purple btn-full"
                >
                    Create Account
                </button>

            </form>

            <p
                class="muted center"
                style="margin-top:18px"
            >
                Already have an account?
                <a href="/login">
                    <b>Login here</b>
                </a>
            </p>

        </div>

    </div>

    """

    return layout(
        "Register",
        body
    )


# ============================================================
# LOGIN
# ============================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        conn = get_db()

        user = conn.execute(
            """
            SELECT *
            FROM users
            WHERE username=?
            """,
            (
                username,
            )
        ).fetchone()

        conn.close()

        if user and check_password_hash(
            user["password"],
            password
        ):

            session.clear()

            session["user_id"] = user["id"]

            session["full_name"] = user["full_name"]

            session["role"] = user["role"]

            flash(
                "Login successful!",
                "success"
            )

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid username or password.",
            "danger"
        )

    body = """

    <div class="auth-wrap">

        <div class="auth-card">

            <div class="auth-logo">
                🔐
            </div>

            <h1>
                Welcome Back
            </h1>

            <p class="muted">
                Sign in to your Milla account.
            </p>

            <form method="post">

                <label>
                    Username
                </label>

                <input
                    name="username"
                    placeholder="Enter username"
                    required
                >

                <label>
                    Password
                </label>

                <input
                    type="password"
                    name="password"
                    placeholder="Enter password"
                    required
                >

                <br>

                <button
                    class="btn btn-purple btn-full"
                >
                    Login
                </button>

            </form>

            <div
                class="panel"
                style="
                    margin-top:18px;
                    margin-bottom:0;
                    background:#fff8ed;
                "
            >

                <b>
                    Demo Admin Account
                </b>

                <br>

                Username:
                <b>admin</b>

                <br>

                Password:
                <b>admin123</b>

            </div>

            <p class="muted center">

                No account yet?

                <a href="/register">
                    <b>Register</b>
                </a>

            </p>

        </div>

    </div>

    """

    return layout(
        "Login",
        body
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("home")
    )


# ============================================================
# DASHBOARD ROUTER
# ============================================================

@app.route("/dashboard")
@login_required
def dashboard():

    if session.get("role") == "Admin":

        return redirect(
            url_for("admin_dashboard")
        )

    return redirect(
        url_for("user_dashboard")
    )


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@app.route("/admin_dashboard")
@admin_required
def admin_dashboard():

    conn = get_db()

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    today_sales = conn.execute(
        """
        SELECT COALESCE(SUM(total),0) AS total
        FROM sales
        WHERE substr(sale_date,1,10)=?
        """,
        (
            today,
        )
    ).fetchone()["total"]

    product_count = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM products
        """
    ).fetchone()["count"]

    low_stock = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM products
        WHERE stock <= 10
        """
    ).fetchone()["count"]

    customer_count = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM customers
        """
    ).fetchone()["count"]

    recent_sales = conn.execute(
        """
        SELECT *
        FROM sales
        ORDER BY id DESC
        LIMIT 7
        """
    ).fetchall()

    conn.close()

    rows = ""

    for sale in recent_sales:

        rows += f"""

        <tr>

            <td>
                <b>#{sale["id"]}</b>
            </td>

            <td>
                {escape(sale["customer"])}
            </td>

            <td>
                <b>
                    ₱{sale["total"]:,.2f}
                </b>
            </td>

            <td>
                {escape(sale["payment"])}
            </td>

            <td>
                {escape(sale["sale_date"])}
            </td>

        </tr>

        """

    body = f"""

    <div class="page-title">

        <h1>
            Hello,
            {escape(session.get("full_name",""))}
            👋
        </h1>

        <p>
            Here is your store overview.
        </p>

    </div>

    <section class="stats">

        <div class="stat">

            <div class="stat-top">

                <span class="stat-label">
                    TODAY'S SALES
                </span>

                <span class="stat-icon">
                    💰
                </span>

            </div>

            <div class="stat-value">
                ₱{today_sales:,.2f}
            </div>

        </div>

        <div class="stat">

            <div class="stat-top">

                <span class="stat-label">
                    PRODUCTS
                </span>

                <span class="stat-icon">
                    🛍️
                </span>

            </div>

            <div class="stat-value">
                {product_count}
            </div>

        </div>

        <div class="stat">

            <div class="stat-top">

                <span class="stat-label">
                    LOW STOCK
                </span>

                <span class="stat-icon">
                    📦
                </span>

            </div>

            <div class="stat-value">
                {low_stock}
            </div>

        </div>

        <div class="stat">

            <div class="stat-top">

                <span class="stat-label">
                    CUSTOMERS
                </span>

                <span class="stat-icon">
                    👥
                </span>

            </div>

            <div class="stat-value">
                {customer_count}
            </div>

        </div>

    </section>

    <div class="section-head">

        <div>

            <h2>
                Quick Actions
            </h2>

            <p>
                Manage your store faster.
            </p>

        </div>

    </div>

    <section class="quick-grid">

        <a
            href="/products"
            class="quick-card"
        >

            <span class="quick-icon">
                🛍️
            </span>

            Manage Products

        </a>

        <a
            href="/inventory"
            class="quick-card"
        >

            <span class="quick-icon">
                📦
            </span>

            Check Inventory

        </a>

        <a
            href="/customers"
            class="quick-card"
        >

            <span class="quick-icon">
                👥
            </span>

            Manage Customers

        </a>

        <a
            href="/sales"
            class="quick-card"
        >

            <span class="quick-icon">
                💰
            </span>

            View Sales

        </a>

    </section>

    <div class="section-head">

        <div>

            <h2>
                Recent Sales
            </h2>

            <p>
                Latest transactions.
            </p>

        </div>

        <a
            href="/sales"
            class="btn btn-soft"
        >
            View All
        </a>

    </div>

    <div class="panel table-wrap">

        <table>

            <tr>

                <th>
                    Sale
                </th>

                <th>
                    Customer
                </th>

                <th>
                    Total
                </th>

                <th>
                    Payment
                </th>

                <th>
                    Date
                </th>

            </tr>

            {rows or '''
            <tr>
                <td
                    colspan="5"
                    class="center"
                >
                    No sales yet.
                </td>
            </tr>
            '''}

        </table>

    </div>

    """

    return layout(
        "Admin Dashboard",
        body
    )


# ============================================================
# USER DASHBOARD
# ============================================================

@app.route("/user_dashboard")
@login_required
def user_dashboard():

    conn = get_db()

    products = conn.execute(
        """
        SELECT *
        FROM products
        WHERE stock > 0
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    cards = ""

    for product in products:

        cards += product_card(
            product,
            show_button=True
        )

    body = f"""

    <div class="page-title">

        <h1>
            Welcome,
            {escape(session.get("full_name",""))}
            🛍️
        </h1>

        <p>
            Find your everyday essentials.
        </p>

    </div>

    <div class="section-head">

        <div>

            <h2>
                Shop Products
            </h2>

            <p>
                Add your favorites to the cart.
            </p>

        </div>

    </div>

    <section class="products-grid">

        {cards}

    </section>

    """

    return layout(
        "User Dashboard",
        body
    )


# ============================================================
# PRODUCTS
# ============================================================

@app.route("/products")
@login_required
def products():

    search = request.args.get(
        "search",
        ""
    ).strip()

    conn = get_db()

    if search:

        products = conn.execute(
            """
            SELECT *
            FROM products

            WHERE
                name LIKE ?
                OR code LIKE ?
                OR category LIKE ?

            ORDER BY name
            """,
            (
                f"%{search}%",
                f"%{search}%",
                f"%{search}%"
            )
        ).fetchall()

    else:

        products = conn.execute(
            """
            SELECT *
            FROM products
            ORDER BY name
            """
        ).fetchall()

    conn.close()

    add_form = ""

    if session.get("role") == "Admin":

        add_form = """

        <div class="panel">

            <div class="section-head"
                 style="margin-top:0">

                <div>

                    <h2>
                        Add New Product
                    </h2>

                    <p>
                        Add an item to your grocery catalog.
                    </p>

                </div>

            </div>

            <form
                method="post"
                action="/products/add"
                enctype="multipart/form-data"
                class="form-grid"
            >

                <div>

                    <label>
                        Product Code
                    </label>

                    <input
                        name="code"
                        placeholder="P013"
                        required
                    >

                </div>

                <div>

                    <label>
                        Product Name
                    </label>

                    <input
                        name="name"
                        placeholder="Product name"
                        required
                    >

                </div>

                <div>

                    <label>
                        Category
                    </label>

                    <input
                        name="category"
                        placeholder="Grocery"
                        required
                    >

                </div>

                <div>

                    <label>
                        Price
                    </label>

                    <input
                        type="number"
                        step="0.01"
                        min="0"
                        name="price"
                        placeholder="0.00"
                        required
                    >

                </div>

                <div>

                    <label>
                        Stock
                    </label>

                    <input
                        type="number"
                        min="0"
                        name="stock"
                        placeholder="0"
                        required
                    >

                </div>

                <div>

                    <label>
                        Unit
                    </label>

                    <input
                        name="unit"
                        value="pcs"
                    >

                </div>

                <div>

                    <label>
                        Product Picture
                    </label>

                    <input
                        type="file"
                        name="image"
                        accept="image/*"
                    >

                </div>

                <div>

                    <button
                        class="btn btn-purple btn-full"
                    >
                        ＋ Add Product
                    </button>

                </div>

            </form>

        </div>

        """

    cards = ""

    for product in products:

        card = product_card(
            product,
            show_button=True
        )

        if session.get("role") == "Admin":

            delete_button = f"""

            <div
                style="margin-top:8px"
            >

                <form
                    method="post"
                    action="/products/delete/{product['id']}"
                    onsubmit="
                        return confirm(
                            'Delete this product?'
                        );
                    "
                >

                    <button
                        class="btn btn-danger btn-small"
                    >
                        🗑️ Delete
                    </button>

                </form>

            </div>

            """

            card = card.replace(
                "</article>",
                delete_button + "</article>"
            )

        cards += card

    body = f"""

    <div class="page-title">

        <h1>
            Products
        </h1>

        <p>
            Browse and manage your grocery catalog.
        </p>

    </div>

    <form
        method="get"
        class="panel searchbar"
    >

        <input
            name="search"
            value="{escape(search)}"
            placeholder="
                🔎 Search product, code, or category
            "
        >

        <button
            class="btn btn-purple"
        >
            Search
        </button>

    </form>

    {add_form}

    <div class="section-head">

        <div>

            <h2>
                Product Catalog
            </h2>

            <p>
                {len(products)} product(s)
            </p>

        </div>

    </div>

    <section class="products-grid">

        {cards or '''

        <div
            class="panel empty"
            style="grid-column:1/-1"
        >

            <div class="empty-icon">
                🛒
            </div>

            <h2>
                No products found
            </h2>

            <p class="muted">
                Try another search.
            </p>

        </div>

        '''}

    </section>

    """

    return layout(
        "Products",
        body
    )


# ============================================================
# ADD PRODUCT
# ============================================================

@app.route(
    "/products/add",
    methods=["POST"]
)
@admin_required
def add_product():

    try:

        code = request.form.get(
            "code",
            ""
        ).strip()

        name = request.form.get(
            "name",
            ""
        ).strip()

        category = request.form.get(
            "category",
            ""
        ).strip()

        price = float(
            request.form.get(
                "price",
                "0"
            )
        )

        stock = int(
            request.form.get(
                "stock",
                "0"
            )
        )

        unit = request.form.get(
            "unit",
            "pcs"
        ).strip() or "pcs"

        if (
            not code
            or not name
            or not category
            or price < 0
            or stock < 0
        ):

            raise ValueError

        filename = ""

        uploaded = request.files.get(
            "image"
        )

        if uploaded and uploaded.filename:

            if not allowed_file(
                uploaded.filename
            ):

                flash(
                    "Invalid image format.",
                    "danger"
                )

                return redirect(
                    url_for("products")
                )

            filename = secure_filename(
                uploaded.filename
            )

            uploaded.save(
                IMAGE_DIR / filename
            )

        conn = get_db()

        conn.execute(
            """
            INSERT INTO products
            (
                code,
                name,
                category,
                price,
                stock,
                unit,
                image
            )
            VALUES(?,?,?,?,?,?,?)
            """,
            (
                code,
                name,
                category,
                price,
                stock,
                unit,
                filename
            )
        )

        conn.commit()

        conn.close()

        flash(
            "Product added successfully!",
            "success"
        )

    except (
        ValueError,
        KeyError,
        sqlite3.IntegrityError
    ):

        flash(
            "Could not add product. Check the fields.",
            "danger"
        )

    return redirect(
        url_for("products")
    )


# ============================================================
# DELETE PRODUCT
# ============================================================

@app.route(
    "/products/delete/<int:product_id>",
    methods=["POST"]
)
@admin_required
def delete_product(product_id):

    conn = get_db()

    product = conn.execute(
        """
        SELECT image
        FROM products
        WHERE id=?
        """,
        (
            product_id,
        )
    ).fetchone()

    conn.execute(
        """
        DELETE FROM products
        WHERE id=?
        """,
        (
            product_id,
        )
    )

    conn.commit()

    conn.close()

    if product and product["image"]:

        image_path = (
            IMAGE_DIR
            / product["image"]
        )

        if image_path.exists():

            try:
                image_path.unlink()
            except OSError:
                pass

    cart = session.get(
        "cart",
        {}
    )

    cart.pop(
        str(product_id),
        None
    )

    session["cart"] = cart

    flash(
        "Product deleted.",
        "success"
    )

    return redirect(
        url_for("products")
    )


# ============================================================
# CART
# ============================================================

@app.route(
    "/cart/add/<int:product_id>",
    methods=["POST"]
)
@login_required
def add_to_cart(product_id):

    conn = get_db()

    product = conn.execute(
        """
        SELECT *
        FROM products
        WHERE id=?
        """,
        (
            product_id,
        )
    ).fetchone()

    conn.close()

    if not product:

        flash(
            "Product not found.",
            "danger"
        )

        return redirect(
            url_for("products")
        )

    if product["stock"] <= 0:

        flash(
            "Product is out of stock.",
            "warning"
        )

        return redirect(
            url_for("products")
        )

    cart = session.get(
        "cart",
        {}
    )

    key = str(
        product_id
    )

    current = int(
        cart.get(
            key,
            0
        )
    )

    if current + 1 > product["stock"]:

        flash(
            "Not enough stock available.",
            "warning"
        )

    else:

        cart[key] = current + 1

        session["cart"] = cart

        flash(
            f'{product["name"]} added to cart!',
            "success"
        )

    return redirect(
        request.referrer
        or url_for("products")
    )


@app.route("/cart")
@login_required
def cart():

    items, total, count = cart_data()

    if not items:

        body = """

        <div class="panel empty">

            <div class="empty-icon">
                🛒
            </div>

            <h1>
                Your Cart is Empty
            </h1>

            <p class="muted">
                Your basket is waiting for something delicious.
            </p>

            <a
                href="/products"
                class="btn btn-purple"
            >
                Browse Products
            </a>

        </div>

        """

        return layout(
            "Cart",
            body
        )

    rows = ""

    for (
        product,
        quantity,
        subtotal
    ) in items:

        rows += f"""

        <tr>

            <td>

                <b>
                    {escape(product["name"])}
                </b>

            </td>

            <td>
                ₱{product["price"]:,.2f}
            </td>

            <td>

                {quantity}

            </td>

            <td>

                <b>
                    ₱{subtotal:,.2f}
                </b>

            </td>

            <td>

                <form
                    method="post"
                    action="/cart/remove/{product['id']}"
                >

                    <button
                        class="btn btn-danger btn-small"
                    >
                        Remove
                    </button>

                </form>

            </td>

        </tr>

        """

    body = f"""

    <div class="page-title">

        <h1>
            Shopping Cart 🛒
        </h1>

        <p>
            {count} item(s) in your basket.
        </p>

    </div>

    <div class="panel table-wrap">

        <table>

            <tr>

                <th>
                    Product
                </th>

                <th>
                    Price
                </th>

                <th>
                    Quantity
                </th>

                <th>
                    Subtotal
                </th>

                <th>
                    Action
                </th>

            </tr>

            {rows}

        </table>

    </div>

    <div class="panel">

        <div class="section-head"
             style="margin-top:0">

            <div>

                <h2>
                    Checkout
                </h2>

                <p>
                    Review your order before completing it.
                </p>

            </div>

            <div
                class="price"
                style="font-size:30px"
            >
                ₱{total:,.2f}
            </div>

        </div>

        <form
            method="post"
            action="/checkout"
            class="form-grid"
        >

            <div>

                <label>
                    Customer Name
                </label>

                <input
                    name="customer"
                    value="{escape(
                        session.get(
                            'full_name',
                            ''
                        )
                    )}"
                >

            </div>

            <div>

                <label>
                    Payment Method
                </label>

                <select
                    name="payment"
                >

                    <option>
                        Cash
                    </option>

                    <option>
                        GCash
                    </option>

                    <option>
                        Card
                    </option>

                </select>

            </div>

            <div>

                <button
                    class="btn btn-coral btn-full"
                >
                    💳 Complete Checkout
                </button>

            </div>

        </form>

    </div>

    """

    return layout(
        "Cart",
        body
    )


# ============================================================
# REMOVE FROM CART
# ============================================================

@app.route(
    "/cart/remove/<int:product_id>",
    methods=["POST"]
)
@login_required
def remove_from_cart(product_id):

    cart = session.get(
        "cart",
        {}
    )

    cart.pop(
        str(product_id),
        None
    )

    session["cart"] = cart

    flash(
        "Item removed from cart.",
        "success"
    )

    return redirect(
        url_for("cart")
    )


# ============================================================
# CHECKOUT
# ============================================================

@app.route(
    "/checkout",
    methods=["POST"]
)
@login_required
def checkout():

    items, total, _ = cart_data()

    if not items:

        flash(
            "Your cart is empty.",
            "warning"
        )

        return redirect(
            url_for("cart")
        )

    customer = request.form.get(
        "customer",
        ""
    ).strip()

    payment = request.form.get(
        "payment",
        "Cash"
    )

    if not customer:

        customer = session.get(
            "full_name",
            "Walk-in Customer"
        )

    conn = get_db()

    try:

        # Check stocks first
        for (
            product,
            quantity,
            _
        ) in items:

            stock = conn.execute(
                """
                SELECT stock
                FROM products
                WHERE id=?
                """,
                (
                    product["id"],
                )
            ).fetchone()

            if (
                not stock
                or stock["stock"] < quantity
            ):

                raise ValueError(
                    f'Not enough stock for {product["name"]}.'
                )

        # Record sale
        conn.execute(
            """
            INSERT INTO sales
            (
                customer,
                total,
                payment,
                sale_date
            )
            VALUES(?,?,?,?)
            """,
            (
                customer,
                total,
                payment,
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        )

        # Decrease stock
        for (
            product,
            quantity,
            _
        ) in items:

            conn.execute(
                """
                UPDATE products
                SET stock=stock-?
                WHERE id=?
                """,
                (
                    quantity,
                    product["id"]
                )
            )

        conn.commit()

        session["cart"] = {}

        flash(
            "Checkout completed successfully!",
            "success"
        )

        return redirect(
            url_for("sales")
            if session.get("role") == "Admin"
            else url_for("products")
        )

    except ValueError as error:

        conn.rollback()

        flash(
            str(error),
            "danger"
        )

        return redirect(
            url_for("cart")
        )

    finally:

        conn.close()


# ============================================================
# SALES
# ============================================================

@app.route("/sales")
@admin_required
def sales():

    conn = get_db()

    sales_data = conn.execute(
        """
        SELECT *
        FROM sales
        ORDER BY id DESC
        """
    ).fetchall()

    total_sales = conn.execute(
        """
        SELECT
            COALESCE(SUM(total),0) AS total
        FROM sales
        """
    ).fetchone()["total"]

    conn.close()

    rows = ""

    for sale in sales_data:

        rows += f"""

        <tr>

            <td>
                <b>
                    #{sale["id"]}
                </b>
            </td>

            <td>
                {escape(sale["customer"])}
            </td>

            <td>
                <b>
                    ₱{sale["total"]:,.2f}
                </b>
            </td>

            <td>
                {escape(sale["payment"])}
            </td>

            <td>
                {escape(sale["sale_date"])}
            </td>

        </tr>

        """

    body = f"""

    <div class="page-title">

        <h1>
            Sales
        </h1>

        <p>
            Review all completed transactions.
        </p>

    </div>

    <div class="stats">

        <div
            class="stat"
            style="grid-column:span 2"
        >

            <div class="stat-top">

                <span class="stat-label">
                    TOTAL SALES
                </span>

                <span class="stat-icon">
                    💰
                </span>

            </div>

            <div class="stat-value">
                ₱{total_sales:,.2f}
            </div>

        </div>

    </div>

    <div class="panel table-wrap">

        <table>

            <tr>

                <th>
                    Sale
                </th>

                <th>
                    Customer
                </th>

                <th>
                    Total
                </th>

                <th>
                    Payment
                </th>

                <th>
                    Date
                </th>

            </tr>

            {rows or '''
            <tr>
                <td
                    colspan="5"
                    class="center"
                >
                    No sales yet.
                </td>
            </tr>
            '''}

        </table>

    </div>

    """

    return layout(
        "Sales",
        body
    )


# ============================================================
# INVENTORY
# ============================================================

@app.route("/inventory")
@admin_required
def inventory():

    conn = get_db()

    products = conn.execute(
        """
        SELECT *
        FROM products
        ORDER BY name
        """
    ).fetchall()

    conn.close()

    rows = ""

    for product in products:

        if product["stock"] > 10:

            status = "Available"

            badge = "badge-good"

        elif product["stock"] > 0:

            status = "Low Stock"

            badge = "badge-low"

        else:

            status = "Out of Stock"

            badge = "badge-out"

        rows += f"""

        <tr>

            <td>
                {escape(product["code"])}
            </td>

            <td>
                <b>
                    {escape(product["name"])}
                </b>
            </td>

            <td>
                {escape(product["category"])}
            </td>

            <td>
                {product["stock"]}
                {escape(product["unit"])}
            </td>

            <td>

                <span
                    class="badge {badge}"
                >
                    {status}
                </span>

            </td>

        </tr>

        """

    body = f"""

    <div class="page-title">

        <h1>
            Inventory
        </h1>

        <p>
            Monitor your current stock levels.
        </p>

    </div>

    <div class="panel table-wrap">

        <table>

            <tr>

                <th>
                    Code
                </th>

                <th>
                    Product
                </th>

                <th>
                    Category
                </th>

                <th>
                    Stock
                </th>

                <th>
                    Status
                </th>

            </tr>

            {rows}

        </table>

    </div>

    """

    return layout(
        "Inventory",
        body
    )


# ============================================================
# CUSTOMERS
# ============================================================

@app.route(
    "/customers",
    methods=["GET", "POST"]
)
@admin_required
def customers():

    conn = get_db()

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        address = request.form.get(
            "address",
            ""
        ).strip()

        if not name:

            flash(
                "Customer name is required.",
                "warning"
            )

        else:

            conn.execute(
                """
                INSERT INTO customers
                (
                    customer_name,
                    phone,
                    email,
                    address
                )
                VALUES(?,?,?,?)
                """,
                (
                    name,
                    phone,
                    email,
                    address
                )
            )

            conn.commit()

            flash(
                "Customer added successfully!",
                "success"
            )

        conn.close()

        return redirect(
            url_for("customers")
        )

    customer_data = conn.execute(
        """
        SELECT *
        FROM customers
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    rows = ""

    for customer in customer_data:

        rows += f"""

        <tr>

            <td>
                <b>
                    {escape(customer["customer_name"])}
                </b>
            </td>

            <td>
                {escape(customer["phone"] or "-")}
            </td>

            <td>
                {escape(customer["email"] or "-")}
            </td>

            <td>
                {escape(customer["address"] or "-")}
            </td>

        </tr>

        """

    body = f"""

    <div class="page-title">

        <h1>
            Customers
        </h1>

        <p>
            Organize your customer records.
        </p>

    </div>

    <div class="panel">

        <div class="section-head"
             style="margin-top:0">

            <div>

                <h2>
                    Add Customer
                </h2>

                <p>
                    Create a customer record.
                </p>

            </div>

        </div>

        <form
            method="post"
            class="form-grid"
        >

            <div>

                <label>
                    Name
                </label>

                <input
                    name="name"
                    required
                >

            </div>

            <div>

                <label>
                    Phone
                </label>

                <input
                    name="phone"
                >

            </div>

            <div>

                <label>
                    Email
                </label>

                <input
                    name="email"
                    type="email"
                >

            </div>

            <div>

                <label>
                    Address
                </label>

                <input
                    name="address"
                >

            </div>

            <div>

                <button
                    class="btn btn-purple"
                >
                    ＋ Add Customer
                </button>

            </div>

        </form>

    </div>

    <div class="panel table-wrap">

        <table>

            <tr>

                <th>
                    Name
                </th>

                <th>
                    Phone
                </th>

                <th>
                    Email
                </th>

                <th>
                    Address
                </th>

            </tr>

            {rows or '''
            <tr>
                <td colspan="4" class="center">
                    No customers yet.
                </td>
            </tr>
            '''}

        </table>

    </div>

    """

    return layout(
        "Customers",
        body
    )


# ============================================================
# USERS
# ============================================================

@app.route("/users")
@admin_required
def users():

    conn = get_db()

    users_data = conn.execute(
        """
        SELECT
            id,
            username,
            full_name,
            role,
            created_at
        FROM users
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    rows = ""

    for user in users_data:

        rows += f"""

        <tr>

            <td>
                {user["id"]}
            </td>

            <td>
                <b>
                    {escape(user["username"])}
                </b>
            </td>

            <td>
                {escape(user["full_name"])}
            </td>

            <td>

                <span
                    class="badge badge-good"
                >
                    {escape(user["role"])}
                </span>

            </td>

            <td>
                {escape(user["created_at"])}
            </td>

        </tr>

        """

    body = f"""

    <div class="page-title">

        <h1>
            Users
        </h1>

        <p>
            Registered accounts and roles.
        </p>

    </div>

    <div class="panel table-wrap">

        <table>

            <tr>

                <th>
                    ID
                </th>

                <th>
                    Username
                </th>

                <th>
                    Full Name
                </th>

                <th>
                    Role
                </th>

                <th>
                    Created
                </th>

            </tr>

            {rows}

        </table>

    </div>

    """

    return layout(
        "Users",
        body
    )


# ============================================================
# CONTACT
# ============================================================

@app.route("/contact")
def contact():

    body = """

    <div class="page-title">

        <h1>
            Contact Us
        </h1>

        <p>
            We'd love to hear from you.
        </p>

    </div>

    <div class="panel">

        <h2>
            Milla Groceries Store
        </h2>

        <p>
            📍
            <b>Location:</b>
            Your Local Community
        </p>

        <p>
            📞
            <b>Phone:</b>
            0917-000-0000
        </p>

        <p>
            ✉️
            <b>Email:</b>
            millagroceries@example.com
        </p>

        <p>
            🕒
            <b>Store Hours:</b>
            Monday - Saturday,
            8:00 AM - 7:00 PM
        </p>

        <hr>

        <h3>
            Need help?
        </h3>

        <p class="muted">
            Please contact the store administrator
            for account, product, inventory,
            and transaction concerns.
        </p>

    </div>

    """

    return layout(
        "Contact",
        body
    )


# ============================================================
# ERROR PAGE
# ============================================================

@app.errorhandler(404)
def not_found(error):

    body = """

    <div class="panel empty">

        <div class="empty-icon">
            🔎
        </div>

        <h1>
            Page Not Found
        </h1>

        <p class="muted">
            The page you requested does not exist.
        </p>

        <a
            href="/"
            class="btn btn-purple"
        >
            Back Home
        </a>

    </div>

    """

    return layout(
        "Page Not Found",
        body
    ), 404


# ============================================================
# START SYSTEM
# ============================================================

if __name__ == "__main__":

    init_db()

    print("")
    print(
        "=================================================="
    )

    print(
        "     MILLA GROCERIES STORE"
    )

    print(
        "     COMPLETE SYSTEM"
    )

    print(
        "=================================================="
    )

    print(
        "Open: http://127.0.0.1:5000"
    )

    print(
        "Admin Username: admin"
    )

    print(
        "Admin Password: admin123"
    )

    print(
        "Database: milla_groceries.db"
    )

    print(
        "=================================================="
    )

    app.run(
        debug=True
    )