def parse_duplicate_args(args):
    if not args:
        return 1, []

    global_mult = 1
    rules = []

    for x in args:
        if "=" not in x:
            global_mult = int(x)
            continue

        left, val = x.split("=")
        val = int(val)

        parts = left.split(",")

        for p in parts:
            p = p.strip()

            if "-" in p:
                a, b = p.split("-")
                rules.append(("range", int(a), int(b), val))
            else:
                rules.append(("single", int(p), val))

    return global_mult, rules


def get_multiplier(page, rules):
    m = 1

    for r in rules:
        if r[0] == "single":
            _, p, v = r
            if page == p:
                m = max(m, v)
        else:
            _, a, b, v = r
            if a <= page <= b:
                m = max(m, v)

    return m
