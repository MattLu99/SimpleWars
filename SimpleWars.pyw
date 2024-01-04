import menu

def main() -> None:
    """Loads the program by calling the menu and starting its setup."""
    simplewars = menu.Window()
    simplewars.game_start()

main()