import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="ShelfTrack", layout="wide")

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

# ---------- SESSION STATES ----------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "show_profile" not in st.session_state:
    st.session_state.show_profile = False

if "edit_product" not in st.session_state:
    st.session_state.edit_product = None


# ---------- HEADER ----------
col1,col2,col3 = st.columns([2,6,2])

with col1:
    st.image("logo.png", width=140)

with col2:
    st.markdown("<h2 style='text-align:center'>Welcome to ShelfTrack</h2>", unsafe_allow_html=True)

with col3:
    if st.button("👤 Profile"):
        st.session_state.show_profile = not st.session_state.show_profile


# ---------- PROFILE ----------
if st.session_state.show_profile:

    st.subheader("Store Profile")

    st.write("Owner: Raj Patel")
    st.write("Email: tulsi.restaurant@gmail.com")
    st.write("Location: Vadodara")
    st.write("Plan: Gold")

    st.divider()


# ---------- HOME ----------
if st.session_state.page == "home":

    st.markdown("<h1 style='text-align:center'>Tulsi</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center'>Tulsi Restaurant</h4>", unsafe_allow_html=True)

    st.write("")

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


# ---------- INVENTORY ----------
elif st.session_state.page == "inventory":

    st.title("Inventory")

    df = pd.read_sql("SELECT * FROM products", conn)

    for index,row in df.iterrows():

        col1,col2,col3,col4,col5,col6 = st.columns([3,2,1,1,1,1])

        col1.write(f"📦 {row['name']}")
        col2.write(f"Stock: {row['stock']}")

        # EDIT
        if col3.button("✏️", key=f"edit_{row['id']}"):
            st.session_state.edit_product = row["id"]

        # ADD STOCK
        if col4.button("➕", key=f"add_{row['id']}"):

            cursor.execute(
                "UPDATE products SET stock = stock + 1 WHERE id=?",
                (row["id"],)
            )

            conn.commit()
            st.rerun()

        # REMOVE STOCK
        if col5.button("➖", key=f"minus_{row['id']}"):

            cursor.execute(
                "UPDATE products SET stock = stock - 1 WHERE id=?",
                (row["id"],)
            )

            conn.commit()
            st.rerun()

        # DELETE
        if col6.button("🗑️", key=f"delete_{row['id']}"):

            cursor.execute(
                "DELETE FROM products WHERE id=?",
                (row["id"],)
            )

            conn.commit()
            st.rerun()


    st.divider()

    # EDIT PANEL
    if st.session_state.edit_product:

        product_id = st.session_state.edit_product

        product = cursor.execute(
            "SELECT * FROM products WHERE id=?",
            (product_id,)
        ).fetchone()

        st.subheader("Edit Product")

        new_name = st.text_input("Product Name", product[1])

        new_stock = st.number_input("Stock", value=product[2], min_value=0)

        if st.button("Update Product"):

            cursor.execute(
                "UPDATE products SET name=?, stock=? WHERE id=?",
                (new_name,new_stock,product_id)
            )

            conn.commit()

            st.session_state.edit_product = None

            st.rerun()

    # ADD NEW PRODUCT
    st.divider()

    st.subheader("Add New Product")

    new_product = st.text_input("New Product Name")

    if st.button("Add Product"):

        cursor.execute(
            "INSERT INTO products (name,stock) VALUES (?,?)",
            (new_product,1)
        )

        conn.commit()

        st.rerun()

    if st.button("⬅ Back"):
        st.session_state.page = "home"


# ---------- PRODUCTS ----------
elif st.session_state.page == "products":

    st.title("All Products")

    df = pd.read_sql("SELECT * FROM products", conn)

    st.table(df)

    if st.button("⬅ Back"):
        st.session_state.page = "home"


# ---------- LOW SUPPLY ----------
elif st.session_state.page == "low":

    st.title("Low Supply")

    df = pd.read_sql("SELECT * FROM products WHERE stock < 10", conn)

    st.table(df)

    if st.button("⬅ Back"):
        st.session_state.page = "home"


# ---------- ORDERS ----------
elif st.session_state.page == "orders":

    st.title("Pending Orders")

    orders = {
        "Order ID":[101,102],
        "Product":["Milk","Eggs"],
        "Quantity":[30,40]
    }

    st.table(pd.DataFrame(orders))

    if st.button("⬅ Back"):
        st.session_state.page = "home"


# ---------- DASHBOARD ----------
elif st.session_state.page == "dashboard":

    st.title("Dashboard")

    df = pd.read_sql("SELECT * FROM products", conn)

    st.metric("Total Products", len(df))

    st.metric("Low Stock", len(df[df["stock"] < 10]))

    if st.button("⬅ Back"):
        st.session_state.page = "home"


# ---------- SUPPLIES ----------
elif st.session_state.page == "supplies":

    st.title("Supplies")

    st.write("Recommended Supplier")

    st.success("FreshFarm Distributors")

    if st.button("⬅ Back"):
        st.session_state.page = "home"


# ---------- NOTIFICATIONS ----------
elif st.session_state.page == "notifications":

    st.title("Notifications")

    df = pd.read_sql("SELECT * FROM products WHERE stock < 10", conn)

    if len(df) == 0:
        st.success("All stock levels normal")

    else:
        st.warning("Low stock items detected")
        st.table(df)

    if st.button("⬅ Back"):
        st.session_state.page = "home"
