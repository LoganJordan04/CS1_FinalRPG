# Fix if the console doesn't print the color properly.
import os
os.system("")


class HealthBar:
    symbol_remaining = "█"
    symbol_lost = "_"
    barrier = "|"
    # ANSI color codes. https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
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
        print(f"{self.entity.name}'s health: {self.entity.health}/{self.entity.health_max}")
        print(f"{self.barrier}"
              f"{self.color if self.is_colored else ""}"
              f"{remaining_bars * self.symbol_remaining}"
              f"{lost_bars * self.symbol_lost}"
              f"{self.colors["default"] if self.is_colored else ""}"
              f"{self.barrier}")
