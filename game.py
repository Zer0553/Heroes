from pygame import mixer
from tkinter import *
import tkinter.messagebox as mb
import random
import keyboard
import sys
from PIL import ImageTk, Image


class Game:
    def __init__(self):
        self.windowgame = Tk()
        self.pole = []
        self.squad = [Unit(False), Unit(False)]
        self.castles_count = 1
        self.drova_igroka = 0
        self.kamen_igroka = 0
        self.drova_enemy = 0
        self.kamen_enenmy = 0
        self.offset = [0, 0]
        self.castle_coords = [1, 2]
        self.enemy_castle_coords = [10, 9]
        self.enemy_hero_coords = [self.enemy_castle_coords[0] - 1, self.enemy_castle_coords[1]]
        self.buttons = []
        self.enemy_squad = [Unit(True), Unit(True)]
        les = 0
        kamen = 0
        for i in range(11):
            self.pole.append([])
            for j in range(11):
                self.pole[i].append("0")
        curcle = 0
        no = False
        while (les + kamen) < 4:
            coords_x = random.randrange(1, 9)
            coords_y = random.randrange(1, 9)
            if self.pole[coords_x][coords_y] == '0' and coords_x != 10 and coords_x != 0 and\
                    coords_y != 0 and coords_y != 10:
                for g in [[0, 0], [1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]:
                    if coords_x + g[0] == 1 and coords_y + g[1] == 2:
                        no = True
                        break
                    if coords_x + g[0] == 10 and coords_y + g[1] == 9:
                        no = True
                        break
                if no:
                    curcle += 1
                    continue
                else:
                    if les <= 1:
                        self.pole[coords_x][coords_y] = "5"
                        if self.pole[coords_x][coords_y] == '5':
                            les += 1
                    else:
                        self.pole[coords_x][coords_y] = "6"
                        if self.pole[coords_x][coords_y] == '6':
                            kamen += 1
            curcle += 1
            if curcle > 1000000:
                break

        for i in range(len(self.pole)):
            for j in range(len(self.pole[i])):
                if self.pole[i][j] == '6' or self.pole[i][j] == '5':
                    try:
                        spawn = random.choice(
                            [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]])
                        if self.pole[i + spawn[0]][j + spawn[1]] == 0:
                            self.pole[i + spawn[0]][j + spawn[1]] = '7'
                        else:
                            while self.pole[i + spawn[0]][j + spawn[1]] != '0':
                                spawn = random.choice(
                                    [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]])
                            self.pole[i + spawn[0]][j + spawn[1]] = '7'
                        continue
                    except IndexError:
                        pass

        self.pole[self.castle_coords[0]][self.castle_coords[1]] = "3"
        self.pole[self.castle_coords[0] + 1][self.castle_coords[1]] = "4"
        self.pole[self.enemy_castle_coords[0]][self.enemy_castle_coords[1]] = "8"
        self.pole[self.enemy_castle_coords[0] - 1][self.enemy_castle_coords[1]] = "9"
        self.button_image_exit = PhotoImage(file='Data/exit.png')
        self.screen_width = int(self.windowgame.winfo_screenwidth())
        self.screen_height = int(self.windowgame.winfo_screenheight())
        self.ground_image = ImageTk.PhotoImage(Image.open('Data/grass.png').resize((220, 220)))
        self.water_image = ImageTk.PhotoImage(Image.open('Data/water.png').resize((220, 220)))
        self.castle_image = ImageTk.PhotoImage(Image.open('Data/castle.png').resize((220, 220)))
        self.hero_image = ImageTk.PhotoImage(Image.open('Data/hero.png').resize((170, 220)))
        self.les_image = ImageTk.PhotoImage(Image.open('Data/les.png').resize((220, 220)))
        self.kamen_image = ImageTk.PhotoImage(Image.open('Data/kamen.png').resize((220, 220)))
        self.enemy_hero_image = ImageTk.PhotoImage(Image.open('Data/enemy_hero.png').resize((170, 220)))
        self.enemy_castle_image = ImageTk.PhotoImage(Image.open('Data/enemy_castle.png').resize((220, 220)))
        self.les_igroka_image = ImageTk.PhotoImage(Image.open('Data/les_igroka.png').resize((220, 220)))
        self.kamen_igroka_image = ImageTk.PhotoImage(Image.open('Data/kamen_igroka.png').resize((220, 220)))
        self.les_enemy_image = ImageTk.PhotoImage(Image.open('Data/les_enemy.png').resize((220, 220)))
        self.kamen_enemy_image = ImageTk.PhotoImage(Image.open('Data/kamen_enemy.png').resize((220, 220)))
        self.enemy_image = ImageTk.PhotoImage(Image.open('Data/enemy.png').resize((220, 220)))
        self.empty_image = ImageTk.PhotoImage(
            Image.open('Data/empty.png').resize((int(self.screen_width), int(self.screen_height / 8) * 2)))
        self.button_caslte_create = ImageTk.PhotoImage(Image.open('Data/caslte_create.png'))
        self.log = Text(self.windowgame, width=int(self.screen_width / 14) - 130,
                        height=int(self.screen_height - self.screen_height / 8), wrap="word")
        self.log.insert(END, 'Добро пожаловать в "Герои"!\n'
                             'Чтобы сделать ход нажмите на поле, максимальная длинна хода - 3 клетки\n'
                             'Для движения камеры нажимайте на стрелочки\n'
                             'чтобы создать новых юнитов нажмите на замок\n')
        keyboard.on_press_key("left", lambda _: self.offset_increase('left'))
        keyboard.on_press_key("right", lambda _: self.offset_increase('right'))
        keyboard.on_press_key("up", lambda _: self.offset_increase('up'))
        keyboard.on_press_key("down", lambda _: self.offset_increase('down'))
        ui_background = Label(self.windowgame, image=self.empty_image)
        self.txt_drova = Label(self.windowgame, text='Дрова:' + str(self.drova_igroka), borderwidth=20, font=("Arial", 20))
        self.txt_kamen = Label(self.windowgame, text='Камень:' + str(self.kamen_igroka), borderwidth=20, font=("Arial", 20))
        self.button_build = Button(self.windowgame, image=self.button_caslte_create, command=self.caslte_create)
        exit_button = Button(self.windowgame, image=self.button_image_exit, command=sys.exit)
        self.txt_drova.place(x=self.screen_width - 200, y=self.screen_height - int(self.screen_height / 8) * 2 + 20)
        self.txt_kamen.place(x=self.screen_width - 200, y=self.screen_height - int(self.screen_height / 8) * 2 + 120)
        self.button_build.place(x=self.screen_width - 200, y=self.screen_height - int(self.screen_height / 8) * 2 + 220)
        exit_button.place(x=self.screen_width - 200, y=self.screen_height - int(self.screen_height / 8) * 2 + 320)
        ui_background.place(x=0, y=self.screen_height - int(self.screen_height / 8) * 2)
        self.log.place(x=int(self.screen_width - (self.screen_width / 12) * 2) + 20, y=0)
        self.focus_pole()
        self.draw_map()
        self.windowgame.attributes('-fullscreen', True)
        self.windowgame.mainloop()

    def move(self, type, row=0, colomn=0):
        for i in range(len(self.pole)):
            for j in range(len(self.pole[i])):
                if self.pole[i][j] == '4':
                    if i - (row + self.offset[0]) < -3:
                        self.log.insert(END, 'Далековато\n')
                        return
                    elif i - (row + self.offset[0]) > 3:
                        self.log.insert(END, 'Далековато\n')
                        return
                    elif j - (colomn + self.offset[1]) < -3:
                        self.log.insert(END, 'Далековато\n')
                        return
                    elif j - (colomn + self.offset[1]) > 3:
                        self.log.insert(END, 'Далековато\n')
                        return
                    elif i - (row + self.offset[0]) + j - (colomn + self.offset[1]) < -3:
                        self.log.insert(END, 'Далековато\n')
                    elif i - (row + self.offset[0]) + j - (colomn + self.offset[1]) > 3:
                        self.log.insert(END, 'Далековато\n')
        if type == 0:
            for i in range(len(self.pole)):
                for j in range(len(self.pole[i])):
                    if self.pole[i][j] == '4':
                        self.pole[i][j] = self.buttons[row][colomn].cget('text')
            self.pole[row + self.offset[0]][colomn + self.offset[1]] = '4'
            self.resources()
            a = self.move_enemy()
            if a == 'fight':
                self.fight(self.enemy_squad)
            else:
                self.focus_pole()
        elif type == 1:
            pass
        elif type == 2:
            for offset in [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]:
                if self.pole[row + self.offset[0] + offset[0]][colomn + self.offset[1] + offset[1]] == '7':
                    self.log.insert(END, 'Рядом враг! захват невозможен\n')
                    return
            self.check_alive()
            if len(self.squad) == 0:
                self.log.insert(END, 'Вам нужен минимум 1 юнит для захвата!\n')
                return
            for i in range(len(self.pole)):
                for j in range(len(self.pole[i])):
                    if self.pole[i][j] == '4':
                        self.pole[i][j] = self.buttons[row][colomn].cget('text')
            try:
                self.pole[row + self.offset[0]][colomn + self.offset[1]] = '5.1'
                self.pole[row + self.offset[0] + 1][colomn + self.offset[1]] = '4'
                self.focus_pole()
            except IndexError:
                self.pole[row + self.offset[0]][colomn + self.offset[1]] = '5.1'
                self.pole[row + self.offset[0] - 1][colomn + self.offset[1]] = '4'
                self.focus_pole()
            self.resources()
            self.log.insert(END, 'Вы заняли Лесопилку! 1 ваш юнит остался в ней\n')
            a = self.move_enemy()
            if a == 'fight':
                self.fight(self.enemy_squad)
            else:
                self.focus_pole()
            self.squad.pop()
        elif type == 4:
            self.check_alive()
            if len(self.squad) < 5:
                if self.drova_igroka >= 10:
                    self.drova_igroka -= 10
                    self.squad.append(Unit(False))
                    self.log.insert(END, 'Вы создали нового юнита! Всего юнитов ' + str(len(self.squad)) + '\n')
                else:
                    self.log.insert(END, 'У вас недостаточно дерева!\n')
            else:
                self.log.insert(END, 'Вы достигли максимума юнитов\n')
            for i in range(len(self.pole)):
                for j in range(len(self.pole[i])):
                    if self.pole[i][j] == '4':
                        self.pole[i][j] = '0'
            try:
                self.pole[row + self.offset[0] + 1][colomn + self.offset[1]] = '4'
            except IndexError:
                for offset in [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]:
                    if self.pole[row + self.offset[0] + offset[0]][colomn + self.offset[1] + offset[1]] == '0':
                        self.pole[row + self.offset[0] + 1][colomn + self.offset[1]] = '4'
                        break
            a = self.move_enemy()
            if a == 'fight':
                self.fight(self.enemy_squad)
            else:
                self.focus_pole()
            self.focus_pole()
        elif type == 3:
            for offset in [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]:
                if self.pole[row + self.offset[0] + offset[0]][colomn + self.offset[1] + offset[1]] == '7':
                    self.log.insert(END, 'Рядом враг! захват невозможен\n')
                    return
            if len(self.squad) == 0:
                self.log.insert(END, 'Вам нужен минимум 1 юнит для захвата!\n')
                return
            for i in range(len(self.pole)):
                for j in range(len(self.pole[i])):
                    if self.pole[i][j] == '4':
                        self.pole[i][j] = self.buttons[row][colomn].cget('text')
            try:
                self.pole[row + self.offset[0]][colomn + self.offset[1]] = '6.1'
                self.pole[row + self.offset[0] + 1][colomn + self.offset[1]] = '4'
                self.focus_pole()
            except IndexError:
                self.pole[row + self.offset[0]][colomn + self.offset[1]] = '6.1'
                self.pole[row + self.offset[0] - 1][colomn + self.offset[1]] = '4'
                self.focus_pole()
            self.resources()
            self.log.insert(END, 'Вы заняли Каменоломню! 1 ваш юнит остался в ней\n')
            a = self.move_enemy()
            if a == 'fight':
                self.fight(self.enemy_squad)
            else:
                self.focus_pole()
            self.squad.pop()
        elif type == 7:
            for i in range(len(self.pole)):
                for j in range(len(self.pole[i])):
                    if self.pole[i][j] == '4':
                        self.pole[i][j] = self.buttons[row][colomn].cget('text')
            self.check_alive()
            if len(self.squad) == 0:
                var = mb.showinfo("О нет!!", "Вы проиграли, нападать на врага \n без юнитов было опрометчиво")
                sys.exit()
            self.resources()
            self.move_enemy()
            self.fight()
            try:
                self.pole[row + self.offset[0]][colomn + self.offset[1]] = '4'
            except IndexError:
                self.pole[row + self.offset[0]][colomn + self.offset[1]] = '4'
        elif type == 8:
            for i in range(len(self.pole)):
                for j in range(len(self.pole[i])):
                    if self.pole[i][j] == '4':
                        self.pole[i][j] = self.buttons[row][colomn].cget('text')
            self.check_alive()
            if len(self.squad) == 0:
                var = mb.showinfo("О нет!!", "Вы проиграли, нападать на врага \n без юнитов было опрометчиво")
                sys.exit()
            self.resources()
            if len(self.enemy_squad) == 0:
                var = mb.showinfo("Ура!", "Вы победили, у вражеского героя небыло юнитов")
                sys.exit()
            self.fight(self.enemy_squad)
            for i in [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]:
                try:
                    if self.pole[row + self.offset[0] + i[0]][colomn + self.offset[1] + i[1]] == '0':
                        self.pole[row + self.offset[0] + i[0]][colomn + self.offset[1] + i[1]] = '4'
                        return
                except IndexError:
                    continue

        elif type == 9:
            if len(self.squad) == 0:
                self.log.insert(END, 'Вам нужен минимум 1 юнит для захвата!\n')
                return
            for i in range(len(self.pole)):
                for j in range(len(self.pole[i])):
                    if self.pole[i][j] == '4':
                        self.pole[i][j] = self.buttons[row][colomn].cget('text')
            for offset in [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]:
                try:
                    if self.pole[row + self.offset[0] + offset[0]][colomn + self.offset[1] + offset[1]] == '0':
                        self.pole[row + self.offset[0] + offset[0]][colomn + self.offset[1] + offset[1]] = '4'
                        break
                except IndexError:
                    continue
            for offset in [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]:
                try:
                    if self.pole[row + self.offset[0] + offset[0]][colomn + self.offset[1] + offset[1]] == '9':
                        if len(self.enemy_squad) < 1:
                            continue
                        else:
                            self.fight(self.enemy_squad)
                        return
                except IndexError:
                    continue
            self.pole[row + self.offset[0]][colomn + self.offset[1]] = '3'
            self.focus_pole()
            self.resources()
            self.log.insert(END, 'Вы заняли Замок противника! 1 ваш юнит остался в нем\n')
            self.check_end_game()
            a = self.move_enemy()
            if a == 'fight':
                self.fight(self.enemy_squad)
            else:
                self.focus_pole()
            self.squad.pop()

    def check_end_game(self):
        castles_enemy = 0
        castles_player = 0
        for i in self.pole:
            for j in i:
                if j == '3':
                    castles_player += 1
                elif j == '8':
                    castles_enemy += 1

        if castles_enemy == 0:
            var = mb.showinfo("Ура!", "Вы победили, на карте не осталось вражеских замков!")
            sys.exit()
        elif castles_player == 0:
            var = mb.showinfo("О нет!!", "Вы проиграли, на карте не осталось ваших замков!")
            sys.exit()


    def move_enemy(self):
        les_enemy = 0
        kamen_enemy = 0
        castle_enemy = 0
        for i in self.pole:
            for j in i:
                if j == '5.2':
                    les_enemy += 1
                elif j =='6.2':
                    kamen_enemy += 1
                elif j == '8':
                    castle_enemy += 1
        if les_enemy >= 1 and kamen_enemy >= 1 and self.kamen_enenmy >= 10:
            if self.pole[self.enemy_hero_coords[0] - 1][self.enemy_hero_coords[1]] == '0':
                self.pole[self.enemy_hero_coords[0] - 1][self.enemy_hero_coords[1]] = '8'
                self.kamen_enenmy -= 10
                return
            else:
                move = [0, 0]
                while self.pole[self.enemy_hero_coords[0] - 1 + move[0]][self.enemy_hero_coords[0] + move[1]] != '0':
                    move = random.choice([[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]])
                for i in range(len(self.pole)):
                    for j in range(len(self.pole[i])):
                        if self.pole[i][j] == '9':
                            self.pole[i][j] = '0'
                self.pole[self.enemy_hero_coords[0] + move[0]][self.enemy_hero_coords[0] + move[1]] = '9'
                self.enemy_hero_coords = [self.enemy_hero_coords[0] + move[0], self.enemy_hero_coords[0] + move[1]]
                self.pole[self.enemy_hero_coords[0] - 1][self.enemy_hero_coords[1]] = '8'
                self.kamen_enenmy -= 10
                return

        elif len(self.enemy_squad) >= 1 and les_enemy < 1:
            arr_of_les = []
            goal_to_les = [100, 100]
            for i in range(len(self.pole)):
                for j in range(len(self.pole[i])):
                    if self.pole[i][j] == '5' or self.pole[i][j] == '5.1':
                        arr_of_les.append([i, j])
            for i in arr_of_les:
                if (abs(goal_to_les[0] - self.enemy_hero_coords[0]) + abs(goal_to_les[1] - self.enemy_hero_coords[1])) > \
                        (abs(i[0] - self.enemy_hero_coords[0]) + abs(i[1] - self.enemy_hero_coords[1])):
                    goal_to_les = [i[0], i[1]]
            can_reach = []
            for i in range(-3, 3):
                for j in range(-3, 3):
                    try:
                        if self.enemy_hero_coords[0] + i < 0 or \
                                self.enemy_hero_coords[1] + j < 0:
                            continue
                        if self.pole[self.enemy_hero_coords[0] + i][self.enemy_hero_coords[1] + j] == '0':
                            can_reach.append([self.enemy_hero_coords[0] + i, self.enemy_hero_coords[1] + j])
                        if self.pole[self.enemy_hero_coords[0] + i][self.enemy_hero_coords[1] + j] == '5' or\
                                self.pole[self.enemy_hero_coords[0] + i][self.enemy_hero_coords[1] + j] == '5.1':
                            for offset in [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]:
                                all_enemies = []
                                if self.pole[self.enemy_hero_coords[0] + i + offset[0]]\
                                    [self.enemy_hero_coords[1] + j + offset[1]] == '7':
                                    all_enemies.append([self.enemy_hero_coords[0] + i + offset[0],
                                    self.enemy_hero_coords[1] + j + offset[1]])
                                    where = [self.enemy_hero_coords[0] + i + offset[0],
                                             self.enemy_hero_coords[1] + j + offset[1]]
                                    win = random.choices([1, 0], weights=[95, 15], k=1)[0]
                                    if win == 1:
                                        for i in range(len(self.pole)):
                                            for j in range(len(self.pole[i])):
                                                if self.pole[i][j] == '9':
                                                    self.pole[i][j] = '0'
                                        self.pole[where[0]][where[1]] = '9'
                                        self.enemy_hero_coords = [where[0], where[1]]
                                        return
                                    else:
                                        self.enemy_squad.pop()
                                        for i in range(len(self.pole)):
                                            for j in range(len(self.pole[i])):
                                                if self.pole[i][j] == '9':
                                                    self.pole[i][j] = '0'
                                        self.pole[where[0]][where[1]] = '9'
                                        self.enemy_hero_coords = [where[0], where[1]]
                                        return

                            if len(all_enemies) == 0:
                                self.pole[goal_to_les[0]][goal_to_les[1]] \
                                    = '5.2'
                                self.enemy_squad.pop()

                            return
                    except IndexError:
                        continue
            where = self.choose_node(can_reach, goal_to_les)
            for i in range(len(self.pole)):
                for j in range(len(self.pole[i])):
                    if self.pole[i][j] == '9':
                        self.pole[i][j] = '0'
            self.pole[where[0]][where[1]] = '9'
            self.enemy_hero_coords = [where[0], where[1]]
        elif len(self.enemy_squad) >= 2 and les_enemy >= 1 and kamen_enemy < 1:
            arr_of_les = []
            goal_to_les = [100, 100]
            for i in range(len(self.pole)):
                for j in range(len(self.pole[i])):
                    if self.pole[i][j] == '6' or self.pole[i][j] == '6.1':
                        arr_of_les.append([i, j])
            for i in arr_of_les:
                if (abs(goal_to_les[0] - self.enemy_hero_coords[0]) + abs(goal_to_les[1] - self.enemy_hero_coords[1])) > \
                        (abs(i[0] - self.enemy_hero_coords[0]) + abs(i[1] - self.enemy_hero_coords[1])):
                    goal_to_les = [i[0], i[1]]
            can_reach = []
            for i in range(-3, 3):
                for j in range(-3, 3):
                    try:
                        if self.enemy_hero_coords[0] + i < 0 or \
                                self.enemy_hero_coords[1] + j < 0:
                            continue
                        if self.pole[self.enemy_hero_coords[0] + i][self.enemy_hero_coords[1] + j] == '0':
                            can_reach.append([self.enemy_hero_coords[0] + i, self.enemy_hero_coords[1] + j])
                        if self.pole[self.enemy_hero_coords[0] + i][self.enemy_hero_coords[1] + j] == '6' or\
                                self.pole[self.enemy_hero_coords[0] + i][self.enemy_hero_coords[1] + j] == '6.1':
                            for offset in [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]:
                                all_enemies = []
                                if self.pole[self.enemy_hero_coords[0] + i + offset[0]]\
                                    [self.enemy_hero_coords[1] + j + offset[1]] == '7':
                                    all_enemies.append([self.enemy_hero_coords[0] + i + offset[0],
                                    self.enemy_hero_coords[1] + j + offset[1]])
                                    where = [self.enemy_hero_coords[0] + i + offset[0],
                                             self.enemy_hero_coords[1] + j + offset[1]]
                                    win = random.choices([1, 0], weights=[95, 15], k=1)[0]
                                    if win == 1:
                                        for i in range(len(self.pole)):
                                            for j in range(len(self.pole[i])):
                                                if self.pole[i][j] == '9':
                                                    self.pole[i][j] = '0'
                                        self.pole[where[0]][where[1]] = '9'
                                        self.enemy_hero_coords = [where[0], where[1]]
                                        return
                                    else:
                                        self.enemy_squad.pop()
                                        for i in range(len(self.pole)):
                                            for j in range(len(self.pole[i])):
                                                if self.pole[i][j] == '9':
                                                    self.pole[i][j] = '0'
                                        self.pole[where[0]][where[1]] = '9'
                                        self.enemy_hero_coords = [where[0], where[1]]
                                        return
                            if len(all_enemies) == 0:
                                self.pole[goal_to_les[0]][goal_to_les[1]] \
                                    = '6.2'
                                self.enemy_squad.pop()

                            return
                    except IndexError:
                        continue
            where = self.choose_node(can_reach, goal_to_les)
            for i in range(len(self.pole)):
                for j in range(len(self.pole[i])):
                    if self.pole[i][j] == '9':
                        self.pole[i][j] = '0'
            self.pole[where[0]][where[1]] = '9'
            self.enemy_hero_coords = [where[0], where[1]]
        elif len(self.enemy_squad) < 2 and les_enemy > 0:
            if self.drova_enemy >= 10 and len(self.enemy_squad) < 5:
                self.enemy_squad.append(Unit(True))
                self.drova_enemy -= 10
                return
            arr_of_les = []
            goal_to_les = [100, 100]
            for i in range(len(self.pole)):
                for j in range(len(self.pole[i])):
                    if self.pole[i][j] == '8':
                        arr_of_les.append([i, j])
            for i in arr_of_les:
                if (abs(goal_to_les[0] - self.enemy_hero_coords[0]) + abs(goal_to_les[1] - self.enemy_hero_coords[1])) > \
                        (abs(i[0] - self.enemy_hero_coords[0]) + abs(i[1] - self.enemy_hero_coords[1])):
                    goal_to_les = [i[0], i[1]]
            can_reach = []
            for i in range(-3, 3):
                for j in range(-3, 3):
                    try:
                        if self.pole[self.enemy_hero_coords[0] + i][self.enemy_hero_coords[1] + j] == '0':
                            if self.enemy_hero_coords[0] + i >= 0 and self.enemy_hero_coords[0] >= 0 + j:
                                can_reach.append([self.enemy_hero_coords[0] + i, self.enemy_hero_coords[1] + j])
                        elif self.enemy_hero_coords[0] + i >= 0 and self.enemy_hero_coords[0] >= 0 + j and\
                                self.pole[self.enemy_hero_coords[0] + i][self.enemy_hero_coords[1] + j] == '8':
                            where = [self.enemy_hero_coords[0] + i - 1, self.enemy_hero_coords[1] + j]
                            for i in range(len(self.pole)):
                                for j in range(len(self.pole[i])):
                                    if self.pole[i][j] == '9':
                                        self.pole[i][j] = '0'
                            self.pole[where[0]][where[1]] = '9'
                            self.enemy_hero_coords = [where[0], where[1]]
                            return
                    except IndexError:
                        continue
            where = self.choose_node(can_reach, goal_to_les)
            for i in range(len(self.pole)):
                for j in range(len(self.pole[i])):
                    if self.pole[i][j] == '9':
                        self.pole[i][j] = '0'
            self.pole[where[0]][where[1]] = '9'
            self.enemy_hero_coords = [where[0], where[1]]
        elif len(self.enemy_squad) >= 3 and castle_enemy >= 2:
            arr_of_les = []
            goal_to_les = [100, 100]
            for i in range(len(self.pole)):
                for j in range(len(self.pole[i])):
                    if self.pole[i][j] == '3':
                        arr_of_les.append([i, j])
            for i in arr_of_les:
                if (abs(goal_to_les[0] - self.enemy_hero_coords[0]) + abs(goal_to_les[1] - self.enemy_hero_coords[1])) > \
                        (abs(i[0] - self.enemy_hero_coords[0]) + abs(i[1] - self.enemy_hero_coords[1])):
                    goal_to_les = [i[0], i[1]]
            can_reach = []
            for i in range(-3, 3):
                for j in range(-3, 3):
                    try:
                        if self.enemy_hero_coords[0] + i < 0 or \
                                self.enemy_hero_coords[1] + j < 0:
                            continue
                        if self.pole[self.enemy_hero_coords[0] + i][self.enemy_hero_coords[1] + j] == '0':
                            can_reach.append([self.enemy_hero_coords[0] + i, self.enemy_hero_coords[1] + j])
                        if self.pole[self.enemy_hero_coords[0] + i][self.enemy_hero_coords[1] + j] == '3':
                            for offset in [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]:
                                if self.pole[self.enemy_hero_coords[0] + i + offset[0]] \
                                        [self.enemy_hero_coords[1] + j + offset[1]] == '4':
                                    if len(self.squad) >= 2:
                                        if self.pole[self.enemy_hero_coords[0] + i + offset[0] + 1]\
                                            [self.enemy_hero_coords[1] + j + offset[1]] =='0':
                                            where = [self.enemy_hero_coords[0] + i + offset[0] + 1,
                                                     self.enemy_hero_coords[1] + j + offset[1]]
                                        else:
                                            where = [self.enemy_hero_coords[0] + i + offset[0] - 1,
                                                     self.enemy_hero_coords[1] + j + offset[1]]
                                        win = random.choices([1, 0], weights=[95, 15], k=1)[0]
                                        if win == 1:
                                            for i in range(len(self.pole)):
                                                for j in range(len(self.pole[i])):
                                                    if self.pole[i][j] == '9':
                                                        self.pole[i][j] = '0'
                                            self.pole[where[0]][where[1]] = '9'
                                            self.enemy_hero_coords = [where[0], where[1]]
                                            return
                                        else:
                                            self.enemy_squad.pop()
                                            for i in range(len(self.pole)):
                                                for j in range(len(self.pole[i])):
                                                    if self.pole[i][j] == '9':
                                                        self.pole[i][j] = '0'
                                            self.pole[where[0]][where[1]] = '9'
                                            self.enemy_hero_coords = [where[0], where[1]]
                                            return
                            self.pole[goal_to_les[0]][goal_to_les[1]] \
                                = '8'
                            self.check_end_game()
                            self.enemy_squad.pop()

                            return
                    except IndexError:
                        continue
            where = self.choose_node(can_reach, goal_to_les)
            for i in range(len(self.pole)):
                for j in range(len(self.pole[i])):
                    if self.pole[i][j] == '9':
                        self.pole[i][j] = '0'
            self.pole[where[0]][where[1]] = '9'
            self.enemy_hero_coords = [where[0], where[1]]
        elif len(self.enemy_squad) > len(self.squad):
            for i in range(-1, 1):
                for j in range(-1, 1):
                    try:
                        if self.enemy_hero_coords[0] + i >= 0 and self.enemy_hero_coords[0] >= 0 + j and \
                                self.pole[self.enemy_hero_coords[0] + i][self.enemy_hero_coords[1] + j] == '4':
                            where = [self.enemy_hero_coords[0] + i - 1, self.enemy_hero_coords[1] + j]
                            for i in range(len(self.pole)):
                                for j in range(len(self.pole[i])):
                                    if self.pole[i][j] == '9':
                                        self.pole[i][j] = '0'
                            if self.pole[where[0]][where[1]] == '0':
                                self.pole[where[0]][where[1]] = '9'
                            else:
                                self.pole[where[0] + 2][where[1]] = '9'
                            self.enemy_hero_coords = [where[0], where[1]]
                            return 'fight'
                    except IndexError:
                        continue
        else:
            if self.drova_enemy >= 10 and len(self.enemy_squad) < 5:
                self.log.insert(END, 'создан юнит')
                self.enemy_squad.append(Unit(True))
                self.drova_enemy -= 10
                return
            arr_of_les = []
            goal_to_les = [100, 100]
            for i in range(len(self.pole)):
                for j in range(len(self.pole[i])):
                    if self.pole[i][j] == '8':
                        arr_of_les.append([i, j])
            for i in arr_of_les:
                if (abs(goal_to_les[0] - self.enemy_hero_coords[0]) + abs(goal_to_les[1] - self.enemy_hero_coords[1])) > \
                        (abs(i[0] - self.enemy_hero_coords[0]) + abs(i[1] - self.enemy_hero_coords[1])):
                    goal_to_les = [i[0], i[1]]
            can_reach = []
            for i in range(-3, 3):
                for j in range(-3, 3):
                    try:
                        if self.pole[self.enemy_hero_coords[0] + i][self.enemy_hero_coords[1] + j] == '0':
                            if self.enemy_hero_coords[0] + i >= 0 and self.enemy_hero_coords[0] >= 0 + j:
                                can_reach.append([self.enemy_hero_coords[0] + i, self.enemy_hero_coords[1] + j])
                        elif self.enemy_hero_coords[0] + i >= 0 and self.enemy_hero_coords[0] >= 0 + j and \
                                self.pole[self.enemy_hero_coords[0] + i][self.enemy_hero_coords[1] + j] == '8':
                            where = [self.enemy_hero_coords[0] + i - 1, self.enemy_hero_coords[1] + j]
                            for i in range(len(self.pole)):
                                for j in range(len(self.pole[i])):
                                    if self.pole[i][j] == '9':
                                        self.pole[i][j] = '0'
                            self.pole[where[0]][where[1]] = '9'
                            self.enemy_hero_coords = [where[0], where[1]]
                            return
                    except IndexError:
                        continue
            where = self.choose_node(can_reach, goal_to_les)
            for i in range(len(self.pole)):
                for j in range(len(self.pole[i])):
                    if self.pole[i][j] == '9':
                        self.pole[i][j] = '0'
            self.pole[where[0]][where[1]] = '9'
            self.enemy_hero_coords = [where[0], where[1]]

    def check_alive(self):
        for i in self.squad:
            if i.is_dead():
                self.squad.remove(i)

    def offset_increase(self, event):
        if event == 'left':
            self.offset[1] -= 1
            if self.offset[1] < 0:
                self.offset[1] += 1
                return
            try:
                for i in range(6):
                    for j in range(10):
                        self.pole[i + self.offset[0]][j + self.offset[1]]
                self.focus_pole()
            except IndexError:
                self.offset[1] += 1
                return
        elif event == 'right':
            self.offset[1] += 1
            try:
                for i in range(6):
                    for j in range(10):
                        self.pole[i + self.offset[0]][j + self.offset[1]]
                self.focus_pole()
            except IndexError:
                self.offset[1] -= 1
                return
        elif event == 'up':
            self.offset[0] -= 1
            if self.offset[0] < 0:
                self.offset[0] += 1
                return
            try:
                for i in range(6):
                    for j in range(10):
                        self.pole[i + self.offset[0]][j + self.offset[1]]
                self.focus_pole()
            except IndexError:
                self.offset[0] += 1
                return
        elif event == 'down':
            self.offset[0] += 1
            try:
                for i in range(6):
                    for j in range(10):
                        self.pole[i + self.offset[0]][j + self.offset[1]]
                self.focus_pole()
            except IndexError:
                self.offset[0] -= 1
                return

    def fight(self, enemies=[]):
        self.log.delete('1.0', END)
        self.button_build.destroy()
        for i in self.buttons:
            for j in i:
                j.grid_remove()
        self.buttons = []
        self.pole_fight = []
        self.choosen_pawn = [0]
        self.type_battle = 0
        units_count = len(self.squad)
        if len(enemies) == 0:
            self.enemies = []
            if units_count < 3:
                self.enemies.append(Unit(True))
            elif units_count == 3:
                for _ in range(3):
                    self.enemies.append(Unit(True))
            else:
                for _ in range(4):
                    self.enemies.append(Unit(True))
            enemies_count = len(self.enemies)
        else:
            self.enemies = enemies
            enemies_count = len(self.enemies)
            self.type_battle = 1
        for i in range(5):
            self.pole_fight.append([])
            for j in range(7):
                if j == 0 and units_count > 0:
                    units_count -= 1
                    self.pole_fight[i].append(self.squad[units_count])
                elif j == 6 and enemies_count > 0:
                    enemies_count -= 1
                    self.pole_fight[i].append(self.enemies[enemies_count])
                else:
                    self.pole_fight[i].append('0')
        self.draw_fight()

    def draw_fight(self):
        if self.check_loose_fight():
            for j in self.buttons:
                for i in j:
                    i.grid_remove()
            self.buttons = []
            self.pole_fight = []
            self.choosen_pawn = [0]
            self.log.delete('1.0', END)
            self.squad = []
            self.log.insert(END, 'Бой окончен! Вы проиграли!!\n')
            self.focus_pole()
            self.log.place(x=int(self.screen_width - (self.screen_width / 12) * 2) + 20, y=0)
            return
        if self.buttons:
            for j in self.buttons:
                for i in j:
                    i.grid_remove()
            self.buttons = []
        for i in range(len(self.pole_fight)):
            self.buttons.append([])
            for j in range(len(self.pole_fight[i])):
                if self.pole_fight[i][j] == '0':
                    self.buttons[i].append(Button(height=int(self.screen_height / 8),
                                                  width=int(self.screen_width / 12), text='0',
                                                  image=self.ground_image, border='0.2',
                                                  command=lambda x=i, y=j: self.move_fight(x, y)))
                else:
                    if self.pole_fight[i][j].is_enemy():
                        if self.pole_fight[i][j].is_dead():
                            if self.type_battle == 1:
                                self.enemy_squad.remove(self.pole_fight[i][j])
                            self.pole_fight[i][j] = '0'
                            self.buttons[i].append(Button(height=int(self.screen_height / 8),
                                                          width=int(self.screen_width / 12), text='0',
                                                          image=self.ground_image, border='0.2',
                                                          command=lambda x=i, y=j: self.move_fight(x, y)))
                        else:
                            self.buttons[i].append(Button(height=int(self.screen_height / 8),
                                                          width=int(self.screen_width / 12), text='0',
                                                          image=self.enemy_image, border='0.2',
                                                          command=lambda x=i, y=j: self.atack_igrok(x, y)))
                    else:
                        if self.pole_fight[i][j].is_dead():
                            self.pole_fight[i][j] = '0'
                            self.buttons[i].append(Button(height=int(self.screen_height / 8),
                                                          width=int(self.screen_width / 12), text='0',
                                                          image=self.ground_image, border='0.2',
                                                          command=lambda x=i, y=j: self.move_fight(x, y)))
                        else:
                            self.buttons[i].append(Button(height=int(self.screen_height / 8),
                                                          width=int(self.screen_width / 12), text='0',
                                                          image=self.hero_image, border='0.2',
                                                          command=lambda x=i, y=j: self.ichooseu(x, y)))

                self.buttons[i][j].grid(row=i + 5, column=j + 5)

        self.windowgame.focus()

    def atack_igrok(self, x, y):
        if self.choosen_pawn[0] == 1:
            if self.choosen_pawn[1] - x < -1 or self.choosen_pawn[1] - x > 1 \
                    or self.choosen_pawn[2] - y < -1 or self.choosen_pawn[2] - y > 1:
                self.log.insert(END, 'Далеко\n')
            else:
                if self.pole_fight[x][y].is_enemy():
                    self.pole_fight[x][y].get_hit()
                    self.log.insert(END, f'Юнит на позиции {self.choosen_pawn[1], self.choosen_pawn[2]}'
                    f' нанес урон Врагу на позиции {x, y}, его оз: {self.pole_fight[x][y].get_hp()}\n')
        self.choosen_pawn = [0]
        self.draw_fight()
        if self.check_win_fight():
            for j in self.buttons:
                for i in j:
                    i.grid_remove()
                    j.remove(i)
            self.pole_fight = []
            self.choosen_pawn = [0]
            self.log.delete('1.0', END)
            self.log.insert(END, 'Бой окончен! Вы победили!\n')
            self.focus_pole()
            self.log.place(x=int(self.screen_width - (self.screen_width / 12) * 2) + 20, y=0)
            return
        else:
            self.enemy_move_fight()

    def ichooseu(self, x, y):
        self.choosen_pawn = [1, x, y, ]

    def enemy_move_fight(self):
        units_location = []
        enemys_location = []
        for i in range(len(self.pole_fight)):
            for j in range(len(self.pole_fight[i])):
                if self.pole_fight[i][j] != '0':
                    if self.pole_fight[i][j].is_enemy():
                        enemys_location.append([i, j])
                    else:
                        units_location.append([i, j])

        choosen_one = random.choice(enemys_location)
        goal = []
        minimum_len = 10
        for i in units_location:
            if abs(choosen_one[0] - i[0] + choosen_one[1] - i[1]) < minimum_len:
                minimum_len = abs(choosen_one[0] - i[0] + choosen_one[1] - i[1])
                goal = i
        reach = []
        for i in [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]:
            try:
                if self.pole_fight[choosen_one[0] + i[0]][choosen_one[1] + i[1]] != '0':
                    if self.pole_fight[choosen_one[0] + i[0]][choosen_one[1] + i[1]].is_enemy():
                        continue
                reach.append([choosen_one[0] + i[0], choosen_one[1] + i[1]])
            except IndexError:
                reach.append([choosen_one[0] + i[0], choosen_one[1] + i[1]])

        for j in reach:
            try:
                if self.pole_fight[j[0]][j[1]] != '0':
                    if not self.pole_fight[j[0]][j[1]].is_enemy():
                        self.pole_fight[j[0]][j[1]].get_hit()
                        self.log.insert(END, f'Враг на позиции {choosen_one[0], choosen_one[1]}'
                        f' нанес урон юниту на позиции {j[0], j[1]}, его оз: {self.pole_fight[j[0]][j[1]].get_hp()}\n')
                        if self.check_loose_fight():
                            for j in self.buttons:
                                for i in j:
                                    i.grid_remove()
                            self.buttons = []
                            self.pole_fight = []
                            self.choosen_pawn = [0]
                            self.log.delete('1.0', END)
                            self.squad = []
                            self.log.insert(END, 'Бой окончен! Вы проиграли!!\n')
                            self.focus_pole()
                            self.log.place(x=int(self.screen_width - (self.screen_width / 12) * 2) + 20, y=0)
                            return
                        self.draw_fight()
                        return
                    else:
                        move = self.choose_node(reach, goal)
                        self.pole_fight[move[0]][move[1]] = self.pole_fight[choosen_one[0]][choosen_one[1]]
                        self.pole_fight[choosen_one[0]][choosen_one[1]] = '0'
                        self.draw_fight()
                    return
            except IndexError:
                continue
        move = self.choose_node(reach, goal)
        self.pole_fight[move[0]][move[1]] = self.pole_fight[choosen_one[0]][choosen_one[1]]
        self.pole_fight[choosen_one[0]][choosen_one[1]] = '0'

    def choose_node(self, reachable, goal):
        min_cost = 200
        best_node = None
        for node in reachable:
            total_cost = abs(goal[0] - node[0]) + abs(goal[1] - node[1])
            if min_cost > total_cost:
                min_cost = total_cost
                best_node = node
        return best_node

    def check_loose_fight(self):
        units_count = 0
        for i in range(len(self.pole_fight)):
            for j in range(len(self.pole_fight[i])):
                if self.pole_fight[i][j] != '0':
                    if not self.pole_fight[i][j].is_enemy():
                        units_count += 1
        if units_count:
            return False
        else:
            return True

    def check_win_fight(self):
        enemy_count = 0

        for i in range(len(self.pole_fight)):
            for j in range(len(self.pole_fight[i])):
                if self.pole_fight[i][j] != '0':
                    if self.pole_fight[i][j].is_enemy():
                        enemy_count += 1
        if enemy_count > 0:
            return False
        else:
            return True

    def move_fight(self, x, y):
        if self.choosen_pawn[0] == 1:
            if self.choosen_pawn[1] - x < -1 or self.choosen_pawn[1] - x > 1 \
                    or self.choosen_pawn[2] - y < -1 or self.choosen_pawn[2] - y > 1:
                self.log.insert(END, 'Далеко\n')
            else:
                self.pole_fight[x][y] = self.pole_fight[self.choosen_pawn[1]][self.choosen_pawn[2]]
                self.pole_fight[self.choosen_pawn[1]][self.choosen_pawn[2]] = '0'
                self.choosen_pawn = [0]
                self.enemy_move_fight()
                self.draw_fight()

    def focus_pole(self):
        self.pole_pomenshe = []
        for i in range(6):
            self.pole_pomenshe.append([])
            for j in range(10):
                self.pole_pomenshe[i].append('')
                self.pole_pomenshe[i][j] = self.pole[i + self.offset[0]][j + self.offset[1]]
        self.draw_map()


    def draw_map(self):
        if self.buttons:
            for i in self.buttons:
                for j in i:
                    j.grid_remove()
        self.buttons = []
        for i in range(6):
            self.buttons.append('')
            self.buttons[i] = []
            for j in range(10):
                self.buttons[i].append('')
                if self.pole_pomenshe[i][j] == '0':
                    self.buttons[i][j] = Button(height=int(self.screen_height / 8),
                                                width=int(self.screen_width / 12), text='0',
                                                image=self.ground_image, border='0.2', )
                    self.buttons[i][j].configure(command=lambda x=i, y=j: self.move(0, x, y))
                elif self.pole_pomenshe[i][j] == '1':
                    self.buttons[i][j] = Button(height=int(self.screen_height / 8),
                                                width=int(self.screen_width / 12),
                                                image=self.water_image, border='0.2',
                                                command=lambda: self.move(1))
                elif self.pole_pomenshe[i][j] == '3':
                    self.buttons[i][j] = Button(height=int(self.screen_height / 8),
                                                width=int(self.screen_width / 12),
                                                image=self.castle_image, border='0.2',
                                                command=lambda x=i, y=j: self.move(4, x, y))
                elif self.pole_pomenshe[i][j] == '4':
                    self.buttons[i][j] = Button(height=int(self.screen_height / 8),
                                                width=int(self.screen_width / 12),
                                                text='0', image=self.hero_image, border='0.2',
                                                command=lambda: self.move(1))
                elif self.pole_pomenshe[i][j] == '5':
                    self.buttons[i][j] = Button(height=int(self.screen_height / 8),
                                                width=int(self.screen_width / 12),
                                                text='0', image=self.les_image,
                                                border='0.2',
                                                command=lambda x=i, y=j: self.move(2, x, y))
                elif self.pole_pomenshe[i][j] == '5.1':
                    self.buttons[i][j] = Button(height=int(self.screen_height / 8),
                                                width=int(self.screen_width / 12),
                                                text='0', image=self.les_igroka_image,
                                                border='0.2',
                                                command=lambda x=i, y=j: self.move(2, x, y))
                elif self.pole_pomenshe[i][j] == '6':
                    self.buttons[i][j] = Button(height=int(self.screen_height / 8),
                                                width=int(self.screen_width / 12),
                                                text='0', image=self.kamen_image,
                                                border='0.2',
                                                command=lambda x=i, y=j: self.move(3, x, y))
                elif self.pole_pomenshe[i][j] == '6.1':
                    self.buttons[i][j] = Button(height=int(self.screen_height / 8),
                                                width=int(self.screen_width / 12),
                                                text='0', image=self.kamen_igroka_image,
                                                border='0.2',
                                                command=lambda x=i, y=j: self.move(3, x, y))
                elif self.pole_pomenshe[i][j] == '7':
                    self.buttons[i][j] = Button(height=int(self.screen_height / 8),
                                                width=int(self.screen_width / 12),
                                                text='0', image=self.enemy_image,
                                                border='0.2',
                                                command=lambda x=i, y=j: self.move(7, x, y))
                elif self.pole_pomenshe[i][j] == '8':
                    self.buttons[i][j] = Button(height=int(self.screen_height / 8),
                                                width=int(self.screen_width / 12),
                                                text='0', image=self.enemy_castle_image,
                                                border='0.2',
                                                command=lambda x=i, y=j: self.move(9, x, y))
                elif self.pole_pomenshe[i][j] == '9':
                    self.buttons[i][j] = Button(height=int(self.screen_height / 8),
                                                width=int(self.screen_width / 12),
                                                text='0', image=self.enemy_hero_image,
                                                border='0.2',
                                                command=lambda x=i, y=j: self.move(8, x, y))
                elif self.pole_pomenshe[i][j] == '6.2':
                    self.buttons[i][j] = Button(height=int(self.screen_height / 8),
                                                width=int(self.screen_width / 12),
                                                text='0', image=self.kamen_enemy_image,
                                                border='0.2',
                                                command=lambda x=i, y=j: self.move(3, x, y))
                elif self.pole_pomenshe[i][j] == '5.2':
                    self.buttons[i][j] = Button(height=int(self.screen_height / 8),
                                                width=int(self.screen_width / 12),
                                                text='0', image=self.les_enemy_image,
                                                border='0.2',
                                                command=lambda x=i, y=j: self.move(2, x, y))
                self.buttons[i][j].grid(row=i, column=j)

        self.txt_drova.configure(text='Дерево:' + str(self.drova_igroka))
        self.txt_kamen.configure(text='Камень:' + str(self.kamen_igroka))
        self.windowgame.focus()



    def resources(self):
        for i in self.pole:
            for j in i:
                if j == '5.1':
                    self.drova_igroka += 1
                elif j == '6.1':
                    self.kamen_igroka += 1
                elif j == '5.2':
                    self.drova_enemy += 1
                elif j == '6.2':
                    self.kamen_enenmy += 1


    def caslte_create(self):
        count_castles = 0
        for i in range(len(self.pole)):
            for j in range(len(self.pole[i])):
                if self.pole[i][j] == '3':
                    count_castles += 1
        for i in range(len(self.pole)):
            for j in range(len(self.pole[i])):
                if self.pole[i][j] == '4' and self.pole[i - 1][j] == '0':
                    if self.kamen_igroka >= 10:
                        if count_castles < 5:
                            self.pole[i - 1][j] = '3'
                            self.kamen_igroka -= 10
                            self.focus_pole()
                            self.log.insert(END, '\n')
                            self.log.insert(END, 'Построен новый замок\n')
                            return
                        else:
                            self.log.insert(END, 'Достигнуто максимальное количество замков\n')
                            return
                    else:
                        self.log.insert(END, 'Недостаточно камня! Нужно 10 камня для постройки замка\n')
                        return
        self.log.insert(END, 'Недостаточно места! Клетка над героем игрока должна быть пустой!\n')


class Unit(object):
    def __init__(self, enemy):
        self.hp = 3
        self.dead = False
        self.enemy = enemy

    def get_hit(self):
        self.hp -= 1
        if self.hp == 0:
            self.dead = True

    def is_enemy(self):
        return self.enemy

    def get_hp(self):
        return self.hp

    def is_dead(self):
        return self.dead
