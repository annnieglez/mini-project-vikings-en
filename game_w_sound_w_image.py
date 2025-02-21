import time
import sys
import random
from vikingsClasses import Soldier, Viking, Saxon, War
import names
from playsound import playsound
from threading import Thread, Event, Lock
import os
import sys
import pygame

stop_event = Event()
output_lock = Lock()

#Intro
def star_wars_intro():
    intro_text = """
    A long time ago in a land far, far away
    The mighty Vikings, fierce and relentless, have set sail 
    from the frozen north, seeking conquest and glory. 
    Meanwhile, the Saxons, stalwart defenders of their fertile lands,
    stand ready to repel the invaders.
    A great battle is about to begin, a clash of steel and willpower
    that will determine the fate of the realm.
    Who will emerge victorious in this epic war?
    Let the battle begin!
    """

    for line in intro_text.split("\n"):
        for char in line:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.03)
        print()

#User imput
def get_user_input():

    # Input Vikings
    while True:
        try:
            viking_warriors = int(input("Enter the number of Viking warriors: "))
            if viking_warriors < 1:
                print("Viking armie must have more than one warrior. Try again.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    #Input Saxons
    while True:
        try:
            saxon_warriors = int(input("Enter the number of Saxon warriors: "))
            if saxon_warriors < 1:
                print("Saxon armie must have more than one warrior. Try again.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
        
    return [viking_warriors, saxon_warriors]

#User bet
def get_user_bet():
    while True:
        user_bet = input("Who do you think will win? Type 'Vikings' or 'Saxons': ").strip().lower()
        if user_bet in ["vikings", "saxons"]:
            return user_bet.capitalize()
        print("Invalid choice. Please type 'Vikings' or 'Saxons'.")

# Generate a random list of names
def generate_realistic_names(count):
    return [names.get_full_name() for name in range(count)]

def battle_animation():
    signs = ["|", "/", "-", "\\"]
    while not stop_event.is_set():  
        for sign in signs:
            sys.stdout.write(f"\rBattle in progress... {sign}") 
            sys.stdout.flush()
            time.sleep(0.2) 
    time.sleep(0.5) 
    with output_lock:  # Clear the Battle in progress line after stopping
        sys.stdout.write("\rWar has ended" + " " * 50 + "\n")
        sys.stdout.flush()

def show_image():
    pygame.init()
    
    # dimension 
    X = 540
    Y = 360

    scrn = pygame.display.set_mode((X, Y)) # create the display surface object of specific dimension
    pygame.display.set_caption("Let the battle start") # set the pygame window name
    
    imp = pygame.image.load("./war_1.jpg").convert() # create a surface object, image is drawn on it
    scrn.blit(imp, (0, 0)) # using blit to copy content from one surface to another
    pygame.display.flip()
    time.sleep(8)
    pygame.quit()

def show_happy_image(winner):
    pygame.init()
    
    # dimension 
    X = 600
    Y = 400

    scrn = pygame.display.set_mode((X, Y)) # create the display surface object of specific dimension
    pygame.display.set_caption(f"Congratulations! You guessed right, {winner} won!") # set the pygame window name
    
    imp = pygame.image.load("./Leonardo-Dicaprio-Cheers.jpg").convert() # create a surface object, image is drawn on it
    scrn.blit(imp, (0, 0)) # using blit to copy content from one surface to another
    pygame.display.flip()
    time.sleep(8)
    pygame.quit()

def show_sad_image():
    pygame.init()
    
    # dimension 
    X = 750
    Y = 1000

    scrn = pygame.display.set_mode((X, Y)) # create the display surface object of specific dimension
    pygame.display.set_caption(f"Better luck next time!") # set the pygame window name
    
    imp = pygame.image.load("./better_luck.jpg").convert() # create a surface object, image is drawn on it
    scrn.blit(imp, (0, 0)) # using blit to copy content from one surface to another
    pygame.display.flip()
    time.sleep(8)
    pygame.quit()

def main():

    #Intro
    
    #star_wars_intro()

    show_image() # show an war image at the start of the game

    #User imput
    army_count = get_user_input()
    user_bet = get_user_bet()
    
    time.sleep(1)
    print("\nLet the battle decide the fate of the realm\n")
    # An animation while calculatios are done
    animation_thread = Thread(target=battle_animation)
    animation_thread.start()

    #Let's begin the army construction
    great_war = War()

    #Create Vikings
    list_names = generate_realistic_names(army_count[0])
    for i in range(0,army_count[0]):
        great_war.addViking(Viking(random.choice(list_names),100,random.randint(0,100)))

    #Create Saxons
    for i in range(0,army_count[1]):
        great_war.addSaxon(Saxon(100,random.randint(0,100)))
    
    #Let's begin the war
    round = 0
    war_result = ""

    while great_war.showStatus() == "Vikings and Saxons are still in the thick of battle.":
        great_war.vikingAttack()
        great_war.saxonAttack()
        #print(f"round: {round} // Viking army: {len(great_war.vikingArmy)} warriors",f"and Saxon army: {len(great_war.saxonArmy)} warriors")
        #print(great_war.showStatus())
        war_result = great_war.showStatus()
        round += 1

    # Stop the animation
    stop_event.set()
    time.sleep(2)
    #print("War has ended\n")
    #Lets show the war results 
    print (war_result)

    #Lets se the bet results
    if user_bet.lower() in war_result.lower():
        show_happy_image(user_bet)

    else:
        show_sad_image()

    print(f"Let's play again!")
    os._exit(1)

def playmusic():
    songfilename = 'soundlong.mp3' #soundlong.mp3
    playsound(songfilename, 1)

# Run the game
if __name__ == "__main__":

    textThread = Thread(target=main)
    soundThread = Thread(target=playmusic)
    soundThread.start()
    textThread.start()