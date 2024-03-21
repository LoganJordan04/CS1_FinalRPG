import os
import sys
import subprocess
import time
import random
from characters import *

# Fix if the console doesn't print the color properly.
os.system("")


def battle_print(hero, enemy, start, healing):
    if start:
        # Clears the screen
        os.system("cls")
        Hero.draw(hero)
        Enemy.draw(enemy)
        hero.health_bar.draw()
        enemy.health_bar.draw()
        print("\n+-------------------------------------------------+")
        # Statements for "a" vs "an" in encounter text.
        if enemy.name.lower().startswith(('a', 'e', 'i', 'o', 'u')):
            print(f"{hero.name} encountered an {enemy.name}!")
        else:
            print(f"{hero.name} encountered a {enemy.name}!")
        # Potion amount print.
        print(f"\nYou have {hero.potions} potions.")
        # Text to advance turn.
        if hero.potions > 0:
            print(f"\nPress A to attack.\nPress H to heal {hero.heal_amount} health.")
        else:
            print(f"\nPress A to attack.")
    else:
        if healing:
            hero.heal()
        os.system("cls")
        Hero.draw(hero)
        Enemy.draw(enemy)
        hero.health_bar.draw()
        enemy.health_bar.draw()
        print("\n+-------------------------------------------------+")
        if healing:
            hero.heal_print()
        else:
            hero.attack_print(enemy)
            enemy.attack_print(hero)
        # Updates the healing amount.
        hero.heal_update()
        print(f"\nYou have {hero.potions} potions.")
        # Determines if the player can heal or not.
        if hero.potions > 0:
            print(f"\nPress A to attack.\nPress H to heal {hero.heal_amount} health.")
        else:
            print(f"\nPress A to attack.")


def drop_print(hero, enemy):
    print(f"\n{enemy.name} dropped {enemy.weapon.name}! Press E to equip it.")
    # Comparing the current weapon and dropped weapon.
    print(f"{hero.weapon.name} damage: {hero.weapon.damage} -> "
          f"{enemy.weapon.name} damage: {enemy.weapon.damage}")


def advance_print(hero, enemy, is_collected, is_dropped, is_buying):
    if not is_buying:
        os.system("cls")
        Hero.draw(hero)
        hero.health_bar.draw()
        print("\n+-------------------------------------------------+")
        # If the dropped coins aren't collected yet.
        if not is_collected:
            hero.coins += enemy.coins
            print(f"{enemy.name} dropped {enemy.coins} coins!")
            print(f"\nYou now have {hero.coins} coins and {hero.potions} potions")
        else:
            print(f"You have {hero.coins} coins and {hero.potions} potions")
        # If the enemy dropped their weapon.
        if is_dropped:
            drop_print(hero, enemy)
        print(f"\nPress B to buy a potion for 20 coins.\nPress Enter to advance.")

    else:
        os.system("cls")
        Hero.draw(hero)
        hero.health_bar.draw()
        print("\n+-------------------------------------------------+")
        if hero.coins < 20:
            print("You don't have enough to buy a potion!")
            print(f"\nYou have {hero.coins} coins and {hero.potions} potions")
        # Buying a potion.
        else:
            hero.potions += 1
            hero.coins -= 20
            print(f"You now have {hero.coins} coins and {hero.potions} potions")
        if is_dropped:
            drop_print(hero, enemy)
        print(f"\nPress B to buy a potion for 20 coins.\nPress Enter to advance.")


def main():
    print("""
                ▄█     █▄   ▄█  ███▄▄▄▄      ▄██████▄     ▄████████       ▄██████▄     ▄████████                     
               ███     ███ ███  ███▀▀▀██▄   ███    ███   ███    ███      ███    ███   ███    ███                     
               ███     ███ ███▌ ███   ███   ███    █▀    ███    █▀       ███    ███   ███    █▀                      
               ███     ███ ███▌ ███   ███  ▄███          ███             ███    ███  ▄███▄▄▄                         
               ███     ███ ███▌ ███   ███ ▀▀███ ████▄  ▀███████████      ███    ███ ▀▀███▀▀▀                         
               ███     ███ ███  ███   ███   ███    ███          ███      ███    ███   ███                            
               ███ ▄█▄ ███ ███  ███   ███   ███    ███    ▄█    ███      ███    ███   ███                            
                ▀███▀███▀  █▀    ▀█   █▀    ████████▀   ▄████████▀        ▀██████▀    ███                            
                                                                                                                     
   ▄████████    ▄████████ ████████▄     ▄████████   ▄▄▄▄███▄▄▄▄      ▄███████▄     ███      ▄█   ▄██████▄  ███▄▄▄▄   
  ███    ███   ███    ███ ███   ▀███   ███    ███ ▄██▀▀▀███▀▀▀██▄   ███    ███ ▀█████████▄ ███  ███    ███ ███▀▀▀██▄ 
  ███    ███   ███    █▀  ███    ███   ███    █▀  ███   ███   ███   ███    ███    ▀███▀▀██ ███▌ ███    ███ ███   ███ 
 ▄███▄▄▄▄██▀  ▄███▄▄▄     ███    ███  ▄███▄▄▄     ███   ███   ███   ███    ███     ███   ▀ ███▌ ███    ███ ███   ███ 
▀▀███▀▀▀▀▀   ▀▀███▀▀▀     ███    ███ ▀▀███▀▀▀     ███   ███   ███ ▀█████████▀      ███     ███▌ ███    ███ ███   ███ 
▀███████████   ███    █▄  ███    ███   ███    █▄  ███   ███   ███   ███            ███     ███  ███    ███ ███   ███ 
  ███    ███   ███    ███ ███   ▄███   ███    ███ ███   ███   ███   ███            ███     ███  ███    ███ ███   ███ 
  ███    ███   ██████████ ████████▀    ██████████  ▀█   ███   █▀   ▄████▀         ▄████▀   █▀    ▀██████▀   ▀█   █▀  
  ███    ███                                                                                                         


                                     Equipped with fists and 5 healing potions, 
             you will battle 20 enemies of increasing difficulty as a chicken to take back what's yours.
                
                                             Press Enter to continue...
    """)
    keyboard.wait("enter")

    restart = True

    while restart:
        hero = Hero("You", 200, 5, 0)
        alive = True

        enemy_num = 1

        while alive:
            # Picking a random enemy of the first tier.
            if enemy_num <= 5:
                enemy = random.choice(tier1_enemies)
            # Picking a random enemy of the 1st and 2nd tiers after 5 enemies.
            # The harder enemies are more likely to be picked.
            elif enemy_num <= 10:
                enemy_choice = random.choices(tier2_enemies, weights=[1, 1, 1, 1, 3, 3, 3])
                # random.choices() returns a list, so this sets the enemy to the actual object.
                enemy = enemy_choice[0]
            # Picking a random enemy of the 2nd and 3rd tiers after 10 enemies.
            elif enemy_num <= 15:
                enemy_choice = random.choices(tier3_enemies, weights=[1, 1, 1, 3, 3])
                enemy = enemy_choice[0]
            # Picking a random enemy of the 3rd and 4th tiers after 15 enemies.
            elif enemy_num <= 20:
                enemy_choice = random.choices(tier4_enemies, weights=[1, 1, 2, 2])
                enemy = enemy_choice[0]
            # Ending the game after 20 enemies.
            else:
                break

            # Sets the enemies health to max so an instance can occur more than once.
            enemy.reset_health()
            enemy.health_bar.update()

            # Initial battle screen printing.
            battle_print(hero, enemy, start=True, healing=False)

            while hero.health > 0 and enemy.health > 0:
                if keyboard.is_pressed("a"):
                    hero.attack(enemy)
                    enemy.attack(hero)
                    battle_print(hero, enemy, start=False, healing=False)
                    # Delay to fix problems with rapid inputs.
                    time.sleep(0.25)
                elif keyboard.is_pressed("h"):
                    battle_print(hero, enemy, start=False, healing=True)
                    time.sleep(0.25)

            if hero.health == 0:
                alive = False
                break

            # This sets the value for the coin drop text to be printed.
            is_collected = False

            # 1/2 chance for an enemy to drop their weapon.
            item_drop = random.randint(1, 2)

            # Weapon can't be equipped if its fists, teeth, or hero is already holding it.
            if (item_drop == 1 and enemy.weapon.name != "Fists" and enemy.weapon.name != "Teeth"
                    and enemy.weapon.name != hero.weapon.name):
                is_dropped = True
                advance_print(hero, enemy, is_collected, is_dropped, is_buying=False)
                # Collecting the coin drop.
                is_collected = True
                while keyboard.read_key() != "enter":
                    # Equipping the dropped weapon.
                    if keyboard.read_key() == "e" and enemy.weapon.name != hero.weapon.name:
                        is_dropped = False
                        hero.equip(enemy.weapon)
                        advance_print(hero, enemy, is_collected, is_dropped, is_buying=False)
                        time.sleep(0.25)
                    # Buying a potion if the player has sufficient coins.
                    elif keyboard.read_key() == "b":
                        advance_print(hero, enemy, is_collected, is_dropped, is_buying=True)
                        time.sleep(0.25)
                    # Hitting enter breaks the loop to advance the game.
                    elif keyboard.read_key() == "enter":
                        break
            # If the player didn't get a weapon drop.
            else:
                is_dropped = False
                advance_print(hero, enemy, is_collected, is_dropped, is_buying=False)
                is_collected = True
                while keyboard.read_key() != "enter":
                    if keyboard.read_key() == "b":
                        advance_print(hero, enemy, is_collected, is_dropped, is_buying=True)
                        time.sleep(0.25)
                    elif keyboard.read_key() == "enter":
                        break

            enemy_num += 1

        # Printing the loss screen.
        if not alive:
            os.system("cls")
            print("""\033[91m
    ▓██   ██▓ ▒█████   █    ██     ██▓     ▒█████    ██████ ▓█████  ▐██▌ 
     ▒██  ██▒▒██▒  ██▒ ██  ▓██▒   ▓██▒    ▒██▒  ██▒▒██    ▒ ▓█   ▀  ▐██▌ 
      ▒██ ██░▒██░  ██▒▓██  ▒██░   ▒██░    ▒██░  ██▒░ ▓██▄   ▒███    ▐██▌ 
      ░ ▐██▓░▒██   ██░▓▓█  ░██░   ▒██░    ▒██   ██░  ▒   ██▒▒▓█  ▄  ▓██▒ 
      ░ ██▒▓░░ ████▓▒░▒▒█████▓    ░██████▒░ ████▓▒░▒██████▒▒░▒████▒ ▒▄▄  
       ██▒▒▒ ░ ▒░▒░▒░ ░▒▓▒ ▒ ▒    ░ ▒░▓  ░░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░░░ ▒░ ░ ░▀▀▒ 
     ▓██ ░▒░   ░ ▒ ▒░ ░░▒░ ░ ░    ░ ░ ▒  ░  ░ ▒ ▒░ ░ ░▒  ░ ░ ░ ░  ░ ░  ░ 
     ▒ ▒ ░░  ░ ░ ░ ▒   ░░░ ░ ░      ░ ░   ░ ░ ░ ▒  ░  ░  ░     ░       ░ 
     ░ ░         ░ ░     ░            ░  ░    ░ ░        ░     ░  ░ ░    
     ░ ░                                                                 
    \033[0m
                             Press R to restart.
                             Press Enter to quit.
            """)
        # Printing the win screen.
        if alive:
            os.system("cls")
            print("""\033[92m
    ██╗   ██╗ ██████╗ ██╗   ██╗    ██╗    ██╗██╗███╗   ██╗██╗
    ╚██╗ ██╔╝██╔═══██╗██║   ██║    ██║    ██║██║████╗  ██║██║
     ╚████╔╝ ██║   ██║██║   ██║    ██║ █╗ ██║██║██╔██╗ ██║██║
      ╚██╔╝  ██║   ██║██║   ██║    ██║███╗██║██║██║╚██╗██║╚═╝
       ██║   ╚██████╔╝╚██████╔╝    ╚███╔███╔╝██║██║ ╚████║██╗
       ╚═╝    ╚═════╝  ╚═════╝      ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═╝
    \033[0m
                       Press R to restart.
                       Press Enter to quit.
            """)
        # If the user wants to restart.
        while True:
            if keyboard.read_key() == "r":
                restart = True
                break
            elif keyboard.read_key() == "enter":
                restart = False
                break


if __name__ == "__main__":
    # Importing the keyboard and colorama pip, which is used as battle input and sprite printing.
    try:
        import keyboard
        import term
    # Installing the pips if they aren't already.
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'keyboard'])
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'py-term'])
        import keyboard
        import term

    main()
