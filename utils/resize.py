def parse_resize_args(args):
    if not args:
        return None, {}

    default = int(args[0])
    overrides = {}

    for x in args[1:]:
        if "=" in x:
            p, s = x.split("=")
            overrides[int(p)] = int(s)

    return default, overrides


def get_resize(cfg, original_index):
    if not cfg:
        return None
    default, overrides = cfg
    return overrides.get(original_index + 1, default)


def apply_resize(img, size):
    if size:
        img.thumbnail((size, size))
    return img
