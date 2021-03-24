from os.path import dirname, join

BASE_PATH = join(dirname(__file__), "..", "pokemon_data")

PATHS = {
    # fmt: off
    "sun": join(BASE_PATH, "sm12", "lower", "Pokémon Sun [v1.2]", "romfs"),
    "moon": join(BASE_PATH, "sm12", "lower", "Pokémon Moon [v1.2]", "romfs"),
    "ultrasun": join(BASE_PATH, "usum12", "lower", "Pokémon Ultra Sun [v1.2]", "romfs"),
    "ultramoon": join(BASE_PATH, "usum12", "lower", "Pokémon Ultra Moon [v1.2]", "romfs"),
    "pikachu": join(BASE_PATH, "lgpe131072", "lower", "Pokémon: Let’s Go, Pikachu! [v131072]", "RomFS"),
    "eevee": join(BASE_PATH, "lgpe131072", "lower", "Pokémon: Let’s Go, Eevee! [v131072]", "RomFS"),
    "sword": join(BASE_PATH, "swsh393216", "lower", "Pokémon Shield [v393216]", "RomFS"),
    "shield": join(BASE_PATH, "swsh393216", "lower", "Pokémon Sword [v393216]", "RomFS"),
}
