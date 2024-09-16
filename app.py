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
st.title("Food Ordering System")

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
        "Chocolate Lava Cake": ["vegetarian", "contains gluten", "contains dairy"],
        "Cheesecake": ["vegetarian", "contains gluten", "contains dairy"],
        "Tiramisu": ["vegetarian", "contains gluten", "contains dairy"],
        "Apple Pie": ["vegetarian", "contains gluten", "contains dairy"],
        "Brownies": ["vegetarian", "contains gluten", "contains dairy"],
        "Lemon Bars": ["vegetarian", "contains gluten", "contains dairy"],
        "Panna Cotta": ["vegetarian", "contains gluten", "contains dairy"],
        "Baklava": ["vegetarian", "contains gluten", "contains dairy"],
        "Pavlova": ["vegetarian", "contains gluten", "contains dairy"],
        "Crème Brûlée": ["vegetarian", "contains gluten", "contains dairy"],
        "Mango Sticky Rice": ["vegan", "gluten-free", "dairy-free"],
        "Fruit Sorbet": ["vegan", "gluten-free", "dairy-free"],
        "Vegan Chocolate Cake": ["vegan", "contains gluten"],
        "Chia Pudding": ["vegan", "gluten-free", "dairy-free"],
        "Coconut Macaroons": ["vegan", "gluten-free"],
        "Almond Cake": ["vegetarian", "contains gluten", "contains dairy"],
        "Peach Cobbler": ["vegetarian", "contains gluten", "contains dairy"],
        "Rice Pudding": ["vegetarian", "contains gluten", "contains dairy"],
        "Tapioca Pudding": ["vegetarian", "contains gluten", "contains dairy"],
        "Key Lime Pie": ["vegetarian", "contains gluten", "contains dairy"],
        "Popsicles": ["vegan", "gluten-free", "dairy-free"],
        "Apple Crisp": ["vegetarian", "contains gluten", "contains dairy"],
        "Pumpkin Pie": ["vegetarian", "contains gluten", "contains dairy"],
        "Matcha Green Tea Cake": ["vegetarian", "contains gluten", "contains dairy"],
        "Coconut Cream Pie": ["vegetarian", "contains gluten", "contains dairy"],
        "Lava Cake": ["vegetarian", "contains gluten", "contains dairy"],
        "Carrot Cake": ["vegetarian", "contains gluten", "contains dairy"],
        "Gelato": ["vegetarian", "contains gluten", "contains dairy"],
        "Rice Krispie Treats": ["vegetarian", "contains gluten", "contains dairy"],
        "Cinnamon Rolls": ["vegetarian", "contains gluten", "contains dairy"],
        "Strawberry Shortcake": ["vegetarian", "contains gluten", "contains dairy"],
        "Fruit Tart": ["vegetarian", "contains gluten", "contains dairy"],
        "Chocolate Mousse": ["vegetarian", "contains gluten", "contains dairy"],
        "Bread Pudding": ["vegetarian", "contains gluten", "contains dairy"],
        "Blueberry Muffins": ["vegetarian", "contains gluten", "contains dairy"],
        "Lemon Meringue Pie": ["vegetarian", "contains gluten", "contains dairy"],
        "Black Forest Cake": ["vegetarian", "contains gluten", "contains dairy"],
        "Raspberry Cheesecake Bars": ["vegetarian", "contains gluten", "contains dairy"],
        "Chocolate Chip Cookies": ["vegetarian", "contains gluten", "contains dairy"],
        "Sweet Potato Pie": ["vegetarian", "contains gluten", "contains dairy"],
        "Coconut Panna Cotta": ["vegetarian", "gluten-free", "dairy-free"],
        "Vegan Cookies": ["vegan", "gluten-free"],
        "Raisin Bran Muffins": ["vegetarian", "contains gluten", "contains dairy"],
        "Toffee Bars": ["vegetarian", "contains gluten", "contains dairy"],
        "Fig Bars": ["vegetarian", "contains gluten", "contains dairy"],
        "Mango Sorbet": ["vegan", "gluten-free", "dairy-free"],
        "Apple Cinnamon Donuts": ["vegetarian", "contains gluten", "contains dairy"],
        "Coconut Banana Bread": ["vegetarian", "contains gluten", "contains dairy"],
        "Apricot Almond Cake": ["vegetarian", "contains gluten", "contains dairy"],
        "Orange Almond Cake": ["vegetarian", "contains gluten", "contains dairy"],
        "Churros": ["vegetarian", "contains gluten", "contains dairy"],
        "S'mores Bars": ["vegetarian", "contains gluten", "contains dairy"],
        "Raspberry Sorbet": ["vegan", "gluten-free", "dairy-free"],
    },  "Drinks": {
        "Mango Smoothie": ["contains dairy"],
        "Berry Blast": ["vegan"],
        "Orange Juice": ["vegan"],
        "Pineapple Coconut Smoothie": ["vegan"],
        "Strawberry Banana Smoothie": ["contains dairy"],
        "Green Juice": ["vegan"],
        "Blueberry Almond Smoothie": ["vegan"],
        "Carrot Ginger Juice": ["vegan"],
        "Apple Cider": ["vegan"],
        "Watermelon Juice": ["vegan"],
        "Avocado Smoothie": ["contains dairy"],
        "Almond Milk Smoothie": ["vegan"],
        "Peach Smoothie": ["vegan"],
        "Pomegranate Juice": ["vegan"],
        "Cucumber Mint Juice": ["vegan"],
        "Grapefruit Juice": ["vegan"],
        "Papaya Smoothie": ["vegan"],
        "Lemon Ginger Detox Juice": ["vegan"],
        "Berry Citrus Smoothie": ["vegan"],
        "Kiwi Mango Juice": ["vegan"],
        "Coconut Water": ["vegan"],
        "Chocolate Banana Smoothie": ["contains dairy"],
        "Green Apple Juice": ["vegan"],
        "Dragon Fruit Smoothie": ["vegan"],
        "Pear and Spinach Smoothie": ["vegan"],
        "Cantaloupe Juice": ["vegan"],
        "Apple and Beetroot Juice": ["vegan"],
        "Berry Yogurt Smoothie": ["contains dairy"],
        "Mango Pineapple Juice": ["vegan"],
        "Sweet Potato Smoothie": ["vegan"],
        "Pina Colada Smoothie": ["contains dairy"],
        "Raspberry Lime Juice": ["vegan"],
        "Tropical Fruit Punch": ["vegan"],
        "Watermelon Mint Juice": ["vegan"],
        "Beet and Carrot Juice": ["vegan"],
        "Tropical Green Smoothie": ["vegan"],
        "Cherry Smoothie": ["vegan"],
        "Ginger Peach Juice": ["vegan"],
        "Apricot Juice": ["vegan"],
        "Matcha Latte": ["contains dairy"],
        "Ginger Lemonade": ["vegan"],
        "Kiwi Lime Juice": ["vegan"],
        "Lavender Lemonade": ["vegan"],
        "Coconut Matcha Smoothie": ["contains dairy"],
        "Peach Lemonade": ["vegan"]
    },
    "Desserts": {
        "Chocolate Lava Cake": ["contains dairy", "contains gluten"],
        "Vanilla Cheesecake": ["contains dairy", "contains gluten"],
        "Apple Pie": ["contains dairy", "contains gluten"],
        "Lemon Meringue Pie": ["contains dairy", "contains gluten"],
        "Tiramisu": ["contains dairy", "contains gluten"],
        "Strawberry Shortcake": ["contains dairy", "contains gluten"],
        "Brownies": ["contains dairy", "contains gluten"],
        "Panna Cotta": ["contains dairy"],
        "Fruit Tart": ["contains gluten"],
        "Carrot Cake": ["contains dairy", "contains gluten"],
        "Cheesecake Brownies": ["contains dairy", "contains gluten"],
        "Chocolate Mousse": ["contains dairy"],
        "Creme Brulee": ["contains dairy"],
        "Peach Cobbler": ["contains dairy", "contains gluten"],
        "Raspberry Sorbet": ["vegan"],
        "Pavlova": ["contains dairy"],
        "Mango Sticky Rice": ["vegan"],
        "Chocolate Chip Cookies": ["contains dairy", "contains gluten"],
        "Lemon Bars": ["contains dairy", "contains gluten"],
        "Almond Cake": ["contains dairy", "contains gluten"],
        "Coconut Macaroons": ["contains gluten"],
        "Rice Pudding": ["contains dairy"],
        "Baked Apples": ["vegan"],
        "Apple Crisp": ["contains dairy", "contains gluten"],
        "Chocolate Covered Strawberries": ["contains dairy"],
        "Pumpkin Pie": ["contains dairy", "contains gluten"],
        "Key Lime Pie": ["contains dairy", "contains gluten"],
        "Coconut Panna Cotta": ["vegan"],
        "Berry Parfait": ["contains dairy"],
        "Chocolate Fondue": ["contains dairy"],
        "Peach Melba": ["contains dairy"],
        "Baked Pears": ["vegan"],
        "Raisin Cookies": ["contains dairy", "contains gluten"],
        "Blueberry Muffins": ["contains dairy", "contains gluten"],
        "Tiramisu Cupcakes": ["contains dairy", "contains gluten"],
        "Cherry Clafoutis": ["contains dairy", "contains gluten"],
        "Coconut Ice Cream": ["contains dairy"],
        "Fruit Sorbet": ["vegan"],
        "Gingerbread Cookies": ["contains dairy", "contains gluten"],
        "Almond Croissants": ["contains dairy", "contains gluten"],
        "Chocolate Tiramisu": ["contains dairy", "contains gluten"],
        "Pistachio Ice Cream": ["contains dairy"],
        "Matcha Cheesecake": ["contains dairy"]
    },
    "Appetizers": {
        "Bruschetta": ["vegetarian", "contains gluten"],
        "Stuffed Mushrooms": ["vegetarian"],
        "Deviled Eggs": ["contains dairy"],
        "Spring Rolls": ["vegan"],
        "Garlic Knots": ["contains gluten"],
        "Stuffed Jalapenos": ["vegetarian"],
        "Spinach Artichoke Dip": ["vegetarian", "contains dairy"],
        "Cucumber Sandwiches": ["vegetarian"],
        "Chicken Satay": ["contains gluten"],
        "Cheese Platter": ["contains dairy"],
        "Hummus with Pita": ["vegan"],
        "Chicken Wings": ["contains gluten"],
        "Pigs in a Blanket": ["contains gluten"],
        "Falafel": ["vegan"],
        "Bruschetta with Tomato": ["vegetarian", "contains gluten"],
        "Caprese Skewers": ["vegetarian"],
        "Mini Quiches": ["contains dairy"],
        "Stuffed Grape Leaves": ["vegan"],
        "Cheese and Crackers": ["contains dairy"],
        "Vegetable Samosas": ["vegan"],
        "Olive Tapenade": ["vegan"],
        "Jalapeno Poppers": ["contains gluten"],
        "Zucchini Fritters": ["vegetarian"],
        "Artichoke Dip": ["vegetarian", "contains dairy"],
        "Cheese Stuffed Meatballs": ["contains dairy"],
        "Spring Roll Wrappers": ["vegan"],
        "Crispy Chickpeas": ["vegan"],
        "Garlic Parmesan Pretzels": ["contains gluten"],
        "Sweet Potato Fries": ["vegan"],
        "Mini Tacos": ["contains gluten"],
        "Antipasto Platter": ["vegetarian"],
        "Caprese Salad Skewers": ["vegetarian"],
        "Buffalo Cauliflower Bites": ["vegan"],
        "Pita Bread with Tzatziki": ["vegetarian"],
        "Stuffed Pita Pockets": ["vegan"],
        "Cheese Fondue": ["contains dairy"],
        "Vegetable Spring Rolls": ["vegan"],
        "Mini Quesadillas": ["contains dairy"]
    },
    "Soups": {
        "Tomato Basil Soup": ["vegan", "gluten-free"],
        "Minestrone Soup": ["vegan", "gluten-free"],
        "Chicken Noodle Soup": ["contains gluten"],
        "Lentil Soup": ["vegan", "gluten-free"],
        "Butternut Squash Soup": ["vegan", "gluten-free"],
        "Clam Chowder": ["contains dairy", "contains gluten"],
        "Vegetable Soup": ["vegan", "gluten-free"],
        "Mushroom Soup": ["vegetarian", "contains dairy"],
        "Chicken Tortilla Soup": ["contains gluten"],
        "Corn Chowder": ["contains dairy", "contains gluten"],
        "Split Pea Soup": ["vegan", "gluten-free"],
        "Beef Barley Soup": ["contains gluten"],
        "Sweet Potato Soup": ["vegan", "gluten-free"],
        "Gazpacho": ["vegan", "gluten-free"],
        "French Onion Soup": ["contains dairy"],
        "Carrot Ginger Soup": ["vegan", "gluten-free"],
        "Pumpkin Soup": ["vegan", "gluten-free"],
        "Creamy Tomato Soup": ["contains dairy"],
        "Cauliflower Soup": ["vegan", "gluten-free"],
        "Spicy Black Bean Soup": ["vegan", "gluten-free"],
        "Thai Coconut Soup": ["vegan", "gluten-free"],
        "Potato Leek Soup": ["vegetarian", "contains dairy"],
        "Green Pea Soup": ["vegan", "gluten-free"],
        "Barley Vegetable Soup": ["vegan", "gluten-free"],
        "Broccoli Cheddar Soup": ["contains dairy"],
        "Chicken and Rice Soup": ["contains gluten"],
        "Roasted Red Pepper Soup": ["vegan", "gluten-free"],
        "Cream of Asparagus Soup": ["contains dairy"],
        "Zucchini Soup": ["vegan", "gluten-free"],
        "Lobster Bisque": ["contains dairy", "contains gluten"],
        "Potato Soup": ["contains dairy"],
        "Kale Soup": ["vegan", "gluten-free"],
        "Spicy Tomato Soup": ["vegan", "gluten-free"],
        "Cabbage Soup": ["vegan", "gluten-free"],
        "Wild Mushroom Soup": ["vegetarian", "contains dairy"],
        "Pea and Mint Soup": ["vegan", "gluten-free"],
        "Sichuan Hot & Sour Soup": ["vegan", "contains gluten"],
        "Italian Wedding Soup": ["contains gluten"],
        "Sweet Corn Soup": ["vegan", "gluten-free"],
        "Red Lentil Soup": ["vegan", "gluten-free"]
    },
        "Sides": {
        "Garlic Mashed Potatoes": ["contains dairy"],
        "Roasted Vegetables": ["vegan", "gluten-free"],
        "French Fries": ["vegan", "gluten-free"],
        "Rice Pilaf": ["vegan", "gluten-free"],
        "Steamed Asparagus": ["vegan", "gluten-free"],
        "Coleslaw": ["vegetarian"],
        "Sweet Potato Fries": ["vegan", "gluten-free"],
        "Crispy Brussels Sprouts": ["vegan", "gluten-free"],
        "Baked Beans": ["vegan"],
        "Corn on the Cob": ["vegan", "gluten-free"],
        "Garlic Bread": ["vegetarian", "contains gluten"],
        "Macaroni and Cheese": ["contains dairy"],
        "Grilled Zucchini": ["vegan", "gluten-free"],
        "Cucumber Salad": ["vegan", "gluten-free"],
        "Roasted Sweet Potatoes": ["vegan", "gluten-free"],
        "Quinoa Salad": ["vegan", "gluten-free"],
        "Hush Puppies": ["contains gluten"],
        "Potato Wedges": ["vegan", "gluten-free"],
        "Vegetable Stir-Fry": ["vegan"],
        "Cheese Sticks": ["contains dairy", "contains gluten"]
    },
    "Sauces & Condiments": {
        "Ketchup": ["vegan", "gluten-free"],
        "Mustard": ["vegan", "gluten-free"],
        "Mayonnaise": ["contains dairy"],
        "Ranch Dressing": ["contains dairy"],
        "Barbecue Sauce": ["vegan"],
        "Hot Sauce": ["vegan", "gluten-free"],
        "Soy Sauce": ["vegan", "contains gluten"],
        "Salsa": ["vegan", "gluten-free"],
        "Guacamole": ["vegan"],
        "Tzatziki": ["contains dairy"],
        "Hummus": ["vegan"],
        "Pesto": ["contains dairy, nuts"],
        "Buffalo Sauce": ["vegan"],
        "Chimichurri": ["vegan"],
        "Balsamic Vinaigrette": ["vegan"],
        "Raspberry Vinaigrette": ["vegan"],
        "Teriyaki Sauce": ["vegan", "contains gluten"],
        "Cranberry Sauce": ["vegan"],
        "Aioli": ["contains dairy"],
        "Sriracha": ["vegan", "gluten-free"]
    },
    "Sandwiches & Wraps": {
        "Chicken Caesar Wrap": ["contains dairy"],
        "Turkey Club Sandwich": ["contains gluten"],
        "Vegetarian Panini": ["vegetarian", "contains gluten"],
        "Grilled Cheese Sandwich": ["contains dairy", "contains gluten"],
        "Falafel Wrap": ["vegan"],
        "Chicken Shawarma Wrap": ["contains gluten"],
        "BLT Sandwich": ["contains gluten"],
        "Caprese Sandwich": ["vegetarian", "contains gluten"],
        "Roast Beef Sandwich": ["contains gluten"],
        "Veggie Wrap": ["vegan"],
        "Turkey & Avocado Sandwich": ["contains gluten"],
        "Pastrami on Rye": ["contains gluten"],
        "Buffalo Chicken Wrap": ["contains gluten"],
        "Mushroom & Swiss Sandwich": ["vegetarian", "contains gluten", "contains dairy"],
        "Grilled Veggie Wrap": ["vegan"],
        "BBQ Pulled Pork Sandwich": ["contains gluten"],
        "Hummus & Veggie Wrap": ["vegan"],
        "Tuna Salad Sandwich": ["contains gluten"],
        "Egg Salad Sandwich": ["contains gluten", "contains dairy"],
        "Greek Salad Wrap": ["vegan"]
    },
    "Pasta": {
        "Spaghetti Bolognese": ["contains gluten"],
        "Fettuccine Alfredo": ["contains dairy"],
        "Penne Arrabbiata": ["vegan"],
        "Lasagna": ["contains dairy", "contains gluten"],
        "Macaroni and Cheese": ["contains dairy"],
        "Pesto Pasta": ["contains dairy"],
        "Ratatouille Pasta": ["vegan"],
        "Carbonara": ["contains dairy", "contains gluten"],
        "Stuffed Shells": ["contains dairy"],
        "Seafood Pasta": ["contains gluten"],
        "Baked Ziti": ["contains dairy", "contains gluten"],
        "Vegan Pasta Primavera": ["vegan"],
        "Pasta with Marinara Sauce": ["vegan"],
        "Mushroom Risotto": ["contains dairy"],
        "Pasta Puttanesca": ["vegan"],
        "Sweet Potato Pasta": ["vegan"],
        "Butternut Squash Pasta": ["vegan"],
        "Cacio e Pepe": ["contains dairy"],
        "Lemon Garlic Pasta": ["vegan"],
        "Eggplant Pasta": ["vegan"]
    },
    "Pizza": {
        "Margherita Pizza": ["vegetarian"],
        "Pepperoni Pizza": ["contains gluten"],
        "Vegetarian Pizza": ["vegetarian"],
        "BBQ Chicken Pizza": ["contains gluten"],
        "Hawaiian Pizza": ["contains gluten"],
        "Mushroom Pizza": ["vegetarian"],
        "Four Cheese Pizza": ["contains dairy"],
        "Veggie Supreme Pizza": ["vegetarian"],
        "Meat Lover's Pizza": ["contains gluten"],
        "Pesto Pizza": ["vegetarian", "contains dairy"],
        "Greek Pizza": ["vegetarian"],
        "White Pizza": ["contains dairy"],
        "Buffalo Chicken Pizza": ["contains gluten"],
        "Spinach & Artichoke Pizza": ["vegetarian"],
        "Sausage & Peppers Pizza": ["contains gluten"],
        "Margherita Flatbread": ["vegetarian"],
        "Pineapple & Ham Pizza": ["contains gluten"],
        "Roasted Vegetable Pizza": ["vegetarian"],
        "Chorizo Pizza": ["contains gluten"],
        "Tomato & Basil Pizza": ["vegetarian"],
        "Zucchini & Goat Cheese Pizza": ["vegetarian", "contains dairy"]
    },
    "Seafood": {
        "Grilled Salmon": ["gluten-free"],
        "Shrimp Scampi": ["contains gluten"],
        "Crab Cakes": ["contains gluten"],
        "Fish Tacos": ["contains gluten"],
        "Seafood Paella": ["contains gluten"],
        "Baked Cod": ["gluten-free"],
        "Clam Chowder": ["contains dairy", "contains gluten"],
        "Mussels in White Wine Sauce": ["contains dairy"],
        "Lobster Roll": ["contains gluten"],
        "Garlic Butter Shrimp": ["gluten-free"],
        "Tuna Steak": ["gluten-free"],
        "Oysters Rockefeller": ["contains dairy"],
        "Grilled Swordfish": ["gluten-free"],
        "Sushi Rolls": ["contains gluten"],
        "Seafood Alfredo": ["contains dairy", "contains gluten"],
        "Shrimp Fried Rice": ["contains gluten"],
        "Salmon Tartare": ["gluten-free"],
        "Crab Legs": ["gluten-free"],
        "Scallops in Lemon Butter Sauce": ["contains dairy"],
        "Prawn Curry": ["vegan"],
        "Octopus Salad": ["gluten-free"]
    },
    "Burgers": {
        "Classic Cheeseburger": ["contains dairy"],
        "Bacon Burger": ["contains gluten"],
        "Veggie Burger": ["vegan"],
        "BBQ Burger": ["contains gluten"],
        "Mushroom Swiss Burger": ["contains dairy"],
        "Chicken Burger": ["contains gluten"],
        "Bison Burger": ["contains gluten"],
        "Black Bean Burger": ["vegan"],
        "Turkey Burger": ["contains gluten"],
        "Sliders": ["contains gluten"],
        "Beef Burger": ["contains gluten"],
        "Fish Burger": ["contains gluten"],
        "Lamb Burger": ["contains gluten"],
        "Portobello Burger": ["vegan"],
        "Greek Burger": ["contains gluten"],
        "Avocado Burger": ["contains gluten"],
        "Jalapeno Burger": ["contains gluten"],
        "Hawaiian Burger": ["contains gluten"],
        "Pork Burger": ["contains gluten"],
        "BBQ Pulled Pork Burger": ["contains gluten"]
    },
    "Breakfast Items": {
        "Pancakes": ["contains dairy", "contains gluten"],
        "French Toast": ["contains dairy", "contains gluten"],
        "Omelette": ["contains dairy"],
        "Avocado Toast": ["vegan"],
        "Bagel with Cream Cheese": ["contains dairy", "contains gluten"],
        "Breakfast Burrito": ["contains gluten"],
        "Granola with Yogurt": ["contains dairy"],
        "Smoothie Bowl": ["vegan"],
        "Eggs Benedict": ["contains dairy", "contains gluten"],
        "Breakfast Sandwich": ["contains gluten", "contains dairy"],
        "Chia Pudding": ["vegan"],
        "Fruit Salad": ["vegan"],
        "Breakfast Quesadilla": ["contains dairy", "contains gluten"],
        "Tofu Scramble": ["vegan"],
        "Muffins": ["contains dairy", "contains gluten"],
        "Breakfast Parfait": ["contains dairy"],
        "Egg & Cheese Croissant": ["contains dairy", "contains gluten"],
        "Breakfast Pizza": ["contains gluten", "contains dairy"],
        "Waffles": ["contains dairy", "contains gluten"],
        "Overnight Oats": ["vegan"]
    },
    "Smoothies & Juices": {
        "Mango Smoothie": ["contains dairy"],
        "Green Juice": ["vegan"],
        "Berry Smoothie": ["vegan"],
        "Orange Juice": ["vegan"],
        "Strawberry Banana Smoothie": ["contains dairy"],
        "Carrot Juice": ["vegan"],
        "Pineapple Smoothie": ["vegan"],
        "Beet Juice": ["vegan"],
        "Apple Smoothie": ["vegan"],
        "Ginger Juice": ["vegan"],
        "Kiwi Smoothie": ["vegan"],
        "Watermelon Juice": ["vegan"],
        "Blueberry Smoothie": ["vegan"],
        "Cucumber Juice": ["vegan"],
        "Tropical Smoothie": ["vegan"],
        "Spinach Smoothie": ["vegan"],
        "Lemonade": ["vegan"],
        "Peach Juice": ["vegan"],
        "Raspberry Smoothie": ["vegan"],
        "Tomato Juice": ["vegan"],
        "Avocado Smoothie": ["contains dairy"]
    },
    "Healthy Options": {
        "Quinoa Salad": ["vegan", "gluten-free"],
        "Grilled Chicken Salad": ["gluten-free"],
        "Vegan Buddha Bowl": ["vegan"],
        "Greek Yogurt with Honey": ["contains dairy"],
        "Vegetable Stir-Fry": ["vegan"],
        "Fruit Smoothie": ["vegan"],
        "Chia Seed Pudding": ["vegan"],
        "Avocado Toast": ["vegan"],
        "Spinach and Feta Salad": ["contains dairy"],
        "Sweet Potato and Black Bean Bowl": ["vegan"],
        "Hummus with Veggies": ["vegan"],
        "Salmon Salad": ["gluten-free"],
        "Roasted Chickpeas": ["vegan"],
        "Cucumber and Tomato Salad": ["vegan"],
        "Almond Butter Banana Toast": ["vegan"],
        "Kale Salad": ["vegan"],
        "Grilled Tofu Salad": ["vegan"],
        "Berry Parfait": ["contains dairy"],
        "Stuffed Bell Peppers": ["vegan"],
        "Lentil Soup": ["vegan"]
    },
    "Specialty Items": {
        "Lobster Mac and Cheese": ["contains dairy"],
        "Duck Confit": ["contains gluten"],
        "Truffle Risotto": ["contains dairy"],
        "Beef Wellington": ["contains gluten"],
        "Foie Gras": ["contains gluten"],
        "Seafood Paella": ["contains gluten"],
        "Rack of Lamb": ["contains gluten"],
        "Spaghetti Carbonara": ["contains dairy", "contains gluten"],
        "Chateaubriand": ["contains gluten"],
        "Braised Short Ribs": ["contains gluten"],
        "Crab Cakes": ["contains gluten"],
        "Miso Glazed Salmon": ["gluten-free"],
        "Stuffed Portobello Mushrooms": ["vegetarian"],
        "Sushi Platter": ["contains gluten"],
        "Osso Buco": ["contains gluten"],
        "Beef Tenderloin": ["contains gluten"],
        "Lobster Roll": ["contains gluten"],
        "Duck Breast": ["contains gluten"],
        "Caviar": ["gluten-free"],
        "Truffle Oil Pasta": ["contains dairy"]
    },
    "Kids’ Menu": {
        "Chicken Tenders": ["contains gluten"],
        "Mac and Cheese": ["contains dairy"],
        "Mini Burgers": ["contains gluten"],
        "Pizza Bites": ["contains gluten"],
        "Grilled Cheese Sandwich": ["contains dairy", "contains gluten"],
        "Hot Dogs": ["contains gluten"],
        "Fruit Kabobs": ["vegan"],
        "Cheese Quesadilla": ["contains dairy", "contains gluten"],
        "Chicken Nuggets": ["contains gluten"],
        "Mini Pancakes": ["contains dairy", "contains gluten"],
        "Spaghetti with Marinara Sauce": ["vegan"],
        "Veggie Sticks with Hummus": ["vegan"],
        "Mac and Cheese Bites": ["contains dairy", "contains gluten"],
        "Peanut Butter and Jelly Sandwich": ["contains gluten"],
        "Mini Corn Dogs": ["contains gluten"],
        "Cheese Pizza": ["contains dairy", "contains gluten"],
        "Fruit Smoothie": ["vegan"],
        "Kids’ Burrito": ["contains gluten"],
        "Chicken Wrap": ["contains gluten"],
        "Mini Tacos": ["contains gluten"]
    },
    "Appetizer Platter": {
        "Bruschetta": ["vegetarian", "contains gluten"],
        "Stuffed Mushrooms": ["vegetarian"],
        "Spring Rolls": ["vegan"],
        "Hummus with Pita": ["vegan"],
        "Falafel": ["vegan"],
        "Caprese Skewers": ["vegetarian"],
        "Cheese Platter": ["contains dairy"],
        "Vegetable Samosas": ["vegan"],
        "Olive Tapenade": ["vegan"],
        "Antipasto Platter": ["vegetarian"],
        "Buffalo Cauliflower Bites": ["vegan"],
        "Mini Quiches": ["contains dairy"],
        "Garlic Knots": ["contains gluten"],
        "Cheese and Crackers": ["contains dairy"],
        "Stuffed Jalapenos": ["vegetarian"],
        "Cucumber Sandwiches": ["vegetarian"],
        "Chicken Satay": ["contains gluten"],
        "Bruschetta with Tomato": ["vegetarian", "contains gluten"],
        "Vegetable Spring Rolls": ["vegan"],
        "Mini Tacos": ["contains gluten"],
        "Cheese Fondue": ["contains dairy"]
    },
    "Breads & Pastries": {
        "Croissants": ["contains dairy", "contains gluten"],
        "Bagels": ["contains gluten"],
        "Muffins": ["contains dairy", "contains gluten"],
        "Scones": ["contains dairy", "contains gluten"],
        "Baguette": ["contains gluten"],
        "Danish Pastries": ["contains dairy", "contains gluten"],
        "Ciabatta Bread": ["contains gluten"],
        "Focaccia": ["contains gluten"],
        "Brioche": ["contains dairy", "contains gluten"],
        "English Muffins": ["contains gluten"],
        "Pita Bread": ["contains gluten"],
        "Pain au Chocolat": ["contains dairy", "contains gluten"],
        "Whole Wheat Bread": ["contains gluten"],
        "Brioche Buns": ["contains dairy", "contains gluten"],
        "Flatbread": ["contains gluten"],
        "Rosemary Olive Oil Bread": ["contains gluten"],
        "Cinnamon Rolls": ["contains dairy", "contains gluten"],
        "Apple Cinnamon Muffins": ["contains dairy", "contains gluten"],
        "Pumpkin Bread": ["contains dairy", "contains gluten"],
        "Chocolate Croissants": ["contains dairy", "contains gluten"],
        "Almond Croissants": ["contains dairy", "contains gluten"]
    },
    "Beverages": {
        "Coffee": ["vegan"],
        "Tea": ["vegan"],
        "Iced Coffee": ["vegan"],
        "Hot Chocolate": ["contains dairy"],
        "Lemonade": ["vegan"],
        "Milkshakes": ["contains dairy"],
        "Smoothies": ["vegan"],
        "Soft Drinks": ["vegan"],
        "Sparkling Water": ["vegan"],
        "Fruit Juices": ["vegan"],
        "Herbal Tea": ["vegan"],
        "Iced Tea": ["vegan"],
        "Hot Cider": ["contains dairy"],
        "Matcha Latte": ["contains dairy"],
        "Golden Milk": ["contains dairy"],
        "Protein Shake": ["contains dairy"],
        "Kombucha": ["vegan"],
        "Coconut Water": ["vegan"],
        "Milk Alternatives": ["vegan"],
        "Cocktails": ["varies"],
        "Mocktails": ["vegan"]
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
