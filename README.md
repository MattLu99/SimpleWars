# Simple Wars
### About the project
This is a project I made for a university assignment in 2019 for the purpose of learning how to use Python. The game is heavily based on the “Advance Wars” game series and many of its features are similar, however certain features/mechanics are very different: addition of more infantry units, difference in damage calculation (new damage types that perform differently based on attacked unit’s armor), absence of aerial and naval units, body-blocking, lack of ammunition and transports.<br/>
The making of this game was a great learning experience and it took me approximately 140 hours to make the whole thing (not counting the time I spent learning Python). The setup window uses TKinter and the actual game uses pygame. The game can store the history of the previously played games in a text file, which is limited to a maximum of 10 game data stored.
The project is mostly in the same way it was back in 2019, I like to preserve it in an “as-it-was-made” state. Only modifications I have made since have been made to make the code more readable or generally improve its documentation.
### Start the game
You can run the game if you: have Python and pygame (pip3 install pygame) installed on your system. If you meet these requirements then all you have to do is run the “SimpleWars.pyw” file and the game should start. The game requires two players to play, have fun!

## Controls
### Mouse
Unit/terrain selection: left-click on a tile.<br/>
  - Left-click on the tile again to unselect the unit.<br/>
  - For factory: left-click again to list units.<br/>
      - Left-click on a purchasable unit to have it spawn.<br/>
Unit movement: left-click on a valid adjacent tile.<br/>
Unit attack: right-click on a unit in range.<br/>
Unit capture: right-click on the tile the unit is on.<br/>
End turn: left-click on the "End Turn" button.<br/>
Exit: left-click on the "Exit" button.
### Keyboard
Movement: W/^ - Up, A/< - Left, S/ˇ - Down, D/> - Right<br/>
Capture: Space, End turn: Enter, Exit: Escape

## How to make your own maps
You can make your own maps by creating a text file, filling it up with the right characters and putting it inside the maps folder. The setup window will automatically detect it and allow you to play on it if it meets all the criteria set for maps, otherwise it will not and notify you of the reason. To make a map, think of your text file as a grid full of letters, where each letter represents a terrain. Each terrain has values that determine how easy it is for different types of units to move on them and they also have a differing defense value that helps the unit that's on it. You can read about the specific details of each terrain in the “__block_translator” method of the “terrains.py” file, but in short, the letters that stand for something are:<br/>
  - O - Saltwater<br/>
  - L - Freshwater<br/>
  - P - Plains<br/>
  - S - Swamp<br/>
  - F - Forest<br/>
  - M - Mountain<br/>
  - D - Wreckage<br/>
  - A - Ghost Town<br/>
  - C - City<br/>
  - 1 - City For Red Team<br/>
  - 2 - City For Blue Team<br/>
  - W - Factory<br/>
  - H - Headquarters<br/>
  - R - Road/Bridge<br/>
Some special features to note about the terrains are that roads auto-detect each other and properties, and correctly chain up based on adjacent tiles. Alternatively, roads can also turn into bridges if they are surrounded by water. Also, if there is any letter in the file that is not recognized, then it is treated as a “Saltwater” tile.<br/>
Each map must have exactly two headquarters and at least two factory tiles to be accepted. It must also have at least 10 letters in height and 10 letters in width, this is to make sure the sidebar functions as intended, but you can have a smaller map by filling up the “empty space” with “Saltwater” since no unit can step on it.<br/>
The way each team gets their headquarters is that the map “translator” looks for the headquarters from the top left, column-by-column, and the first one it finds is going to be the Red team’s HQ while the other one is going to be the Blue team’s HQ.