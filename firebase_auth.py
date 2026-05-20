import pyrebase
firebaseConfig = {
    "apiKey": "AIzaSyBmLhx-B7nsIz4OomTlPSBofHK4G6AdYcc",
    "authDomain": "lib-automation-29f1a.firebaseapp.com",
    "databaseURL": "https://lib-automation-29f1a-default-rtdb.firebaseio.com",
    "projectId": "lib-automation-29f1a",
    "storageBucket": "lib-automation-29f1a.firebasestorage.app",
    "messagingSenderId": "372857580976",
    "appId": "1:372857580976:web:adf0837ca6a46210defa75",
    "measurementId": "G-Q7WXNQ0XRG"
  }

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()
db = firebase.database()

print("Firebase connected successfully")