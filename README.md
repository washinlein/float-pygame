# float-pygame

#### Introduction
The goal of this project is to create a simple game and learn python using pygame library. 
Comments and positive feedback are very welcome!

#### Float - Game Description
"Float" is a simple platform game with some puzzle and skill mechanics. The goal of the game is to collect all lamps in each room in order to get to the next. The game finishes when 
all rooms have been completed.

- Player movement:
    - The player starts at the top of the room and can only move left or right.
    - Jump off the platforms to get to lower positions and collect items along the way. 
    - While in mid-air the player can activate his floating ability which allows him to slow down the falling speed so he can collect more items.
    
- Collecting lamps:
     - Only lit lamps can be collected so that if the player collects an unlit lamp, the room resets and he'll have to try again.
     - The order in which the lamps are lit depends on the current room setup and the player will have to figure out how to get to the next lamp without falling below it, as he won't be able to reach for it again.

#### Python version and current dependencies

- Python 2.7
- pygame 1.9.3
- PyTMX 3.20.17
