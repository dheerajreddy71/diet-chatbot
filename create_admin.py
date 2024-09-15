import sqlite3
from hashlib import sha256

def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Connect to SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Define admin credentials
admin_username = "admin"
admin_password = "admin123"  # Use a strong password in production

# Check if the admin account already exists
c.execute('SELECT * FROM users WHERE username = ?', (admin_username,))
admin_exists = c.fetchone()

if not admin_exists:
    # Insert admin account if it doesn't exist
    c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
              (admin_username, hash_password(admin_password), "admin"))
    conn.commit()
    print("Admin account created successfully.")
else:
    print("Admin account already exists.")

# Close the database connection
conn.close()
