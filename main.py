import argparse
from converter import ImageToPDFConverter
from utils import parse_group_args, parse_duplicate_args, parse_resize_args, parse_compress_args


def main():
    parser = argparse.ArgumentParser(description="Image -> PDF")

    parser.add_argument("inputs", nargs="+")
    parser.add_argument("-o", "--output", required=True)

    parser.add_argument(
        "--sort",
        "-s",
        nargs="?",
        const="asc",
        default="asc",
        choices=["asc", "desc"],
        help="--sort asc|desc [default: asc]",
    )

    parser.add_argument(
        "--resize", "--r", nargs="*", help="--resize [global size] [page=size]"
    )
    parser.add_argument(
        "--duplicate", "--d", nargs="*", help="--duplicate [global multiplier] [page=multiplier]"
    )
    parser.add_argument(
        "--group",
        "--g",
        nargs="+",
        metavar="EXT",
        help=("--group EXT1 EXT2 *"),
    )
    parser.add_argument(
        "--compress none|low|medium|high",
        nargs="?",
        const="medium",
        default="none",
        choices=["none", "low", "medium", "high",]
    )
    args = parser.parse_args()

    resize_cfg = parse_resize_args(args.resize)

    try:
        dup_cfg = parse_duplicate_args(args.duplicate)
        group_cfg = parse_group_args(args.group)
        compress_cfg = parse_compress_args(args.compress)
    except ValueError as e:
        parser.error(str(e))

    converter = ImageToPDFConverter(resize=resize_cfg, compress=compress_cfg)
    converter.load_images(
        args.inputs,
        sort=args.sort,
        duplicate=dup_cfg,
        group=group_cfg,
    )
    converter.convert(args.output)


if __name__ == "__main__":
    main()
