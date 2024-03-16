import os
import random
from characters import Hero, Enemy
from weapons import iron_sword, weapon_choices
from art import enemy_sword1


def main():
    enemy_sword1()

    name = input("Enter the hero's name: ")
    hero = Hero(name, 100)
    hero.equip(iron_sword)

    random_weapon = random.choice(weapon_choices)
    enemy = Enemy("Enemy", 100, random_weapon)

    while hero.health > 0 and enemy.health > 0:
        # Clears the screen if ran in terminal.
        os.system("cls")

        hero.attack(enemy)
        enemy.attack(hero)
        hero.health_bar.draw()
        enemy.health_bar.draw()

        if hero.health <= 50:
            hero.heal()
            hero.health_bar.draw()
            enemy.health_bar.draw()

        input()


if __name__ == "__main__":
    main()
