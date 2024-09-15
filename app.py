import streamlit as st
import logging
import random
import time

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

menu_items = {
    "Salads": {
        "Caesar Salad": ["vegetarian", "gluten-free", "low-sugar", "low-sodium"],
        "Quinoa Salad": ["vegan", "gluten-free", "dairy-free", "low-sugar", "high-protein"],
        "Greek Salad": ["vegetarian", "gluten-free", "low-sodium", "low-sugar"],
        "Kale & Avocado Salad": ["vegan", "gluten-free", "dairy-free", "low-sodium", "high-fiber", "low-sugar"],
        "Caprese Salad": ["vegetarian", "gluten-free", "low-sodium", "low-sugar"],
        # Add 100 more salad items here with different tags
    },
    "Main Courses": {
        "Grilled Chicken": ["high-protein", "gluten-free", "low-sodium", "low-sugar"],
        "Pasta Primavera": ["vegetarian", "contains gluten", "low-sugar"],
        "Vegetable Stir-fry": ["vegan", "gluten-free", "low-sodium"],
        "Beef Burger (No Bun)": ["high-protein", "gluten-free", "low-sugar"],
        "Lentil Soup": ["vegan", "gluten-free", "dairy-free", "high-fiber", "low-sugar"],
        "Grilled Salmon": ["high-protein", "gluten-free", "low-sodium", "rich in Omega-3"],
        "Vegan Buddha Bowl": ["vegan", "gluten-free", "dairy-free", "low-sodium"],
        "Margherita Pizza": ["vegetarian", "contains gluten", "contains dairy"],
        "Chickpea Curry": ["vegan", "gluten-free", "low-sodium", "high-protein"],
        "Eggplant Parmesan": ["vegetarian", "contains gluten", "low-sodium", "low-sugar"],
        "Steamed Cod with Vegetables": ["high-protein", "gluten-free", "low-sodium", "low-sugar"],
        # Add 100 more main course items here with different tags
    },
    "Drinks": {
        "Fruit Smoothie": ["vegan", "dairy-free", "low-sugar", "gluten-free"],
        "Iced Tea (unsweetened)": ["gluten-free", "dairy-free", "low-sugar", "low-sodium"],
        "Mango Lassi (No Sugar)": ["vegetarian", "contains dairy", "gluten-free", "low-sugar"],
        "Almond Milk Latte": ["vegan", "gluten-free", "dairy-free", "low-sugar"],
        "Green Tea": ["vegan", "gluten-free", "dairy-free", "low-sugar", "low-sodium"],
        "Coconut Water": ["vegan", "gluten-free", "dairy-free", "low-sodium", "low-sugar"],
        "Carrot Juice": ["vegan", "gluten-free", "low-sugar", "high in Vitamin A"],
        "Beetroot Juice": ["vegan", "gluten-free", "low-sodium", "rich in iron"],
        # Add 100 more drink items here with different tags
    },
    "Desserts": {
        "Sugar-Free Chocolate Cake": ["vegetarian", "contains gluten", "low-sugar", "contains dairy"],
        "Fruit Salad": ["vegan", "gluten-free", "dairy-free", "low-sodium", "low-sugar"],
        "Vegan Brownie": ["vegan", "contains gluten", "low-sodium"],
        "Chia Pudding": ["vegan", "gluten-free", "dairy-free", "low-sugar"],
        "Baked Apples": ["vegan", "gluten-free", "low-sodium", "low-sugar"],
        "Frozen Yogurt (No Sugar)": ["vegetarian", "gluten-free", "contains dairy", "low-sugar"],
        "Oatmeal Cookies (No Sugar)": ["vegan", "contains gluten", "low-sugar", "high-fiber"],
        # Add 100 more dessert items here with different tags
    },
    "Appetizers": {
        "Garlic Bread": ["vegetarian", "contains gluten"],
        "Bruschetta": ["vegetarian", "contains gluten"],
        "Falafel": ["vegan", "gluten-free", "dairy-free", "low-sodium", "high-protein"],
        "Spring Rolls": ["vegan", "contains gluten", "low-sodium"],
        "Stuffed Mushrooms": ["vegetarian", "gluten-free", "low-sodium"],
        "Guacamole with Chips": ["vegan", "gluten-free", "dairy-free", "low-sodium"],
        "Roasted Chickpeas": ["vegan", "gluten-free", "low-sodium", "low-sugar", "high-protein"],
        "Baked Zucchini Fries": ["vegan", "gluten-free", "low-sodium"],
        # Add 100 more appetizer items here with different tags
    }
}

# Define dietary preferences, including specific health condition restrictions
dietary_preferences = {
    "vegan": [
        "Quinoa Salad", "Kale & Avocado Salad", "Greek Salad", "Vegetable Stir-fry",
        "Lentil Soup", "Vegan Buddha Bowl", "Chickpea Curry", "Falafel", "Spring Rolls",
        "Roasted Chickpeas", "Baked Zucchini Fries", "Fruit Smoothie", "Almond Milk Latte",
        "Green Tea", "Coconut Water", "Carrot Juice", "Beetroot Juice", "Fruit Salad",
        "Vegan Brownie", "Chia Pudding", "Baked Apples", "Oatmeal Cookies",
        # Add 500 more vegan items here
    ],
    "vegetarian": [
        "Caesar Salad", "Greek Salad", "Caprese Salad", "Pasta Primavera", "Margherita Pizza",
        "Eggplant Parmesan", "Garlic Bread", "Bruschetta", "Stuffed Mushrooms", "Mango Lassi (No Sugar)",
        "Frozen Yogurt (No Sugar)", "Sugar-Free Chocolate Cake",
        # Add 500 more vegetarian items here
    ],
    "gluten-free": [
        "Caesar Salad", "Quinoa Salad", "Greek Salad", "Kale & Avocado Salad", "Chicken & Spinach Salad",
        "Grilled Chicken", "Vegetable Stir-fry", "Lentil Soup", "Grilled Salmon", "Vegan Buddha Bowl",
        "Chickpea Curry", "Steamed Cod with Vegetables", "Fruit Smoothie", "Iced Tea", "Mango Lassi",
        "Almond Milk Latte", "Green Tea", "Coconut Water", "Carrot Juice", "Beetroot Juice", "Fruit Salad",
        "Chia Pudding", "Baked Apples", "Frozen Yogurt", "Roasted Chickpeas", "Baked Zucchini Fries",
        # Add 500 more gluten-free items here
    ],
    "dairy-free": [
        "Quinoa Salad", "Kale & Avocado Salad", "Vegetable Stir-fry", "Lentil Soup", "Vegan Buddha Bowl",
        "Chickpea Curry", "Steamed Cod with Vegetables", "Fruit Smoothie", "Almond Milk Latte",
        "Green Tea", "Coconut Water", "Carrot Juice", "Beetroot Juice", "Fruit Salad", "Chia Pudding",
        "Baked Apples", "Oatmeal Cookies", "Falafel", "Roasted Chickpeas", "Baked Zucchini Fries",
        # Add 500 more dairy-free items here
    ],
    "low-sugar": [
        "Quinoa Salad", "Greek Salad", "Kale & Avocado Salad", "Chicken & Spinach Salad", "Grilled Chicken",
        "Lentil Soup", "Beef Burger (No Bun)", "Grilled Salmon", "Fruit Smoothie", "Iced Tea (unsweetened)",
        "Almond Milk Latte", "Green Tea", "Coconut Water", "Carrot Juice", "Sugar-Free Chocolate Cake",
        "Fruit Salad", "Chia Pudding", "Frozen Yogurt (No Sugar)", "Baked Apples", "Oatmeal Cookies",
        # Add 500 more low-sugar items here
    ],
    "low-sodium": [
        "Caesar Salad", "Greek Salad", "Kale & Avocado Salad", "Grilled Chicken", "Vegetable Stir-fry",
        "Lentil Soup", "Grilled Salmon", "Vegan Buddha Bowl", "Chickpea Curry", "Steamed Cod with Vegetables",
        "Fruit Smoothie", "Iced Tea (unsweetened)", "Green Tea", "Coconut Water", "Carrot Juice",
        "Beetroot Juice", "Fruit Salad", "Chia Pudding", "Baked Apples", "Roasted Chickpeas",
        "Baked Zucchini Fries", "Stuffed Mushrooms",
        # Add 500 more low-sodium items here
    ],
    "high-protein": [
        "Grilled Chicken", "Chickpea Curry", "Beef Burger (No Bun)", "Lentil Soup", "Grilled Salmon",
        "Vegan Buddha Bowl", "Roasted Chickpeas", "Oatmeal Cookies", "Almond Milk Latte", "Carrot Juice",
        "Beetroot Juice", "Fruit Salad", "Chia Pudding",
        # Add 500 more high-protein items here
    ],
}
# Order tracking simulation
order_status = [
    "Order Received", "Preparing Your Order", "Cooking In Progress", "Order Packed", "Out for Delivery", "Delivered"
]

# Define a function to simulate order processing
def process_order():
    st.write("Processing your order...")
    status = random.choice(order_status)
    for i in range(len(order_status)):
        st.write(f"Status: {order_status[i]}")
        time.sleep(2)
        if i == len(order_status) - 1:
            st.success("Your order has been delivered!")
        else:
            st.info(f"Next step: {order_status[i+1]}")

# Streamlit App
st.title("Restaurant Menu & Ordering System")

# Initialize session state for cart and order tracking
if "cart" not in st.session_state:
    st.session_state.cart = []

if "order_placed" not in st.session_state:
    st.session_state.order_placed = False

# Sidebar menu to choose between options
menu_option = st.sidebar.selectbox(
    "Choose an option",
    ["View Menu", "View Cart", "Track Order"]
)

# View Menu
if menu_option == "View Menu":
    category = st.selectbox("Select a Category", list(menu_items.keys()))
    if category:
        st.write(f"Here are the items in the {category} category:")
        for item in menu_items[category]:
            st.write(f"- {item} ({', '.join(menu_items[category][item])})")
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
