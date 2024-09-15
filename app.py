import streamlit as st
import streamlit_authenticator as stauth
from googletrans import Translator
from datetime import datetime
import random

# Initial data setup
menu_items = [
    {'name': 'Pizza Margherita', 'price': 8, 'ingredients': 'Tomato, Mozzarella, Basil', 'allergens': 'Dairy'},
    {'name': 'Vegan Salad', 'price': 5, 'ingredients': 'Lettuce, Tomato, Cucumber', 'allergens': None},
    {'name': 'Spaghetti Bolognese', 'price': 10, 'ingredients': 'Beef, Tomato, Pasta', 'allergens': 'Gluten'},
    {'name': 'Chicken Burger', 'price': 9, 'ingredients': 'Chicken, Lettuce, Tomato', 'allergens': 'Gluten, Dairy'}
]

discounts = {"FREEDISH": 10}  # Promo code for 10% off

# Mock user credentials
users = {"user1": "password", "user2": "password123"}

# User Authentication
authenticator = stauth.Authenticate(list(users.keys()), list(users.values()), "some_cookie", "some_key", cookie_expiry_days=1)
name, authentication_status, username = authenticator.login("Login", "sidebar")

# Translator
translator = Translator()

# Function to calculate order total
def calculate_total(order, promo_code=None):
    total = sum(item['price'] for item in order)
    if promo_code and promo_code in discounts:
        total = total * (1 - discounts[promo_code] / 100)
    return total

# Function to filter menu based on search query
def search_menu(query):
    return [item for item in menu_items if query.lower() in item['name'].lower()]

# Main Page Content
if authentication_status:
    st.title(f"Welcome, {name}")
    
    # Search Functionality
    search_query = st.text_input("Search for dishes:")
    if search_query:
        menu = search_menu(search_query)
    else:
        menu = menu_items

    # Display Menu
    st.subheader("Menu")
    order = []
    for item in menu:
        st.write(f"{item['name']} - ${item['price']}")
        st.write(f"Ingredients: {item['ingredients']}")
        if item['allergens']:
            st.warning(f"Allergens: {item['allergens']}")
        quantity = st.number_input(f"Quantity of {item['name']}", min_value=0, max_value=10, key=item['name'])
        if quantity > 0:
            order.extend([item] * quantity)

    # Customizations (e.g., sauces, sides)
    if order:
        st.subheader("Order Customization")
        for item in order:
            st.write(f"Customize {item['name']}")
            if item['name'] == 'Pizza Margherita':
                extras = st.multiselect("Choose extras for Pizza:", ["Extra Cheese", "Olives", "Pepperoni"], key=f"{item['name']}_extras")
                st.write(f"You selected: {extras}")

    # Apply Promo Code
    promo_code = st.text_input("Promo Code:")
    
    # Order Summary
    if order:
        st.subheader("Order Summary")
        total_price = calculate_total(order, promo_code)
        for item in order:
            st.write(f"{item['name']} - ${item['price']}")
        if promo_code and promo_code in discounts:
            st.success(f"Promo code applied! {discounts[promo_code]}% off")
        st.write(f"Total: ${total_price}")

        # Confirm and Place Order
        if st.button("Place Order"):
            st.success("Order placed successfully!")
            order_time = datetime.now().strftime("%H:%M:%S")
            delivery_time = f"{random.randint(20, 40)} minutes"
            st.write(f"Order Time: {order_time}")
            st.write(f"Estimated Delivery Time: {delivery_time}")

            # Feedback
            st.subheader("Feedback")
            rating = st.slider("Rate your experience:", 1, 5)
            feedback = st.text_area("Leave feedback:")
            if st.button("Submit Feedback"):
                st.write(f"Thank you for your feedback! Rating: {rating}/5")
    
    # Dietary Restriction Filtering
    st.sidebar.subheader("Dietary Preferences")
    gluten_free = st.sidebar.checkbox("Gluten Free")
    dairy_free = st.sidebar.checkbox("Dairy Free")
    vegan = st.sidebar.checkbox("Vegan")
    
    # Filter based on preferences
    if gluten_free or dairy_free or vegan:
        filtered_menu = [item for item in menu_items if (gluten_free and 'Gluten' not in item['allergens']) or (dairy_free and 'Dairy' not in item['allergens']) or (vegan and 'Beef' not in item['ingredients'])]
        if filtered_menu:
            st.sidebar.write("Filtered Menu:")
            for item in filtered_menu:
                st.sidebar.write(item['name'])
        else:
            st.sidebar.write("No items match your dietary preferences.")
    
    # Multi-language Support
    lang_option = st.sidebar.selectbox("Choose language", ['English', 'French', 'Spanish'])
    if lang_option != 'English':
        translation = translator.translate("Welcome to the restaurant menu app!", dest=lang_option[:2].lower())
        st.sidebar.write(translation.text)

    # Logout Button
    authenticator.logout("Logout", "sidebar")

elif authentication_status == False:
    st.error("Invalid username or password")
else:
    st.warning("Please log in to access the menu")
