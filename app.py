import streamlit as st
import sqlite3
from hashlib import sha256

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_password = sha256(password.encode()).hexdigest()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        st.success("Registration successful!")
    except sqlite3.IntegrityError:
        st.error("Username already exists.")
    conn.close()

def verify_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_password = sha256(password.encode()).hexdigest()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
    user = c.fetchone()
    conn.close()
    return user

# Initialize database
init_db()

# Initialize session state for user login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# Functions for login and registration
def login(username, password):
    if verify_user(username, password):
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.success("Logged in successfully!")
    else:
        st.error("Invalid username or password")

def register(username, password):
    register_user(username, password)

# Streamlit app
st.title("Food Ordering System")

# Authentication page
if not st.session_state.logged_in:
    option = st.sidebar.selectbox("Select an option", ["Login", "Register"])
    
    if option == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            login(username, password)
    
    elif option == "Register":
        st.subheader("Register")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Register"):
            register(username, password)

else:
    # After login, show the ordering system
    st.subheader("Welcome, " + st.session_state.current_user)
    menu_option = st.sidebar.selectbox(
        "Choose an option",
        ["View Menu", "View Cart", "Track Order"]
    )

    # Define menu items
    menu_items = {
        "Salads": {
            "Caesar Salad": ["vegetarian", "gluten-free", "low-sugar", "low-sodium"],
            "Quinoa Salad": ["vegan", "gluten-free", "dairy-free", "low-sugar", "high-protein"],
            "Greek Salad": ["vegetarian", "gluten-free", "low-sodium", "low-sugar"],
            "Kale & Avocado Salad": ["vegan", "gluten-free", "dairy-free", "low-sodium", "high-fiber", "low-sugar"],
            "Caprese Salad": ["vegetarian", "gluten-free", "low-sodium", "low-sugar"],
        },
        "Main Courses": {
            "Grilled Chicken": ["high-protein", "gluten-free", "low-sodium", "low-sugar"],
            "Pasta Primavera": ["vegetarian", "contains gluten", "low-sugar"],
            "Vegetable Stir-fry": ["vegan", "gluten-free", "low-sodium"],
            "Beef Burger (No Bun)": ["high-protein", "gluten-free", "low-sugar"],
            "Lentil Soup": ["vegan", "gluten-free", "dairy-free", "high-fiber", "low-sugar"],
            "Grilled Salmon": ["high-protein", "gluten-free", "low-sodium", "rich in Omega-3"],
        },
        "Drinks": {
            "Fruit Smoothie": ["vegan", "dairy-free", "low-sugar", "gluten-free"],
            "Iced Tea (unsweetened)": ["gluten-free", "dairy-free", "low-sugar", "low-sodium"],
            "Mango Lassi (No Sugar)": ["vegetarian", "contains dairy", "gluten-free", "low-sugar"],
        },
        "Desserts": {
            "Sugar-Free Chocolate Cake": ["vegetarian", "contains gluten", "low-sugar", "contains dairy"],
            "Fruit Salad": ["vegan", "gluten-free", "dairy-free", "low-sodium", "low-sugar"],
            "Vegan Brownie": ["vegan", "contains gluten", "low-sodium"],
        }
    }

    dietary_restrictions = ["None", "Vegan", "Vegetarian", "Gluten-Free", "Dairy-Free", "Low-Sugar", "Low-Sodium", "High-Protein"]

    order_status = [
        "Order Received", "Preparing Your Order", "Cooking In Progress", "Order Packed", "Out for Delivery", "Delivered"
    ]

    # Initialize session state for cart and order tracking
    if "cart" not in st.session_state:
        st.session_state.cart = []

    if "order_placed" not in st.session_state:
        st.session_state.order_placed = False

    # Sidebar menu to choose between options
    selected_restriction = st.sidebar.selectbox("Select Dietary Restriction", dietary_restrictions)
    
    if menu_option == "View Menu":
        category = st.selectbox("Select a Category", list(menu_items.keys()))
        
        if category:
            st.write(f"Here are the items in the {category} category:")

            # Display only items that match the selected dietary restriction
            for item, tags in menu_items[category].items():
                if selected_restriction == "None" or selected_restriction.lower() in tags:
                    st.write(f"- {item} ({', '.join(tags)})")
                    if st.button(f"Add {item} to Cart", key=item):
                        st.session_state.cart.append(item)
                        st.success(f"{item} added to cart!")

    elif menu_option == "View Cart":
        st.write("Your Cart:")
        if st.session_state.cart:
            for item in st.session_state.cart:
                st.write(f"- {item}")
            if st.button("Place Order"):
                st.session_state.order_placed = True
                st.session_state.cart = []  # Clear cart after placing order
                st.success("Your order has been placed!")
        else:
            st.write("Your cart is empty.")

    elif menu_option == "Track Order":
        if st.session_state.order_placed:
            def process_order():
                st.write("Processing your order...")
                for i in range(len(order_status)):
                    st.write(f"Status: {order_status[i]}")
                    time.sleep(2)
                    if i == len(order_status) - 1:
                        st.success("Your order has been delivered!")
                    else:
                        st.info(f"Next step: {order_status[i + 1]}")
            
            process_order()
        else:
            st.write("No order placed yet.")
