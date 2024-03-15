class Weapon:
    def __init__(self, name, weapon_type, damage):
        self.name = name
        self.weapon_type = weapon_type
        self.damage = damage


iron_sword = Weapon("Iron Sword", "melee", 5)
short_bow = Weapon("Short Bow", "ranged", 4)
fists = Weapon("Fists", "melee", 2)

weapon_choices = [iron_sword, short_bow, fists]
