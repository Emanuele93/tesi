import requests

try:
    r = requests.post("http://programmingisagame.netsons.org/evaluate_exercise.php",
                      data={'username': 'Emanuele', 'password': '1234', 'class': 'Merlino class',
                            'id': 'Emanuele2019-03-09d', 'vote': 5.77, 'username2': 'prof'})
    print(r.text)
except requests.exceptions.RequestException as e:
    print('no')
