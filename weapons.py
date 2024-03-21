"""
This script determines the class and instances of weapons.
"""


class Weapon:
    """A class the defines weapons."""
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage


# Weapon instances
fists = Weapon("Fists", 5)
teeth = Weapon("Teeth", 6)
dagger = Weapon("Dagger", 7)
iron_sword = Weapon("Iron Sword", 8)
iron_axe = Weapon("Iron Axe", 10)
staff = Weapon("Staff", 12)
iron_greatsword = Weapon("Iron Greatsword", 14)
iron_battleaxe = Weapon("Iron Battleaxe", 16)
