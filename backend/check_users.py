from database import Database
import hashlib

db = Database()

print("=== Current Users in Database ===")
for user in db.users.find():
    print(f"\nUsername: {user['username']}")
    print(f"Role: {user['role']}")
    print(f"Password hash: {user['password'][:20]}...")

print("\n=== Testing Login ===")
# Test admin login
result = db.verify_user("admin", "admin123")
if result:
    print("✓ admin/admin123 - Login successful!")
else:
    print("✗ admin/admin123 - Login failed!")

# Test user login  
result = db.verify_user("user", "user123")
if result:
    print("✓ user/user123 - Login successful!")
else:
    print("✗ user/user123 - Login failed!")

print("\n=== Password Hash Check ===")
expected_admin = hashlib.sha256("admin123".encode()).hexdigest()
expected_user = hashlib.sha256("user123".encode()).hexdigest()

admin_user = db.users.find_one({"username": "admin"})
user_user = db.users.find_one({"username": "user"})

print(f"Expected admin123 hash: {expected_admin}")
print(f"Actual admin hash:      {admin_user['password'] if admin_user else 'NOT FOUND'}")
print(f"Match: {expected_admin == admin_user['password'] if admin_user else False}")

print(f"\nExpected user123 hash: {expected_user}")
print(f"Actual user hash:      {user_user['password'] if user_user else 'NOT FOUND'}")
print(f"Match: {expected_user == user_user['password'] if user_user else False}")
