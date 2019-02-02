import json

import requests

r = requests.post("http://programmingisagame.netsons.org/get_class_exercise_solutions.php",
                  data={'username': 'Emanuele', 'password': '1234', 'exercise': 'Emanuele2019-01-28Esercizio 10', 'class': 'Merlino class'})

if r.text != "":
    j = json.loads(r.text)
    for i in j:
        print(i)
