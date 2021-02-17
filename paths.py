from os.path import dirname, join

BASE_PATH = join(dirname(__file__), "..", "pokemon_data")

PATHS = {
    "pikachu": join(
        BASE_PATH,
        "lgpe131072",
        "Pokémon: Let’s Go, Pikachu! [v131072]",
        "RomFS",
    ),
    "eevee": join(
        BASE_PATH,
        "lgpe131072",
        "Pokémon: Let’s Go, Eevee! [v131072]",
        "RomFS",
    ),
    "sword": join(
        BASE_PATH,
        "swsh393216",
        "Pokémon Shield [v393216]",
        "RomFS",
    ),
    "shield": join(
        BASE_PATH,
        "swsh393216",
        "Pokémon Sword [v393216]",
        "RomFS",
    ),
}
