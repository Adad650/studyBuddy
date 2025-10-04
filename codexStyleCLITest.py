import curses

def curses_menu(stdscr):
    curses.curs_set(0)
    options = ["Add study session", "View stats", "Quit"]
    index = 0

    while True:
        stdscr.erase()
        stdscr.addstr(0, 0, "Study Buddy")
        for i, label in enumerate(options):
            style = curses.A_REVERSE if i == index else curses.A_NORMAL
            stdscr.addstr(2 + i, 2, label, style)
        key = stdscr.getch()

        if key in (curses.KEY_UP, ord('k')):
            index = (index - 1) % len(options)
        elif key in (curses.KEY_DOWN, ord('j')):
            index = (index + 1) % len(options)
        elif key in (curses.KEY_ENTER, 10, 13):
            if index == 0:
                add_session()
            elif index == 1:
                show_stats()
            else:
                break

def add_session():
    print(" Adding a session...")

def show_stats():
    print(" Showing stats...")

if __name__ == "__main__":
    curses.wrapper(curses_menu)