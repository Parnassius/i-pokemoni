from __future__ import annotations

from os.path import join

from utils import read_as_int

from .item_info import ItemInfo


class ItemInfoSwSh(ItemInfo):
    _SIZE = 0x30
    _TYPE = "singlefile"
    _PATH = join("bin", "pml", "item", "item.dat")

    def __init__(self, table, path: str, id: int, data: bytes) -> None:
        super().__init__(table, path, id, data)

        self._price = read_as_int(4, self._data, 0x00)
        self.watt_price = read_as_int(4, self._data, 0x04)
        self.bp_dynite_price = read_as_int(4, self._data, 0x08)
        """
        "premier-ball", 1       max-lair-dynite-ore
        "hp-up", 2              max-lair-dynite-ore    hammerlocke-bp-shop
        "protein", 2            max-lair-dynite-ore    hammerlocke-bp-shop
        "iron", 2               max-lair-dynite-ore    hammerlocke-bp-shop
        "carbos", 2             max-lair-dynite-ore    hammerlocke-bp-shop
        "calcium", 2            max-lair-dynite-ore    hammerlocke-bp-shop
        "rare-candy", 20                               hammerlocke-bp-shop
        "pp-up", 10                                    hammerlocke-bp-shop
        "zinc", 2               max-lair-dynite-ore    hammerlocke-bp-shop
        "white-herb", 15                                                                                   battle-tower-bp-shop-right
        "macho-brace", 10                              hammerlocke-bp-shop
        "mental-herb", 15                                                                                  battle-tower-bp-shop-right
        "choice-band", 25                                                                                  battle-tower-bp-shop-right
        "light-clay", 15                                                                                   battle-tower-bp-shop-right
        "life-orb", 25                                                                                     battle-tower-bp-shop-right
        "power-herb", 15                                                                                   battle-tower-bp-shop-right
        "toxic-orb", 10
        "flame-orb", 10
        "focus-sash", 15                                                                                   battle-tower-bp-shop-right
        "zoom-lens", 15
        "destiny-knot", 10                             hammerlocke-bp-shop
        "choice-scarf", 25                                                                                 battle-tower-bp-shop-right
        "power-bracer", 10                             hammerlocke-bp-shop
        "power-belt", 10                               hammerlocke-bp-shop
        "power-lens", 10                               hammerlocke-bp-shop
        "power-band", 10                               hammerlocke-bp-shop
        "power-anklet", 10                             hammerlocke-bp-shop
        "power-weight", 10                             hammerlocke-bp-shop
        "choice-specs", 25                                                                                 battle-tower-bp-shop-right
        "protector", 10                                hammerlocke-bp-shop
        "reaper-cloth", 10                             hammerlocke-bp-shop
        "razor-claw", 10                               hammerlocke-bp-shop
        "air-balloon", 15                                                                                  battle-tower-bp-shop-right
        "red-card", 20                                                                                     battle-tower-bp-shop-right
        "absorb-bulb", 10                                                                                  battle-tower-bp-shop-right
        "cell-battery", 10                                                                                 battle-tower-bp-shop-right
        "eject-button", 20                                                                                 battle-tower-bp-shop-right
        "weakness-policy", 20                                                                              battle-tower-bp-shop-right
        "assault-vest", 25                                                                                 battle-tower-bp-shop-right
        "ability-capsule", 50   max-lair-dynite-ore                                                        battle-tower-bp-shop-right
        "whipped-dream", 10                            hammerlocke-bp-shop
        "sachet", 10                                   hammerlocke-bp-shop
        "luminous-moss", 10                                                                                battle-tower-bp-shop-right
        "snowball", 10                                                                                     battle-tower-bp-shop-right
        "bottle-cap", 25        max-lair-dynite-ore                                                        battle-tower-bp-shop-right
        "adrenaline-orb", 10                                                                               battle-tower-bp-shop-right
        "beast-ball", 150       max-lair-dynite-ore
        "terrain-extender", 15                                                                             battle-tower-bp-shop-right
        "throat-spray", 10                                                                                 battle-tower-bp-shop-right
        "eject-pack", 20                                                                                   battle-tower-bp-shop-right
        "blunder-policy", 20                                                                               battle-tower-bp-shop-right
        "room-service", 15                                                                                 battle-tower-bp-shop-right
        "exp-candy-l", 1        max-lair-dynite-ore
        "exp-candy-xl", 3       max-lair-dynite-ore
        "dynamax-candy", 2      max-lair-dynite-ore
        "lonely-mint", 50                                                     battle-tower-bp-shop-left
        "adamant-mint", 50                                                    battle-tower-bp-shop-left
        "naughty-mint", 50                                                    battle-tower-bp-shop-left
        "brave-mint", 50                                                      battle-tower-bp-shop-left
        "bold-mint", 50                                                       battle-tower-bp-shop-left
        "impish-mint", 50                                                     battle-tower-bp-shop-left
        "lax-mint", 50                                                        battle-tower-bp-shop-left
        "relaxed-mint", 50                                                    battle-tower-bp-shop-left
        "modest-mint", 50                                                     battle-tower-bp-shop-left
        "mild-mint", 50                                                       battle-tower-bp-shop-left
        "rash-mint", 50                                                       battle-tower-bp-shop-left
        "quiet-mint", 50                                                      battle-tower-bp-shop-left
        "calm-mint", 50                                                       battle-tower-bp-shop-left
        "gentle-mint", 50                                                     battle-tower-bp-shop-left
        "careful-mint", 50                                                    battle-tower-bp-shop-left
        "sassy-mint", 50                                                      battle-tower-bp-shop-left
        "timid-mint", 50                                                      battle-tower-bp-shop-left
        "hasty-mint", 50                                                      battle-tower-bp-shop-left
        "jolly-mint", 50                                                      battle-tower-bp-shop-left
        "naive-mint", 50                                                      battle-tower-bp-shop-left
        "serious-mint", 50                                                    battle-tower-bp-shop-left
        "wishing-piece", 3      max-lair-dynite-ore
        "armorite-ore", 3       max-lair-dynite-ore
        "ability-patch", 200    max-lair-dynite-ore
        """

        self.held_effect = int(self._data[0x0C])  # 0x02
        self.held_argument = int(self._data[0x0D])  # 0x03
        self.natural_gift_effect = int(self._data[0x0E])  # 0x04
        self.fling_effect = 0  # moved?
        self.fling_power = int(self._data[0x12])  # 0x06
        self.natural_gift_power = int(self._data[0x0F])  # 0x07
        self.packed = read_as_int(2, self._data, 0x10)  # 0x08

        self.effect_field = int(self._data[0x13])  # 0x0A
        self.effect_battle = int(self._data[0x14])  # 0x0B

        # 0x15 => 1 or 0

        self._pocket = int(self._data[0x16])

        self._consumable = int(self._data[0x17])  # 0x0E
        self.sort_index = int(self._data[0x18])  # 0x0F

        # 0x19 => 0
        # 0x1A => ma che ne so è una sbrodolata infinita, ma tanti sono 0xFF
        # 0x1B => boh altra sbrodolata

        # 0x1C
        #  1 = balls
        #  2 = nothing
        #  3 = berries
        #  4 = tm/tr
        #  5 = normal gem

        # 0x1D => ordine o giù di lì (tm/tr/palle/bacche)

        self.cure_inflict = int(self._data[0x1E])  # 0x10
        self._boost_0 = int(self._data[0x1F])  # 0x11
        self._boost_1 = int(self._data[0x20])  # 0x12
        self._boost_2 = int(self._data[0x21])  # 0x13
        self._boost_3 = int(self._data[0x22])  # 0x14
        self.function_flags_0 = int(self._data[0x23])  # 0x15
        self.function_flags_1 = int(self._data[0x24])  # 0x16

        self.ev_hp = read_as_int(1, self._data, 0x25, True)  # 0x17
        self.ev_attack = read_as_int(1, self._data, 0x26, True)  # 0x18
        self.ev_defense = read_as_int(1, self._data, 0x27, True)  # 0x19
        self.ev_speed = read_as_int(1, self._data, 0x28, True)  # 0x1A
        self.ev_special_attack = read_as_int(1, self._data, 0x29, True)  # 0x1B
        self.ev_special_defense = read_as_int(1, self._data, 0x2A, True)  # 0x1C

        self.heal_amount = int(self._data[0x2B])  # 0x1D
        self.pp_gain = int(self._data[0x2C])  # 0x1E

        self.friendship_1 = read_as_int(1, self._data, 0x2D, True)  # 0x1F
        self.friendship_2 = read_as_int(1, self._data, 0x2E, True)  # 0x20
        self.friendship_3 = read_as_int(1, self._data, 0x2F, True)  # 0x21

    @property
    def fling_effect_id(self) -> int:
        return 0  # i have no idea

    def category_id(self, identifier: str) -> int:
        if (
            self._pocket == 1
        ):  # healing items + vitamins + repels + ability capsule + ability patch + mints
            if identifier.startswith("exp-candy-") or identifier in (
                "ability-patch",
                "dynamax-candy",
            ):
                return 26  # medicine => vitamins
            if identifier.endswith("-mint"):
                return 50  # medicine => nature-mints

        if (
            self._pocket == 2
        ):  #  evo stones + "useful?" held items (genesect's drives, toxic orb, choice band, amulet coin, ...)
            if identifier in ("rusted-sword", "rusted-shield"):
                return 18  # misc => species-specific
            if self.evo_stone or identifier.endswith("-sweet"):
                return 10  # misc => evolution
            if identifier in (
                "throat-spray",
                "eject-pack",
                "heavy-duty-boots",
                "blunder-policy",
                "room-service",
                "utility-umbrella",
            ):
                return 12  # misc => held-items

        if (
            self._pocket == 3
        ):  #  apricorns + various food + ★-items + max honey + galarica twig/cuff/wreath + amorite/dynite ore
            if identifier in (
                "wishing-piece",
                "galarica-twig",
                "galarica-cuff",
                "armorite-ore",
                "galarica-wreath",
                "dynite-ore",
            ):
                return 9  # misc => collectibles
            if identifier == "max-honey":
                return 29  # medicines => revival
            if identifier in (
                "sausages",
                "bobs-food-tin",
                "bachs-food-tin",
                "tin-of-beans",
                "bread",
                "pasta",
                "mixed-mushrooms",
                "smoke-poke-tail",
                "large-leek",
                "fancy-apple",
                "brittle-bones",
                "pack-of-potatoes",
                "pungent-root",
                "salad-mix",
                "fried-food",
                "boiled-egg",
                "fruit-bunch",
                "moomoo-cheese",
                "spice-mix",
                "fresh-cream",
                "packaged-curry",
                "coconut-milk",
                "instant-noodles",
                "precooked-burger",
                "gigantamix",
            ):
                return 51  # misc => curry-ingredients
            if identifier.startswith("dynamax-crystal-"):
                return 49  # misc => dynamax-crystals

        if self._pocket == 4:  #  x-items + pokedoll + max mushrooms
            if (
                self.boost_attack
                or self.boost_defense
                or self.boost_special_attack
                or self.boost_special_defense
                or self.boost_speed
                or self.boost_accuracy
                or self.boost_crit
                or self.cure_inflict_guard_spec
            ):
                return 1  # battle => stat-boosts

        if self._pocket == 7:  # machines
            return 37  # all-machines

        if self._pocket == 9:  # key
            if identifier in (
                "pokemon-box-link",
                "fishing-rod--galar",
                "rotom-bike",
                "camping-gear",
                "hi-tech-earbuds",
                "catching-charm",
                "rotom-catalog",
                "style-card",
                "exp-charm",
                "mark-charm",
            ):
                return 21  # gameplay
            if identifier in (
                "endorsement",
                "wishing-star",
                "dynamax-band",
                "old-letter",
                "sonias-book",
                "armor-pass",
                "legendary-clue-1",
                "legendary-clue-2",
                "legendary-clue-3",
                "legendary-clue-question",
                "crown-pass",
                "wooden-crown",
                "radiant-petal",
                "white-mane-hair",
                "black-mane-hair",
                "iceroot-carrot",
                "shaderoot-carrot",
                "carrot-seeds",
                "reins-of-unity",
            ):
                return 22  # plot-advancement
            if identifier in (
                "band-autograph",
                "rotom-bike--water-mode",
                "rotom-bike--sparkling-white",
                "rotom-bike--glistening-black",
                "reins-of-unity--merge",
                "reins-of-unity--split",
            ):
                return 23  # unused

        if self._pocket == 10:  # treasures + fossils
            if identifier.startswith("fossilized-"):
                return 35  # misc => dex-completion

        if self._pocket == 255:  # everything else
            if identifier in ("wishing-chip"):
                return 23  # key => unused

        print("no category_id: ", self._pocket, identifier)
        return 0
