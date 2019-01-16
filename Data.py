import datetime


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
                 color_styles, delivery_date=None, solution=None,  resources_used=None):
        self.id = ex_id
        self.creator = creator
        self.date = date
        self.title = title
        self.text = text
        self.level = level
        self.white_paper_mode = white_paper_mode
        self.start_code = start_code
        self.limits = limits
        self.executable = executable
        self.color_styles = color_styles
        self.delivery_date = delivery_date
        self.solution = solution
        self.resources_used = resources_used

    def set_solution(self, solution):
        self.solution = solution


class Data:
    def __init__(self):
        self.my_name = "Emanuele"
        self.my_proff = "Proff"

        self.code_result_horizontal_orientation = True

        self.code_font_size = 20

        self.color_styles = self.get_my_color_styles()

        self.exercises = self.get_homework()

        self.owned_variables = self.get_owned_variables_numbers()

    def get_owned_variables_numbers(self):
        # ToDo da prendere da file
        lib = {
            'lines': 10,
            'variables': 4,
            'if': 3,
            'elif': 5,
            'else': 3,
            'for': 3,
            'while': 2,
            'functions': 0
        }
        return lib

    def get_my_color_styles(self):
        # ToDo guardare da file le mie preferenze
        return DefaultColorStyles()

    def get_homework(self):
        # ToDo da prendere online
        functions_limit0 = {'lines': 10, 'variables': 4, 'if': 1, 'elif': 3, 'else': 1, 'conditions': 5, 'for': 2, 'while': 1, 'cycles': 3, 'def': 0}
        functions_limit1 = {'lines': 10, 'variables': 4, 'if': 1, 'elif': 3, 'else': 1, 'conditions': 5, 'for': 2, 'while': 1, 'cycles': 3, 'def': 0}
        functions_limit2 = {'lines': 10, 'variables': 4, 'if': 1, 'elif': 3, 'else': 1, 'conditions': 5, 'for': 2, 'while': 1, 'cycles': 3, 'def': 0}
        functions_limit3 = {'lines': 10, 'variables': 4, 'if': 1, 'elif': 3, 'else': 1, 'conditions': 5, 'for': 2, 'while': 1, 'cycles': 3, 'def': 0}

        exercises = [
            Exercise(0, self.my_proff, "08/01/2019", 'Esercizio 1', 'Fai i compiti', 'Difficile', False, 'print("ciao")', functions_limit0, True, None),
            Exercise(1, self.my_proff, "08/01/2019", 'Esercizio 2', 'Fai tutti i compiti', 'Difficile', True, '', functions_limit1, True, None),
            Exercise(2, self.my_proff, "20/01/2019", 'Esercizio 3', 'Fai qualche compito', 'Medio', False, 'print("ciao a tutti")', functions_limit2, False, None, ),
            Exercise(3, self.my_proff, "20/01/2019", 'Esercizio 4', 'Non fare i compiti', 'Facile', True, 'print("ciao a lele")', functions_limit3, False, None)
        ]

        # Todo predere da file lo stile e la soluzione
        for i in exercises:
            i.color_styles = self.color_styles
        exercises[0].solution = "print('nooo')"
        exercises[2].solution='print("ciao a tutti")'

        return exercises

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
        self.string_tag_start = '<span style=\" color: #ff0000;\">'
        self.string_tag_end = '</span>'

        self.comment_tag_start = '<span style=\" color: #999999;\">'
        self.comment_tag_end = '</span>'

        self.multi_line_comment_tag_start = '<span style=\" color: #990099;\">'
        self.multi_line_comment_tag_end = '</span>'

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

        '''
        self.exercises_delivered = [
            Exercise(4, "07/01/2019", 'Esercizio 5', 'Fai i compiti', 'Difficile', False, 'print("ciao")', 5, True)
        ]
        '''

    '''
    def deliver(self, id):
        for es in self.exercises:
            if es.id == id:
                self.exercises.remove(es)
                self.exercises_delivered.append(es)
    '''
