from .file import normalize_ext, sort_files


def parse_group_args(args):
    if not args:
        return None
    seen = set()
    slots = []
    for token in args:
        if token == "*":
            key = "*"
        else:
            ext = token.lower().lstrip(".")
            key = ".jpg" if ext == "jpeg" else f".{ext}"
        if key in seen:
            raise ValueError(f"--group has duplicate entry: '{token}'")
        seen.add(key)
        slots.append(key)
    return slots


def group_files(files, slots, sort_order="asc"):
    explicit_exts = {s for s in slots if s != "*"}
    buckets = {slot: [] for slot in slots}
    for f in files:
        ext = normalize_ext(f)
        if ext in explicit_exts:
            buckets[ext].append(f)
        elif "*" in buckets:
            buckets["*"].append(f)
    result = []
    for slot in slots:
        bucket = sort_files(buckets[slot], sort_order)
        result.extend(bucket)
    return result
