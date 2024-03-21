"""
This script determines the classes, methods, and instances of the hero and enemies.
"""

from weapons import *
from healthbar import *


class Character:
    """A class that defines the attributes of the characters."""
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


class P:
    """A class which allows for the printing of 2 separate vertical colored unicode blocks."""
    # ANSI escape code resource https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
    # Hex to ANSI color converter https://ajalt.github.io/colormath/converter/

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
    """A Character subclass that defines the attributes of the hero or player."""
    def __init__(self, name, health, potions, coins):
        super().__init__(name, health)
        self.potions = potions
        self.coins = coins
        self.default_weapon = self.weapon
        self.health_bar = HealthBar(self, color="green")
        self.heal_amount = 0

    def equip(self, weapon):
        self.weapon = weapon
        return f"{self.name} equipped {self.weapon.name}!"

    def heal(self):
        """Heals the player but doesn't go over max health."""
        if self.potions <= 0:
            pass
        else:
            if self.health >= self.health_max - 125:
                self.heal_amount = self.health_max - self.health
            else:
                self.heal_amount = 125
            self.health += self.heal_amount
            self.health_bar.update()
            self.potions -= 1

    def heal_update(self):
        """Updates the heal amount text."""
        if self.health >= self.health_max - 125:
            self.heal_amount = self.health_max - self.health
        else:
            self.heal_amount = 125

    def heal_print(self):
        if self.potions <= 0:
            print(f"You are all out of potions!")
        else:
            if self.heal_amount == 0:
                print(f"{self.name} healed {self.heal_amount} health!\nThat was a waste...")
            else:
                print(f"{self.name} healed {self.heal_amount} health!")

    def draw(self):
        """Prints the pixel art for the player for each equipped weapon."""
        # Original chicken player pixel art by handsofhope
        # https://www.reddit.com/r/PixelArt/comments/fqu1ri/wanted_to_take_a_stab_at_restricting_size_8x8_and/

        # Player sprite art when no weapon is equipped.
        if self.weapon == fists:
            term.pos(2, 7)
            print(f"    {P(0, 231).c}{P(0, 231).c}")
            term.pos(3, 7)
            print(f" {P(0, 231).c}{P(231, 231).c}{P(231, 233).c}{P(231, 231).c}{P(231, 233).c}")
            term.pos(4, 7)
            print(f"{P(0, 231).c}{P(231, 231).c}{P(231, 231).c}{P(231, 231).c}{P(215, 231).c}{P(215, 203).c}"
                  f"{P(0, 231).c}")
            term.pos(5, 7)
            print(f" {P(231, 215).c}{P(231, 0).c}{P(231, 0).c}{P(231, 0).c}{P(231, 215).c}")
        # Player sprite art when dagger is equipped.
        elif self.weapon == dagger:
            # Sets the cursor position for correct sprite positioning.
            term.pos(2, 7)
            print(f"    {P(0, 231).c}{P(0, 231).c}")
            term.pos(3, 7)
            print(f" {P(0, 231).c}{P(231, 231).c}{P(231, 233).c}{P(231, 231).c}{P(231, 233).c} {P(0, 185).c}")
            term.pos(4, 7)
            print(f"{P(0, 231).c}{P(231, 231).c}{P(231, 231).c}{P(231, 231).c}{P(215, 231).c}{P(215, 203).c}"
                  f"{P(0, 231).c}{P(185, 231).c}")
            term.pos(5, 7)
            print(f" {P(231, 215).c}{P(231, 0).c}{P(231, 0).c}{P(231, 0).c}{P(231, 215).c}")
        # Player sprite art when iron sword is equipped.
        elif self.weapon == iron_sword:
            term.pos(2, 7)
            print(f"    {P(0, 231).c}{P(0, 231).c}")
            term.pos(3, 7)
            print(f" {P(0, 231).c}{P(231, 231).c}{P(231, 233).c}{P(231, 231).c}{P(231, 233).c} {P(251, 251).c}")
            term.pos(4, 7)
            print(f"{P(0, 231).c}{P(231, 231).c}{P(231, 231).c}{P(231, 231).c}{P(215, 231).c}{P(215, 203).c}"
                  f"{P(0, 231).c}{P(251, 231).c}")
            term.pos(5, 7)
            print(f" {P(231, 215).c}{P(231, 0).c}{P(231, 0).c}{P(231, 0).c}{P(231, 215).c} {P(238, 0).c}")
        # Player sprite art when iron axe is equipped.
        elif self.weapon == iron_axe:
            term.pos(2, 7)
            print(f"    {P(0, 231).c}{P(0, 231).c}{P(0, 244).c}{P(0, 251).c}{P(0, 251).c}")
            term.pos(3, 7)
            print(f" {P(0, 231).c}{P(231, 231).c}{P(231, 233).c}{P(231, 231).c}{P(231, 233).c}{P(244, 244).c}"
                  f"{P(251, 0).c}{P(251, 251).c}")
            term.pos(4, 7)
            print(f"{P(0, 231).c}{P(231, 231).c}{P(231, 231).c}{P(231, 231).c}{P(215, 231).c}{P(215, 203).c}"
                  f"{P(244, 231).c}")
            term.pos(5, 7)
            print(f" {P(231, 215).c}{P(231, 0).c}{P(231, 0).c}{P(231, 0).c}{P(231, 215).c}{P(238, 0).c}")
        # Player sprite art when staff is equipped.
        elif self.weapon == staff:
            term.pos(2, 7)
            print(f"    {P(0, 231).c}{P(0, 231).c} {P(125, 251).c}")
            term.pos(3, 7)
            print(f" {P(0, 231).c}{P(231, 231).c}{P(231, 233).c}{P(231, 231).c}{P(231, 233).c} {P(251, 251).c}")
            term.pos(4, 7)
            print(f"{P(0, 231).c}{P(231, 231).c}{P(231, 231).c}{P(231, 231).c}{P(215, 231).c}{P(215, 203).c}"
                  f"{P(0, 231).c}{P(251, 231).c}")
            term.pos(5, 7)
            print(f" {P(231, 215).c}{P(231, 0).c}{P(231, 0).c}{P(231, 0).c}{P(231, 215).c} {P(251, 251).c}")
        # Player sprite art when iron greatsword is equipped.
        elif self.weapon == iron_greatsword:
            term.pos(2, 7)
            print(f"    {P(0, 231).c}{P(0, 231).c} {P(231, 231).c}")
            term.pos(3, 7)
            print(f" {P(0, 231).c}{P(231, 231).c}{P(231, 233).c}{P(231, 231).c}{P(231, 233).c} {P(231, 231).c}")
            term.pos(4, 7)
            print(f"{P(0, 231).c}{P(231, 231).c}{P(231, 231).c}{P(231, 231).c}{P(215, 231).c}{P(215, 203).c}"
                  f"{P(0, 231).c}{P(251, 231).c}")
            term.pos(5, 7)
            print(f" {P(231, 215).c}{P(231, 0).c}{P(231, 0).c}{P(231, 0).c}{P(231, 215).c} {P(238, 0).c}")
        # Player sprite art when iron battleaxe is equipped.
        elif self.weapon == iron_battleaxe:
            term.pos(2, 7)
            print(f"    {P(0, 231).c}{P(0, 231).c}{P(244, 244).c}{P(231, 231).c}{P(231, 231).c}")
            term.pos(3, 7)
            print(f" {P(0, 231).c}{P(231, 231).c}{P(231, 233).c}{P(231, 231).c}{P(231, 233).c}{P(244, 244).c}"
                  f" {P(231, 0).c}")
            term.pos(4, 7)
            print(f"{P(0, 231).c}{P(231, 231).c}{P(231, 231).c}{P(231, 231).c}{P(215, 231).c}{P(215, 203).c}"
                  f"{P(244, 231).c}")
            term.pos(5, 7)
            print(f" {P(231, 215).c}{P(231, 0).c}{P(231, 0).c}{P(231, 0).c}{P(231, 215).c}{P(244, 244).c}")
        # Player sprite error.
        else:
            term.pos(1, 7)
            print("\033[91mAn error with the player sprite occurred!")


class Enemy(Character):
    """A Character subclass that defines the attributes of enemies."""
    def __init__(self, name, health, weapon, coins):
        super().__init__(name, health)
        self.weapon = weapon
        self.coins = coins
        self.health_bar = HealthBar(self, color="red")

    def reset_health(self):
        self.health = self.health_max

    def draw(self):
        """Prints the pixel art for the player for each equipped weapon."""
        # Original enemy pixel art by La3eb https://opengameart.org/forumtopic/how-to-get-better-at-P-art

        # Slime sprite art.
        if self.name == "Slime":
            term.pos(2, 37)
            print(f" {P(0, 83).c}{P(83, 34).c}{P(83, 34).c}{P(83, 34).c}{P(0, 22).c} ")
            term.pos(3, 37)
            print(f"{P(0, 83).c}{P(83, 34).c}{P(34, 34).c}{P(83, 34).c}{P(83, 83).c}{P(22, 34).c}{P(0, 22).c}")
            term.pos(4, 37)
            print(f"{P(83, 83).c}{P(34, 34).c}{P(34, 34).c}{P(34, 34).c}{P(34, 34).c}{P(34, 22).c}{P(22, 22).c}")
            term.pos(5, 37)
            print(f" {P(22, 0).c}{P(22, 0).c}{P(22, 0).c}{P(22, 0).c}{P(22, 0).c}")
        # Rat sprite art.
        elif self.name == "Rat":
            term.pos(3, 37)
            print(f" {P(251, 243).c}{P(251, 243).c}{P(0, 243).c}{P(251, 243).c}{P(251, 251).c}")
            term.pos(4, 37)
            print(f"{P(0, 243).c}{P(167, 243).c}{P(243, 243).c}{P(167, 243).c}{P(243, 243).c}{P(0, 243).c}"
                  f" {P(251, 251).c}")
            term.pos(5, 37)
            print(f" {P(251, 0).c} {P(243, 243).c}{P(243, 243).c}{P(243, 243).c}{P(243, 243).c}")
        # Goblin sprite art.
        elif self.name == "Goblin":
            term.pos(2, 37)
            print(f"  {P(0, 34).c}{P(34, 34).c}{P(34, 34).c}{P(0, 34).c}")
            term.pos(3, 37)
            print(f"{P(0, 34).c} {P(185, 34).c}{P(34, 34).c}{P(185, 34).c}{P(34, 22).c}")
            term.pos(4, 37)
            print(f"{P(34, 0).c}{P(22, 0).c}{P(22, 22).c}{P(22, 22).c}{P(22, 22).c}{P(22, 34).c}{P(22, 34).c}")
            term.pos(5, 37)
            print(f"  {P(22, 22).c}{P(22, 0).c}{P(22, 0).c}{P(22, 22).c}")
        # Goblin sprite art.
        elif self.name == "Skeleton":
            term.pos(2, 37)
            print(f" {P(0, 251).c}{P(251, 251).c}{P(251, 251).c}{P(0, 251).c}")
            term.pos(3, 37)
            print(f" {P(233, 251).c}{P(251, 251).c}{P(233, 251).c}{P(251, 240).c}{P(0, 240).c}{P(0, 251).c}")
            term.pos(4, 37)
            print(f"{P(251, 0).c} {P(240, 0).c}{P(240, 251).c}{P(240, 251).c}{P(240, 0).c} {P(251, 0).c}")
            term.pos(5, 37)
            print(f"  {P(240, 240).c}{P(240, 0).c}{P(240, 0).c}{P(240, 240).c}")
        # Goblin Thief sprite art.
        elif self.name == "Goblin Thief":
            term.pos(2, 37)
            print(f"{P(0, 185).c} {P(0, 244).c}{P(244, 244).c}{P(244, 244).c}{P(0, 244).c}")
            term.pos(3, 37)
            print(f"{P(185, 34).c}{P(0, 22).c}{P(185, 34).c}{P(34, 34).c}{P(185, 34).c}{P(34, 22).c}{P(0, 22).c}")
            term.pos(4, 37)
            print(f"{P(22, 0).c}{P(22, 0).c}{P(22, 22).c}{P(22, 22).c}{P(22, 22).c}{P(22, 34).c}{P(22, 22).c}")
            term.pos(5, 37)
            print(f"  {P(244, 244).c}{P(244, 0).c}{P(244, 0).c}{P(244, 244).c}")
        # Sword Warrior sprite art.
        elif self.name == "Sword Warrior":
            term.pos(2, 37)
            print(f"{P(251, 251).c} {P(0, 244).c}{P(244, 244).c}{P(244, 244).c}{P(0, 244).c}")
            term.pos(3, 37)
            print(f"{P(251, 180).c}{P(0, 31).c}{P(233, 180).c}{P(180, 180).c}{P(233, 180).c}{P(180, 94).c}"
                  f"{P(0, 94).c}{P(0, 94).c}")
            term.pos(4, 37)
            print(f"{P(31, 0).c}{P(31, 0).c}{P(31, 31).c}{P(31, 31).c}{P(31, 31).c}{P(94, 94).c}{P(237, 94).c}"
                  f"{P(94, 94).c}")
            term.pos(5, 37)
            print(f"  {P(244, 244).c}{P(244, 0).c}{P(244, 0).c}{P(244, 244).c}")
        # Axe Warrior sprite art.
        elif self.name == "Axe Warrior":
            term.pos(2, 37)
            print(f"{P(251, 251).c}{P(251, 251).c}{P(244, 244).c}{P(0, 251).c}{P(251, 251).c}{P(251, 251).c}"
                  f"{P(0, 251).c}")
            term.pos(3, 37)
            print(f"{P(251, 0).c} {P(244, 244).c}{P(233, 180).c}{P(180, 180).c}{P(233, 180).c}{P(180, 31).c}"
                  f"{P(0, 31).c}")
            term.pos(4, 37)
            print(f"  {P(180, 0).c}{P(31, 31).c}{P(31, 31).c}{P(31, 31).c}{P(31, 31).c}{P(31, 0).c}")
            term.pos(5, 37)
            print(f"   {P(251, 251).c}{P(251, 0).c}{P(251, 0).c}{P(251, 251).c}")
        # Goblin Mage sprite art.
        elif self.name == "Goblin Mage":
            term.pos(2, 37)
            print(f"{P(125, 251).c} {P(0, 22).c}{P(22, 22).c}{P(22, 22).c}{P(22, 22).c}{P(22, 0).c}")
            term.pos(3, 37)
            print(f"{P(251, 251).c} {P(185, 34).c}{P(34, 34).c}{P(185, 34).c}{P(22, 22).c} {P(0, 34).c}")
            term.pos(4, 37)
            print(f"{P(34, 251).c}{P(22, 0).c}{P(22, 22).c}{P(22, 22).c}{P(22, 22).c}{P(22, 22).c}{P(22, 0).c}")
            term.pos(5, 37)
            print(f"{P(251, 251).c} {P(22, 22).c}{P(22, 22).c}{P(22, 22).c}{P(22, 22).c}{P(22, 22).c}{P(0, 22).c}")
        # Undead Mage sprite art.
        elif self.name == "Undead Mage":
            term.pos(2, 37)
            print(f"{P(125, 251).c} {P(0, 251).c}{P(251, 251).c}{P(251, 251).c}{P(0, 251).c}")
            term.pos(3, 37)
            print(f"{P(251, 92).c}{P(0, 92).c}{P(233, 251).c}{P(251, 251).c}{P(233, 251).c}{P(251, 92).c}{P(0, 92).c}"
                  f"{P(251, 0).c}")
            term.pos(4, 37)
            print(f"{P(251, 251).c} {P(92, 92).c}{P(92, 92).c}{P(92, 92).c}{P(92, 92).c}")
            term.pos(5, 37)
            print(f"{P(251, 251).c} {P(92, 92).c}{P(92, 92).c}{P(92, 92).c}{P(92, 92).c}{P(92, 92).c}{P(0, 92).c}")
        # Sword Knight sprite art.
        elif self.name == "Sword Knight":
            term.pos(2, 37)
            print(f"{P(231, 231).c} {P(244, 251).c}{P(0, 251).c}{P(0, 251).c}{P(244, 251).c}")
            term.pos(3, 37)
            print(f"{P(231, 231).c} {P(233, 251).c}{P(233, 233).c}{P(233, 251).c}{P(251, 251).c}")
            term.pos(4, 37)
            print(f"{P(251, 238).c}{P(251, 0).c}{P(251, 251).c}{P(251, 251).c}{P(244, 244).c}{P(244, 246).c}"
                  f"{P(244, 244).c}")
            term.pos(5, 37)
            print(f"  {P(251, 251).c}{P(251, 0).c}{P(244, 0).c}{P(244, 251).c}{P(244, 0).c}")
        # Axe Knight sprite art.
        elif self.name == "Axe Knight":
            term.pos(2, 37)
            print(f"{P(231, 231).c}{P(231, 231).c}{P(244, 244).c}{P(0, 251).c}{P(0, 251).c}{P(0, 251).c}{P(0, 251).c}")
            term.pos(3, 37)
            print(f"{P(231, 0).c} {P(244, 244).c}{P(233, 251).c}{P(233, 233).c}{P(233, 251).c}{P(251, 251).c}")
            term.pos(4, 37)
            print(f"  {P(244, 251).c}{P(251, 251).c}{P(251, 251).c}{P(251, 251).c}{P(251, 251).c}{P(251, 251).c}")
            term.pos(5, 37)
            print(f"  {P(244, 244).c}{P(251, 251).c}{P(251, 0).c}{P(251, 0).c}{P(251, 251).c}")
        # Enemy sprite error.
        else:
            term.pos(1, 37)
            print("\033[91mAn error with the enemy sprite occurred!")


# Enemy instances
slime = Enemy("Slime", 40, fists, 6)
rat = Enemy("Rat", 30, teeth, 4)
goblin = Enemy("Goblin", 60, fists, 10)
skeleton = Enemy("Skeleton", 50, fists, 8)
goblin_thief = Enemy("Goblin Thief", 100, dagger, 16)
sword_warrior = Enemy("Sword Warrior", 120, iron_sword, 12)
axe_warrior = Enemy("Axe Warrior", 110, iron_axe, 13)
goblin_mage = Enemy("Goblin Mage", 100, staff, 20)
undead_mage = Enemy("Undead Mage", 90, staff, 17)
sword_knight = Enemy("Sword Knight", 160, iron_greatsword, 32)
axe_knight = Enemy("Axe Knight", 150, iron_battleaxe, 31)

# Lists for each tier of enemies.
tier1_enemies = [slime, rat, goblin, skeleton]
tier2_enemies = [slime, rat, goblin, skeleton, goblin_thief, sword_warrior, axe_warrior]
tier3_enemies = [goblin_thief, sword_warrior, axe_warrior, goblin_mage, undead_mage]
tier4_enemies = [goblin_mage, undead_mage, sword_knight, axe_knight]
