import firebase_admin
from firebase_admin import credentials, firestore
import os

firebase_path = os.path.join(os.getcwd(), "firebase_key.json")

cred = credentials.Certificate(firebase_path)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

print("Firebase connected successfully")
print("Project ID:", cred.project_id)