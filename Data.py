import json
import requests
from PyQt5.QtWidgets import QDialog

from windows.ConfirmWindow import ConfirmWindow


class KeyWord:
    def __init__(self, word, color, bold):
        self.word = word
        self.color = color
        self.bold = bold

    def tagged_word(self):
        tagged = '<span style=\" color: ' + self.color + ';\">' + self.word + '</span>'
        if self.bold:
            return '<b>' + tagged + '</b>'
        return tagged


class Exercise:
    def __init__(self, ex_id, creator, date, title, text, level, white_paper_mode, start_code, limits, executable,
                 color_styles=None, delivery_date=None, solution=None, resources_used=None):
        self.id = ex_id
        self.creator = creator
        self.date = date
        self.title = title
        self.text = text
        self.level = level
        self.white_paper_mode = white_paper_mode
        self.start_code = start_code
        self.limits = limits  # 10
        self.executable = executable

        self.color_styles = color_styles
        self.delivery_date = delivery_date
        self.solution = solution
        self.resources_used = resources_used

    def set_solution(self, solution):
        self.solution = solution


class Data:
    variables_numbers = {
        'lines': [0, 5, 10, 12, 14, 16, 18, 20, 30, 40, 50, 100],
        'variables': [0, 2, 4, 5, 6, 7, 8, 10, 15, 20],
        'if': [0, 1, 2, 3, 5, 7, 10],
        'elif': [0, 1, 2, 3, 5, 7, 10, 15],
        'else': [0, 1, 2, 3, 5, 7, 10],
        'for': [0, 1, 2, 3, 5, 7],
        'while': [0, 1, 2, 3, 5, 7],
        'functions': [0, 1, 2, 3, 5, 7]
    }

    variables_cost = {
        'lines': [2, 4, 8, 20, 40, 80, 80, 80, 100, 100, 100, 200],
        'variables': [2, 20, 20, 20, 20, 20, 20, 40, 50, 100],
        'if': [2, 20, 20, 20, 50, 50, 100],
        'elif': [2, 10, 10, 20, 20, 40, 50, 100],
        'else': [2, 20, 20, 20, 50, 50, 100],
        'for': [20, 20, 20, 50, 50, 100],
        'while': [20, 20, 20, 50, 50, 100],
        'functions': [40, 40, 40, 50, 50, 100]
    }

    def __init__(self):
        self.my_name = "prof"
        self.my_psw = "1234"
        self.my_class = "Merlino class"
        self.my_proff = None
        self.mates = []
        self.get_class_components()

        self.code_result_horizontal_orientation = True
        self.code_font_size = 20
        self.code_font_family = 'Courier New'

        self.money = None
        self.current_image = None
        self.level_variables = None
        self.owned_colors = []
        self.owned_images = []
        self.make_homework_coin = False
        self.watch_homework_coin = False
        self.exercises = []
        self.get_user_data()

        self.color_styles = self.get_my_color_styles()

        self.owned_variables = self.get_owned_variables_numbers()

        self.all_colors = self.get_colors()

        self.all_images = self.get_images()

    def get_user_data(self):
        self.money = 0
        self.current_image = '0.png'
        self.level_variables = {'lines': 0, 'variables': 0, 'if': 0, 'elif': 0,
                                'else': 0, 'for': 0, 'while': 0, 'functions': 0}
        self.owned_colors = []
        self.owned_images = []
        self.make_homework_coin = False
        self.watch_homework_coin = False
        try:
            r = requests.post("http://programmingisagame.netsons.org/get_user.php",
                              data={'username': self.my_name, 'password': self.my_psw})
            j = json.loads(r.text)
            if len(j) > 0:
                self.money = int(j[0]['money'])
                lev = (j[0]['level_variables']).split(',')
                self.level_variables = {'lines': int(lev[0]), 'variables': int(lev[1]), 'if': int(lev[2]), 'elif': int(lev[3]),
                                        'else': int(lev[4]), 'for': int(lev[5]), 'while': int(lev[6]), 'functions': int(lev[7])}
                self.owned_colors = (j[0]['owned_colors']).split(',')
                self.current_image = j[0]['current_image']
                self.owned_images = j[0]['owned_images'].split(',')
                self.make_homework_coin = False if int(j[0]['make_homework_coin']) == 0 else True
                self.watch_homework_coin = False if int(j[0]['watch_homework_coin']) == 0 else True
        except requests.exceptions.RequestException as e:
            confirm = ConfirmWindow('Gamification - Errore di connessione',
                                    "<span style=\" color: red;\"> Attenzione, si sono verificati problemi di "
                                    "connessione<br>Controllare la propria connessione internet</span>",
                                    ok="Chiudi il programma", cancel=None)
            if confirm.exec_() == QDialog.Accepted:
                print('ok')
            confirm.deleteLater()
            exit()

    def get_colors(self):
        col = ['#ffffff', '#ff0000', '#00ff00', '#0000ff', '#990099'
            , '#000000', '#964218', '#85ff74', '#126597', '#337744'
            , '#974631', '#712893', '#256947', '#256914', '#367469']
        if len(self.owned_colors) == len(col):
            return self.owned_colors.copy()
        return col

    def get_images(self):
        return {'1.png': 100, '2.png': 100, '3.png': 100, '4.png': 100, '5.png': 100,
                '6.png': 500, '7.png': 500, '8.png': 500, '9.png': 500, '10.png': 500,
                '11.png': 1000, '12.png': 1000, '13.png': 1000, '14.png': 1000, '15.png': 1000}

    def get_owned_variables_numbers(self):
        lib = {
            'lines': None if self.level_variables['lines'] == len(self.variables_numbers['lines']) else
            self.variables_numbers['lines'][self.level_variables['lines']],
            'variables': None if self.level_variables['variables'] == len(self.variables_numbers['variables']) else
            self.variables_numbers['variables'][self.level_variables['variables']],
            'if': None if self.level_variables['if'] == len(self.variables_numbers['if']) else
            self.variables_numbers['if'][self.level_variables['if']],
            'elif': None if self.level_variables['elif'] == len(self.variables_numbers['elif']) else
            self.variables_numbers['elif'][self.level_variables['elif']],
            'else': None if self.level_variables['else'] == len(self.variables_numbers['else']) else
            self.variables_numbers['else'][self.level_variables['else']],
            'for': None if self.level_variables['for'] == len(self.variables_numbers['for']) else
            self.variables_numbers['for'][self.level_variables['for']],
            'while': None if self.level_variables['while'] == len(self.variables_numbers['while']) else
            self.variables_numbers['while'][self.level_variables['while']],
            'functions': None if self.level_variables['functions'] == len(self.variables_numbers['functions']) else
            self.variables_numbers['functions'][self.level_variables['functions']]
        }
        return lib

    def get_my_color_styles(self):
        # ToDo guardare da file le mie preferenze
        return DefaultColorStyles()

    def get_class_components(self):
        self.my_proff = ''
        self.mates = []
        try:
            r = requests.post("http://programmingisagame.netsons.org/get_class_components.php",
                              data={'username': self.my_name, 'password': self.my_psw, 'class': self.my_class})
            j = json.loads(r.text)
            for i in j:
                if int(i['student_type']) > 0:
                    self.mates.append(i['username'])
                else:
                    self.my_proff = i['username']
        except requests.exceptions.RequestException as e:
            confirm = ConfirmWindow('Gamification - Errore di connessione',
                                    "<span style=\" color: red;\"> Attenzione, si sono verificati problemi di "
                                    "connessione<br>Controllare la propria connessione internet</span>",
                                    ok="Chiudi il programma", cancel=None)
            if confirm.exec_() == QDialog.Accepted:
                print('ok')
            confirm.deleteLater()
            exit()

    def get_homework(self):
        self.exercises = []
        try:
            r = requests.post("http://programmingisagame.netsons.org/get_homeworks.php",
                              data={'username': self.my_name, 'password': self.my_psw, 'class': self.my_class})
            j = json.loads(r.text)
            for i in j:
                date = i['date'].split('-')[2] + "/" + i['date'].split('-')[1] + "/" + i['date'].split('-')[0]
                level = 'Facile' if int(i['level']) == 1 else ('Medio' if int(i['level']) == 2 else 'Difficile')
                white_paper_mode = False if int(i['white_paper_mode']) == 0 else True
                lev = i['limits'].split(',')
                limits = {'lines': None if lev[0] == 'None' else int(lev[0]),
                          'variables': None if lev[1] == 'None' else int(lev[1]),
                          'if': None if lev[2] == 'None' else int(lev[2]),
                          'elif': None if lev[3] == 'None' else int(lev[3]),
                          'else': None if lev[4] == 'None' else int(lev[4]),
                          'conditions': None if lev[5] == 'None' else int(lev[5]),
                          'for': None if lev[6] == 'None' else int(lev[6]),
                          'while': None if lev[7] == 'None' else int(lev[7]),
                          'cycles': None if lev[8] == 'None' else int(lev[8]),
                          'def': None if lev[9] == 'None' else int(lev[9])}
                executable = False if int(i['executable']) == 0 else True

                ex = Exercise(i['exercise_id'], i['creator'], date, i['title'], i['text'], level, white_paper_mode,
                              i['start_code'], limits, executable)

                r = requests.post("http://programmingisagame.netsons.org/get_exercise_solution.php",
                                  data={'username': self.my_name, 'password': self.my_psw, 'exercise': i['exercise_id'],
                                        'class':self.my_class})
                j = json.loads(r.text)
                if len(j)>0:
                    cs_used = j[0]['color_styles'].split(',')
                    cs = DefaultColorStyles()
                    cs.code_background_color = cs_used[0]
                    cs.code_text_color = cs_used[1]
                    cs.results_background_color = cs_used[2]
                    cs.results_text_color = cs_used[3]
                    cs.error_results_background_color = cs_used[4]
                    cs.error_results_text_color = cs_used[5]
                    cs.string_color = cs_used[6]
                    cs.comment_color = cs_used[7]
                    cs.multi_line_comment_color = cs_used[8]
                    cs.keyWords[0].color = cs_used[9]
                    cs.keyWords[0].bold = True if cs_used[10] == 'T' else False
                    cs.keyWords[1].bold = cs_used[11]
                    cs.keyWords[1].bold = True if cs_used[12] == 'T' else False
                    cs.keyWords[2].bold = cs_used[13]
                    cs.keyWords[2].bold = True if cs_used[14] == 'T' else False
                    cs.keyWords[3].bold = cs_used[15]
                    cs.keyWords[3].bold = True if cs_used[16] == 'T' else False
                    cs.keyWords[4].bold = cs_used[17]
                    cs.keyWords[4].bold = True if cs_used[18] == 'T' else False
                    cs.keyWords[5].bold = cs_used[19]
                    cs.keyWords[5].bold = True if cs_used[20] == 'T' else False
                    cs.keyWords[6].bold = cs_used[21]
                    cs.keyWords[6].bold = True if cs_used[22] == 'T' else False
                    cs.keyWords[7].bold = cs_used[23]
                    cs.keyWords[7].bold = True if cs_used[24] == 'T' else False
                    cs.keyWords[8].bold = cs_used[25]
                    cs.keyWords[8].bold = True if cs_used[26] == 'T' else False
                    cs.keyWords[9].bold = cs_used[27]
                    cs.keyWords[9].bold = True if cs_used[28] == 'T' else False
                    cs.keyWords[10].bold = cs_used[29]
                    cs.keyWords[10].bold = True if cs_used[30] == 'T' else False
                    cs.keyWords[11].bold = cs_used[31]
                    cs.keyWords[11].bold = True if cs_used[32] == 'T' else False
                    cs.keyWords[12].bold = cs_used[33]
                    cs.keyWords[12].bold = True if cs_used[34] == 'T' else False
                    cs.keyWords[13].bold = cs_used[35]
                    cs.keyWords[13].bold = True if cs_used[36] == 'T' else False
                    cs.keyWords[14].bold = cs_used[37]
                    cs.keyWords[14].bold = True if cs_used[38] == 'T' else False
                    ex.color_styles = cs
                    ex.delivery_date = j[0]['delivery_date'].split('-')[2] + "/" + j[0]['delivery_date'].split('-')[1] \
                                       + "/" + j[0]['delivery_date'].split('-')[0]
                    ex.solution = j[0]['solution']
                    lev = j[0]['resources_used'].split(',')
                    ex.resources_used = {'lines': int(lev[0]), 'variables': int(lev[1]), 'if': int(lev[2]),
                                         'elif': int(lev[3]), 'else': int(lev[4]), 'conditions': int(lev[5]),
                                         'for': int(lev[6]), 'while': int(lev[7]), 'cycles': int(lev[8]),
                                         'def': int(lev[9])}
                self.exercises.append(ex)
        except requests.exceptions.RequestException as e:
            confirm = ConfirmWindow('Gamification - Errore di connessione',
                                    "<span style=\" color: red;\"> Attenzione, si sono verificati problemi di "
                                    "connessione<br>Controllare la propria connessione internet</span>",
                                    ok="Riprova", cancel="Chiudi il programma")
            if confirm.exec_() == QDialog.Accepted:
                self.get_homework()
                confirm.deleteLater()
            else:
                confirm.deleteLater()
                exit()

    def save_exercise(self, exercise):
        # Todo salva su file exercise.slution
        return

    def send_exercise(self, exercise):
        self.save_exercise(exercise)
        # ToDo fare online

    def addExercise(self, exercise):
        # ToDo da mandare online
        exercise.color_styles = self.color_styles
        self.exercises.append(exercise)


class DefaultColorStyles:
    def __init__(self):
        self.code_background_color = 'white'
        self.code_text_color = 'black'
        self.results_background_color = 'white'
        self.results_text_color = 'black'
        self.error_results_background_color = 'white'
        self.error_results_text_color = 'red'

        self.string_color = '#ff0000'
        self.comment_color = '#999999'
        self.multi_line_comment_color = '#990099'

        self.keyWords = [
            KeyWord('if', '#0000ff', True),
            KeyWord('elif', '#0000ff', True),
            KeyWord('else', '#0000ff', True),
            KeyWord('for', '#0000ff', True),
            KeyWord('while', '#0000ff', True),
            KeyWord('def', '#0000ff', True),
            KeyWord('import', '#0000ff', True),
            KeyWord('is', '#0000ff', True),
            KeyWord('in', '#0000ff', True),
            KeyWord('not', '#0000ff', True),
            KeyWord('None', '#0000ff', True),
            KeyWord('class', '#0000ff', True),
            KeyWord('print', '#0000ff', False),
            KeyWord('True', '#00ff00', False),
            KeyWord('False', '#00ff00', False)
        ]

    def __copy__(self):
        color_styles = DefaultColorStyles()

        color_styles.code_background_color = self.code_background_color
        color_styles.code_text_color = self.code_text_color
        color_styles.results_background_color = self.results_background_color
        color_styles.results_text_color = self.results_text_color
        color_styles.error_results_background_color = self.error_results_background_color
        color_styles.error_results_text_color = self.error_results_text_color

        color_styles.string_color = self.string_color
        color_styles.comment_color = self.comment_color
        color_styles.multi_line_comment_color = self.multi_line_comment_color

        color_styles.keyWords = []

        for i in self.keyWords:
            color_styles.keyWords.append(KeyWord(i.word, i.color, i.bold))
        return color_styles
