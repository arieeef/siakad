

import firebase_admin
from firebase_admin import credentials, firestore
from pyrebase import initialize_app

firebaseConfig= {
    'apiKey': "AIzaSyAQui0dtWk0qeY7QkHB_VZ49h4MQtA-Ueg",
    'authDomain': "siakad-2f454.firebaseapp.com",
    'databaseURL': "https://siakad-2f454-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "siakad-2f454",
    'storageBucket': "siakad-2f454.appspot.com",
    'messagingSenderId': "49157089131",
    'appId': "1:49157089131:web:6082f25ae0fe16f28ece2e"
}

firebase = initialize_app(firebaseConfig)
storage = firebase.storage()

cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def get_all_collection(collection, orderBy=None, direction=None):
    if orderBy:
        collects_ref = db.collection(collection).order_by(
            orderBy, direction=direction)
    else:
        collects_ref = db.collection(collection)
    collects = collects_ref.stream()
    RETURN = []
    for collect in collects:
        ret = collect.to_dict()
        ret['id'] = collect.id
        RETURN.append(ret)
    return RETURN