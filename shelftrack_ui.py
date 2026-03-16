import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="ShelfTrack", layout="centered")

# ---------- DATABASE ----------
conn = sqlite3.connect("inventory.db", check_same_thread=False)
cursor = conn.cursor()

# users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
store TEXT,
subscription TEXT,
contact TEXT
)
""")

# products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
id INTEGER PRIMARY KEY AUTOINCREMENT,
store TEXT,
name TEXT,
category TEXT,
stock INTEGER
)
""")

conn.commit()

# ---------- SESSION STATE ----------
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "login"

if "edit_product" not in st.session_state:
    st.session_state.edit_product = None


# ---------- LOGIN / SIGNUP ----------
if st.session_state.page == "login":

    st.title("ShelfTrack")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # LOGIN
    with tab1:

        name = st.text_input("Your Name")

        if st.button("Login"):

            user = cursor.execute(
                "SELECT * FROM users WHERE name=?",
                (name,)
            ).fetchone()

            if user:
                st.session_state.user = user
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("User not found")

    # SIGNUP
    with tab2:

        name = st.text_input("Name")
        store = st.text_input("Store Name")
        contact = st.text_input("Contact")

        subscription = st.selectbox(
            "Subscription",
            ["Silver", "Gold"]
        )

        if st.button("Create Account"):

            cursor.execute(
                "INSERT INTO users (name,store,subscription,contact) VALUES (?,?,?,?)",
                (name, store, subscription, contact)
            )

            conn.commit()

            st.success("Account created")


# ---------- DASHBOARD ----------
elif st.session_state.page == "dashboard":

    user = st.session_state.user
    store = user[2]

    st.title(f"{store} Dashboard")

    df = pd.read_sql(
        "SELECT * FROM products WHERE store=?",
        conn,
        params=(store,)
    )

    total_products = len(df)
    low_stock = len(df[df["stock"] < 10])

    col1, col2 = st.columns(2)

    col1.metric("Total Products", total_products)
    col2.metric("Low Stock", low_stock)

    st.divider()

    if st.button("Inventory"):
        st.session_state.page = "inventory"
        st.rerun()

    if st.button("Analytics"):
        st.session_state.page = "analytics"
        st.rerun()

    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()


# ---------- INVENTORY ----------
elif st.session_state.page == "inventory":

    user = st.session_state.user
    store = user[2]

    st.title(f"{store} Inventory")

    df = pd.read_sql(
        "SELECT * FROM products WHERE store=?",
        conn,
        params=(store,)
    )

    search = st.text_input("Search product")

    if search:
        df = df[df["name"].str.contains(search, case=False)]

    for index, row in df.iterrows():

        col1, col2, col3, col4, col5 = st.columns([3,2,1,1,1])

        col1.write(f"📦 {row['name']}")

        if row["stock"] < 10:
            col2.write(f"🔴 {row['stock']}")
        else:
            col2.write(f"🟢 {row['stock']}")

        # ADD STOCK
        if col3.button("➕", key=f"add{row['id']}"):

            cursor.execute(
                "UPDATE products SET stock=stock+1 WHERE id=?",
                (row["id"],)
            )

            conn.commit()
            st.rerun()

        # REMOVE STOCK
        if col4.button("➖", key=f"sub{row['id']}"):

            cursor.execute(
                "UPDATE products SET stock=stock-1 WHERE id=?",
                (row["id"],)
            )

            conn.commit()
            st.rerun()

        # DELETE PRODUCT
        if col5.button("🗑", key=f"del{row['id']}"):

            cursor.execute(
                "DELETE FROM products WHERE id=?",
                (row["id"],)
            )

            conn.commit()
            st.rerun()

    st.divider()

    new_product = st.text_input("New Product")

    category = st.selectbox(
        "Category",
        ["Dairy", "Grains", "Vegetables", "Snacks", "Other"]
    )

    if st.button("Add Product"):

        cursor.execute(
            "INSERT INTO products (store,name,category,stock) VALUES (?,?,?,?)",
            (store, new_product, category, 1)
        )

        conn.commit()

        st.rerun()

    if st.button("Back"):
        st.session_state.page = "dashboard"
        st.rerun()


# ---------- ANALYTICS ----------
elif st.session_state.page == "analytics":

    user = st.session_state.user
    store = user[2]

    st.title("Inventory Analytics")

    df = pd.read_sql(
        "SELECT name,stock FROM products WHERE store=?",
        conn,
        params=(store,)
    )

    if not df.empty:
        st.bar_chart(df.set_index("name"))
    else:
        st.info("No data yet")

    if st.button("Back"):
        st.session_state.page = "dashboard"
        st.rerun()
