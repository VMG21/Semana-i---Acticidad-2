import pyrebase
import time
import json

config = {
  "apiKey": "AIzaSyAOyrlBHH-MIv4cSfJ4Q-0P5eBujsojRKY",
  "authDomain": "semana-i-7c2e6.firebaseapp.com",
  "databaseURL": "https://semana-i-7c2e6-default-rtdb.firebaseio.com",
  "projectId": "semana-i-7c2e6",
  "storageBucket": "semana-i-7c2e6.appspot.com",
  "messagingSenderId": "935089298155",
  "appId": "1:935089298155:web:fb68831bfff0c261de3cae"
}

while True:
    i = 0
    for i in range(7):
        data = json.load(open('config1.json'))
        configs = data[i]

        firebase = pyrebase.initialize_app(configs)
        db = firebase.database()
    
        all_users = db.child("users").get()

        for users in all_users.each():
            firebase2 = pyrebase.initialize_app(config)
            db2 = firebase.database()
            
            db2.child("users").child(users.key()).update(users.val())

    time.sleep(10)