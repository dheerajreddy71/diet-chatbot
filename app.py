import streamlit as st
import logging
import random
import time
from streamlit_authenticator import Authenticate

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Authentication Setup
authenticator = Authenticate(
    usernames=['user1', 'user2'],
    passwords=['password1', 'password2'],
    names=['User One', 'User Two'],
    cookie_name='restaurant_app',
    cookie_expiry_days=30
)

# Sample Data
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
order_status = ["Order Received", "Preparing Your Order", "Cooking In Progress", "Order Packed", "Out for Delivery", "Delivered"]

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

# User Authentication
if not authenticator.is_authenticated:
    username, password = authenticator.login()
    if username and password:
        st.session_state.user = username
    else:
        st.stop()

# Initialize session state for cart and order tracking
if "cart" not in st.session_state:
    st.session_state.cart = []

if "order_placed" not in st.session_state:
    st.session_state.order_placed = False

if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "addresses" not in st.session_state:
    st.session_state.addresses = []

if "feedback" not in st.session_state:
    st.session_state.feedback = []

# Sidebar menu to choose between options
menu_option = st.sidebar.selectbox(
    "Choose an option",
    ["View Menu", "View Cart", "Track Order", "User Profile"]
)

# User Profile
if menu_option == "User Profile":
    st.write(f"Welcome, {st.session_state.user}!")
    st.write("Your Favorites:")
    if st.session_state.favorites:
        for item in st.session_state.favorites:
            st.write(f"- {item}")
    else:
        st.write("No favorites yet.")
    
    st.write("Your Addresses:")
    if st.session_state.addresses:
        for address in st.session_state.addresses:
            st.write(f"- {address}")
    else:
        st.write("No addresses saved.")
    
    feedback = st.text_area("Provide Feedback:")
    if st.button("Submit Feedback"):
        st.session_state.feedback.append(feedback)
        st.success("Feedback submitted!")
    
# View Menu
elif menu_option == "View Menu":
    search_query = st.text_input("Search for a dish:")
    category = st.selectbox("Select a Category", list(menu_items.keys()))
    
    if category:
        st.write(f"Here are the items in the {category} category:")

        for item, tags in menu_items[category].items():
            if search_query.lower() in item.lower() and (selected_restriction == "None" or selected_restriction.lower() in tags):
                st.write(f"- {item} ({', '.join(tags)})")
                if st.button(f"Add {item} to Cart", key=item):
                    st.session_state.cart.append(item)
                    st.success(f"{item} added to cart!")
                if st.button(f"Add {item} to Favorites", key=f"fav_{item}"):
                    if item not in st.session_state.favorites:
                        st.session_state.favorites.append(item)
                        st.success(f"{item} added to favorites!")

# View Cart
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

# Track Order
elif menu_option == "Track Order":
    if st.session_state.order_placed:
        process_order()
    else:
        st.write("No order placed yet.")
