import streamlit as st
import logging
import time
import random

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock Data
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

# Define a function to simulate order processing
def process_order():
    st.write("Processing your order...")
    for i in range(len(order_status)):
        st.write(f"Status: {order_status[i]}")
        time.sleep(2)
        if i == len(order_status) - 1:
            st.success("Your order has been delivered!")
        else:
            st.info(f"Next step: {order_status[i + 1]}")

# Streamlit App
st.title("Restaurant Menu & Ordering System")

# Dark/Light Mode
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

if st.sidebar.checkbox('Dark Mode', value=st.session_state.dark_mode):
    st.session_state.dark_mode = True
    st.markdown("""
        <style>
        body {
            background-color: #000000;
            color: #FFFFFF;
        }
        </style>
        """, unsafe_allow_html=True)
else:
    st.session_state.dark_mode = False
    st.markdown("""
        <style>
        body {
            background-color: #FFFFFF;
            color: #000000;
        }
        </style>
        """, unsafe_allow_html=True)

# Multi-language Support
lang = st.sidebar.selectbox("Select Language", ["English", "Spanish"])

# Initialize session state for cart, order tracking, user authentication, and favorites
if "cart" not in st.session_state:
    st.session_state.cart = []
if "order_placed" not in st.session_state:
    st.session_state.order_placed = False
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "feedback" not in st.session_state:
    st.session_state.feedback = []

# Sidebar menu to choose between options
menu_option = st.sidebar.selectbox(
    "Choose an option",
    ["Login", "View Menu", "View Cart", "Track Order", "Favorites", "Feedback"]
)

# User Authentication
if menu_option == "Login":
    if not st.session_state.user_authenticated:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            # Mock authentication
            if username == "user" and password == "pass":
                st.session_state.user_authenticated = True
                st.success("Logged in successfully!")
            else:
                st.error("Invalid credentials.")
    else:
        st.write("You are already logged in.")

# View Menu
elif menu_option == "View Menu":
    if not st.session_state.user_authenticated:
        st.warning("Please log in to view the menu.")
    else:
        search_query = st.text_input("Search Menu")
        category = st.selectbox("Select a Category", list(menu_items.keys()))
        
        if category:
            st.write(f"Here are the items in the {category} category:")
            for item, tags in menu_items[category].items():
                if search_query.lower() in item.lower() and (selected_restriction == "None" or selected_restriction.lower() in tags):
                    st.write(f"- {item} ({', '.join(tags)})")
                    if st.button(f"Add {item} to Cart", key=item):
                        st.session_state.cart.append(item)
                        st.success(f"{item} added to cart!")
                    if st.button(f"Add {item} to Favorites", key=favorite_key := f"{item}_favorite"):
                        st.session_state.favorites.append(item)
                        st.success(f"{item} added to favorites!")

# View Cart
elif menu_option == "View Cart":
    if not st.session_state.user_authenticated:
        st.warning("Please log in to view your cart.")
    else:
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

# Track Order
elif menu_option == "Track Order":
    if not st.session_state.user_authenticated:
        st.warning("Please log in to track your order.")
    elif st.session_state.order_placed:
        process_order()
    else:
        st.write("No order placed yet.")

# Favorites
elif menu_option == "Favorites":
    if not st.session_state.user_authenticated:
        st.warning("Please log in to view your favorites.")
    else:
        st.write("Your Favorites:")
        if st.session_state.favorites:
            for item in st.session_state.favorites:
                st.write(f"- {item}")
        else:
            st.write("You have no favorites yet.")

# Feedback
elif menu_option == "Feedback":
    if not st.session_state.user_authenticated:
        st.warning("Please log in to provide feedback.")
    else:
        feedback = st.text_area("Provide your feedback here")
        if st.button("Submit Feedback"):
            st.session_state.feedback.append(feedback)
            st.success("Thank you for your feedback!")

# Miscellaneous
# Payment Integration (Mock)
def mock_payment():
    st.write("Payment Integration (Mock):")
    if st.button("Proceed to Payment"):
        st.success("Payment successful!")

# Customizable Orders (Example of adding customization)
def customize_order():
    st.write("Customize Your Order:")
    customization = st.text_input("Special Instructions")
    if st.button("Submit Customization"):
        st.success(f"Customization: {customization} added to your order!")

# Estimation of Delivery Time (Mock)
def estimated_delivery_time():
    st.write("Estimated Delivery Time:")
    time_estimate = random.randint(20, 60)
    st.write(f"Your order will be delivered in approximately {time_estimate} minutes.")

# Final Notes
st.write("Thank you for using our Restaurant Menu & Ordering System!")
