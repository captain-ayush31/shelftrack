import streamlit as st

st.set_page_config(page_title="ShelfTrack", layout="wide")

# ---------- SESSION STATES ----------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "show_profile" not in st.session_state:
    st.session_state.show_profile = False


# ---------- STYLING ----------
st.markdown("""
<style>

.block-container{
padding-top:1rem;
}

header {visibility:hidden;}
footer {visibility:hidden;}

.store{
text-align:center;
font-size:50px;
font-weight:700;
}

.subtitle{
text-align:center;
font-size:22px;
color:#555;
}

.metric-card{
background:white;
padding:20px;
border-radius:12px;
text-align:center;
box-shadow:0px 3px 10px rgba(0,0,0,0.1);
}

.gold{
color:#D4AF37;
font-weight:600;
}

</style>
""", unsafe_allow_html=True)


# ---------- DATA ----------
products = {
    "Product": ["Rice","Milk","Eggs","Butter","Flour"],
    "Stock": [50,10,5,30,60]
}

pending_orders = {
    "Order ID":[101,102,103],
    "Product":["Milk","Eggs","Vegetables"],
    "Quantity":[20,30,50]
}

low_supply = {
    "Product":["Milk","Eggs"],
    "Stock Left":[10,5]
}


# ---------- HEADER ----------
col1,col2,col3 = st.columns([2,6,2])

with col1:
    st.image("logo.png", width=120)

with col2:
    st.markdown("<h2 style='text-align:center;'>Welcome to ShelfTrack</h2>", unsafe_allow_html=True)

with col3:
    if st.button("👤 Profile"):
        st.session_state.show_profile = not st.session_state.show_profile


# ---------- PROFILE ----------
if st.session_state.show_profile:

    st.subheader("Store Profile")

    st.write("Owner: Raj Patel")
    st.write("Email: tulsi.restaurant@gmail.com")
    st.write("Location: Vadodara")
    st.markdown("<span class='gold'>Plan: Gold</span>", unsafe_allow_html=True)

    st.divider()


# ---------- HOME PAGE ----------
if st.session_state.page == "home":

    st.markdown("<div class='store'>Tulsi</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Tulsi Restaurant</div>", unsafe_allow_html=True)

    st.write("")

    col1,col2,col3 = st.columns(3)

    with col1:
        if st.button("Total Products\n120", use_container_width=True):
            st.session_state.page = "products"

    with col2:
        if st.button("Pending Orders\n6", use_container_width=True):
            st.session_state.page = "orders"

    with col3:
        if st.button("Low Supply\n4", use_container_width=True):
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


# ---------- PRODUCTS ----------
elif st.session_state.page == "products":

    st.title("Total Products")

    st.table(products)

    if st.button("⬅ Back"):
        st.session_state.page = "home"


# ---------- PENDING ORDERS ----------
elif st.session_state.page == "orders":

    st.title("Pending Orders")

    st.table(pending_orders)

    if st.button("⬅ Back"):
        st.session_state.page = "home"


# ---------- LOW SUPPLY ----------
elif st.session_state.page == "low":

    st.title("Low Supply Items")

    st.table(low_supply)

    if st.button("⬅ Back"):
        st.session_state.page = "home"


# ---------- DASHBOARD ----------
elif st.session_state.page == "dashboard":

    st.title("Dashboard")

    col1,col2,col3 = st.columns(3)

    col1.metric("Total Products","120")
    col2.metric("Pending Orders","6")
    col3.metric("Low Supply","4")

    if st.button("⬅ Back"):
        st.session_state.page = "home"


# ---------- INVENTORY ----------
elif st.session_state.page == "inventory":

    st.title("Inventory")

    st.table(products)

    if st.button("⬅ Back"):
        st.session_state.page = "home"


# ---------- NOTIFICATIONS ----------
elif st.session_state.page == "notifications":

    st.title("Notifications")

    st.warning("Milk stock running low")
    st.warning("Egg inventory low")

    if st.button("⬅ Back"):
        st.session_state.page = "home"


# ---------- SUPPLIES ----------
elif st.session_state.page == "supplies":

    st.title("Supplies")

    st.write("Recommended Supplier: FreshFarm Distributors")
    st.write("Milk Price: ₹27 per unit")

    if st.button("⬅ Back"):
        st.session_state.page = "home"