# Defines the ANSI escape code for ease of use.
esc = "\033[38;5;"


# Original pixel art from La3eb https://opengameart.org/forumtopic/how-to-get-better-at-pixel-art
# Hex to ANSI color converter https://ajalt.github.io/colormath/converter/
# Trust the process...
def enemy_sword1():
    print(f"{esc}251m█  {esc}244m█{esc}244m█")
    print(f"{esc}251m█ {esc}244m█{esc}244m█{esc}244m█{esc}244m█")
    print(f"{esc}251m█ {esc}22m█{esc}34m█{esc}22m█{esc}34m█")
    print(f"{esc}34m█{esc}22m█{esc}34m█{esc}34m█{esc}34m█{esc}22m█{esc}22m█")
    print(f"{esc}22m█{esc}22m█{esc}22m█{esc}22m█{esc}22m█{esc}22m█{esc}22m█")
    print(f"  {esc}22m█{esc}22m█{esc}22m█{esc}34m█{esc}22m█")
    print(f"  {esc}244m█{esc}244m█{esc}244m█{esc}244m█")
    print(f"  {esc}244m█  {esc}244m█")
    # Resets the text color back to normal
    print("\033[0m")
