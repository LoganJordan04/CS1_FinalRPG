import os
import sys
import subprocess
import time
import random

from characters import *

# Fix if the console doesn't print the color properly.
os.system("")


def main():
    hero = Hero("You", 150)

    # Clears the screen if ran in terminal.
    os.system("cls")

    while True:
        enemy = random.choice(enemy_list)
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
        print(f"\nPress A to attack.\nPress H to heal {hero.heal_amount} health.")

        while hero.health > 0 and enemy.health > 0:
            if keyboard.is_pressed("a"):
                os.system("cls")
                hero.attack(enemy)
                enemy.attack(hero)

                Hero.draw(hero)
                Enemy.draw(enemy)
                hero.health_bar.draw()
                enemy.health_bar.draw()
                print("\n+-------------------------------------------------+")
                hero.attack_print(enemy)
                enemy.attack_print(hero)
                hero.heal_amount_update()
                print(f"\nPress A to attack.\nPress H to heal {hero.heal_amount} health.")
                # Delay to fix problems with rapid inputs.
                time.sleep(0.25)
            elif keyboard.is_pressed("h"):
                os.system("cls")
                hero.heal()

                Hero.draw(hero)
                Enemy.draw(enemy)
                hero.health_bar.draw()
                enemy.health_bar.draw()
                print("\n+-------------------------------------------------+")
                hero.heal_print()
                hero.heal_amount_update()
                print(f"\nPress A to attack.\nPress H to heal {hero.heal_amount} health.")
                time.sleep(0.25)

        if hero.health == 0:
            os.system("cls")
            return False

        os.system("cls")


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
