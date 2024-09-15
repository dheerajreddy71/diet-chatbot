import streamlit as st
import sqlite3
from hashlib import sha256
import time
from googletrans import Translator

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, role TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS feedback
                 (username TEXT, feedback_text TEXT, rating INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS orders
                 (username TEXT, order_details TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Hashing function for passwords
def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Function to check user credentials
def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user

# Mock function to get delivery time
def get_estimated_delivery_time():
    return "Your order will be delivered in approximately 30-45 minutes."

# Multi-language support
def translate_text(text, target_language):
    translator = Translator()
    return translator.translate(text, dest=target_language).text

# Streamlit App
st.title("Restaurant Menu & Ordering System")

# Initialize session state for cart, authentication, and pages
if "cart" not in st.session_state:
    st.session_state.cart = []
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "admin" not in st.session_state:
    st.session_state.admin = False
if "page" not in st.session_state:
    st.session_state.page = "Login"
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "order_placed" not in st.session_state:
    st.session_state.order_placed = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Language selection
language = st.sidebar.selectbox("Choose Language", ["English", "French", "Spanish"])

# Display pages based on session state
if st.session_state.page == "Login":
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = authenticate_user(username, password)
        if user:
            st.session_state.authenticated = True
            st.session_state.username = username  # Store username in session state
            st.session_state.admin = user[2] == "admin"  # Set admin status based on role
            st.session_state.page = "Ordering"
        else:
            st.error("Invalid username or password")

    st.write("Don't have an account?")
    if st.button("Register"):
        st.session_state.page = "Register"

elif st.session_state.page == "Register":
    st.header("Register")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    is_admin = st.checkbox("Admin")

    if st.button("Register"):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (new_username, hash_password(new_password), "admin" if is_admin else "user"))
            conn.commit()
            st.success("Registration successful! Please log in.")
            st.session_state.page = "Login"
        except sqlite3.IntegrityError:
            st.error("Username already exists.")
        conn.close()

elif st.session_state.page == "Ordering":
    if not st.session_state.authenticated:
        st.session_state.page = "Login"
        
    st.header("Ordering Page")
    
    # Sidebar menu to choose between options
    menu_option = st.sidebar.selectbox(
        "Choose an option",
        ["View Menu", "View Cart", "Track Order", "Favorites", "Feedback", "Admin - View Feedback"]
    )

    # Allow user to set dietary restrictions
    dietary_restrictions = ["None", "Vegan", "Vegetarian", "Gluten-Free", "Dairy-Free", "Low-Sugar", "Low-Sodium", "High-Protein"]
    selected_restriction = st.sidebar.selectbox("Select Dietary Restriction", dietary_restrictions)

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

    order_status = [
        "Order Received", "Preparing Your Order", "Cooking In Progress", "Order Packed", "Out for Delivery", "Delivered"
    ]

    def process_order():
        st.write("Processing your order...")
        for i in range(len(order_status)):
            st.write(f"Status: {order_status[i]}")
            time.sleep(2)
            if i == len(order_status) - 1:
                st.success("Your order has been delivered!")
            else:
                st.info(f"Next step: {order_status[i + 1]}")

    if menu_option == "View Menu":
        category = st.selectbox("Select a Category", list(menu_items.keys()))
        search_query = st.text_input("Search Menu Items")
        
        if category:
            st.write(f"Here are the items in the {category} category:")

            for item, tags in menu_items[category].items():
                if (selected_restriction == "None" or selected_restriction.lower() in tags) and search_query.lower() in item.lower():
                    st.write(f"- {item} ({', '.join(tags)})")
                    if st.button(f"Add {item} to Cart", key=item):
                        st.session_state.cart.append(item)
                        st.success(f"{item} added to cart!")
                    if st.button(f"Add {item} to Favorites", key=item + "_fav"):
                        st.session_state.favorites.append(item)
                        st.success(f"{item} added to favorites!")

    elif menu_option == "View Cart":
        st.write("Your Cart:")
        if st.session_state.cart:
            for item in st.session_state.cart:
                st.write(f"- {item}")
            estimated_delivery = get_estimated_delivery_time()
            st.write(f"Estimated Delivery Time: {estimated_delivery}")
            if st.button("Place Order"):
                st.session_state.order_placed = True
                st.session_state.cart = []  # Clear cart after placing order
                conn = sqlite3.connect('users.db')
                c = conn.cursor()
                order_details = ', '.join(st.session_state.cart)
                c.execute('INSERT INTO orders (username, order_details) VALUES (?, ?)', (st.session_state.username, order_details))
                conn.commit()
                conn.close()
                st.success("Your order has been placed!")
        else:
            st.write("Your cart is empty.")

    elif menu_option == "Track Order":
        if st.session_state.order_placed:
            process_order()
        else:
            st.write("No order placed yet.")

    elif menu_option == "Favorites":
        st.write("Your Favorites:")
        if st.session_state.favorites:
            for item in st.session_state.favorites:
                st.write(f"- {item}")
        else:
            st.write("No favorites yet.")

    elif menu_option == "Feedback":
        st.header("Submit Feedback")
        feedback_text = st.text_area("Enter your feedback")
        rating = st.slider("Rating", 1, 5)

        if st.button("Submit Feedback"):
            try:
                if st.session_state.authenticated:
                    conn = sqlite3.connect('users.db')
                    c = conn.cursor()
                    c.execute('INSERT INTO feedback (username, feedback_text, rating) VALUES (?, ?, ?)',
                              (st.session_state.username, feedback_text, rating))
                    conn.commit()
                    conn.close()
                    st.success("Thank you for your feedback!")
                else:
                    st.error("You need to log in to submit feedback.")
            except Exception as e:
                st.error(f"Error: {e}")

    elif menu_option == "Admin - View Feedback":
        if not st.session_state.admin:
            st.error("Access denied. Admins only.")
        else:
            st.header("Admin - View Feedback")
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute('SELECT * FROM feedback')
            feedback = c.fetchall()
            conn.close()

            if feedback:
                for fb in feedback:
                    st.write(f"Username: {fb[0]}")
                    st.write(f"Feedback: {fb[1]}")
                    st.write(f"Rating: {fb[2]}")
                    st.write("---")
            else:
                st.write("No feedback available yet.")
