import argparse
from converter import ImageToPDFConverter
from utils import (
    parse_group_args,
    parse_duplicate_args,
    parse_resize_args,
    parse_compress_args,
)


def main():
    parser = argparse.ArgumentParser(description="Image -> PDF")

    parser.add_argument("inputs", nargs="+")
    parser.add_argument("-o", "--output", required=True)

    # ✅ Updated sort argument
    parser.add_argument(
        "--sort",
        "-s",
        nargs="+",
        metavar=("FIELD", "ORDER"),
        default=["name", "asc"],
        help="Sort by FIELD (file, name, date) and optional ORDER (asc, desc)",
    )

    parser.add_argument(
        "--resize",
        "-r",
        nargs="*",
        help="--resize [global size] [page=size]",
    )

    parser.add_argument(
        "--duplicate",
        "-d",
        nargs="*",
        help="--duplicate [global multiplier] [page=multiplier]",
    )

    parser.add_argument(
        "--group",
        "-g",
        nargs="+",
        metavar="EXT",
        help="--group EXT1 EXT2 *",
    )

    parser.add_argument(
        "--compress",
        nargs="?",
        const="medium",
        default="none",
        choices=["none", "low", "medium", "high"],
    )

    args = parser.parse_args()

    # ✅ Normalize and validate --sort
    valid_fields = {"file", "name", "date"}
    valid_orders = {"asc", "desc"}

    sort_args = args.sort

    if len(sort_args) == 1:
        field = sort_args[0]
        order = "asc"
    elif len(sort_args) == 2:
        field, order = sort_args
    else:
        parser.error("--sort takes 1 or 2 arguments only")

    if field not in valid_fields:
        parser.error(f"Invalid sort field: {field}")

    if order not in valid_orders:
        parser.error(f"Invalid sort order: {order}")

    args.sort = (field, order)

    # ✅ Parse other configs
    resize_cfg = parse_resize_args(args.resize)

    try:
        dup_cfg = parse_duplicate_args(args.duplicate)
        group_cfg = parse_group_args(args.group)
        compress_cfg = parse_compress_args(args.compress)
    except ValueError as e:
        parser.error(str(e))

    # ✅ Run converter
    converter = ImageToPDFConverter(
        resize=resize_cfg,
        compress=compress_cfg,
    )

    converter.load_images(
        args.inputs,
        sort=args.sort, # type: ignore
        duplicate=dup_cfg,
        group=group_cfg,
    )

    converter.convert(args.output)


if __name__ == "__main__":
    main()