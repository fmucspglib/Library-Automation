import pyrebase

firebase_Config = {
    "apiKey": "AIzaSyBjqaFESOTp10fsesq-5kyHf4hI0bCKzEs",
    "authDomain": "lib-auto-3cf8b.firebaseapp.com",
    "databaseURL": "https://lib-auto-3cf8b-default-rtdb.firebaseio.com/",
    "projectId": "lib-auto-3cf8b",
    "storageBucket": "lib-auto-3cf8b.appspot.com",
    "messagingSenderId": "160237048109",
    "appId": "1:160237048109:web:bf70e6a131750cd0d143a4"
}

firebase = pyrebase.initialize_app(firebase_Config)
auth = firebase.auth()

print("Firebase connected successfully")
print("Project ID:", firebase_Config["projectId"])