import argparse

from scripts.dump_letsgo import DumpLetsGo
from scripts.dump_sm import DumpSM
from scripts.dump_swsh import DumpSwSh
from scripts.dump_usum import DumpUsUm

if __name__ == "__main__":
    dumpers = {
        "sm": DumpSM,
        "usum": DumpUsUm,
        "letsgo": DumpLetsGo,
        "swsh": DumpSwSh,
    }

    parser = argparse.ArgumentParser()
    for i, d in dumpers.items():
        parser.add_argument(f"--{i}", action="extend", nargs="*", choices=d._SECTIONS)
    args = parser.parse_args()

    for i, d in dumpers.items():
        sections = getattr(args, i, None)
        if sections is not None:
            d(sections or d._SECTIONS)
