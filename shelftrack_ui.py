import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="ShelfTrack", layout="wide")

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "show_profile" not in st.session_state:
    st.session_state.show_profile = False


# ---------- DATABASE ----------
conn = sqlite3.connect("inventory.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
stock INTEGER
)
""")

conn.commit()


# ---------- HEADER ----------
col1,col2,col3 = st.columns([2,6,2])

with col1:
    st.image("logo.png", width=140)

with col2:
    st.markdown("<h2 style='text-align:center'>Welcome to ShelfTrack</h2>", unsafe_allow_html=True)

with col3:
    if st.button("👤 Profile"):
        st.session_state.show_profile = not st.session_state.show_profile


# ---------- PROFILE PANEL ----------
if st.session_state.show_profile:

    st.subheader("Store Profile")

    st.write("Owner: Raj Patel")
    st.write("Email: tulsi.restaurant@gmail.com")
    st.write("Location: Vadodara, Gujarat")
    st.write("Plan: Gold")

    st.divider()


# ---------- HOME PAGE ----------
if st.session_state.page == "home":

    st.markdown("<h1 style='text-align:center'>Tulsi</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center'>Tulsi Restaurant</h4>", unsafe_allow_html=True)

    st.write("")

    # Metrics
    col1,col2,col3 = st.columns(3)

    with col1:
        if st.button("Total Products", use_container_width=True):
            st.session_state.page = "products"

    with col2:
        if st.button("Pending Orders", use_container_width=True):
            st.session_state.page = "orders"

    with col3:
        if st.button("Low Supply", use_container_width=True):
            st.session_state.page = "low"

    st.write("")
    st.write("")

    # Navigation
    col1,col2 = st.columns(2)

    with col1:
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"

        if st.button("📦 Inventory", use_container_width=True):
            st.session_state.page = "inventory"

    with col2:
        if st.button("🔔 Notifications", use_container_width=True):
            st.session_state.page = "notifications"

        if st.button("🚚 Supplies", use_container_width=True):
            st.session_state.page = "supplies"


# ---------- TOTAL PRODUCTS ----------
elif st.session_state.page == "products":

    st.title("All Products")

    df = pd.read_sql("SELECT * FROM products", conn)

    st.table(df)

    if st.button("⬅ Back"):
        st.session_state.page = "home"


# ---------- PENDING ORDERS ----------
elif st.session_state.page == "orders":

    st.title("Pending Orders")

    orders = {
        "Order ID":[101,102,103],
        "Product":["Milk","Eggs","Vegetables"],
        "Quantity":[20,30,50]
    }

    st.table(pd.DataFrame(orders))

    if st.button("⬅ Back"):
        st.session_state.page = "home"


# ---------- LOW SUPPLY ----------
elif st.session_state.page == "low":

    st.title("Low Supply Products")

    df = pd.read_sql("SELECT * FROM products WHERE stock < 15", conn)

    st.table(df)

    if st.button("⬅ Back"):
        st.session_state.page = "home"


# ---------- DASHBOARD ----------
elif st.session_state.page == "dashboard":

    st.title("Dashboard Overview")

    df = pd.read_sql("SELECT * FROM products", conn)

    total_products = len(df)

    low_products = len(df[df["stock"] < 15])

    st.metric("Total Products", total_products)
    st.metric("Low Supply Items", low_products)

    if st.button("⬅ Back"):
        st.session_state.page = "home"


# ---------- INVENTORY ----------
elif st.session_state.page == "inventory":

    st.title("Inventory Management")

    # Show products
    df = pd.read_sql("SELECT * FROM products", conn)

    st.subheader("Current Inventory")

    st.table(df)

    st.divider()

    # Add Product Form
    st.subheader("Add Product")

    name = st.text_input("Product Name")

    stock = st.number_input("Stock Quantity", min_value=1)

    if st.button("Add Product"):

        cursor.execute(
            "INSERT INTO products (name, stock) VALUES (?,?)",
            (name,stock)
        )

        conn.commit()

        st.success("Product added successfully")

    if st.button("⬅ Back"):
        st.session_state.page = "home"


# ---------- NOTIFICATIONS ----------
elif st.session_state.page == "notifications":

    st.title("Notifications")

    df = pd.read_sql("SELECT * FROM products WHERE stock < 15", conn)

    if len(df) == 0:
        st.success("No alerts")

    else:
        st.warning("Low stock detected")

        st.table(df)

    if st.button("⬅ Back"):
        st.session_state.page = "home"


# ---------- SUPPLIES ----------
elif st.session_state.page == "supplies":

    st.title("Supplier Recommendations")

    st.write("Recommended Supplier")

    st.success("FreshFarm Distributors")

    st.write("Milk Price: ₹27 per unit")

    if st.button("⬅ Back"):
        st.session_state.page = "home"

elif st.session_state.page == "inventory":

    st.title("Inventory Management")

    # Get products from database
    df = pd.read_sql("SELECT * FROM products", conn)

    st.subheader("Current Inventory")

    # Show products with delete buttons
    for index, row in df.iterrows():

        col1, col2, col3 = st.columns([4,2,1])

        col1.write(row["name"])
        col2.write(f"Stock: {row['stock']}")

        if col3.button("Delete", key=row["id"]):

            cursor.execute(
                "DELETE FROM products WHERE id=?",
                (row["id"],)
            )

            conn.commit()

            st.success("Product removed")

            st.rerun()

    st.divider()

    # Add product section
    st.subheader("Add Product")

    name = st.text_input("Product Name")

    stock = st.number_input("Stock Quantity", min_value=1)

    if st.button("Add Product"):

        cursor.execute(
            "INSERT INTO products (name, stock) VALUES (?,?)",
            (name, stock)
        )

        conn.commit()

        st.success("Product added")

        st.rerun()

    if st.button("⬅ Back"):
        st.session_state.page = "home"

