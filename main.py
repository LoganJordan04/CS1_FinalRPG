import os
from characters import Hero, Enemy
from weapons import short_bow, iron_sword


def main():
    name = input("Enter the hero's name: ")
    hero = Hero(name, 100)
    hero.equip(iron_sword)
    enemy = Enemy("Enemy", 100, short_bow)

    while True:
        # Clears the screen if ran in terminal.
        os.system("cls")

        hero.attack(enemy)
        enemy.attack(hero)

        hero.health_bar.draw()
        enemy.health_bar.draw()

        if not input("Press Enter to quit: "):
            break


if __name__ == "__main__":
    main()
