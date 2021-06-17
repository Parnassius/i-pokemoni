from os.path import dirname, join

VEEKUN_PATH = join(
    dirname(__file__), "..", "veekun", "pokedex", "pokedex", "data", "csv"
)

BASE_PATH = join(dirname(__file__), "..", "pokemon_data")

PATHS = {
    # fmt: off
    "omegaruby": join(BASE_PATH, "oras14", "lower", "Pokémon Omega Ruby [v1.4]", "romfs"),
    "alphasapphire": join(BASE_PATH, "oras14", "lower", "Pokémon Alpha Sapphire [v1.4]", "romfs"),
    "sun": join(BASE_PATH, "sm12", "lower", "Pokémon Sun [v1.2]", "romfs"),
    "moon": join(BASE_PATH, "sm12", "lower", "Pokémon Moon [v1.2]", "romfs"),
    "ultrasun": join(BASE_PATH, "usum12", "lower", "Pokémon Ultra Sun [v1.2]", "romfs"),
    "ultramoon": join(BASE_PATH, "usum12", "lower", "Pokémon Ultra Moon [v1.2]", "romfs"),
    "pikachu": join(BASE_PATH, "lgpe131072", "lower", "Pokémon: Let’s Go, Pikachu! [v131072]", "RomFS"),
    "eevee": join(BASE_PATH, "lgpe131072", "lower", "Pokémon: Let’s Go, Eevee! [v131072]", "RomFS"),
    "sword": join(BASE_PATH, "swsh458752", "lower", "Pokémon Shield [v458752]", "RomFS"),
    "shield": join(BASE_PATH, "swsh458752", "lower", "Pokémon Sword [v458752]", "RomFS"),

    "home": join(BASE_PATH, "home327680", "lower", "RomFS"),
}
