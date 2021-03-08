from __future__ import annotations

from os.path import join
from typing import TYPE_CHECKING

from utils import read_as_int

from .personal_info_sm import PersonalInfoSM

if TYPE_CHECKING:
    from .personal_table import PersonalTable


class PersonalInfoLetsGo(PersonalInfoSM):
    _PATH = join("bin", "pokelib", "personal", "personal_total.bin")
    _MAX_ID = 809

    def __init__(self, table: PersonalTable, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self.go_species = read_as_int(2, self._data, 0x48)

        self.special_tutors = [
            [self._id == 966] * 3  # pikachu-starter
            + [self._id == 979] * 8  # eevee-starter
        ]

        self.pokedex_numbers = {}
        if self._id <= 151:
            self.pokedex_numbers["letsgo-kanto"] = self._id
        elif self._id == 808:  # meltan
            self.pokedex_numbers["letsgo-kanto"] = 152
        elif self._id == 809:  # melmetal
            self.pokedex_numbers["letsgo-kanto"] = 153

        self.is_present_in_game = self._id <= 151 or self._id in (
            808,  # meltan
            809,  # melmetal
            850,  # venusaur mega
            851,  # charizard mega-x
            852,  # charizard mega-y
            867,  # blastoise mega
            909,  # beedrill mega
            898,  # pidgeot mega
            916,  # rattata alola
            917,  # raticate alola
            966,  # pikachu starter
            919,  # raichu alola
            920,  # sandshrew alola
            921,  # sandslash alola
            922,  # vulpix alola
            923,  # ninetales alola
            953,  # diglett alola
            954,  # dugtrio alola
            924,  # meowth alola
            925,  # persian alola
            871,  # alakazam mega
            926,  # geodude alola
            927,  # graveler alola
            928,  # golem alola
            896,  # slowbro mega
            929,  # grimer alola
            930,  # muk alola
            837,  # gengar mega
            931,  # exeggutor alola
            932,  # marowak alola
            868,  # kangaskhan mega
            862,  # pinsir mega
            869,  # gyarados mega
            979,  # eevee starter
            863,  # aerodactyl mega
            853,  # mewtwo mega-x
            854,  # mewtwo mega-y
        )
