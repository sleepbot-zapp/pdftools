from .duplicate import parse_duplicate_args, get_multiplier
from .grouping import parse_group_args, group_files
from .resize import parse_resize_args, get_resize, apply_resize
from .file import collect_files, filter_supported, sort_files
from .compress import compress_pdf, parse_compress_args

__all__ = (
    "parse_duplicate_args",
    "get_multiplier",
    "parse_group_args",
    "group_files",
    "parse_resize_args",
    "get_resize",
    "apply_resize",
    "collect_files",
    "filter_supported",
    "sort_files",
    "compress_pdf",
    "parse_compress_args",
)
