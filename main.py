import os
import sys
import subprocess
import time
import random

# Fix if the console doesn't print the color properly.
os.system("")


class Character:
    def __init__(self, name, health):
        self.name = name
        self.health = health
        self.health_max = health
        # Sets the default weapon
        self.weapon = fists

    def attack(self, target):
        target.health -= self.weapon.damage
        # Avoids going below 0 health
        target.health = max(target.health, 0)
        target.health_bar.update()

    def attack_print(self, target):
        print(f"{self.name} dealt {self.weapon.damage} damage to {target.name} with {self.weapon.name}!")


# P (short for Pixel) class creation which allows for the printing of 2 separate vertical colored blocks.
# ANSI escape code resource https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
class P:
    # t = top pixel, b = bottom pixel.
    def __init__(self, t, b):
        # \033[ is the ANSI escape code which allows color printing.
        # 38;5;{t}m sets the color of the upper/lower half if only one is needed.
        # 48;5;{b}m sets the color of the lower half if both are needed.
        # 0m sets the color back to default.
        if t == 0:
            self.c = f"\033[38;5;{b}m▄\033[0m"
        elif b == 0:
            self.c = f"\033[38;5;{t}m▀\033[0m"
        else:
            self.c = f"\033[38;5;{t};48;5;{b}m▀\033[0m"


class Hero(Character):
    def __init__(self, name, health):
        super().__init__(name, health)
        self.default_weapon = self.weapon
        self.health_bar = HealthBar(self, color="green")
        self.heal_amount = 0

    def equip(self, weapon):
        self.weapon = weapon
        return f"{self.name} equipped {self.weapon.name}!"

    def heal(self):
        if self.health >= self.health_max - 25:
            self.heal_amount = self.health_max - self.health
        else:
            self.heal_amount = 25
        self.health += self.heal_amount
        self.health_bar.update()

    def heal_amount_update(self):
        if self.health >= self.health_max - 25:
            self.heal_amount = self.health_max - self.health
        else:
            self.heal_amount = 25

    def heal_print(self):
        if self.heal_amount == 0:
            print(f"{self.name} healed {self.heal_amount} health!\nThat was a waste...")
        else:
            print(f"{self.name} healed {self.heal_amount} health!")

    def draw(self, weapon):
        self.weapon = weapon
        # Original pixel art from La3eb https://opengameart.org/forumtopic/how-to-get-better-at-P-art
        # Hex to ANSI color converter https://ajalt.github.io/colormath/converter/
        # Sets the cursor position.
        term.pos(1, 7)
        # Player sprite art.
        print(f"{P(251, 251).c} {P(0, 244).c}{P(244, 244).c}{P(244, 244).c}{P(0, 244).c}")
        term.pos(2, 7)
        print(f"{P(251, 180).c}{P(0, 31).c}{P(233, 180).c}{P(180, 180).c}{P(233, 180).c}{P(180, 94).c}"
              f"{P(0, 94).c}{P(0, 94).c}")
        term.pos(3, 7)
        print(f"{P(31, 0).c}{P(31, 0).c}{P(31, 31).c}{P(31, 31).c}{P(31, 31).c}{P(94, 94).c}{P(237, 94).c}"
              f"{P(94, 94).c}")
        term.pos(4, 7)
        print(f"  {P(244, 244).c}{P(244, 0).c}{P(244, 0).c}{P(244, 244).c}")


class Enemy(Character):
    def __init__(self, name, health, weapon, tier):
        super().__init__(name, health)
        self.weapon = weapon
        self.health_bar = HealthBar(self, color="red")
        self.tier = tier

    def draw(self):
        # Slime sprite art.
        if self.name == "Slime":
            term.pos(1, 37)
            print(f" {P(0, 83).c}{P(83, 34).c}{P(83, 34).c}{P(83, 34).c}{P(0, 22).c} ")
            term.pos(2, 37)
            print(f"{P(0, 83).c}{P(83, 34).c}{P(34, 34).c}{P(83, 34).c}{P(83, 83).c}{P(22, 34).c}{P(0, 22).c}")
            term.pos(3, 37)
            print(f"{P(83, 83).c}{P(34, 34).c}{P(34, 34).c}{P(34, 34).c}{P(34, 34).c}{P(34, 22).c}{P(22, 22).c}")
            term.pos(4, 37)
            print(f" {P(22, 0).c}{P(22, 0).c}{P(22, 0).c}{P(22, 0).c}{P(22, 0).c}")
        # Rat sprite art.
        elif self.name == "Rat":
            term.pos(2, 37)
            print(f" {P(251, 243).c}{P(251, 243).c}{P(0, 243).c}{P(251, 243).c}{P(251, 251).c}")
            term.pos(3, 37)
            print(f"{P(0, 243).c}{P(167, 243).c}{P(243, 243).c}{P(167, 243).c}{P(243, 243).c}{P(0, 243).c}"
                  f" {P(251, 251).c}")
            term.pos(4, 37)
            print(f" {P(251, 0).c} {P(243, 243).c}{P(243, 243).c}{P(243, 243).c}{P(243, 243).c}")
        # Goblin sprite art.
        elif self.name == "Goblin":
            term.pos(1, 37)
            print(f"  {P(0, 34).c}{P(34, 34).c}{P(34, 34).c}{P(0, 34).c}")
            term.pos(2, 37)
            print(f"{P(0, 34).c} {P(185, 34).c}{P(34, 34).c}{P(185, 34).c}{P(34, 22).c}")
            term.pos(3, 37)
            print(f"{P(34, 0).c}{P(22, 0).c}{P(22, 22).c}{P(22, 22).c}{P(22, 22).c}{P(22, 34).c}{P(22, 34).c}")
            term.pos(4, 37)
            print(f"  {P(22, 22).c}{P(22, 0).c}{P(22, 0).c}{P(22, 22).c}")
        # Goblin sprite art.
        elif self.name == "Skeleton":
            term.pos(1, 37)
            print(f" {P(0, 251).c}{P(251, 251).c}{P(251, 251).c}{P(0, 251).c}")
            term.pos(2, 37)
            print(f" {P(233, 251).c}{P(251, 251).c}{P(233, 251).c}{P(251, 240).c}{P(0, 240).c}{P(0, 251).c}")
            term.pos(3, 37)
            print(f"{P(251, 0).c} {P(240, 0).c}{P(240, 251).c}{P(240, 251).c}{P(240, 0).c} {P(251, 0).c}")
            term.pos(4, 37)
            print(f"  {P(240, 240).c}{P(240, 0).c}{P(240, 0).c}{P(240, 240).c}")
        # Goblin Thief sprite art.
        elif self.name == "Goblin Thief":
            term.pos(1, 37)
            print(f"{P(0, 185).c} {P(0, 244).c}{P(244, 244).c}{P(244, 244).c}{P(0, 244).c}")
            term.pos(2, 37)
            print(f"{P(185, 34).c}{P(0, 22).c}{P(185, 34).c}{P(34, 34).c}{P(185, 34).c}{P(34, 22).c}{P(0, 22).c}")
            term.pos(3, 37)
            print(f"{P(22, 0).c}{P(22, 0).c}{P(22, 22).c}{P(22, 22).c}{P(22, 22).c}{P(22, 34).c}{P(22, 22).c}")
            term.pos(4, 37)
            print(f"  {P(244, 244).c}{P(244, 0).c}{P(244, 0).c}{P(244, 244).c}")
        # Sword Warrior sprite art.
        elif self.name == "Sword Warrior":
            term.pos(1, 37)
            print(f"{P(251, 251).c} {P(0, 244).c}{P(244, 244).c}{P(244, 244).c}{P(0, 244).c}")
            term.pos(2, 37)
            print(f"{P(251, 180).c}{P(0, 31).c}{P(233, 180).c}{P(180, 180).c}{P(233, 180).c}{P(180, 94).c}"
                  f"{P(0, 94).c}{P(0, 94).c}")
            term.pos(3, 37)
            print(f"{P(31, 0).c}{P(31, 0).c}{P(31, 31).c}{P(31, 31).c}{P(31, 31).c}{P(94, 94).c}{P(237, 94).c}"
                  f"{P(94, 94).c}")
            term.pos(4, 37)
            print(f"  {P(244, 244).c}{P(244, 0).c}{P(244, 0).c}{P(244, 244).c}")
        # Axe Warrior sprite art.
        elif self.name == "Axe Warrior":
            term.pos(1, 37)
            print(f"{P(251, 251).c}{P(251, 251).c}{P(244, 244).c}{P(0, 251).c}{P(251, 251).c}{P(251, 251).c}"
                  f"{P(0, 251).c}")
            term.pos(2, 37)
            print(f"{P(251, 0).c} {P(244, 244).c}{P(233, 180).c}{P(180, 180).c}{P(233, 180).c}{P(180, 31).c}"
                  f"{P(0, 31).c}")
            term.pos(3, 37)
            print(f"  {P(180, 0).c}{P(31, 31).c}{P(31, 31).c}{P(31, 31).c}{P(31, 31).c}{P(31, 0).c}")
            term.pos(4, 37)
            print(f"   {P(251, 251).c}{P(251, 0).c}{P(251, 0).c}{P(251, 251).c}")
        # Goblin Mage sprite art.
        elif self.name == "Goblin Mage":
            term.pos(1, 37)
            print(f"{P(125, 251).c} {P(0, 22).c}{P(22, 22).c}{P(22, 22).c}{P(22, 22).c}{P(22, 0).c}")
            term.pos(2, 37)
            print(f"{P(251, 251).c} {P(185, 34).c}{P(34, 34).c}{P(185, 34).c}{P(22, 22).c} {P(0, 34).c}")
            term.pos(3, 37)
            print(f"{P(34, 251).c}{P(22, 0).c}{P(22, 22).c}{P(22, 22).c}{P(22, 22).c}{P(22, 22).c}{P(22, 0).c}")
            term.pos(4, 37)
            print(f"{P(251, 251).c} {P(22, 22).c}{P(22, 22).c}{P(22, 22).c}{P(22, 22).c}{P(22, 22).c}{P(0, 22).c}")
        # Undead Mage sprite art.
        elif self.name == "Undead Mage":
            term.pos(1, 37)
            print(f"{P(125, 251).c} {P(0, 251).c}{P(251, 251).c}{P(251, 251).c}{P(0, 251).c}")
            term.pos(2, 37)
            print(f"{P(251, 92).c}{P(0, 92).c}{P(233, 251).c}{P(251, 251).c}{P(233, 251).c}{P(251, 92).c}{P(0, 92).c}"
                  f"{P(251, 0).c}")
            term.pos(3, 37)
            print(f"{P(251, 251).c} {P(92, 92).c}{P(92, 92).c}{P(92, 92).c}{P(92, 92).c}")
            term.pos(4, 37)
            print(f"{P(251, 251).c} {P(92, 92).c}{P(92, 92).c}{P(92, 92).c}{P(92, 92).c}{P(92, 92).c}{P(0, 92).c}")
        # Sword Knight sprite art.
        elif self.name == "Sword Knight":
            term.pos(1, 37)
            print(f"{P(244, 244).c} {P(244, 251).c}{P(0, 251).c}{P(0, 251).c}{P(244, 251).c}")
            term.pos(2, 37)
            print(f"{P(244, 244).c} {P(233, 251).c}{P(233, 233).c}{P(233, 251).c}{P(251, 251).c}")
            term.pos(3, 37)
            print(f"{P(251, 0).c}{P(251, 0).c}{P(251, 251).c}{P(251, 251).c}{P(244, 244).c}{P(244, 246).c}"
                  f"{P(244, 244).c}")
            term.pos(4, 37)
            print(f"  {P(251, 251).c}{P(251, 0).c}{P(244, 0).c}{P(244, 251).c}{P(244, 0).c}")
        # Axe Knight sprite art.
        elif self.name == "Axe Knight":
            term.pos(1, 37)
            print(f"{P(251, 251).c}{P(251, 251).c}{P(244, 244).c}{P(0, 251).c}{P(0, 251).c}{P(0, 251).c}{P(0, 251).c}")
            term.pos(2, 37)
            print(f"{P(251, 0).c} {P(244, 244).c}{P(233, 251).c}{P(233, 233).c}{P(233, 251).c}{P(251, 251).c}")
            term.pos(3, 37)
            print(f"  {P(244, 251).c}{P(251, 251).c}{P(251, 251).c}{P(251, 251).c}{P(251, 251).c}{P(251, 251).c}")
            term.pos(4, 37)
            print(f"  {P(244, 244).c}{P(251, 251).c}{P(251, 0).c}{P(251, 0).c}{P(251, 251).c}")


class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage


class HealthBar:
    symbol_remaining = "█"
    symbol_lost = "_"
    barrier = "|"
    colors = {"default": "\033[0m",
              "green": "\033[92m",
              "red": "\033[91m",
              }

    def __init__(self, entity, length=20, is_colored=True, color=""):
        self.entity = entity
        self.length = length
        self.max_value = entity.health_max
        self.current_value = entity.health
        self.is_colored = is_colored
        self.color = self.colors.get(color) or self.colors["default"]

    def update(self):
        self.current_value = self.entity.health

    def draw(self):
        remaining_bars = round(self.current_value / self.max_value * self.length)
        lost_bars = self.length - remaining_bars
        if self.entity.name == "You":
            print(f"\n{self.entity.name}r health: {self.entity.health}/{self.entity.health_max}")
            print(f"{self.barrier}"
                  f"{self.color if self.is_colored else ""}"
                  f"{remaining_bars * self.symbol_remaining}"
                  f"{lost_bars * self.symbol_lost}"
                  f"{self.colors["default"] if self.is_colored else ""}"
                  f"{self.barrier}")
        else:
            term.pos(6, 30)
            print(f"{self.entity.name}'s health: {self.entity.health}/{self.entity.health_max}")
            term.pos(7, 30)
            print(f"{self.barrier}"
                  f"{self.color if self.is_colored else ""}"
                  f"{remaining_bars * self.symbol_remaining}"
                  f"{lost_bars * self.symbol_lost}"
                  f"{self.colors["default"] if self.is_colored else ""}"
                  f"{self.barrier}")


# Weapons
fists = Weapon("Fists", 3)
claws = Weapon("Claws", 4)
dagger = Weapon("Dagger", 5)
iron_sword = Weapon("Iron Sword", 6)
iron_axe = Weapon("Iron Axe", 8)
staff = Weapon("Staff", 10)
iron_greatsword = Weapon("Iron Greatsword", 12)
iron_battleaxe = Weapon("Iron Battleaxe", 14)

# Enemies
slime = Enemy("Slime", 30, fists, 1)
rat = Enemy("Rat", 20, claws, 1)
goblin = Enemy("Goblin", 50, fists, 1)
skeleton = Enemy("Skeleton", 60, fists, 1)
goblin_thief = Enemy("Goblin Thief", 110, dagger, 2)
sword_warrior = Enemy("Sword Warrior", 130, iron_sword, 2)
axe_warrior = Enemy("Axe Warrior", 120, iron_axe, 2)
goblin_mage = Enemy("Goblin Mage", 70, staff, 3)
undead_mage = Enemy("Undead Mage", 80, staff, 3)
sword_knight = Enemy("Sword Knight", 180, iron_greatsword, 4)
axe_knight = Enemy("Axe Knight", 170, iron_battleaxe, 4)

enemy_list = [slime, rat, goblin, skeleton, goblin_thief, sword_warrior, axe_warrior, goblin_mage, undead_mage,
              sword_knight, axe_knight]


def main():
    hero = Hero("You", 150)

    # Clears the screen if ran in terminal.
    os.system("cls")

    hero.equip(iron_sword)

    while True:
        enemy = random.choice(enemy_list)
        Hero.draw(hero, iron_sword)
        Enemy.draw(enemy)
        hero.health_bar.draw()
        enemy.health_bar.draw()
        print("\n+-------------------------------------------------+")
        print(f"{hero.name} encountered a(n) {enemy.name}!")
        print(f"\nPress A to attack.\nPress H to heal {hero.heal_amount} health.")

        while hero.health > 0 and enemy.health > 0:
            if keyboard.is_pressed("a"):
                os.system("cls")
                hero.attack(enemy)
                enemy.attack(hero)

                Hero.draw(hero, iron_sword)
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

                Hero.draw(hero, iron_sword)
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
