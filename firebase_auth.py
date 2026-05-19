import pyrebase
import firebase_auth


firebaseConfig = {

    "apiKey": "AIzaSyCXrwtR0kXsOkX6yWE6D2QTm_cGAxSijpg",

    "authDomain": "library-automation2.firebaseapp.com",

    "projectId": "library-automation2",

    "storageBucket": "library-automation2.firebasestorage.app",

    "messagingSenderId": "89065060409",

    "appId": "1:89065060409:web:21f2cf8dacee22e936b5e8",

    "databaseURL": "https://library-automation-97a80-default-rtdb.firebaseio.com/pip"
}


firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()