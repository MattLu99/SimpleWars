import os
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

import game
import display

class Window:
    location = 'Maps'
    filelist = os.listdir(location)
    window = tk.Tk()
    bgcolor = 'LimeGreen'
    
    def __init__(self, width=420, height=280):
        self.__window_setup(width, height)
        self.__window_elements()

    def game_start(self):
        self.window.mainloop()

    def __window_setup(self, width, height):
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry("{}x{}+{}+{}".format(width, height, x, y))
        self.window.resizable(False, False)
        self.window['bg'] = self.bgcolor
        self.window.title("Simple Wars")

    def __window_elements(self):
        tk.Label(self.window, text="Simple Wars", font=("Broadway", 46), bg=self.bgcolor).pack()
        self.__display_teams()
        self.__playernames_entry()
        self.__mapselect_combobox()
        self.__extras_info()

    def __display_teams(self):
        teamsdisplay = tk.Frame(self.window, bg=self.bgcolor)
        teamsdisplay.pack()
        tk.Label(teamsdisplay, text="Red team", font=("Arial Bold", 12), bg="#d32f2f").pack(side=tk.LEFT)
        tk.Label(teamsdisplay, width=10, bg=self.bgcolor).pack(side=tk.LEFT)
        tk.Label(teamsdisplay, text="Blue team", font=("Arial Bold", 12), bg="#0d48a1").pack(side=tk.RIGHT)

    def __playernames_entry(self):
        playernames = tk.Frame(self.window, bg=self.bgcolor)
        playernames.pack()
        self.player1 = tk.Entry(playernames)
        self.player1.pack(side=tk.LEFT)
        tk.Label(playernames, text="  vs  ", font=("Arial Bold", 12), bg=self.bgcolor).pack(side=tk.LEFT)
        self.player2 = tk.Entry(playernames)
        self.player2.pack(side=tk.RIGHT)

    def __mapselect_combobox(self):
        mapselect = tk.Frame(self.window, bg=self.bgcolor)
        mapselect.pack()
        tk.Label(mapselect, text="Maps:", font=("Arial Bold", 12), bg=self.bgcolor).pack(side=tk.LEFT)
        self.mapcbox = ttk.Combobox(mapselect, values=self.__viewinfo(), width=21)
        self.mapcbox.pack(side=tk.LEFT)
        tk.Button(mapselect, text="Start game", command=lambda:self.__get_gamemap()).pack(side=tk.RIGHT)

    def __extras_info(self):
        tk.Label(self.window, bg=self.bgcolor).pack()
        tk.Button(self.window, text="Game history", font=("Arial Bold", 15), command=lambda:self.__get_toplist(), width=15).pack()
        tk.Label(self.window, bg=self.bgcolor).pack()
        tk.Button(self.window, text="How to play", font=("Arial Bold", 15), command=lambda:self.__get_gamerules(), width=15).pack()

    def __viewinfo(self):
        viewlist = []
        for file in self.filelist:
            if '_' in file:
                viewlist.append(self.__to_show(file.split('_')))
            else:
                viewlist.append(self.__to_show(file.split(' ')))
        return viewlist

    def __to_show(self, name):
        n = len(name)
        if name[n - 1].endswith(".txt"):
            name[n - 1] = name[n - 1].replace(".txt", "", 1)
        else:
            name.append("(Invalid map!)")
        for i in range(n):
            name[i] = name[i][0].upper() + name[i][1:]
        return ' '.join(name)

    def __get_gamemap(self):
        if self.player1.get() == "" or self.player2.get() == "":
            showinfo("Error!", "Both players are required to have a name!")
        elif self.mapcbox.current() == -1:
            showinfo("Error!", "The selected map doesn't exist!")
        else:
            mapname = self.filelist[self.mapcbox.current()]
            path = os.path.join(self.location, self.filelist[self.mapcbox.current()])
            if path.endswith(".txt"):
                rawmap, x, y = self.__map_reader(path)
                if len(rawmap) == 0:
                    showinfo("Error!", "The selected map is an invalid type or is empty!")
                else:
                    if self.__map_fits_needs(rawmap, x, y):
                        showinfo("Error!", "The selected map doesn't conform to the basic requirements!")
                    else:
                        team1 = self.player1.get()
                        team2 = self.player2.get()
                        self.window.destroy()
                        mapname = self.__to_show(mapname.split('_')) if '_' in mapname else self.__to_show(mapname.split(' '))
                        SimpleWars = game.Start(x, y)
                        SimpleWars.play(rawmap, mapname, team1, team2)
            else:
                showinfo("Error!", "The selected item is not a text file!")

    def __map_reader(self, path):
        rawmap = []
        try:
            with open(path, "rt", encoding="utf-8") as file:
                for line in file:
                    rawmap.append(line.rstrip('\n'))
            x = 0
            for l in rawmap:
                if len(l) > x:
                    x = len(l)
            y = len(rawmap)
            for i in range(y):
                rawmap[i] += 'O' * (x - len(rawmap[i]))
            return rawmap, x, y
        except PermissionError:
            return [], 0, 0

    def __map_fits_needs(self, rawmap, x, y):
        hqnum = 0
        wsnum = 0
        for line in rawmap:
            for char in line:
                if char == 'H':
                    hqnum += 1
                elif char == 'W':
                    wsnum += 1
        return hqnum != 2 or wsnum < 2 or x < 10 or y < 10

    def __get_toplist(self):
        try:
            matchhistory = []
            with open("matchhistory.txt", "rt", encoding="utf-8") as f:
                for line in f:
                    matchhistory.append(line.rstrip('\n'))
            display.matchhistory(matchhistory)
        except FileNotFoundError:
            display.matchhistory(["No game history data stored."])

    def __get_gamerules(self):
        display.info()