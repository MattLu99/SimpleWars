import pygame as py
import pygame.gfxdraw as pgfx

import terrains
import units

class Index:
    """Class for storing coordinate/location data of anything on the map and easily doing operations on them."""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        """Default equals function override, checks if Indexes have the same location data."""
        return self.x == other.x and self.y == other.y

    def __sub__(self, other: object) -> object:
        """Default subtract function override, takes the two indexes and subtracts the values of the smaller from the larger one, then returns the result in a new Index."""
        return Index(max(self.x, other.x) - min(self.x, other.x), max(self.y, other.y) - min(self.y, other.y))

    def __abs__(self):
        """Default absolute function override, only adds up the values of the index, since the location data won't give negatives."""
        return self.x + self.y

class Start:
    """Class that takes the width and height of the game map, then prepares and starts the game."""
    BLOCK = 32                      #WIDTH AND HEIGHT OF A BLOCK IN PIXELS
    TEAMS = ["Red", "Blue"]         #List for storin all playable teams.
    team_buildings = []             #List for storing the number of buildings a team has.
    team_money = [0] * len(TEAMS)   #List for storing the amount of money each team has.
    #Colors of playing field elements:
    default_color = py.Color("#ffff80")
    toolbar_bgcolor = py.Color("DimGray")
    toolbar_fgcolor = py.Color("#ffff80")
    color_red = py.Color("#d32f2f")
    color_blue = py.Color("#0d48a1")
    #Essential data types for storing lots of similar data:
    toolbar = []
    workshop = []
    unit_types = []
    unit_prices = {}
    terrainmap = []
    unitmap = []
    victor = ""

    def __init__(self, xrn: int, yrn: int):
        self.xrn = xrn
        self.yrn = yrn

    def play(self, rawmap: list[list], mapname: str, *playernames) -> None:
        """Most important function of the program. 
        Takes the raw map data, the map's name and the names of players, processes all the information and then starts the main gamplay loop."""
        py.init()
        team_turn, turn_count = 0, 1
        window = self.window_setup(rawmap, mapname, playernames)
        spawner_selected, has_won, quit = False, False, False
        spawner_position, on, selected = None, None, None
        #MAIN GAMEPLAY LOOP
        while not quit:
            event = py.event.wait()
            if event.type == py.MOUSEBUTTONDOWN:
                x, y = event.pos
                on = Index(x // self.BLOCK, y // self.BLOCK)
                on_in_map = on.x < self.xrn
                spawner_selected = False if on_in_map else spawner_selected
                if has_won:
                    selected, quit = self.win_view(on_in_map, on, mapname, playernames, turn_count)
                elif event.button == 1:
                    if on_in_map:
                        if selected is not None and selected == on:
                            #SELECTED CLICKED
                            selected = None
                        elif self.unitmap[on.x][on.y] is not None:
                            #UNIT SELECTED
                            selected = Index(on.x, on.y)
                        elif selected is not None and self.unitmap[on.x][on.y] is None:
                            #SELECTED MOVEMENT
                            if self.move_on_terrain(on, selected, team_turn):
                                on, selected = self.unit_step_on(window, on, selected)
                            else:
                                selected = None
                        elif self.unitmap[on.x][on.y] is None and self.terrainmap[on.x][on.y].is_team_workshop(self.TEAMS[team_turn]):
                            #WORKSHOP SELECTED
                            spawner_selected = True
                            spawner_position, selected = Index(on.x, on.y), None
                            self.workshopselected_draw(window)
                    elif not on_in_map and self.toolbar[on.x-self.xrn][on.y] == 1:
                        #END TURN
                        on, selected, spawner_selected = None, None, False
                        team_turn, turn_count = self.end_turn(team_turn, turn_count)
                    elif not on_in_map and self.toolbar[on.x-self.xrn][on.y] == 2:
                        #QUIT GAME
                        quit = True
                    elif not on_in_map and spawner_selected:
                        #UNIT PRODUCTION
                        on, selected, spawner_selected = self.workshop_production(window, team_turn, spawner_position, Index(x // self.BLOCK - self.xrn, y // (self.BLOCK // 2)))
                    else:
                        selected = None
                elif event.button == 3 and selected is not None:
                    if on_in_map and self.unitmap[selected.x][selected.y].can_attack(self.TEAMS[team_turn], self.unitmap[on.x][on.y], self.terrainmap[on.x][on.y]):
                        distance = abs(on - selected)
                        if self.unitmap[selected.x][selected.y].in_attack_range(distance):
                            #SELECTED ATTACKING
                            self.unit_attacking_on(on, selected, distance)
                            selected, has_won = self.check_casualties(window, on, selected)
                        elif distance == 0 and self.unitmap[selected.x][selected.y].can_capture(self.terrainmap[on.x][on.y]):
                            #SELECTED CAPTURING
                            has_won = self.unit_capturing_on(window, on, selected)
                    else:
                        selected = None
            if event.type == py.KEYDOWN and not has_won:
                #ACTIONS WITH KEYBOARD: QUIT, END TURN, SELECTED CAPTURING, MOVE SELECTED
                if event.key == py.K_ESCAPE:
                    quit = True
                elif event.key == py.K_RETURN:
                    on, selected, spawner_selected = None, None, False
                    team_turn, turn_count = self.end_turn(team_turn, turn_count)
                elif selected is not None and event.key == py.K_SPACE and self.unitmap[selected.x][selected.y].can_capture(self.terrainmap[selected.x][selected.y]):
                    has_won = self.unit_capturing_on(window, selected, selected)
                elif selected is not None and (event.key == py.K_UP or event.key == py.K_w) and selected.y - 1 >= 0 and self.keyboard_movement(selected, team_turn, ymod=-1):
                    on, selected = self.unit_step_on(window, None, selected, ymod=-1)
                elif selected is not None and (event.key == py.K_RIGHT or event.key == py.K_d) and selected.x + 1 < self.xrn and self.keyboard_movement(selected, team_turn, xmod=1):
                    on, selected = self.unit_step_on(window, None, selected, xmod=1)
                elif selected is not None and (event.key == py.K_DOWN or event.key == py.K_s) and selected.y + 1 < self.yrn and self.keyboard_movement(selected, team_turn, ymod=1):
                    on, selected = self.unit_step_on(window, None, selected, ymod=1)
                elif selected is not None and (event.key == py.K_LEFT or event.key == py.K_a) and selected.x - 1 >= 0 and self.keyboard_movement(selected, team_turn, xmod=-1):
                    on, selected = self.unit_step_on(window, None, selected, xmod=-1)
            self.update_toolbar(window, team_turn, turn_count, selected, on, spawner_selected)
            if event.type == py.QUIT:
                if has_won:
                    self.write_statistics("matchhistory.txt", playernames, turn_count, mapname)
                quit = True
        py.quit()

    def toolbar_setup(self, xtlb: int) -> list[list]:
        """Prepares the toolbar interface location for use."""
        toolbar = [[0 for i in range(self.yrn)] for j in range(xtlb)]
        for x in range(1, xtlb-1):
            for y in range(self.yrn - 4, self.yrn - 2):
                toolbar[x][y] = 1
            for y in range(self.yrn - 1, self.yrn):
                toolbar[x][y] = 2
        return toolbar

    def workshop_setup(self, xtlb: int) -> list[list]:
        """Prepares the workshop interface location for use."""
        workshop = [[None for i in range(self.yrn * 2)] for j in range(xtlb)]
        counter = 0
        for y in range(4, 12):
            for x in range(0, xtlb // 2):
                workshop[x][y] = counter
            counter += 1
            for x in range(xtlb // 2, xtlb):
                workshop[x][y] = counter
            counter += 1
        return workshop

    def window_setup(self, rawmap: list[list], mapname: str, playernames: list) -> object:
        """Sets up the complete window of the game and prepares its grid locations for use."""
        self.toolbar, self.workshop = self.toolbar_setup(6), self.workshop_setup(6)
        self.unit_types, self.unit_prices = units.get_units(), units.get_prices()
        window = py.display.set_mode((self.xrn * self.BLOCK + len(self.toolbar) * self.BLOCK, self.yrn * self.BLOCK))
        py.display.set_caption("{} - {}".format(mapname, " versus ".join(playernames)))
        window.fill(self.default_color)
        self.map_drawadd(window, rawmap)
        return window

    def currentteam_draw(self, window: object, team: str) -> None:
        """Changes the toolbar's grid to display the team that is currently active."""
        xon = self.xrn * self.BLOCK
        yon = 0
        font = py.font.SysFont("Arial Bold", 32)
        pgfx.box(window, py.Rect(xon, yon, 3 * self.BLOCK, self.BLOCK), self.toolbar_bgcolor)
        text = font.render('{}'.format(team), True,  self.color_red if team == "Red" else self.color_blue)
        window.blit(text, (xon + 2, yon + 4))

    def currentturn_draw(self, window: object, turns: int) -> None:
        """Changes turn related data on the toolbar's grid."""
        xon = self.xrn * self.BLOCK + 3 * self.BLOCK
        yon = 0
        font = py.font.SysFont("Arial Bold", 32)
        pgfx.box(window, py.Rect(xon, yon, 3 * self.BLOCK, self.BLOCK), self.toolbar_bgcolor)
        text = font.render('{}. day'.format(turns), True, self.toolbar_fgcolor)
        window.blit(text, (xon + 2, yon + 4))

    def currentmoney_draw(self, window: object, team: str) -> None:
        """Changes the money display on the toolbar, to show the funds of the currently active team."""
        xon = self.xrn * self.BLOCK
        yon = self.BLOCK
        font = py.font.SysFont("Arial Bold", 22)
        pgfx.box(window, py.Rect(xon, yon, 6 * self.BLOCK, self.BLOCK), self.toolbar_bgcolor)
        buildings = font.render('Buildings: {}'.format(self.team_buildings[team]), True, self.toolbar_fgcolor)
        money = font.render('Funds: {}'.format(self.team_money[team]), True, self.toolbar_fgcolor)
        window.blit(buildings, (xon + 4, yon + 8))
        window.blit(money, (xon + 4 + (3 * self.BLOCK), yon + 8))

    def terraininfo_draw(self, window: object, terrain: terrains.Terrain) -> None:
        """Displays all information of the given terrain."""
        xon = self.xrn * self.BLOCK
        yon = 2 * self.BLOCK
        font = py.font.SysFont("Arial Bold", 22)
        teamcolor = self.color_red if terrain.team == "Red" else self.color_blue
        terrain_title = font.render("{}{}".format("" if terrain.team is None else terrain.team + " ", terrain.type), True, self.toolbar_fgcolor if terrain.team is None else teamcolor)
        font = py.font.SysFont("Arial Bold", 16)
        capture_info = "Capture: {}%".format(terrain.remaining_health()) if terrain.capturable else ""
        terrain_info1 = font.render("Defense: {}    {}".format(terrain.defense, capture_info), True, self.toolbar_fgcolor)
        valid_transports = ""
        if terrain.all_one_movement():
            valid_transports = "All movement types: 1"
        else:
            valid_transports = ", ".join(["{}: {}".format(transports, terrain.transports[transports]) for transports in terrain.transports if terrain.transports[transports] != 0])
        terrain_info2 = font.render("{}".format(valid_transports), True, self.toolbar_fgcolor)
        window.blit(terrain_title, (xon + 4, yon + 12))
        terrains.block_draw(terrain, window, (xon + 5 * self.BLOCK, yon))
        window.blit(terrain_info1, (xon + 4, yon + self.BLOCK + 4))
        window.blit(terrain_info2, (xon + 2, yon + self.BLOCK + self.BLOCK // 2 + 4))

    def unitinfo_draw(self, window: object, unit: units.Unit) -> None:
        """Displays all information of the given unit."""
        xon = self.xrn * self.BLOCK
        yon = 4 * self.BLOCK
        font = py.font.SysFont("Arial Bold", 16)
        unit_title = font.render("{} unit:  {}%".format(unit.type, round(unit.health, 2)), True, self.color_red if unit.team == "Red" else self.color_blue)
        attack_range = "{}".format(unit.maxrange) if unit.minrange == 1 else "{}-{}".format(unit.minrange, unit.maxrange)
        unit_info1 = font.render("Can attack?  {}    Range:  {}".format("Yes" if not unit.attacked else "No", attack_range), True, self.toolbar_fgcolor)
        unit_info2 = font.render("Ammo:  {}    Moves:  {}".format(unit.ammunition, unit.speed - unit.moved), True, self.toolbar_fgcolor)
        unit_info3 = font.render("Can move?  {}    Type:  {}".format("Yes" if unit.moved < unit.speed else "No", unit.movement), True, self.toolbar_fgcolor)
        window.blit(unit_title, (xon + 2, yon + 2))
        window.blit(unit_info1, (xon + 2, yon + self.BLOCK // 2 + 2))
        units.block_draw(unit, window, (xon + 5 * self.BLOCK, yon))
        window.blit(unit_info2, (xon + 2, yon + self.BLOCK + 2))
        window.blit(unit_info3, (xon + 2, yon + self.BLOCK + self.BLOCK // 2 + 2))

    def endturn_draw(self, window: object, message: str, fgcolor: py.Color) -> None:
        """Displays the end turn button, based on given parameters."""
        xon = self.xrn * self.BLOCK + self.BLOCK
        yon = self.yrn * self.BLOCK - 4 * self.BLOCK
        font = py.font.SysFont("Arial Bold", 40)
        pgfx.box(window, py.Rect(xon, yon, 4 * self.BLOCK, 2 * self.BLOCK), self.toolbar_bgcolor)
        text = font.render(message, True, fgcolor)
        window.blit(text, (xon + 2, yon + 20))

    def exit_draw(self, window: object, message: str, fgcolor: py.Color) -> None:
        """Displays the exit button, based on given parameters."""
        xon = self.xrn * self.BLOCK + self.BLOCK
        yon = self.yrn * self.BLOCK - self.BLOCK
        font = py.font.SysFont("Arial Bold", 36)
        pgfx.box(window, py.Rect(xon, yon, 4 * self.BLOCK, self.BLOCK), self.toolbar_bgcolor)
        text = font.render(message, True, fgcolor)
        window.blit(text, (xon + 20, yon + 4))

    def map_drawadd(self, window: object, rawmap: list[list]) -> None:
        """Prepares every element of the display window and draws them according to the grid data."""
        self.team_buildings, self.terrainmap = terrains.drawadd(window, self.BLOCK, rawmap, self.xrn, self.yrn)
        self.unitmap = units.drawadd(window, self.BLOCK, self.terrainmap, self.xrn, self.yrn)
        for team in self.TEAMS:
            self.start_day(team)
        self.endturn_draw(window, 'End Turn', self.toolbar_fgcolor)
        self.exit_draw(window, 'Exit', self.toolbar_fgcolor)
        py.display.update()

    def update_toolbar(self, window: object, turn: int, turns: int, selected: Index, on: Index, spawner_selected: bool) -> None:
        """Updates the toolbar based on currently active team, turn and selection data."""
        self.currentteam_draw(window, self.TEAMS[turn])
        self.currentturn_draw(window, turns)
        self.currentmoney_draw(window, turn)
        if not spawner_selected:
            pgfx.box(window, py.Rect(self.xrn * self.BLOCK, 2 * self.BLOCK, 6 * self.BLOCK, 4 * self.BLOCK), self.toolbar_bgcolor)
            if on is not None and on.x < self.xrn:
                self.terraininfo_draw(window, self.terrainmap[on.x][on.y])
            if selected is not None:
                self.unitinfo_draw(window, self.unitmap[selected.x][selected.y])
        py.display.update()

    def workshopselected_draw(self, window: object) -> None:
        """Displays all units in the workshop grid space for buying."""
        xon = self.xrn * self.BLOCK
        yon = 2 * self.BLOCK
        font = py.font.SysFont("Arial Bold", 16)
        pgfx.box(window, py.Rect(xon, yon, 6 * self.BLOCK, 4 * self.BLOCK), self.toolbar_bgcolor)
        counter = 0
        for i in range(0, len(self.unit_types), 2):
            textone = font.render("{}: {}".format(self.unit_types[i], self.unit_prices[i]), True, self.toolbar_fgcolor)
            texttwo = font.render("{}: {}".format(self.unit_types[i+1], self.unit_prices[i+1]), True, self.toolbar_fgcolor)
            window.blit(textone, (xon + 2, yon + 2 + counter * (self.BLOCK // 2)))
            window.blit(texttwo, (xon + 2 + 3 * self.BLOCK, yon + 2 + counter * (self.BLOCK // 2)))
            counter += 1

    def winner_draw(self, window: object, winner: Index, teamcolor: str) -> None:
        """Displays winner on window based on given data."""
        self.victor = self.unitmap[winner.x][winner.y].team
        self.endturn_draw(window, "Winner:", teamcolor)
        self.exit_draw(window, "{}".format(self.victor), teamcolor)

    def win_view(self, in_map: bool, on: Index, mapname: str, playernames: tuple, turns: int) -> tuple:
        """Takes in all data regarding the winning side and handles all victory related possibilites that could occur.
            Returns with a tuple containing the Index of the last selection and if the player(s) quit while winning."""
        if not in_map and self.toolbar[on.x-self.xrn][on.y] != 0:
            self.write_statistics("matchhistory.txt", playernames, turns, mapname)
            return None, True
        elif in_map and self.unitmap[on.x][on.y] is not None:
            return Index(on.x, on.y), False
        return None, False

    def write_statistics(self, location: str, playernames: tuple, turns: int, mapname: str) -> None:
        """Takes all data regarding the match and writes it in a text file for storage."""
        matchhistory = []
        victor = playernames[0] if self.victor == "Red" else playernames[1]
        loser = playernames[1] if self.victor == "Red" else playernames[0]
        matchhistory.append("{} took {} turns to defeat {} on the {} map.".format(victor, turns, loser, mapname))
        try:
            with open(location, "rt", encoding="utf-8") as fr:
                matchhistory = [line.rstrip('\n') for line in fr]
            while len(matchhistory) > 10:
                matchhistory.pop()
        except FileNotFoundError:
            pass
        with open(location, "wt", encoding="utf-8") as fw:
            for line in matchhistory:
                fw.write(line + '\n')

    def end_turn(self, team: str, count: int) -> tuple:
        """Handles all data for ending the turn. Returns with a tuple containing the appropriate turn datas."""
        if team == len(self.TEAMS) - 1:
            for i in range(len(self.TEAMS)):
                self.team_money[i] += self.team_buildings[i] * 10
            self.start_day(self.TEAMS[0])
            return 0, count + 1
        self.start_day(self.TEAMS[team + 1])
        return team + 1, count

    def unit_step_on(self, window: object, on: Index, selected: Index, xmod: int = 0, ymod: int = 0) -> tuple:
        """Function that makes selected unit take a step towards the choosen direction and returns with a tuple containing the new two new Index objects."""
        if on is None:
            on = Index(selected.x + xmod, selected.y + ymod)
        self.terrainmap[selected.x][selected.y].health = self.unit_movement(window, selected, on)
        self.unitmap[on.x][on.y], self.unitmap[selected.x][selected.y] = self.unitmap[selected.x][selected.y], None
        self.unitmap[on.x][on.y].has_moved(self.terrainmap[on.x][on.y])
        return Index(on.x, on.y), Index(on.x, on.y)

    def unit_attacking_on(self, on: Index, selected: Index, distance: int) -> None:
        """Handles attacks between two untis, that are found witht the given Index objects. 
            If the attacked unit lived and can counterattack, then the attacker takes damage as well"""
        self.unitmap[on.x][on.y].getting_attacked(self.unitmap[selected.x][selected.y], self.terrainmap[on.x][on.y])
        if distance == 1 and self.unitmap[on.x][on.y].minrange == 1 and self.unitmap[on.x][on.y].health > 0:
            self.unitmap[selected.x][selected.y].getting_attacked(self.unitmap[on.x][on.y], self.terrainmap[selected.x][selected.y])
        self.unitmap[selected.x][selected.y].has_attacked()

    def unit_capturing_on(self, window: object, on: Index, selected: Index) -> bool:
        """Function that handles property capture based on locations and returns a boolean with the result."""
        team = self.terrainmap[selected.x][selected.y].team
        self.unitmap[selected.x][selected.y].has_attacked()
        if self.terrainmap[selected.x][selected.y].getting_captured(self.unitmap[selected.x][selected.y]):
            return self.unit_finished_capture(window, on, team)
        return False

    def unit_finished_capture(self, window: object, on: Index, team: Index) -> bool:
        """Function that checks to see if unit has finished capture of building. If an opposing HQ was captured returns True, otherwise False."""
        team_id = 0 if self.unitmap[on.x][on.y].team == "Red" else 1
        if team == 'Red':
            self.team_buildings[0] -= 1
        elif team == 'Blue':
            self.team_buildings[1] -= 1
        self.team_buildings[team_id] += 1
        terrains.block_draw(self.terrainmap[on.x][on.y], window, (on.x * self.BLOCK, on.y * self.BLOCK))
        units.block_draw(self.unitmap[on.x][on.y], window, (on.x * self.BLOCK, on.y * self.BLOCK))
        if self.terrainmap[on.x][on.y].is_a_hq():
            self.winner_draw(window, on, self.color_red if self.unitmap[on.x][on.y].team == "Red" else self.color_blue)
            return True
        return False

    def move_on_terrain(self, on: Index, selected: Index, turn: int) -> bool:
        """Checks if the selected unit can do a valid move on the mouse-selected terrain('s location)."""
        is_team_turn = self.unitmap[selected.x][selected.y].team == self.TEAMS[turn]
        return is_team_turn and abs(on - selected) == 1 and self.unitmap[selected.x][selected.y].enough_moves_left(self.terrainmap[on.x][on.y])

    def keyboard_movement(self, selected: Index, turn: int, xmod: int = 0, ymod: int = 0) -> bool:
        """Checks if selected unit can do a valid move on the given terrain('s location), based on keyboard movement."""
        is_team_turn = self.unitmap[selected.x][selected.y].team == self.TEAMS[turn]
        is_empty = self.unitmap[selected.x + xmod][selected.y + ymod] is None
        return is_team_turn and self.unitmap[selected.x][selected.y].enough_moves_left(self.terrainmap[selected.x + xmod][selected.y + ymod]) and is_empty

    def unit_movement(self, window: object, selected: Index, on: Index) -> int:
        """Redraws the terrain and unit on the grid after movement and returns with the full health value of the terrain."""
        terrains.block_draw(self.terrainmap[selected.x][selected.y], window, (selected.x * self.BLOCK, selected.y * self.BLOCK))
        units.block_draw(self.unitmap[selected.x][selected.y], window, (on.x * self.BLOCK, on.y * self.BLOCK))
        return self.terrainmap[selected.x][selected.y].default_health

    def workshop_production(self, window: object, turn: int, location: Index, on: Index) -> tuple:
        """Produces the selected unit for the appropriate team, then returns with a tuple containing the location data. Does nothing if purchase was not valid."""
        unit_selection = self.workshop[on.x][on.y]
        if self.team_money[turn] >= self.unit_prices[unit_selection] and self.unit_prices[unit_selection] != 0:
            self.team_money[turn] -= self.unit_prices[unit_selection]
            self.unitmap[location.x][location.y] = units.spawn_unit(self.TEAMS[turn], self.unit_types[unit_selection])
            units.block_draw(self.unitmap[location.x][location.y], window, (location.x * self.BLOCK, location.y * self.BLOCK))
            return location, location, False
        return None, None, True

    def check_casualties(self, window: object, on: Index, selected: Index) -> tuple:
        """Checks to see if any new units have died, then returns the selection data."""
        if self.unitmap[on.x][on.y].health <= 0:
            return selected, self.unit_died(window, on, selected)
        elif self.unitmap[selected.x][selected.y].health <= 0:
            return None, self.unit_died(window, selected, on)
        return selected, False

    def unit_died(self, window: object, killed: Index, killer: Index) -> None:
        """Checks for unit death circumstances and returns true if the killed unit was the last of its team (leading to a win condition)."""
        terrains.block_draw(self.terrainmap[killed.x][killed.y], window, (killed.x * self.BLOCK, killed.y * self.BLOCK))
        team = self.unitmap[killed.x][killed.y].team
        self.terrainmap[killed.x][killed.y].health = self.terrainmap[killed.x][killed.y].default_health
        self.unitmap[killed.x][killed.y] = None
        if self.last_unit_killed(team):
            self.winner_draw(window, killer, self.color_red if self.unitmap[killer.x][killer.y].team == "Red" else self.color_blue)
            return True
        return False

    def last_unit_killed(self, team: str) -> bool:
        """Checks to see if there are any other units remaining of the faction."""
        #While not the most optimal solution, I'm really proud of managing to put this much functionality in a single line.
        return all([all([unit.team != team for unit in line if unit is not None]) for line in self.unitmap])

    def start_day(self, team: str) -> None:
        """Function that does all actions for starting the given teams turn, by reseting actions and healing if valid."""
        for x in range(len(self.unitmap)):
            for y in range(len(self.unitmap[0])):
                if self.unitmap[x][y] is not None and self.unitmap[x][y].team == team:
                    self.unitmap[x][y].reset_actions()
                    if team == self.unitmap[x][y].team and self.unitmap[x][y].team == self.terrainmap[x][y].team:
                        self.unitmap[x][y].heal_up()