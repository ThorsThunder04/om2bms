import os

from argparse import ArgumentParser

import om2bms.om_to_bms


if __name__ == '__main__':

    parser = ArgumentParser(description='Convert a .osu osu!mania file to a BMS file. '
                                        'Outputs to directory of om2bms.py',
                            add_help=True,
                            allow_abbrev=True)

    parser.add_argument('-i', '--in_file',
                        action='store',
                        help='Path to file to be converted.',
                        type=str)

    parser.add_argument('-hs', '--hitsound',
                        action='store_false',
                        default=False,
                        help='Disables hitsounds.')

    parser.add_argument('-b', '--bg',
                        action='store_false',
                        default=True,
                        help='Disables background conversion.')

    parser.add_argument('-o', '--offset',
                        default=0,
                        type=int,
                        help="Adjusts music start time by [offset] ms.")

    parser.add_argument('-j', '--judge',
                        default=2,
                        type=int,
                        help="Judge difficulty. Defaults to EASY. "
                        "(3: EASY), (2: NORMAL), (1: HARD), (0: VERY HARD)")

    args = parser.parse_args()

    cwd = os.getcwd()

    om2bms.om_to_bms.OsuManiaToBMSParser._convertion_options = {
        "HITSOUND": args.hitsound,
        "VIDEO": False,
        "BG": args.bg,
        "OFFSET": args.offset,
        "JUDGE": args.judge
    }
    convert = om2bms.om_to_bms.OsuManiaToBMSParser(
        args.in_file, os.getcwd(), args.in_file)
    print("Done")
    exit(0)
