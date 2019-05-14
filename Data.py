from os import path, getcwd
import Server_call_master


class Exercise:
    def __init__(self, ex_id, creator, date, title, text, level, white_paper_mode, start_code, limits, executable,
                 lookable, approved, validation_type, self_validation, color_styles=None, delivery_date=None,
                 solution=None, resources_used=None, vote=None, missing_votes=0):
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
        self.lookable = lookable
        self.approved = approved
        self.validation_type = validation_type
        self.self_validation = self_validation

        self.color_styles = color_styles
        self.delivery_date = delivery_date
        self.solution = solution
        self.resources_used = resources_used
        self.vote = vote
        self.missing_votes = missing_votes

    def set_solution(self, solution):
        self.solution = solution


class Data:
    variables_numbers = {
        'lines': [1, 5, 10, 12, 14, 16, 18, 20, 30, 40, 50, 100],
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

    level_progression = [10, 20, 40, 60, 90, 120, 160, 200, 250, 300, 360, 420, 490, 560, 640, 720, 810, 900]

    def __init__(self):
        f = open("user_info.txt", "r")
        self.my_name = f.readline()[0:-1]
        self.my_psw = f.readline()[0:-1]
        self.my_class = f.readline()[0:-1]
        self.my_proff = []
        self.mates = []
        self.approving_type = 0
        self.correction_type = 0
        self.comments_visible = True
        self.language = 1
        self.student_exercises_visible = True
        self.get_class_components()

        if self.language == 2:
            self.variables_numbers['lines'] = [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

        self.code_result_horizontal_orientation = True if f.readline()[0:-1] == "True" else False
        self.code_font_size = int(f.readline())
        self.code_font_family = 'Courier New'
        f.close()

        self.money = None
        self.level = None
        self.current_image = None
        self.level_variables = None
        self.owned_colors = []
        self.owned_images = []
        self.make_homework_coin = False
        self.watch_homework_coin = False
        self.visible = True
        self.exercises = []
        self.get_user_data()

        if not path.isfile('styles/_preferred.txt'):
            directory = "styles/_default_python.txt" if self.language == 1 else "styles/_default_c.txt"
            f = open(directory, "r")
            text = f.read()
            f.close()
            f = open('styles/_preferred.txt', "w")
            f.write(text)
            f.close()

        self.color_styles = self.get_file_color_styles("styles/_preferred.txt")

        self.default_color_styles = self.get_file_color_styles(
            "styles/_default_python.txt" if self.language == 1 else "styles/_default_c.txt")

        self.owned_variables = self.get_owned_variables_numbers()

        self.all_colors = self.get_colors()

        self.all_images = self.get_images()

    def get_user_data(self):
        self.money = 0
        self.level = 0
        self.current_image = '0.png'
        self.level_variables = {'lines': 0, 'variables': 0, 'if': 0, 'elif': 0,
                                'else': 0, 'for': 0, 'while': 0, 'functions': 0}
        self.owned_colors = []
        self.owned_images = []
        self.make_homework_coin = False
        self.watch_homework_coin = False
        self.visible = True
        j = Server_call_master.get_user({'username': self.my_name, 'password': self.my_psw})
        if j is not None:
            self.money = int(j[0]['money'])
            self.level = int(j[0]['exp'])
            self.visible = j[0]['visible'] == '1'
            lev = (j[0]['level_variables']).split(',')
            self.level_variables = {'lines': int(lev[0]), 'variables': int(lev[1]), 'if': int(lev[2]),
                                    'elif': int(lev[3]),
                                    'else': int(lev[4]), 'for': int(lev[5]), 'while': int(lev[6]),
                                    'functions': int(lev[7])}
            self.owned_colors = (j[0]['owned_colors']).split(',')
            self.current_image = j[0]['current_image']
            self.owned_images = j[0]['owned_images'].split(',')
            self.make_homework_coin = False if int(j[0]['make_homework_coin']) == 0 else True
            self.watch_homework_coin = False if int(j[0]['watch_homework_coin']) == 0 else True

    def get_colors(self):
        col = ['#ffffff', '#ff0000', '#00ff00', '#0000ff', '#ff0080',
               '#000000', '#964218', '#85ff74', '#126597', '#ff8080',
               '#ff8000', '#712893', '#256947', '#fffa80', '#367469']
        if len(self.owned_colors) == len(col):
            return self.owned_colors.copy()
        return col

    @staticmethod
    def get_images():
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

    def get_class_components(self):
        self.my_proff = []
        self.mates = []
        j, k = Server_call_master.get_class_components({'username': self.my_name, 'password': self.my_psw,
                                                        'class': self.my_class})
        if j is not None:
            for i in j:
                if int(i['student_type']) > 0:
                    self.mates.append(i['username'])
                else:
                    self.my_proff.append(i['username'])

            self.student_exercises_visible = k['student_ex_visible'] == '1'
            self.correction_type = int(k['correction_type'])
            self.approving_type = int(k['approving_type'])
            self.comments_visible = int(k['comments_visible']) == 1
            self.language = int(k['language'])

    def get_homework(self):
        self.exercises = []

        j, k = Server_call_master.get_homeworks(self.my_name, self.my_psw, self.my_class)
        if j is not None:
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
                lookable = False if int(i['lookable']) == 0 else True
                approved = False if int(i['approved']) == 0 else True
                validation_type = int(i['validation_type'])
                self_validation = False if int(i['self_validation']) == 0 else True

                mv = 0
                if validation_type > 0 and ((self_validation and i['creator'] == self.my_name) or
                                            (not self_validation and self.my_name in self.my_proff)):
                    mv = Server_call_master.get_count_missing_corrections(
                        {'username': self.my_name, 'password': self.my_psw,
                         'class': self.my_class, 'exercise': i['exercise_id']})

                ex = Exercise(i['exercise_id'], i['creator'], date, i['title'], i['text'], level, white_paper_mode,
                              i['start_code'], limits, executable, lookable, approved, validation_type, self_validation,
                              missing_votes=mv)

                find = False
                for solution_k in k:
                    if solution_k['id'] == i['exercise_id']:
                        find = True
                        cs_used = solution_k['color_styles'].split(' , ')
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
                        for j in range(9, len(cs_used)):
                            el = cs_used[j].split(' - ')
                            cs.keyWords[el[0]] = (el[1], el[2])
                        ex.color_styles = cs
                        ex.delivery_date = \
                            solution_k['delivery_date'].split('-')[2] + "/" + \
                            solution_k['delivery_date'].split('-')[1] + "/" + \
                            solution_k['delivery_date'].split('-')[0]
                        ex.solution = solution_k['solution']
                        lev = solution_k['resources_used'].split(',')
                        ex.resources_used = {'lines': int(lev[0]), 'variables': int(lev[1]), 'if': int(lev[2]),
                                             'elif': int(lev[3]), 'else': int(lev[4]),
                                             'conditions': int(lev[2]) + int(lev[3]) + int(lev[4]), 'for': int(lev[5]),
                                             'while': int(lev[6]), 'cycles': int(lev[5]) + int(lev[6]),
                                             'def': int(lev[7])}
                        ex.vote = solution_k['evaluation']

                if not find:
                    file = i['exercise_id']
                    saves_file_name = 'saves/' + i['exercise_id'] + '.txt'
                    styles_file_name = 'styles/' + i['exercise_id'] + '.txt'
                    if file.__contains__('"') or file.__contains__("'") or file.__contains__('?') \
                            or file.__contains__('\\') or file.__contains__('/') or file.__contains__(":") \
                            or file.__contains__("*") or file.__contains__("<") or file.__contains__(">") \
                            or file.__contains__("|"):
                        if path.isfile('styles/_lib.txt'):
                            f = open('styles/_lib.txt', 'r')
                            for c in f:
                                print(c)
                                if c != "" and c[len(c.split(':')[0]) + 1:-1] == file:
                                    styles_file_name = 'styles/' + c.split(':')[0] + '.txt'
                            f.close()

                        if path.isfile('saves/_lib.txt'):
                            f = open('saves/_lib.txt', 'r')
                            for c in f:
                                if c[len(c.split(':')[0]) + 1:-1] == file:
                                    saves_file_name = 'saves/' + c.split(':')[0] + '.txt'
                            f.close()

                    if path.isfile(saves_file_name):
                        f = open(saves_file_name, "r")
                        ex.solution = f.read()
                        f.close()
                    if path.isfile(styles_file_name):
                        ex.color_styles = self.get_file_color_styles(styles_file_name)
                self.exercises.append(ex)

    @staticmethod
    def get_file_color_styles(file):
        styles = DefaultColorStyles()
        f = open(file, "r")
        styles.code_background_color = f.readline()[0:-1].split(' - ')[1]
        styles.code_text_color = f.readline()[0:-1].split(' - ')[1]
        styles.results_background_color = f.readline()[0:-1].split(' - ')[1]
        styles.results_text_color = f.readline()[0:-1].split(' - ')[1]
        styles.error_results_background_color = f.readline()[0:-1].split(' - ')[1]
        styles.error_results_text_color = f.readline()[0:-1].split(' - ')[1]

        styles.string_color = f.readline()[0:-1].split(' - ')[1]
        styles.comment_color = f.readline()[0:-1].split(' - ')[1]
        styles.multi_line_comment_color = f.readline()[0:-1].split(' - ')[1]

        keys = {}
        r = f.readline()
        while r != '':
            r = r[0:-1].split(' - ')
            keys[r[0]] = (r[1], True if r[2] == 'True' else False)
            r = f.readline()

        styles.keyWords = keys
        f.close()
        return styles

    @staticmethod
    def write_file_color_styles(file, styles):
        if file.__contains__('"') or file.__contains__("'") or file.__contains__('?') or file[7:-4].__contains__('\\') \
                or file[7:-4].__contains__('/') or file.__contains__(":") or file.__contains__("*") \
                or file.__contains__("<") or file.__contains__(">") or file.__contains__("|"):
            not_find = True
            file_name = '0'
            if path.isfile('styles/_lib.txt'):
                f = open('styles/_lib.txt', 'r')
                for i in f:
                    if not_find:
                        if i[len(i.split(':')[0]) + 1:-1] == file[7:-4]:
                            not_find = False
                            file_name = i.split(':')[0]
                        else:
                            file_name = str(int(i.split(':')[0]) + 1)
                f.close()
            if not_find:
                f = open('styles/_lib.txt', 'a')
                f.write(file_name + ':' + file[7:-4] + '\n')
                f.close()
            f = open('styles/' + file_name + '.txt', "w")
        else:
            f = open(file, "w")
        text = ""
        text += "code_background_color - " + styles.code_background_color + '\n'
        text += "code_text_color - " + styles.code_text_color + '\n'
        text += "results_background_color - " + styles.results_background_color + '\n'
        text += "results_text_color - " + styles.results_text_color + '\n'
        text += "error_results_background_color - " + styles.error_results_background_color + '\n'
        text += "error_results_text_color - " + styles.error_results_text_color + '\n'

        text += "string_color - " + styles.string_color + '\n'
        text += "comment_color - " + styles.comment_color + '\n'
        text += "multi_line_comment_color - " + styles.multi_line_comment_color + '\n'

        for i in styles.keyWords.keys():
            text += i + " - " + styles.keyWords[i][0] + ' - ' + str(styles.keyWords[i][1]) + '\n'

        f.write(text)
        f.close()

    @staticmethod
    def get_path():
        return getcwd()


class DefaultColorStyles:
    def __init__(self):
        self.code_background_color = 'white'
        self.code_text_color = 'white'
        self.results_background_color = 'white'
        self.results_text_color = 'white'
        self.error_results_background_color = 'white'
        self.error_results_text_color = 'white'

        self.string_color = 'white'
        self.comment_color = 'white'
        self.multi_line_comment_color = 'white'

        self.keyWords = {}

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

        color_styles.keyWords = {}

        for i in self.keyWords.keys():
            color_styles.keyWords[i] = (self.keyWords[i][0], self.keyWords[i][1])
        return color_styles
