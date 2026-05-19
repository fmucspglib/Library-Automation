import os
import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    if os.getenv("RENDER"):
        cred = credentials.Certificate("/etc/secrets/firebase_key.json")
    else:
        cred = credentials.Certificate("firebase_key.json")

    firebase_admin.initialize_app(cred)

db = firestore.client()
print("Firebase Connected Successfully!")