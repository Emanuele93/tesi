import requests

r = requests.post("http://programmingisagame.netsons.org/get_class_achievement_progress.php",
                  data={'username': 'Emanuele', 'password': '1234', 'class': 'Merlino class'})

print(r.text)

