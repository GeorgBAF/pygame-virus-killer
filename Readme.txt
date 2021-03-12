# Simple 2-player space stoot'm'up game using pygame. I used the original code that Tim (Tech with Tim) goes through and shares in this video. 
# https://www.youtube.com/watch?v=jO6qQDNa2UY
# 
# I added/changed the follow functionality in Tims original code:
# Background music and red fighter sound effect changed.
# Background image  and some text colors changed. Red fighter changed to virus graphic. 
# Splash screen with instructions for the single/two players.
# Default is one-player mode, where the virus moves and fires randomly. 
# If player 2 keys are touched, the gameplay changes to 2-player mode. 
# A syringe (vaccine) graphic added that protects the starfigter against the virus. 
# The virus comes in three waves. Each time the virus moves more aggresivly, and starfighter fire velocity decreses.
# The starfighter needs to beat the virus 3 times to win the game.
# Added a py2exe setup.py file to create exe, but ended up using pyinstaller to create the exe instead. 
# 
# Exe created with pyinstaller main2.py --onefile --noconsole (package all in one file and do not show console window during runtime)
# Added "Assets" folder next to exe file to have all the files needed to run.
# Had to whitelist the exe in Avast antivirus, or else it would block it.
#
# This application is soly for demonstation purposes. Some files and code could be copyright protected. Please do not distribute or use comercially.
