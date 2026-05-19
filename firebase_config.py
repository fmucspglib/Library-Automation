import firebase_admin
from firebase_admin import credentials, firestore

# Path to JSON key file
cred = credentials.Certificate("C:\library-automation\Firebase_key.json")

# Initialize Firebase
firebase_admin.initialize_app(cred)

db = firestore.client()

print("Firebase Connected Successfully!")