from random import randint, choice
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image


WIDTH = 420
HEIGHT = 600
COUNT_OBJ = 9
SIZE_OBJ = WIDTH / 3


class Games(Canvas):
    def __init__(self):
        Canvas.__init__(self, width=WIDTH, height=HEIGHT, bg="White", highlightthickness=0)
        self.start_settings()
        self.main_menu()
        self.pack()

    def start_settings(self):
        self.who_choice = {}    # Словарь {имя: выбор}
        self.step = ""    # Кто ходит в игре
        self.choice_players_obj = [""] * COUNT_OBJ    # Массив клеточек игрового поля
        self.coords_x, self.coords_y = [""] * COUNT_OBJ, [""] * COUNT_OBJ    # Координаты нажатого объекта
        self.btn = False    # Кнопки
        self.obj_rect, self.obj_nolik = False, False    # Обьект квадрата и нолика
        self.obj_krestik = ImageTk.PhotoImage(Image.open("iconki\krest.png").resize((90, 90), Image.ANTIALIAS))  # Объект крестика
        self.dict_choice = {}    # Словарь право выбора игрока
        self.random_number = 0    # Жеребьевка игрока для выбора X или O
        self.random_number_bot = 0    # Жеребьевка для бота X или O
        self.mode, self.mode_bot = "", ""    # Режим игры и режим игры компьютера
        self.click_obj = 0    # Нажатый объект (Индекс)
        self.menu_now = ""    # В каком меню находимся
        self.winner = ""    # Победитель
        self.number = 0  # Число для среднего уровня игры бота
        self.winner_obj = []  # Массив выигравших объектов

    def install_btn(self, x, y, text, width):
        self.btn = Button(window, text=text, width=width, height=2, cursor="hand2", bg="Black", fg="#C3FF00")
        self.create_window(x, y, window=self.btn, anchor="center", tag="pause")
        self.btn.bind("<Button-1>", self.btn_click)

    def btn_back(self, x, y, text):
        btn = Button(window, text="Назад", width=15, height=2, cursor="hand2", bg="Black", fg="#C3FF00")
        self.create_window(x, y, window=btn, anchor="center")
        btn.bind("<Button-1>", self.btn_click)
        self.menu_now = text

    def load_name(self, event, name1, name2):
        if self.menu_now == "Choice_name":
            self.delete(ALL)
            name1 = name1.get().strip()
            if name2 == "Компьютер":
                self.mode = "bot"
            else:
                name2 = name2.get().strip()
                self.mode = "1 на 1"

            if len(name1) == 0 and len(name2) == 0:
                self.who_choice = {"Player1": "", "Player2": ""}
            elif len(name1) == 0:
                self.who_choice = {"Player1": "", name2: ""}
            elif len(name2) == 0:
                self.who_choice = {name1: "", "Player2": ""}
            else:
                if name1 == name2:
                    name2 = name2 + "2"
                self.who_choice = {name1: "", name2: ""}

            self.choice_xo()

    def load_objects(self, start):
        for i in range(1, 3):
            self.create_line(SIZE_OBJ * i, HEIGHT-WIDTH, SIZE_OBJ * i, HEIGHT, width=5)
        self.create_line(0, HEIGHT / 1.9, HEIGHT, HEIGHT / 1.9, width=5)
        self.create_line(0, HEIGHT / 1.31, HEIGHT, HEIGHT / 1.31, width=5)

        for i in range(1, 4):
            self.obj_rect = self.create_rectangle((i - 1) * (WIDTH / 3), HEIGHT / 3.35, i * (WIDTH / 3), HEIGHT / 1.9, width=4, fill="Gray", tag="rect")
            self.obj_rect = self.create_rectangle((i - 1) * (WIDTH / 3), HEIGHT / 1.9, i * (WIDTH / 3), HEIGHT / 1.31, width=4, fill="Gray", tag="rect")
            self.obj_rect = self.create_rectangle((i - 1) * (WIDTH / 3), HEIGHT / 1.31, i * (WIDTH / 3), HEIGHT - 2, width=4, fill="Gray", tag="rect")

        self.install_btn(WIDTH - 50, HEIGHT / 20, "Пауза", 7)

        self.create_text(WIDTH / 28, WIDTH / 28, anchor="nw", fill="Black", font=("Tahoma", 14), text="Кто ходит:", tag="going")
        self.create_text(WIDTH / 28, WIDTH / 4.67, anchor="nw", fill="Black", font=("Tahoma", 14), text="Что у вас:", tag="what")

        if start:
            for i in list(self.who_choice.keys()):
                if self.who_choice.get(i) == "Крестик (X)":
                    self.step = i
                    self.create_text(WIDTH / 3.23, WIDTH / 28, anchor="nw", fill="Black", font=("Tahoma", 15), text=self.step, tag="text")
                    self.create_image(WIDTH / 3, WIDTH / 7, image=self.obj_krestik, anchor="nw", tag="krest_text")

        self.bind("<Button-1>", lambda event="": self.what_element_click(event))

    def main_menu(self):
        name_btn_menu = ["1 на 1", "С ботом", "Выйти из игры"]
        self.create_text(WIDTH / 2, HEIGHT / 6, anchor="center", fill="Black", font=("Tahoma", 26), text="Меню:")
        for i in range(1, 4):
            self.install_btn(WIDTH / 2, HEIGHT / 5 + (85 * i), name_btn_menu[i - 1], 15)
        self.menu_now = "main_menu"

    def menu_vs_bot(self):
        # Ввод имени игрока:
        self.create_text(WIDTH / 2, HEIGHT / 6, anchor="center", fill="Black", font=("Tahoma", 14), text="Введите имя игрока 1:")
        text_name1 = Entry(window, width=25, font=("Tahoma", 12), fg="Black", bd=3)
        self.create_window(WIDTH / 2, HEIGHT / 4.5, window=text_name1, anchor="center")
        self.install_btn(WIDTH / 2, HEIGHT / 1.8, "Ок", 15)

        text_name1.focus_force()
        text_name1.bind("<Return>", lambda event="", name1=text_name1, name2="Компьютер": self.load_name(event, name1, name2))
        self.btn.bind("<Button-1>", lambda event="", name1=text_name1, name2="Компьютер": self.load_name(event, name1, name2))

        self.btn_back(WIDTH / 2, HEIGHT / 1.4, "Choice_name")

    def menu_1x1(self):
        # Ввод имени первого игрока:
        self.create_text(WIDTH / 2, HEIGHT / 6, anchor="center", fill="Black", font=("Tahoma", 14), text="Введите имя 1-го игрока:")
        text_name1 = Entry(window, width=25, font=("Tahoma", 12), fg="Black", bd=3)
        self.create_window(WIDTH / 2, HEIGHT / 4.5, window=text_name1, anchor="center")

        # Ввод имени второго игрока:
        self.create_text(WIDTH / 2, HEIGHT / 3.2, anchor="center", fill="Black", font=("Tahoma", 14), text="Введите имя 2-го игрока:")
        text_name2 = Entry(window, width=25, font=("Tahoma", 12), fg="Black", bd=3)
        self.create_window(WIDTH / 2, HEIGHT / 2.7, window=text_name2, anchor="center")

        self.install_btn(WIDTH / 2, HEIGHT / 1.8, "Ок", 15)

        text_name1.focus_force()
        text_name1.bind("<Return>", lambda event="", element=text_name2: self.change_focus(event, element))
        text_name2.bind("<Return>", lambda event="", name1=text_name1, name2=text_name2: self.load_name(event, name1, name2))
        self.btn.bind("<Button-1>", lambda event="", name1=text_name1, name2=text_name2: self.load_name(event, name1, name2))

        self.btn_back(WIDTH / 2, HEIGHT / 1.4, "Choice_name")

    def choice_xo(self):
        self.random_number = randint(1, 2)
        self.dict_choice = {"1": list(self.who_choice.keys())[0], "2": list(self.who_choice.keys())[1]}
        if self.mode == "1 на 1":
            self.create_text(WIDTH / 2, HEIGHT / 6, anchor="center", fill="Black", font=("Tahoma", 15), text=f"{self.dict_choice[str(self.random_number)]} выбирает (X) или (O):")
            self.install_btn(WIDTH / 2, HEIGHT / 3, "Крестик (X)", 15)
            self.install_btn(WIDTH / 2, HEIGHT / 2, "Нолик (O)", 15)
            self.btn_back(WIDTH / 2, HEIGHT / 1.52, "Choice_x_o")
        else:
            self.computer_choice()

    def computer_choice(self):
        self.create_text(WIDTH / 2, HEIGHT / 6, anchor="center", fill="Black", font=("Tahoma", 15), text=f"{self.dict_choice[str(self.random_number)]} выбирает (X) или (O):")
        if self.dict_choice[str(self.random_number)] == "Компьютер":
            if self.menu_now == "level_bot" and self.random_number == 2:
                pass
            else:
                self.random_number_bot = randint(1, 2)
            if self.random_number_bot == 1:
                self.who_choice[list(self.who_choice.keys())[0]] = "Нолик (O)"
                self.who_choice[list(self.who_choice.keys())[1]] = "Крестик (X)"
            else:
                self.who_choice[list(self.who_choice.keys())[0]] = "Крестик (X)"
                self.who_choice[list(self.who_choice.keys())[1]] = "Нолик (O)"

            self.create_text(WIDTH / 2, HEIGHT / 3, anchor="center", fill="Black", font=("Tahoma", 13), text=f"Компьютер выбрал: {list(self.who_choice.values())[1]}")
            self.create_text(WIDTH / 2, HEIGHT / 2.3, anchor="center", fill="Black", font=("Tahoma", 13), text=f"Вам достался: {list(self.who_choice.values())[0]}")
            self.install_btn(WIDTH / 2, HEIGHT / 1.7, "Ок", 15)
            self.btn_back(WIDTH / 2, HEIGHT / 1.35, "Choice_x_o")
        else:
            self.install_btn(WIDTH / 2, HEIGHT / 3, "Крестик (X)", 15)
            self.install_btn(WIDTH / 2, HEIGHT / 2, "Нолик (O)", 15)
            self.btn_back(WIDTH / 2, HEIGHT / 1.52, "Choice_x_o")

    def menu_pause(self):
        name_btn_menu = ["Продолжить", "Заново", "Меню", "Выйти из игры"]
        self.create_text(WIDTH / 2, HEIGHT / 6, anchor="center", fill="Black", font=("Tahoma", 24), text="Пауза")
        for i in range(1, 5):
            self.install_btn(WIDTH / 2, HEIGHT / 5 + (85 * i), name_btn_menu[i - 1], 15)
        self.menu_now = "menu_pause"

    def winner_menu(self):
        self.delete(ALL)
        name_btn_menu = ["Играть снова", "Меню", "Выйти из игры"]
        self.create_text(WIDTH / 2, HEIGHT / 6, anchor="center", fill="Black", font=("Tahoma", 24), text=self.winner)
        for i in range(1, 4):
            self.install_btn(WIDTH / 2, HEIGHT / 5 + (85 * i), name_btn_menu[i - 1], 15)
        self.menu_now = "winner"

    def choice_level_bot(self):
        self.create_text(WIDTH / 2, HEIGHT / 6, anchor="center", fill="Black", font=("Tahoma", 14), text="Выберите уровень игры компьютера:")

        name_btn_menu = ["Низкий", "Средний", "Высокий", "Назад"]
        for i in range(1, 5):
            self.install_btn(WIDTH / 2, HEIGHT / 5 + (85 * i), name_btn_menu[i - 1], 15)
        self.menu_now = "level_bot"

    def change_name_going(self):
        sign = self.who_choice.get(self.step)
        num_index = list(self.who_choice.values()).index(sign)
        if num_index == 1:
            self.step = list(self.who_choice.keys())[0]
        else:
            self.step = list(self.who_choice.keys())[1]
        self.create_text(WIDTH / 3.23, WIDTH / 28, anchor="nw", fill="Black", font=("Tahoma", 15), text=self.step, tag="text")
        return sign

    def think_bot(self):
        sign = self.who_choice.get(self.step)
        if sign == "Крестик (X)":
            sign = "x"
            sign1 = "o"
        else:
            sign = "o"
            sign1 = "x"

        win, index1 = self.think_bot_win(sign)
        deff, index2 = self.think_bot_def(sign1)
        go, index3 = self.think_bot_go(sign, sign1)

        if win != "" and deff != "":
            self.click_obj = index1
        if win != "" and deff == "":
            self.click_obj = index1
        if win == "" and deff != "":
            self.click_obj = index2
        if win == "" and deff == "" and go != "":
            self.click_obj = index3

        if self.choice_players_obj[self.click_obj] != "":
            self.bad_level_bot()
        else:
            find_obj = self.find_withtag("rect")[self.click_obj]
            coords = self.coords(find_obj)
            self.coords_x[self.click_obj], self.coords_y[self.click_obj] = [coords[0], coords[2]], [coords[1], coords[3]]
            self.start_game(True, coords)

    def bad_level_bot(self):
        sign = self.who_choice.get(self.step)
        if sign == "Крестик (X)":
            sign = "x"
        else:
            sign = "o"

        win, index1 = self.think_bot_win(sign)
        if win != "":
            self.click_obj = index1
        else:
            while True:
                index_random = randint(0, 8)
                if self.choice_players_obj[index_random] != "":
                    continue
                self.click_obj = index_random
                break
        find_obj = self.find_withtag("rect")[self.click_obj]
        coords = self.coords(find_obj)
        self.coords_x[self.click_obj], self.coords_y[self.click_obj] = [coords[0], coords[2]], [coords[1], coords[3]]
        self.start_game(True, coords)

    def average_level_bot(self):
        if self.number == 0:
            self.bad_level_bot()
            self.number = 1
        else:
            self.think_bot()
            self.number = 0

    def think_bot_win(self, sign):
        if (self.choice_players_obj[3] == sign and self.choice_players_obj[6] == sign) and self.choice_players_obj[0] == "":
            self.click_obj = 0
        elif (self.choice_players_obj[4] == sign and self.choice_players_obj[8] == sign) and self.choice_players_obj[0] == "":
            self.click_obj = 0
        elif (self.choice_players_obj[1] == sign and self.choice_players_obj[2] == sign) and self.choice_players_obj[0] == "":
            self.click_obj = 0
        elif (self.choice_players_obj[4] == sign and self.choice_players_obj[7] == sign) and self.choice_players_obj[1] == "":
            self.click_obj = 1
        elif (self.choice_players_obj[0] == sign and self.choice_players_obj[2] == sign) and self.choice_players_obj[1] == "":
            self.click_obj = 1
        elif (self.choice_players_obj[0] == sign and self.choice_players_obj[1] == sign) and self.choice_players_obj[2] == "":
            self.click_obj = 2
        elif (self.choice_players_obj[4] == sign and self.choice_players_obj[6] == sign) and self.choice_players_obj[2] == "":
            self.click_obj = 2
        elif (self.choice_players_obj[5] == sign and self.choice_players_obj[8] == sign) and self.choice_players_obj[2] == "":
            self.click_obj = 2
        elif (self.choice_players_obj[4] == sign and self.choice_players_obj[5] == sign) and self.choice_players_obj[3] == "":
            self.click_obj = 3
        elif (self.choice_players_obj[0] == sign and self.choice_players_obj[6] == sign) and self.choice_players_obj[3] == "":
            self.click_obj = 3
        elif (self.choice_players_obj[3] == sign and self.choice_players_obj[5] == sign) and self.choice_players_obj[4] == "":
            self.click_obj = 4
        elif (self.choice_players_obj[2] == sign and self.choice_players_obj[6] == sign) and self.choice_players_obj[4] == "":
            self.click_obj = 4
        elif (self.choice_players_obj[0] == sign and self.choice_players_obj[8] == sign) and self.choice_players_obj[4] == "":
            self.click_obj = 4
        elif (self.choice_players_obj[1] == sign and self.choice_players_obj[7] == sign) and self.choice_players_obj[4] == "":
            self.click_obj = 4
        elif (self.choice_players_obj[4] == sign and self.choice_players_obj[3] == sign) and self.choice_players_obj[5] == "":
            self.click_obj = 5
        elif (self.choice_players_obj[2] == sign and self.choice_players_obj[8] == sign) and self.choice_players_obj[5] == "":
            self.click_obj = 5
        elif (self.choice_players_obj[0] == sign and self.choice_players_obj[3] == sign) and self.choice_players_obj[6] == "":
            self.click_obj = 6
        elif (self.choice_players_obj[8] == sign and self.choice_players_obj[7] == sign) and self.choice_players_obj[6] == "":
            self.click_obj = 6
        elif (self.choice_players_obj[4] == sign and self.choice_players_obj[2] == sign) and self.choice_players_obj[6] == "":
            self.click_obj = 6
        elif (self.choice_players_obj[4] == sign and self.choice_players_obj[1] == sign) and self.choice_players_obj[7] == "":
            self.click_obj = 7
        elif (self.choice_players_obj[6] == sign and self.choice_players_obj[8] == sign) and self.choice_players_obj[7] == "":
            self.click_obj = 7
        elif (self.choice_players_obj[0] == sign and self.choice_players_obj[4] == sign) and self.choice_players_obj[8] == "":
            self.click_obj = 8
        elif (self.choice_players_obj[6] == sign and self.choice_players_obj[7] == sign) and self.choice_players_obj[8] == "":
            self.click_obj = 8
        elif (self.choice_players_obj[2] == sign and self.choice_players_obj[5] == sign) and self.choice_players_obj[8] == "":
            self.click_obj = 8
        if self.choice_players_obj[self.click_obj] != "":
            return "", ""
        else:
            return "win", self.click_obj

    def think_bot_def(self, sign1):
        if (self.choice_players_obj[3] == sign1 and self.choice_players_obj[6] == sign1) and self.choice_players_obj[0] == "":
            self.click_obj = 0
        elif (self.choice_players_obj[4] == sign1 and self.choice_players_obj[8] == sign1) and self.choice_players_obj[0] == "":
            self.click_obj = 0
        elif (self.choice_players_obj[1] == sign1 and self.choice_players_obj[2] == sign1) and self.choice_players_obj[0] == "":
            self.click_obj = 0
        elif (self.choice_players_obj[4] == sign1 and self.choice_players_obj[7] == sign1) and self.choice_players_obj[1] == "":
            self.click_obj = 1
        elif (self.choice_players_obj[0] == sign1 and self.choice_players_obj[2] == sign1) and self.choice_players_obj[1] == "":
            self.click_obj = 1
        elif (self.choice_players_obj[0] == sign1 and self.choice_players_obj[1] == sign1) and self.choice_players_obj[2] == "":
            self.click_obj = 2
        elif (self.choice_players_obj[4] == sign1 and self.choice_players_obj[6] == sign1) and self.choice_players_obj[2] == "":
            self.click_obj = 2
        elif (self.choice_players_obj[5] == sign1 and self.choice_players_obj[8] == sign1) and self.choice_players_obj[2] == "":
            self.click_obj = 2
        elif (self.choice_players_obj[4] == sign1 and self.choice_players_obj[5] == sign1) and self.choice_players_obj[3] == "":
            self.click_obj = 3
        elif (self.choice_players_obj[0] == sign1 and self.choice_players_obj[6] == sign1) and self.choice_players_obj[3] == "":
            self.click_obj = 3
        elif (self.choice_players_obj[3] == sign1 and self.choice_players_obj[5] == sign1) and self.choice_players_obj[4] == "":
            self.click_obj = 4
        elif (self.choice_players_obj[2] == sign1 and self.choice_players_obj[6] == sign1) and self.choice_players_obj[4] == "":
            self.click_obj = 4
        elif (self.choice_players_obj[0] == sign1 and self.choice_players_obj[8] == sign1) and self.choice_players_obj[4] == "":
            self.click_obj = 4
        elif (self.choice_players_obj[1] == sign1 and self.choice_players_obj[7] == sign1) and self.choice_players_obj[4] == "":
            self.click_obj = 4
        elif (self.choice_players_obj[0] == sign1 and self.choice_players_obj[6] == sign1) and self.choice_players_obj[4] == "":
            self.click_obj = 4
        elif (self.choice_players_obj[4] == sign1 and self.choice_players_obj[3] == sign1) and self.choice_players_obj[5] == "":
            self.click_obj = 5
        elif (self.choice_players_obj[2] == sign1 and self.choice_players_obj[8] == sign1) and self.choice_players_obj[5] == "":
            self.click_obj = 5
        elif (self.choice_players_obj[0] == sign1 and self.choice_players_obj[3] == sign1) and self.choice_players_obj[6] == "":
            self.click_obj = 6
        elif (self.choice_players_obj[8] == sign1 and self.choice_players_obj[7] == sign1) and self.choice_players_obj[6] == "":
            self.click_obj = 6
        elif (self.choice_players_obj[4] == sign1 and self.choice_players_obj[2] == sign1) and self.choice_players_obj[6] == "":
            self.click_obj = 6
        elif (self.choice_players_obj[4] == sign1 and self.choice_players_obj[1] == sign1) and self.choice_players_obj[7] == "":
            self.click_obj = 7
        elif (self.choice_players_obj[6] == sign1 and self.choice_players_obj[8] == sign1) and self.choice_players_obj[7] == "":
            self.click_obj = 7
        elif (self.choice_players_obj[0] == sign1 and self.choice_players_obj[4] == sign1) and self.choice_players_obj[8] == "":
            self.click_obj = 8
        elif (self.choice_players_obj[6] == sign1 and self.choice_players_obj[7] == sign1) and self.choice_players_obj[8] == "":
            self.click_obj = 8
        elif (self.choice_players_obj[2] == sign1 and self.choice_players_obj[5] == sign1) and self.choice_players_obj[8] == "":
            self.click_obj = 8

        if self.choice_players_obj[self.click_obj] != "":
            return "", ""
        else:
            return "def", self.click_obj

    def think_bot_go(self, sign, sign1):  # sign - комп, sign1 - игрок
        if self.choice_players_obj[4] == sign1 and self.choice_players_obj[0] == "" and self.choice_players_obj[2] == "" and self.choice_players_obj[6] == "" and self.choice_players_obj[8] == "":
            list = [0, 2, 6, 8]
            self.click_obj = choice(list)
        if self.choice_players_obj[0] == sign1 or self.choice_players_obj[2] == sign1 or self.choice_players_obj[6] == sign1 or self.choice_players_obj[8] == sign1 and self.choice_players_obj[4] == "":
            self.click_obj = 4
        if self.choice_players_obj[3] == sign1 and self.choice_players_obj[6] == "":
            self.click_obj = 6
        if self.choice_players_obj[0] == sign1 and self.choice_players_obj[8] == sign1 and self.choice_players_obj[1] == "" and self.choice_players_obj[3] == "" and self.choice_players_obj[5] == "" and self.choice_players_obj[7] == "":
            list = [1, 3, 5, 7]
            self.click_obj = choice(list)
        if self.choice_players_obj[2] == sign1 and self.choice_players_obj[6] == sign1 and self.choice_players_obj[1] == "" and self.choice_players_obj[3] == "" and self.choice_players_obj[5] == "" and self.choice_players_obj[7] == "":
            list = [1, 3, 5, 7]
            self.click_obj = choice(list)
        if self.choice_players_obj[3] == sign1 and self.choice_players_obj[7] == sign1 and self.choice_players_obj[6] == "":
            self.click_obj = 6
        if self.choice_players_obj[1] == sign1 and self.choice_players_obj[3] == sign1 and self.choice_players_obj[0] == "":
            self.click_obj = 0
        if self.choice_players_obj[0] == sign and self.choice_players_obj[7] == sign and self.choice_players_obj[1] == "":
            self.click_obj = 1

        if self.choice_players_obj[self.click_obj] != "":
            return "", ""
        else:
            return "go", self.click_obj

    def user_going(self):
        try:
            find_obj = self.find_withtag("rect")[self.click_obj]
            coords = self.coords(find_obj)
            self.start_game(True, coords)
        except IndexError:
            pass

    def start_game(self, start, coords):
        self.menu_now = "game"
        try:
            if self.choice_players_obj[self.click_obj] == "":
                self.delete("text", "krest_text", "nolik_text")

                sign = self.change_name_going()

                if sign == "Крестик (X)":
                    self.create_image((coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2, image=self.obj_krestik, anchor="center", tag="krest")
                    self.obj_nolik = self.create_oval(WIDTH / 3, WIDTH / 7, HEIGHT / 2.5, HEIGHT / 3.75, width=12, tag="nolik_text")
                    self.choice_players_obj[self.click_obj] = "x"
                else:
                    self.obj_nolik = self.create_oval(coords[0] + 20, coords[1] + 20, coords[2] - 20, coords[3] - 20, width=12, tag="nolik")
                    self.create_image(WIDTH / 3, WIDTH / 7, image=self.obj_krestik, anchor="nw", tag="krest_text")
                    self.choice_players_obj[self.click_obj] = "o"

                self.winner, self.winner_obj = self.result_win()
                if self.winner != None or self.winner == "Ничья":
                    self.delete("text", "krest_text", "nolik_text", "what", "going", "pause")
                    self.show_winner()
                else:
                    if self.step == "Компьютер" and self.mode_bot == "Низкий":
                        self.bad_level_bot()
                    if self.step == "Компьютер" and self.mode_bot == "Средний":
                        self.average_level_bot()
                    if self.step == "Компьютер" and self.mode_bot == "Высокий":
                        self.think_bot()
        except IndexError:
            pass

    def continue_game(self):
        self.load_objects(False)
        self.delete("text")
        self.delete("krest_text")
        self.delete("nolik_text")
        self.create_text(WIDTH / 3.23, WIDTH / 28, anchor="nw", fill="Black", font=("Tahoma", 15), text=self.step, tag="text")

        sign = self.who_choice.get(self.step)
        if sign == "Крестик (X)":
            self.create_image(WIDTH / 3, WIDTH / 7, image=self.obj_krestik, anchor="nw", tag="krest_text")
        else:
            self.obj_nolik = self.create_oval(WIDTH / 3, WIDTH / 7, HEIGHT / 2.5, HEIGHT / 3.75, width=12, tag="nolik_text")

        for i in range(len(self.choice_players_obj)):
            if self.choice_players_obj[i] == "x":
                self.create_image(int(self.coords_x[i][0] + self.coords_x[i][1]) / 2,
                                  int(self.coords_y[i][0] + self.coords_y[i][1]) / 2, image=self.obj_krestik, anchor="center", tag="krest")
            if self.choice_players_obj[i] == "o":
                self.obj_nolik = self.create_oval(int(self.coords_x[i][0]) + 20, int(self.coords_y[i][0]) + 20,
                                                  int(self.coords_x[i][1]) - 20, int(self.coords_y[i][1]) - 20, width=12, tag="nolik")

    def show_winner(self):
        self.create_text(WIDTH / 2, HEIGHT / 13, anchor="center", fill="Black", font=("Tahoma", 19), text=self.winner)
        self.install_btn(WIDTH / 2, HEIGHT / 5, "Ок", 10)
        self.change_color_winner()
        self.menu_now = "show_winner"

    def change_color_winner(self):
        for index in self.winner_obj:
            obj = self.find_withtag("rect")[index]
            self.itemconfigure(obj, fill="")

    def result_win(self):
        winner_x = ""
        winner_o = ""
        for keys in list(self.who_choice.keys()):
            if self.who_choice.get(keys) == "Крестик (X)":
                winner_x = f"Победитель: {keys}"
        for keys in list(self.who_choice.keys()):
            if self.who_choice.get(keys) == "Нолик (O)":
                winner_o = f"Победитель: {keys}"

        if self.choice_players_obj[0] == "x" and self.choice_players_obj[3] == "x" and self.choice_players_obj[6] == "x":
            return winner_x, [0, 3, 6]
        elif self.choice_players_obj[6] == "x" and self.choice_players_obj[7] == "x" and self.choice_players_obj[8] == "x":
            return winner_x, [6, 7, 8]
        elif self.choice_players_obj[0] == "x" and self.choice_players_obj[1] == "x" and self.choice_players_obj[2] == "x":
            return winner_x, [0, 1, 2]
        elif self.choice_players_obj[2] == "x" and self.choice_players_obj[5] == "x" and self.choice_players_obj[8] == "x":
            return winner_x, [2, 5, 8]
        elif self.choice_players_obj[3] == "x" and self.choice_players_obj[4] == "x" and self.choice_players_obj[5] == "x":
            return winner_x, [3, 4, 5]
        elif self.choice_players_obj[2] == "x" and self.choice_players_obj[4] == "x" and self.choice_players_obj[6] == "x":
            return winner_x, [2, 4, 6]
        elif self.choice_players_obj[0] == "x" and self.choice_players_obj[4] == "x" and self.choice_players_obj[8] == "x":
            return winner_x, [0, 4, 8]
        elif self.choice_players_obj[1] == "x" and self.choice_players_obj[4] == "x" and self.choice_players_obj[7] == "x":
            return winner_x, [1, 4, 7]

        elif self.choice_players_obj[0] == "o" and self.choice_players_obj[3] == "o" and self.choice_players_obj[6] == "o":
            return winner_o, [0, 3, 6]
        elif self.choice_players_obj[6] == "o" and self.choice_players_obj[7] == "o" and self.choice_players_obj[8] == "o":
            return winner_o, [6, 7, 8]
        elif self.choice_players_obj[0] == "o" and self.choice_players_obj[1] == "o" and self.choice_players_obj[2] == "o":
            return winner_o, [0, 1, 2]
        elif self.choice_players_obj[2] == "o" and self.choice_players_obj[5] == "o" and self.choice_players_obj[8] == "o":
            return winner_o, [2, 5, 8]
        elif self.choice_players_obj[3] == "o" and self.choice_players_obj[4] == "o" and self.choice_players_obj[5] == "o":
            return winner_o, [3, 4, 5]
        elif self.choice_players_obj[2] == "o" and self.choice_players_obj[4] == "o" and self.choice_players_obj[6] == "o":
            return winner_o, [2, 4, 6]
        elif self.choice_players_obj[0] == "o" and self.choice_players_obj[4] == "o" and self.choice_players_obj[8] == "o":
            return winner_o, [0, 4, 8]
        elif self.choice_players_obj[1] == "o" and self.choice_players_obj[4] == "o" and self.choice_players_obj[7] == "o":
            return winner_o, [1, 4, 7]

        a = 0
        for i in self.choice_players_obj:
            if i != "":
                a += 1
            if a == 9:
                return "Ничья", []
        return None, ""

    def btn_click(self, event):
       self.delete(ALL)
       if event.widget["text"] == "1 на 1":
           self.menu_1x1()

       elif event.widget["text"] == "С ботом":
           self.menu_vs_bot()

       elif event.widget["text"] == "Выйти из игры":
           if messagebox.askyesno("Выход из программы", "Хотите выйти?"):
               window.quit()
           else:
               if self.menu_now == "winner":
                   self.winner_menu()
               elif self.menu_now == "menu_pause":
                   self.menu_pause()
               else:
                   self.main_menu()
       elif event.widget["text"] == "Крестик (X)":
           if self.random_number == 1:
               self.who_choice = {list(self.who_choice.keys())[0]: "Крестик (X)", list(self.who_choice.keys())[1]: "Нолик (O)"}
           else:
               self.who_choice = {list(self.who_choice.keys())[0]: "Нолик (O)", list(self.who_choice.keys())[1]: "Крестик (X)"}
           if self.mode != "bot":
               self.load_objects(True)
           else:
               self.choice_level_bot()

       elif event.widget["text"] == "Нолик (O)":
           if self.random_number == 1:
               self.who_choice = {list(self.who_choice.keys())[0]: "Нолик (O)", list(self.who_choice.keys())[1]: "Крестик (X)"}
           else:
               self.who_choice = {list(self.who_choice.keys())[0]: "Крестик (X)", list(self.who_choice.keys())[1]: "Нолик (O)"}
           if self.mode != "bot":
               self.load_objects(True)
           else:
               self.choice_level_bot()

       elif event.widget["text"] == "Назад":
           if self.menu_now == "Choice_name":
               self.main_menu()
           elif self.menu_now == "Choice_x_o":
               if self.mode == "1 на 1":
                   self.menu_1x1()
               else:
                   self.menu_vs_bot()
           elif self.menu_now == "level_bot":
               self.computer_choice()

       elif event.widget["text"] == "Пауза":
           self.menu_pause()

       elif event.widget["text"] == "Продолжить":
           self.continue_game()

       elif event.widget["text"] == "Заново" or event.widget["text"] == "Играть снова":
           self.choice_players_obj = [""] * COUNT_OBJ
           self.load_objects(True)
           if self.mode_bot == "Низкий":
               if self.who_choice.get("Компьютер") == "Крестик (X)":
                   self.bad_level_bot()
           if self.mode_bot == "Средний":
               if self.who_choice.get("Компьютер") == "Крестик (X)":
                   self.average_level_bot()
           if self.mode_bot == "Высокий":
               if self.who_choice.get("Компьютер") == "Крестик (X)":
                   self.bad_level_bot()

       elif event.widget["text"] == "Меню":
           self.start_settings()
           self.main_menu()

       elif event.widget["text"] == "Ок":
            if self.menu_now == "show_winner":
                self.winner_menu()
            else:
                self.choice_level_bot()

       elif event.widget["text"] == "Низкий":
           self.mode_bot = event.widget["text"]
           self.load_objects(True)
           if self.who_choice.get("Компьютер") == "Крестик (X)":
               self.bad_level_bot()

       elif event.widget["text"] == "Средний":
           self.mode_bot = event.widget["text"]
           self.load_objects(True)
           if self.who_choice.get("Компьютер") == "Крестик (X)":
               self.average_level_bot()

       elif event.widget["text"] == "Высокий":
           self.mode_bot = event.widget["text"]
           self.load_objects(True)
           if self.who_choice.get("Компьютер") == "Крестик (X)":
               self.think_bot()

    def what_element_click(self, event):
        x = event.x
        y = event.y
        if (x >= 0 and x <= 135) and (y >= 180 and y <= 310):
            self.click_obj = 0
        elif (x >= 140 and x <= 275) and (y >= 180 and y <= 310):
            self.click_obj = 3
        elif (x >= 280 and x <= 418) and (y >= 180 and y <= 310):
            self.click_obj = 6
        elif (x >= 0 and x <= 135) and (y >= 320 and y <= 455):
            self.click_obj = 1
        elif (x >= 140 and x <= 275) and (y >= 320 and y <= 455):
            self.click_obj = 4
        elif (x >= 280 and x <= 418) and (y >= 320 and y <= 455):
            self.click_obj = 7
        elif (x >= 0 and x <= 135) and (y >= 460 and y <= 595):
            self.click_obj = 2
        elif (x >= 140 and x <= 275) and (y >= 460 and y <= 595):
            self.click_obj = 5
        elif (x >= 280 and x <= 418) and (y >= 460 and y <= 595):
            self.click_obj = 8
        else:
            self.click_obj = 9
        try:
            obj = self.find_withtag("rect")[self.click_obj]
            xy = self.coords(obj)
            self.coords_x[self.click_obj], self.coords_y[self.click_obj] = [xy[0], xy[2]], [xy[1], xy[3]]
        except IndexError:
            pass

        if self.menu_now == "show_winner":
            pass
        else:
            self.user_going()

    def change_focus(self, event, element):
        element.focus_force()


def close_window():
    if messagebox.askyesno("Выход из приложения", "Хотите выйти?"):
        window.quit()


window = Tk()
window.title("Крестики Нолики")
window.resizable(False, False)
window.board = Games()

w_user = window.winfo_screenwidth()
h_user = window.winfo_screenheight()
x = int(w_user / 2 - WIDTH / 2)
y = int(h_user / 2 - HEIGHT / 2)
window.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
window.iconbitmap(r"iconki\main.ico")
window.protocol("WM_DELETE_WINDOW", close_window)
window.mainloop()
