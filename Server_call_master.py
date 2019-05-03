import json
import requests
from PyQt5.QtWidgets import QDialog

from windows.ConfirmWindow import ConfirmWindow

URL = "http://thegameofprogramming.altervista.org"  # "http://programmingisagame.netsons.org"
ERROR_message_connection = "<span style=\" color: red;\"> Attenzione, si sono verificati problemi di " \
                                 "connessione<br>Non è stato possibile comunicare col server<br>Controllare la " \
                                 "propria connessione internet</span>"
ERROR_message_server_error = "<span style=\" color: red;\"> Attenzione, il server ha restituito un messaggio " \
                                   "di errore.<br>Se il problema persiste, richiedere assistenza</span>"
ERROR_message_data_error = "<span style=\" color: red;\"> Attenzione, i dati inviati al server non hanno " \
                                 "fornito alcun risultato.<br>Se il problema persiste, richiedere assistenza</span>"


def dialog_message_close(message):
    confirm = ConfirmWindow('Gamification - Errore', message, ok="Chiudi il programma", cancel=None)
    confirm.exec_()
    confirm.deleteLater()
    exit()


def dialog_message(message):
    confirm = ConfirmWindow('Gamification - Errore', message, ok="OK", cancel="Chiudi il programma")
    if confirm.exec_() == QDialog.Accepted:
        confirm.deleteLater()
    else:
        confirm.deleteLater()
        exit()


def get_user(d):
    try:
        r = requests.post(URL + "/get_user.php", data=d)
        j = json.loads(r.text)
        if len(j) > 0:
            r = requests.post(URL + "/update_achievements.php", data=d)
            if len(json.loads(r.text.split("-")[1])) > 0:
                return j
        dialog_message_close(ERROR_message_data_error)
        return None
    except requests.exceptions.RequestException:
        dialog_message_close(ERROR_message_connection)
    except ValueError:
        dialog_message_close(ERROR_message_server_error)


def get_class_components(d):
    try:
        r = requests.post(URL + "/get_class_components.php", data=d)
        j = json.loads(r.text)
        if len(j) > 0:
            r = requests.post(URL + "/get_class_parameters.php", data=d)
            k = json.loads(r.text)
            if len(k) > 0:
                return j, k[0]
        dialog_message_close(ERROR_message_data_error)
        return None, None
    except requests.exceptions.RequestException:
        dialog_message_close(ERROR_message_connection)
    except ValueError:
        dialog_message_close(ERROR_message_server_error)


def get_homeworks(n, p, c):
    try:
        r = requests.post(URL + "/get_homeworks.php", data={'username': n, 'password': p, 'class': c})
        if r.text != "":
            j = json.loads(r.text)
            r = requests.post(URL + "/get_user_solutions.php", data={'username': n, 'password': p})
            k = json.loads(r.text)
            return j, k
        dialog_message(ERROR_message_data_error)
        return None, None
    except requests.exceptions.RequestException:
        dialog_message(ERROR_message_connection)
        return None, None
    except ValueError:
        dialog_message(ERROR_message_server_error)
        return None, None


def get_count_missing_corrections(d):
    try:
        r = requests.post(URL + "/get_count_missing_corrections.php", data=d)
        if r.text != "":
            return int(r.text)
        dialog_message(ERROR_message_data_error)
        return 0
    except requests.exceptions.RequestException:
        dialog_message(ERROR_message_connection)
        return 0
    except ValueError:
        dialog_message(ERROR_message_server_error)
        return 0


def get_class_users(d):
    try:
        r = requests.post(URL + "/get_class_users.php", data=d)
        if r != "":
            return json.loads(r.text)
        dialog_message(ERROR_message_data_error)
        return []
    except requests.exceptions.RequestException:
        dialog_message(ERROR_message_connection)
        return []
    except ValueError:
        dialog_message(ERROR_message_server_error)
        return []


def access(s, o, d):
    try:
        r = requests.post(URL + s, data=d)
        if r.text in o:
            return r.text
        dialog_message(ERROR_message_server_error)
        return None
    except requests.exceptions.RequestException:
        dialog_message(ERROR_message_connection)
        return None


def set_variable(s, d):
    try:
        r = requests.post(URL + s, data=d)
        if r.text == "ok":
            return True
        elif r.text == "":
            dialog_message(ERROR_message_data_error)
        else:
            dialog_message(ERROR_message_server_error)
        return False
    except requests.exceptions.RequestException:
        dialog_message(ERROR_message_connection)
        return False


def check_variable(s, d):
    try:
        r = requests.post(URL + s, data=d)
        if r.text == "ok":
            return True
        elif r.text != "":
            dialog_message(ERROR_message_server_error)
        return False
    except requests.exceptions.RequestException:
        dialog_message(ERROR_message_connection)
        return False


def add_solution(d):
    try:
        r = requests.post(URL + "/add_solution.php", data=d)
        if r.text != "" and (r.text == "ok" or (int(r.text.split(',')[0]) >= 0 and int(r.text.split(',')[1]) >= 0)):
            return r.text
        dialog_message(ERROR_message_data_error)
        return ""
    except requests.exceptions.RequestException:
        dialog_message(ERROR_message_connection)
        return ""
    except ValueError:
        dialog_message(ERROR_message_server_error)
        return ""


def click_watch_homework_coin(d):
    try:
        r = requests.post(URL + "/click_watch_homework_coin.php", data=d)
        if r.text == "removed" or r.text == "" or r.text == "ok":
            return r.text
        elif r.text != "":
            dialog_message(ERROR_message_server_error)
        return ""
    except requests.exceptions.RequestException:
        dialog_message(ERROR_message_connection)
        return ""


def get_class_exercise_solutions(d):
    try:
        r = requests.post(URL + "/get_class_exercise_solutions.php", data=d)
        if r.text != "":
            return json.loads(r.text[1: len(r.text)]), r.text[0:1]
        dialog_message(ERROR_message_data_error)
        return None, None
    except requests.exceptions.RequestException:
        dialog_message(ERROR_message_connection)
        return None, None
    except ValueError:
        dialog_message(ERROR_message_server_error)
        return None, None


def exercise_add_comment(d):
    try:
        r = requests.post(URL + "/exercise_add_comment.php", data=d)
        if r.status_code == 200:
            if r.text != "":
                return r.text
            dialog_message(ERROR_message_data_error)
        else:
            dialog_message(ERROR_message_server_error)
        return ""
    except requests.exceptions.RequestException:
        dialog_message(ERROR_message_connection)
        return ""


def get_class_achievement_progress(d):
    try:
        r = requests.post(URL + "/get_class_achievement_progress.php", data=d)
        if r.text != "":
            return json.loads(r.text)
        dialog_message(ERROR_message_data_error)
        return ""
    except requests.exceptions.RequestException:
        dialog_message(ERROR_message_connection)
        return ""
    except ValueError:
        dialog_message(ERROR_message_server_error)
        return ""


def update_achievements(d):
    try:
        r = requests.post(URL + "/update_achievements.php", data=d)
        if r.text != "":
            return json.loads(r.text.split("-")[0]), r.text.split("-")[1][1:-1].split(',')
        dialog_message(ERROR_message_data_error)
        return [], None
    except requests.exceptions.RequestException:
        dialog_message(ERROR_message_connection)
        return [], None
    except ValueError:
        dialog_message(ERROR_message_server_error)
        return [], None
