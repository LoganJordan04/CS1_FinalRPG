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

    hero.equip(iron_greatsword)

    # Clears the screen.
    os.system("cls")

    enemy_num = 1

    while True:
        print(enemy_num)
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
        # Enemy fallback and error print if enemy_num is outside of range.
        else:
            enemy = slime
            print("\033[91mThe enemy num is outside range!")

        # Sets the enemies health to max so an instance can occur more than once.
        enemy.reset_health()
        enemy.health_bar.update()

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

        enemy_num += 1

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
