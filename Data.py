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
    def __init__(self, title, text, level, white_paper_mode, start_code, line_limit, executable, solution=None):
        self.title = title
        self.text = text
        self.level = level
        self.white_paper_mode = white_paper_mode
        self.start_code = start_code
        self.line_limit = line_limit
        self.executable = executable
        self.solution = solution

    def set_solution(self, solution):
        self.solution = solution


class Data:
    def __init__(self):
        self.string_tag_start = '<span style=\" color: #ff0000;\">'
        self.string_tag_end = '</span>'

        self.comment_tag_start = '<span style=\" color: #999999;\">'
        self.comment_tag_end = '</span>'

        self.multi_line_comment_tag_start = '<span style=\" color: #990099;\">'
        self.multi_line_comment_tag_end = '</span>'

        self.keyWords = [
            KeyWord('print', '#0000ff', False),
            KeyWord('if', '#0000ff', True),
            KeyWord('True', '#00ff00', False),
            KeyWord('False', '#00ff00', False),
            KeyWord('for', '#0000ff', True),
            KeyWord('in', '#0000ff', True),
            KeyWord('def', '#0000ff', True),
            KeyWord('import', '#0000ff', True),
            KeyWord('is', '#0000ff', True),
            KeyWord('not', '#0000ff', True),
            KeyWord('None', '#0000ff', True),
            KeyWord('class', '#0000ff', True)
        ]

        self.exercises = [
            Exercise('Esercizio 1', 'Fai i compiti', 'Difficile', False, 'print("ciao")', 5, True),
            Exercise('Esercizio 2', 'Fai tutti i compiti', 'Difficile', True, '', None, True),
            Exercise('Esercizio 3', 'Fai qualche compito', 'Medio', False, 'print("ciao a tutti")', 10, False),
            Exercise('Esercizio 4', 'Non fare i compiti', 'Facile', True, 'print("ciao a lele")', 1, False)
        ]
