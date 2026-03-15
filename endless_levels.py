

from Dungeon_Generator import DungeonGenerator

# default dimensions match those used elsewhere in the project
DUNGEON_W = 61
DUNGEON_H = 35


def print_map(dungeon: Dungeon) -> None:
    for row in dungeon.grid:
        print("".join(row))
    print()


def main():
    print("Endless random map generator (Ctrl-C to quit)")
    try:
        while True:
            gen = DungeonGenerator(DUNGEON_W, DUNGEON_H)
            grid = gen.generate()
            # wrap structure for compatibility with earlier print_map
            class D:
                def __init__(self, g):
                    self.grid = g
            print_map(D(grid))
            input("-- press Enter for next map --")
    except KeyboardInterrupt:
        print("\nGenerator stopped.")


if __name__ == "__main__":
    main()
