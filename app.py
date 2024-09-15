import streamlit as st
import sqlite3
from hashlib import sha256
import time

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, role TEXT)''')
    conn.commit()
    conn.close()

def setup_sample_admin():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', ('admin',))
    if not c.fetchone():
        c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                  ('admin', hash_password('admin123'), 'admin'))
        conn.commit()
    conn.close()


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

# Function to get user role
def get_user_role(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT role FROM users WHERE username = ?', (username,))
    role = c.fetchone()
    conn.close()
    return role[0] if role else None

# Function to register a new user
def register_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                  (username, hash_password(password), 'user'))
        conn.commit()
        st.success("Registration successful! Please log in.")
    except sqlite3.IntegrityError:
        st.error("Username already exists.")
    conn.close()

# Mock function to get delivery time
def get_estimated_delivery_time():
    return "Your order will be delivered in approximately 30-45 minutes."

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
    st.session_state.username = None  # Store the username of the logged-in user

init_db()
setup_sample_admin()

# Page navigation
if st.session_state.page == "Login":
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = authenticate_user(username, password)
        if user:
            role = get_user_role(username)
            if role == 'admin':
                st.session_state.admin = True
            st.session_state.authenticated = True
            st.session_state.username = username  # Store the username
            st.session_state.page = "Ordering" if role == 'user' else "AdminDashboard"
        else:
            st.error("Invalid username or password")

    if st.button("Go to Register"):
        st.session_state.page = "Register"

elif st.session_state.page == "Register":
    st.header("Register")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    if st.button("Register"):
        register_user(new_username, new_password)
        st.session_state.page = "Login"

elif st.session_state.page == "Ordering":
    if not st.session_state.authenticated:
        st.session_state.page = "Login"
        
    st.header("Ordering Page")
    
    # Sidebar menu to choose between options
    menu_option = st.sidebar.selectbox(
        "Choose an option",
        ["View Menu", "View Cart", "Track Order", "Favorites", "Feedback"]
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
        "Spinach & Strawberry Salad": ["vegan", "gluten-free", "dairy-free", "low-sugar"],
        "Chickpea & Cucumber Salad": ["vegan", "gluten-free", "dairy-free", "high-protein"],
        "Roasted Beet Salad": ["vegan", "gluten-free", "dairy-free", "low-sugar", "high-fiber"],
        "Avocado & Black Bean Salad": ["vegan", "gluten-free", "dairy-free", "high-protein", "low-sugar"],
        "Asian Noodle Salad": ["vegetarian", "contains gluten", "dairy-free"],
        "Southwestern Corn Salad": ["vegan", "gluten-free", "dairy-free", "low-sodium", "high-fiber"],
        "Thai Mango Salad": ["vegan", "gluten-free", "dairy-free", "low-sugar"],
        "Cobb Salad": ["vegetarian", "gluten-free", "contains dairy"],
        "Mediterranean Chickpea Salad": ["vegan", "gluten-free", "dairy-free", "high-protein"],
        "Waldorf Salad": ["vegetarian", "contains nuts", "contains dairy"],
        "Farro Salad": ["vegetarian", "gluten-free", "contains dairy"],
        "Black-Eyed Pea Salad": ["vegan", "gluten-free", "dairy-free", "high-protein"],
        "Corn & Avocado Salad": ["vegan", "gluten-free", "dairy-free", "low-sodium"],
        "Fruit & Nut Salad": ["vegetarian", "gluten-free", "contains nuts"],
        "Roasted Sweet Potato Salad": ["vegan", "gluten-free", "dairy-free"],
        "Panzanella Salad": ["vegetarian", "contains gluten"],
        "Lentil Salad": ["vegan", "gluten-free", "dairy-free", "high-protein"],
        "Pico de Gallo Salad": ["vegan", "gluten-free", "dairy-free"],
        "Arugula & Parmesan Salad": ["vegetarian", "gluten-free", "contains dairy"],
        "Carrot & Raisin Salad": ["vegan", "gluten-free", "dairy-free"],
        "Apple & Walnut Salad": ["vegetarian", "gluten-free", "contains nuts"],
        "Zucchini & Tomato Salad": ["vegan", "gluten-free", "dairy-free"],
        "Cucumber & Tomato Salad": ["vegan", "gluten-free", "dairy-free"],
        "Sesame Ginger Salad": ["vegan", "gluten-free", "dairy-free"],
        "Avocado & Tomato Salad": ["vegan", "gluten-free", "dairy-free"],
        "Chilled Gazpacho Salad": ["vegan", "gluten-free", "dairy-free"],
        "Corn & Bean Salad": ["vegan", "gluten-free", "dairy-free", "high-protein"],
        "Beet & Goat Cheese Salad": ["vegetarian", "gluten-free", "contains dairy"],
        "Butternut Squash Salad": ["vegan", "gluten-free", "dairy-free"],
        "Cabbage & Carrot Salad": ["vegan", "gluten-free", "dairy-free"],
        "Spinach & Feta Salad": ["vegetarian", "gluten-free", "contains dairy"],
        "Pasta Salad": ["vegetarian", "contains gluten"],
        "Grape & Walnut Salad": ["vegetarian", "gluten-free", "contains nuts"],
        "Radish & Cucumber Salad": ["vegan", "gluten-free", "dairy-free"],
        "Sweet Potato & Kale Salad": ["vegan", "gluten-free", "dairy-free"],
        "Berry & Spinach Salad": ["vegan", "gluten-free", "dairy-free"],
        "Pear & Gorgonzola Salad": ["vegetarian", "gluten-free", "contains dairy"],
        "Tomato & Mozzarella Salad": ["vegetarian", "gluten-free", "contains dairy"],
        "Roasted Vegetable Salad": ["vegan", "gluten-free", "dairy-free"],
        "Miso Salad": ["vegan", "gluten-free", "dairy-free"],
        "Hummus & Veggie Salad": ["vegan", "gluten-free", "dairy-free"],
        "Citrus & Avocado Salad": ["vegan", "gluten-free", "dairy-free"],
    },
        "Main Courses": {
        "Grilled Chicken": ["high-protein", "gluten-free", "low-sodium", "low-sugar"],
        "Pasta Primavera": ["vegetarian", "contains gluten", "low-sugar"],
        "Vegetable Stir-fry": ["vegan", "gluten-free", "low-sodium"],
        "Beef Burger (No Bun)": ["high-protein", "gluten-free", "low-sugar"],
        "Lentil Soup": ["vegan", "gluten-free", "dairy-free", "high-fiber", "low-sugar"],
        "Grilled Salmon": ["high-protein", "gluten-free", "low-sodium", "rich in Omega-3"],
        "Chicken Alfredo": ["contains gluten", "contains dairy"],
        "Stuffed Bell Peppers": ["vegetarian", "gluten-free", "dairy-free"],
        "Eggplant Parmesan": ["vegetarian", "contains dairy"],
        "Shrimp Scampi": ["gluten-free", "contains dairy"],
        "Beef Stroganoff": ["contains gluten", "contains dairy"],
        "Chicken Teriyaki": ["gluten-free", "contains soy"],
        "Vegetarian Lasagna": ["vegetarian", "contains gluten", "contains dairy"],
        "Falafel Wraps": ["vegan", "gluten-free"],
        "Pork Schnitzel": ["contains gluten"],
        "Butternut Squash Risotto": ["vegetarian", "contains dairy"],
        "Chickpea Curry": ["vegan", "gluten-free", "dairy-free"],
        "Baked Ziti": ["vegetarian", "contains gluten", "contains dairy"],
        "Thai Red Curry": ["vegan", "gluten-free", "dairy-free"],
        "Chicken Parmesan": ["contains gluten", "contains dairy"],
        "Beef Tacos": ["contains gluten", "contains dairy"],
        "Grilled Portobello Mushrooms": ["vegan", "gluten-free"],
        "Sweet and Sour Chicken": ["contains gluten", "contains soy"],
        "Vegetable Korma": ["vegan", "gluten-free", "dairy-free"],
        "Turkey Meatballs": ["gluten-free"],
        "Spaghetti Bolognese": ["contains gluten", "contains dairy"],
        "Chicken Enchiladas": ["contains gluten", "contains dairy"],
        "Coconut Curry Shrimp": ["gluten-free", "contains dairy"],
        "Quinoa-Stuffed Eggplant": ["vegan", "gluten-free", "dairy-free"],
        "Mushroom Risotto": ["vegetarian", "contains dairy"],
        "BBQ Ribs": ["gluten-free"],
        "Vegetable Paella": ["vegan", "gluten-free"],
        "Pork Belly with Apples": ["contains gluten"],
        "Lamb Chops": ["gluten-free"],
        "Chicken Caesar Salad": ["contains gluten", "contains dairy"],
        "Beef Burritos": ["contains gluten", "contains dairy"],
        "Grilled Tuna Steak": ["gluten-free"],
        "Spinach and Ricotta Stuffed Chicken": ["contains dairy"],
        "Cajun Chicken Pasta": ["contains gluten"],
        "Thai Basil Beef": ["gluten-free"],
        "Vegetable Tempura": ["vegetarian", "contains gluten"],
        "Chicken Shawarma": ["gluten-free"],
        "Baked Falafel with Hummus": ["vegan", "gluten-free"],
        "Pork Fried Rice": ["contains gluten"],
        "Zucchini Noodles with Pesto": ["vegan", "gluten-free", "dairy-free"],
        "Balsamic Glazed Chicken": ["gluten-free"],
        "Stuffed Portobello Mushrooms": ["vegan", "gluten-free", "dairy-free"],
        "Lentil Shepherd's Pie": ["vegan", "gluten-free"],
        "Barbecue Chicken Pizza": ["contains gluten", "contains dairy"],
        "Beef Wellington": ["contains gluten", "contains dairy"],
    },
        "Drinks": {
        "Fruit Smoothie": ["vegan", "dairy-free", "low-sugar", "gluten-free"],
        "Iced Tea (Unsweetened)": ["gluten-free", "dairy-free", "low-sugar", "low-sodium"],
        "Mango Lassi (No Sugar)": ["vegetarian", "contains dairy", "gluten-free", "low-sugar"],
        "Green Juice": ["vegan", "gluten-free", "dairy-free"],
        "Coconut Water": ["vegan", "gluten-free", "dairy-free"],
        "Herbal Tea": ["vegan", "gluten-free", "dairy-free"],
        "Cold Brew Coffee": ["vegan", "gluten-free", "dairy-free"],
        "Hot Chocolate": ["vegetarian", "contains dairy"],
        "Lemonade": ["vegan", "gluten-free", "dairy-free"],
        "Chia Seed Drink": ["vegan", "gluten-free", "dairy-free"],
        "Almond Milk": ["vegan", "gluten-free", "low-sugar"],
        "Matcha Latte": ["vegetarian", "contains dairy"],
        "Ginger Ale": ["vegan", "gluten-free"],
        "Sparkling Water": ["vegan", "gluten-free", "dairy-free"],
        "Apple Cider": ["vegan", "gluten-free", "dairy-free"],
        "Berry Smoothie": ["vegan", "dairy-free", "low-sugar", "gluten-free"],
        "Pineapple Juice": ["vegan", "gluten-free", "dairy-free"],
        "Mint Mojito": ["vegan", "gluten-free"],
        "Cucumber Lemonade": ["vegan", "gluten-free", "dairy-free"],
        "Soy Milk": ["vegan", "gluten-free"],
        "Protein Shake": ["vegan", "dairy-free", "gluten-free"],
        "Iced Coffee": ["vegan", "gluten-free", "dairy-free"],
        "Orange Juice": ["vegan", "gluten-free", "dairy-free"],
        "Carrot Juice": ["vegan", "gluten-free", "dairy-free"],
        "Watermelon Juice": ["vegan", "gluten-free", "dairy-free"],
        "Tropical Punch": ["vegan", "gluten-free", "dairy-free"],
        "Raspberry Lemonade": ["vegan", "gluten-free", "dairy-free"],
        "Kombucha": ["vegan", "gluten-free", "dairy-free"],
        "Lavender Lemonade": ["vegan", "gluten-free", "dairy-free"],
        "Berry Infused Water": ["vegan", "gluten-free", "dairy-free"],
        "Peach Iced Tea": ["vegan", "gluten-free"],
        "Hibiscus Tea": ["vegan", "gluten-free", "dairy-free"],
        "Apple Mint Cooler": ["vegan", "gluten-free", "dairy-free"],
        "Cherry Juice": ["vegan", "gluten-free", "dairy-free"],
        "Coconut Milkshake": ["vegetarian", "contains dairy"],
        "Ginger Lemon Tea": ["vegan", "gluten-free"],
        "Tamarind Drink": ["vegan", "gluten-free", "dairy-free"],
        "Cinnamon Apple Cider": ["vegan", "gluten-free"],
        "Blueberry Smoothie": ["vegan", "dairy-free", "low-sugar", "gluten-free"],
        "Strawberry Banana Smoothie": ["vegan", "dairy-free", "low-sugar", "gluten-free"],
        "Coconut Pineapple Juice": ["vegan", "gluten-free", "dairy-free"],
        "Cranberry Juice": ["vegan", "gluten-free", "dairy-free"],
        "Lemon Basil Soda": ["vegan", "gluten-free"],
        "Sweetened Almond Milk": ["vegan", "gluten-free"],
        "Matcha Smoothie": ["vegan", "dairy-free", "gluten-free"],
        "Iced Matcha Latte": ["vegetarian", "contains dairy"],
        "Spiced Chai": ["vegetarian", "contains dairy"],
        "Peach Smoothie": ["vegan", "dairy-free", "low-sugar", "gluten-free"],
        "Papaya Juice": ["vegan", "gluten-free", "dairy-free"],
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
                st.success("Your order has been placed!")
        else:
            st.write("Your cart is empty.")

    elif menu_option == "Track Order":
        if st.session_state.order_placed:
            st.write("Tracking your order...")
            for status in order_status:
                st.write(f"Status: {status}")
                time.sleep(2)
        else:
            st.write("No orders placed yet.")

    elif menu_option == "Favorites":
        st.write("Your Favorites:")
        if st.session_state.favorites:
            for item in st.session_state.favorites:
                st.write(f"- {item}")
        else:
            st.write("No favorite items yet.")

    elif menu_option == "Feedback":
        st.write("Submit Feedback")
        feedback_text = st.text_area("Your Feedback")
        if st.button("Submit Feedback"):
            if st.session_state.authenticated:
                username = st.session_state.username  # Use the logged-in username
                conn = sqlite3.connect('feedback.db')
                c = conn.cursor()
                c.execute('''CREATE TABLE IF NOT EXISTS feedback
                             (username TEXT, feedback TEXT)''')
                c.execute('INSERT INTO feedback (username, feedback) VALUES (?, ?)',
                          (username, feedback_text))
                conn.commit()
                conn.close()
                st.success("Thank you for your feedback!")
            else:
                st.error("You need to log in to submit feedback.")

elif st.session_state.page == "AdminDashboard":
    if not st.session_state.authenticated or not st.session_state.admin:
        st.session_state.page = "Login"
    
    st.header("Admin Dashboard")
    
    # Display feedback from users
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute('SELECT username, feedback FROM feedback')
    feedback = c.fetchall()
    conn.close()
    
    st.subheader("User Feedback")
    if feedback:
        for user_feedback in feedback:
            st.write(f"User: {user_feedback[0]}")
            st.write(f"Feedback: {user_feedback[1]}")
            st.write("---")
    else:
        st.write("No feedback yet.")
    
    # Display all users
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT username FROM users WHERE role = ?', ('user',))
    users = c.fetchall()
    conn.close()
    
    st.subheader("Registered Users")
    if users:
        for user in users:
            st.write(f"User: {user[0]}")
            st.write("---")
    else:
        st.write("No registered users.")

    # Display user orders
    st.subheader("User Orders")
    # Simulated orders, replace with actual order data
    st.write("This section will display order history for users.")

if st.session_state.authenticated:
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.page = "Login"
        st.session_state.cart = []
        st.session_state.order_placed = False
        st.session_state.favorites = []
        st.session_state.admin = False
        st.session_state.username = None
