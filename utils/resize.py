def parse_resize_args(args):
    if not args:
        return None, {}

    def parse_size(s):
        try:
            w, h = s.lower().split("x")
            return int(w), int(h)
        except:
            raise ValueError(f"Invalid resize format: {s} (use WIDTHxHEIGHT)")

    default = parse_size(args[0])
    overrides = {}

    for x in args[1:]:
        if "=" in x:
            p, s = x.split("=")
            overrides[int(p)] = parse_size(s)

    return default, overrides


def get_resize(cfg, page):
    if not cfg:
        return None
    default, overrides = cfg
    return overrides.get(page, default)


def apply_resize(img, size):
    if size:
        return img.resize(size)
    return img
