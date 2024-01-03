import menu

def main() -> None:
    """Starts the program by calling the menu and finishing its setup."""
    simplewars = menu.Window()
    simplewars.game_start()

main()