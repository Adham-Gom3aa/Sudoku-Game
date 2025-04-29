import random
import tkinter as tk
import tkinter.messagebox
import mysql.connector as mysql


class Database:
    def __init__(self):
        self.mydb = mysql.connect(
            host="localhost",
            user="root",
            password="root",
            database="soduku",
            autocommit=True
        )
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute('CREATE DATABASE IF NOT EXISTS soduku')
        self.mycursor.execute('CREATE TABLE IF NOT EXISTS sudoku (id INT AUTO_INCREMENT PRIMARY KEY, '
                              'Wins INT,Strikes_Left INT,'
                              'difficulty Text)')

    def insert_data(self, wins, strikes_left, difficulty):
        query = '''INSERT INTO sudoku (Wins,Strikes_Left,difficulty) VALUES (%s,%s,%s)'''
        self.mycursor.execute(query, (wins, strikes_left, difficulty))

    def get_lenght(self,df=None):
        if not df:
            query = '''SELECT Wins FROM sudoku'''
        elif df=='Easy':
            query = '''SELECT Wins FROM sudoku WHERE difficulty = 'Easy' '''
        elif df=='Medium':
            query = '''SELECT Wins FROM sudoku WHERE difficulty = 'Medium' '''
        elif df=='Hard':
            query = '''SELECT Wins FROM sudoku WHERE difficulty = 'Hard' '''
        elif df=='Very Hard':
            query = '''SELECT Wins FROM sudoku WHERE difficulty = 'Very Hard' '''
        elif df=='Extreme':
            query = '''SELECT Wins FROM sudoku WHERE difficulty = 'Extreme' '''
        self.mycursor.execute(query)
        result = self.mycursor.fetchall()
        if len(result)==0:
            return 1
        return len(result)

    def get_wins(self):
        query = '''SELECT Wins FROM sudoku'''
        self.mycursor.execute(query)
        result = self.mycursor.fetchall()
        return sum(wins[0] for wins in result)

    def Easy_wins(self):
        query = '''SELECT Wins FROM sudoku WHERE Wins =1 AND difficulty = 'Easy' '''
        self.mycursor.execute(query)
        result = self.mycursor.fetchall()
        print(result)
        return sum(wins[0] for wins in result)

    def Mid_wins(self):
        query = '''SELECT Wins FROM sudoku WHERE Wins =1 AND difficulty = 'Medium' '''
        self.mycursor.execute(query)
        result = self.mycursor.fetchall()
        print(result)
        return sum(wins[0] for wins in result)

    def Hard_wins(self):
        query = '''SELECT Wins FROM sudoku WHERE Wins =1 AND difficulty = 'Hard' '''
        self.mycursor.execute(query)
        result = self.mycursor.fetchall()
        print(result)
        return sum(wins[0] for wins in result)

    def VeryHard_wins(self):
        query = '''SELECT Wins FROM sudoku WHERE Wins =1 AND difficulty = 'Very Hard' '''
        self.mycursor.execute(query)
        result = self.mycursor.fetchall()
        print(result)
        return sum(wins[0] for wins in result)

    def Extreme_wins(self):
        query = '''SELECT Wins FROM sudoku WHERE Wins =1 AND difficulty = 'Extreme' '''
        self.mycursor.execute(query)
        result = self.mycursor.fetchall()
        print(result)
        return sum(wins[0] for wins in result)

    def perfect_wins(self):
        self.mycursor.execute('''SELECT Wins FROM sudoku WHERE Wins =1 AND strikes_left = 3''')
        result = self.mycursor.fetchall()
        return sum(wins[0] for wins in result)

class SodukuSquares:
    def __init__(self):
        self.soduku = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for i in range(9)]
        self.solve()
        self.convertor()
        self.game = [i[:] for i in self.soduku]
        self.difficulty = 50

    def is_valid(self, row, col, num):
        for i in range(9):
            if self.soduku[row][i] == num or self.soduku[i][col] == num:
                return False
            sq_row = 3 * (row // 3)
            sq_col = 3 * (col // 3)
            for i in range(3):
                for j in range(3):
                    if self.soduku[sq_row + i][sq_col + j] == num:
                        return False

        return True

    def solve(self):
        if not self.find_empty():
            return True
        row, col = self.find_empty()
        nums = [i for i in range(1, 10)]
        random.shuffle(nums)
        for num in nums:
            if self.is_valid(row, col, num):
                self.soduku[row][col] = num
                if self.solve():
                    return True
                self.soduku[row][col] = 0
        return False

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.soduku[i][j] == 0:
                    return (i, j)
        return None

    def remove_cells(self):
        if not hasattr(self, "removes"):
            self.removes = 0
        while self.removes < self.difficulty:
            x = random.randint(0, 8)
            y = random.randint(0, 8)
            while self.game[x][y] == '  ':
                x = random.randint(0, 8)
                y = random.randint(0, 8)
            self.game[x][y] = "  "
            self.removes += 1
            self.remove_cells()

    def convertor(self):
        for j in range(9):
            for i in range(9):
                self.soduku[i][j] = str(self.soduku[i][j])

class MainPage:
    def __init__(self):

        self.root = tk.Tk()
        self.root.config(bg='white')
        self.root.title('Soduku')
        self.root.geometry('400x500')
        self.root.config(bg='white')

        button = tk.Button(self.root, text='Extreme', command=self.Extreme, font=('Tahoma', 15, 'bold'),bg='#8B0000')
        button.pack(pady=20)
        button = tk.Button(self.root, text='Very Hard', command=self.Veryhard, font=('Tahoma', 15, 'bold'),bg='#B22222')
        button.pack(pady=20)
        button1 = tk.Button(self.root, text='Hard', command=self.hard, font=('Tahoma', 15, 'bold'),bg='#CD5C5C')
        button1.pack(pady=20)
        button2 = tk.Button(self.root, text='Medium', command=self.mid, font=('Tahoma', 15, 'bold'),bg='#F08080')
        button2.pack(pady=20)
        button2 = tk.Button(self.root, text='Easy', command=self.easy, font=('Tahoma', 15, 'bold'),bg='#FFE4E1')
        button2.pack(pady=20)
        stats = tk.Button(self.root, text='Stats', command=self.Stats, font=('Tahoma', 15, 'bold'),bg='white')
        stats.pack(pady=20)
        self.root.mainloop()

    def Stats(self):
        self.root.destroy()
        newRoot = tk.Tk()
        newRoot.title('Stats')
        newRoot.geometry('400x400')
        db = Database()
        wins = tk.Label(newRoot, text=f"Wins: {db.get_wins()}", font=("Arial", 15),border=5)
        losses = tk.Label(newRoot, text=f"Losses: {db.get_lenght()-db.get_wins()}", font=("Arial", 15),border=5)
        easy_wins = tk.Label(newRoot, text=f"Easy Wins: {db.Easy_wins()}   ,  Win Rate: {db.Easy_wins()/db.get_lenght('Easy')*100:.2f}", font=("Arial", 10),border=5)
        med_wins = tk.Label(newRoot, text=f"Medium Wins: {db.Mid_wins()}   ,  Win Rate: {db.Mid_wins()/db.get_lenght('Medium')*100:.2f}", font=("Arial", 10),border=5)
        hard_wins = tk.Label(newRoot, text=f"Hard Wins: {db.Hard_wins()}   ,  Win Rate: {db.Hard_wins()/db.get_lenght('Hard')*100:.2f}", font=("Arial", 10),border=5)
        veryhard_wins = tk.Label(newRoot, text=f"Very Hard Wins: {db.VeryHard_wins()}   ,  Win Rate: {db.VeryHard_wins()/db.get_lenght('Very Hard')*100:.2f}", font=("Arial", 10),border=5)
        extreme_wins = tk.Label(newRoot, text=f"Extreme Wins: {db.Extreme_wins()}   ,  Win Rate: {db.Extreme_wins()/db.get_lenght('Extreme')*100:.2f}", font=("Arial", 10),border=5)
        perfect_wins=tk.Label(newRoot,text=f"Perfect Wins: {db.perfect_wins()}",font=("Arial",10),border=5)
        wins.pack(pady=10)
        easy_wins.pack(pady=5)
        med_wins.pack(pady=5)
        hard_wins.pack(pady=5)
        veryhard_wins.pack(pady=5)
        extreme_wins.pack(pady=5)
        perfect_wins.pack(pady=5)
        losses.pack(pady=10)
        back=tk.Button(newRoot,text='Back',command=lambda : [newRoot.destroy(), MainPage()],font=('Tahoma',15,'bold'))
        back.pack(pady=10)
        newRoot.mainloop()

    def Extreme(self):
        self.root.destroy()
        self.s1 = SodukuSquares()
        self.s1.difficulty = 60
        self.s1.solve()
        self.s1.remove_cells()
        gui=SodukuGUI(self.s1,'Extreme')

    def Veryhard(self):
        self.root.destroy()
        self.s1 = SodukuSquares()
        self.s1.difficulty = 55
        self.s1.solve()
        self.s1.remove_cells()
        gui=SodukuGUI(self.s1,'Very Hard')


    def hard(self):
        self.root.destroy()
        self.s1 = SodukuSquares()
        self.s1.difficulty = 45
        self.s1.solve()
        self.s1.remove_cells()
        gui=SodukuGUI(self.s1,'Hard')
    def mid(self):
        self.root.destroy()
        self.s1 = SodukuSquares()
        self.s1.difficulty = 40
        self.s1.solve()
        self.s1.remove_cells()
        gui=SodukuGUI(self.s1,'Medium')


    def easy(self):
        self.root.destroy()
        self.s1 = SodukuSquares()
        self.s1.difficulty = 30
        self.s1.solve()
        self.s1.remove_cells()
        gui=SodukuGUI(self.s1,'Easy')

class SodukuGUI:
    def __init__(self, s1,diff):
        self.colors=['black','white','gray','lightgray','red','green','blue','lightgreen','pink','#8c8b8b','lightblue']
        self.s1 = s1
        self.root = tk.Tk()
        self.root.title('Soduku')
        self.strick = 3
        self.lives = tk.Label(self.root, text=f"Lives: {self.strick}", font=("Arial", 15))
        self.lives.pack()
        self.frame = tk.Frame((self.root), pady=50)
        self.sudFrame = tk.Frame(self.root, border=5)
        self.game = s1.game
        self.buttons = [[None for _ in range(9)] for _ in range(9)]
        self.selected = None
        self.count = 0
        self.win_check = 0
        self.repeat={'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'  ':0}
        self.db = Database()
        self.moves = []
        self.buttonKeys=[]
        self.LabelKeys=[]
        self.difficulty = diff
        self.edit_coloers=[self.colors[1],self.colors[10]]
        self.active = False
        self.placeholder=[[''for _ in range(9)]for _ in range(9)]
        self.edit=tk.Button(self.frame,text='Edit',command=lambda :self.edit_mode(),font=('Tahoma',15,'bold'),bg=self.colors[1])
        self.edit.grid(row=2,column=2,columnspan=2,sticky='ew',pady=5)
        color = [self.colors[1], self.colors[3]]
        for i in range(9):
            for j in range(9):
                if i % 3 == 0 and j == 0:
                    color.reverse()
                if self.game[i][j] == '  ':
                    if self.count >= 9:
                        self.count = 0
                    if self.count < 3 or self.count >= 6:
                        button = tk.Button(self.sudFrame, text=self.game[i][j], width=5, height=2,
                                           command=lambda i=i, j=j: self.clicked(i, j), bg=color[1])
                        button.grid(row=i, column=j, sticky='nsew')
                        self.count += 1
                    else:
                        button = tk.Button(self.sudFrame, text=self.game[i][j], width=5, height=2,
                                           command=lambda i=i, j=j: self.clicked(i, j), bg=color[0])
                        button.grid(row=i, column=j, sticky='nsew')
                        self.count += 1
                else:
                    if self.count >= 9:
                        self.count = 0
                    if self.count < 3 or self.count >= 6:
                        button = tk.Button(self.sudFrame, text=self.game[i][j], width=4, height=2, font='Tahoma 9 bold',
                                           fg=self.colors[0], command=lambda i=i, j=j: self.clicked(i, j), bg=color[1])
                        button.grid(row=i, column=j, sticky='nsew')
                        self.count += 1
                    else:
                        button = tk.Button(self.sudFrame, text=self.game[i][j], width=4, height=2, font='Tahoma 9 bold',
                                           fg=self.colors[0], command=lambda i=i, j=j: self.clicked(i, j), bg=color[0])
                        button.grid(row=i, column=j, sticky='nsew')
                        self.count += 1
                self.buttons[i][j] = button
                self.repeat[self.game[i][j]] += 1
        self.sudFrame.pack()
        nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        for i in range(9):
            button = tk.Button(self.frame, text=nums[i], width=3, command=lambda num=nums[i]: self.choosen(num),
                               font=('Tahoma', 15, 'bold'), bg=self.colors[1],fg=self.colors[6])
            lable = tk.Label(self.frame, text=self.repeat[nums[i]], font=('Tahoma', 12, 'bold'))
            lable.grid(row=1, column=i, padx=5, sticky='ew')
            button.grid(row=0, column=i, padx=5, sticky='ew')
            self.buttonKeys.append(button)
            self.LabelKeys.append(lable)


        button = tk.Button(self.frame, text='Undo', width=3, command=lambda: self.Undo(), font=('Tahoma', 15, 'bold'),bg=self.colors[1])
        back=tk.Button(self.frame,text='Back',command=lambda : [self.root.destroy(), MainPage()],font=('Tahoma',15,'bold'),bg=self.colors[1])
        clear=tk.Button(self.frame,text='Clear',command=lambda : self.clear(),font=('Tahoma',15,'bold'),bg=self.colors[1])
        clear.grid(row=2, column=0, columnspan=2, sticky='ew', pady=5)
        back.grid(row=2, column=6, columnspan=3, sticky='ew', pady=5)
        button.grid(row=2, column=4, columnspan=2, sticky='ew', pady=5)
        self.button_disable()
        self.frame.pack()
        self.root.mainloop()
    def clear(self):
        if self.selected:
            row, col = self.selected
            if self.buttons[row][col].config('font')[-1] != 'Tahoma 9 bold':
                if self.buttons[row][col].config('fg')[-1] == self.colors[5]:
                    self.buttons[row][col].config(text='  ',fg=self.colors[1])
                    self.repeat[self.game[row][col]] -= 1
                    self.button_disable()
                    self.win_check -= 1
                    self.game[row][col] = '  '
                else:
                    self.buttons[row][col].config(text='  ')
                if self.placeholder[row][col]:
                    self.placeholder[row][col] = self.placeholder[row][col][:-1]
                    if not self.placeholder[row][col]:
                        self.buttons[row][col].config(text='  ')

        self.color_reset()

    def Undo(self):
        self.color_reset()
        if not self.moves:
            return
        row, col, value = self.moves.pop()
        if self.buttons[row][col].config('fg')[-1] == self.colors[5]:
            self.repeat[self.game[row][col]] -= 1
            self.button_disable()
            self.win_check -= 1
            self.buttons[row][col].config(text='  ',fg=self.colors[1])
            self.game[row][col] = '  '
        else:
            self.buttons[row][col].config(text=value)
        if self.placeholder[row][col]:
            self.placeholder[row][col] = self.placeholder[row][col][:-1]
            if not self.placeholder[row][col]:
                self.buttons[row][col].config(text='  ')

    def edit_mode(self):
        self.active=not self.active
        self.edit_coloers.reverse()
        self.edit.config(bg=self.edit_coloers[0])
    def clicked(self, row, col):
        self.color_reset()
        self.selected = (row, col)
        print(self.s1.soduku[row][col])

        for i in range(9):
            for j in range(9):
                if self.buttons[i][j].config('text')[-1] == self.buttons[row][col].config('text')[-1]:
                    if self.buttons[i][j].config('fg')[-1] == self.colors[4] and self.buttons[i][j].config('text')[-1] != '  ' and self.buttons[i][j].config('font')[-1] != 'Tahoma 7 bold':
                        self.buttons[i][j].config(bg=self.colors[8])
                    if self.buttons[i][j].config('fg')[-1] != self.colors[4] and self.buttons[i][j].config('text')[-1] != '  ' and self.buttons[i][j].config('font')[-1] != 'Tahoma 7 bold':
                        self.buttons[i][j].config(bg=self.colors[7])
                    if i == row and j == col and self.buttons[i][j].config('text')[-1] == '  ' or (self.buttons[i][j].config('font')[-1] == 'Tahoma 7 bold' and i == row and j == col):
                        self.buttons[i][j].config(bg=self.colors[9])

    def color_reset(self):
        color = [self.colors[1], self.colors[3]]
        for i in range(9):
            for j in range(9):
                if i % 3 == 0 and j == 0:
                    color.reverse()
                if self.count >= 9:
                    self.count = 0
                if self.count < 3 or self.count >= 6:
                    self.buttons[i][j].config(bg=color[1])
                    self.count += 1
                else:
                    self.buttons[i][j].config(bg=color[0])
                    self.count += 1
        self.count = 0

    def button_disable(self):
        print(self.repeat)
        for i in self.repeat:
             if i !='  ':
                 self.LabelKeys[int(i)-1].config(text=self.repeat[i])
             if self.repeat[i] ==9 and i !='  ':
                 self.buttonKeys[int(i)-1].config(state='disabled',bg=self.colors[2])
             elif self.repeat[i] < 9 and i !='  ':
                 self.buttonKeys[int(i)-1].config(state='normal',bg=self.colors[1])

    def choosen(self, value):
        self.color_reset()
        if not self.selected:
            for i in range(9):
                for j in range(9):
                    if self.buttons[i][j].config('text')[-1] == value and self.buttons[i][j].config('font')[-1] != 'Tahoma 7 bold':
                        if self.buttons[i][j].config('fg')[-1] == self.colors[4] and self.buttons[i][j].config('text')[-1] != '  ':
                            self.buttons[i][j].config(bg=self.colors[8])
                        if self.buttons[i][j].config('fg')[-1] != self.colors[4] and self.buttons[i][j].config('text')[-1] != '  ':
                            self.buttons[i][j].config(bg=self.colors[7])
        elif self.selected:
            row, col = self.selected
            if self.active:
                self.color_reset()
                if not hasattr(self, "place_counter"):
                    self.place_counter=0
                    self.row_counter=0
                if value in self.placeholder[row][col]:
                    self.placeholder[row][col].remove(value)
                if value not in self.placeholder[row][col]:
                    self.moves.append((row, col, self.buttons[row][col].config('text')[-1]))
                    self.placeholder[row][col] +=value

                temp=''
                print(temp)
                for i in range(len(sorted(self.placeholder[row][col]))):
                    if i==3 or i==6:
                        temp+='\n'
                    temp+=sorted(self.placeholder[row][col])[i]+" "

                self.buttons[row][col].config(text=temp,font='Tahoma 7 bold',fg=self.colors[6])
                return

            if self.buttons[row][col].config('fg')[-1] == self.colors[0] or self.buttons[row][col].config('fg')[-1] == self.colors[5]:
                for i in range(9):
                    for j in range(9):
                        if self.buttons[i][j].config('text')[-1] == value:
                            if self.buttons[i][j].config('fg')[-1] == self.colors[4] and self.buttons[i][j].config('text')[-1] != '  ':
                                self.buttons[i][j].config(bg=self.colors[8])
                            if self.buttons[i][j].config('fg')[-1] != self.colors[4] and self.buttons[i][j].config('text')[-1] != '  ':
                                self.buttons[i][j].config(bg=self.colors[7])
                return
            if self.s1.soduku[row][col] == value:
                self.moves.append((row, col, self.buttons[row][col].config('text')[-1]))
                self.buttons[row][col].config(text=value, fg=self.colors[5], bg=self.colors[7],font='Tahoma 9')
                self.game[row][col] = value
                self.repeat[self.game[row][col]] += 1
                self.selected = None
                self.button_disable()
                self.win_check += 1
            elif self.s1.soduku[row][col] != value:
                self.strick -= 1
                self.moves.append((row, col, self.buttons[row][col].config('text')[-1]))
                self.lives.config(text=f"Lives: {self.strick}")
                self.buttons[row][col].config(text=value, fg=self.colors[4], bg=self.colors[8])
                if self.strick <= 0:
                    tk.messagebox.showinfo("Game Over", "Game Over")
                    self.root.destroy()
                    self.db.insert_data(0, self.strick, self.difficulty)
                    MainPage()
            if self.win_check == self.s1.difficulty:
                tk.messagebox.showinfo("Congratulations", "You Won")
                print(self.difficulty)
                self.root.destroy()
                self.db.insert_data(1, self.strick, self.difficulty)
                MainPage()

MainPage()