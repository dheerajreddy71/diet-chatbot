import streamlit as st
import logging
import time
from transformers import pipeline
from streamlit_authenticator import Authenticate
from googletrans import Translator

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Example menu items
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

# Initialize Streamlit Authenticator
authenticator = Authenticate(
    credentials={
        "usernames": {
            "testuser": {"password": "testpassword"}
        }
    },
    cookie_name="session",
    cookie_expiry_days=1,
    login_url="http://localhost:8501/login"
)

# Initialize NLP chatbot
chatbot = pipeline('conversational', model='facebook/blenderbot-400M-distill')

def chat_with_bot(user_input):
    response = chatbot(user_input)
    return response[0]['generated_text']

# Define functions for various features
def process_order():
    st.write("Processing your order...")
    for i in range(len(order_status)):
        st.write(f"Status: {order_status[i]}")
        time.sleep(2)
        if i == len(order_status) - 1:
            st.success("Your order has been delivered!")
        else:
            st.info(f"Next step: {order_status[i + 1]}")

def search_menu(query):
    results = []
    for category, items in menu_items.items():
        for item, tags in items.items():
            if query.lower() in item.lower():
                results.append((category, item, tags))
    return results

def translate_text(text, lang="en"):
    translator = Translator()
    return translator.translate(text, dest=lang).text

# Streamlit App
st.title("Restaurant Menu & Ordering System")

# Initialize session state for cart and order tracking
if "cart" not in st.session_state:
    st.session_state.cart = []

if "order_placed" not in st.session_state:
    st.session_state.order_placed = False

if "user" not in st.session_state:
    st.session_state.user = None

# Sidebar menu
menu_option = st.sidebar.selectbox(
    "Choose an option",
    ["Login", "View Menu", "View Cart", "Track Order", "Chat with Bot", "Search Menu"]
)

# Handle authentication
if menu_option == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticator.authenticate(username, password):
            st.session_state.user = username
            st.success("Logged in successfully!")
        else:
            st.error("Invalid credentials")

# Handle Chatbot
elif menu_option == "Chat with Bot":
    user_input = st.text_input("Ask me anything about our menu:")
    if user_input:
        bot_response = chat_with_bot(user_input)
        st.write(f"Bot: {bot_response}")

# Handle Menu Search
elif menu_option == "Search Menu":
    query = st.text_input("Enter a dish name or ingredient:")
    if query:
        results = search_menu(query)
        if results:
            for result in results:
                st.write(f"Category: {result[0]}, Dish: {result[1]}, Tags: {', '.join(result[2])}")
        else:
            st.write("No results found.")

# Allow user to set dietary restrictions
selected_restriction = st.sidebar.selectbox("Select Dietary Restriction", dietary_restrictions)

# View Menu
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

# Add more features as needed based on the outlined functionalities.

