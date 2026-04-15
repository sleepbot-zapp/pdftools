import os


def collect_files(paths):
    out = []
    for p in paths:
        if os.path.isdir(p):
            out.extend(os.path.join(p, f) for f in os.listdir(p))
        else:
            out.append(p)
    return out


def normalize_ext(p):
    e = os.path.splitext(p)[1].lower()
    return ".jpg" if e == ".jpeg" else e


def filter_supported(files, supported_formats):
    return [f for f in files if normalize_ext(f) in supported_formats]


def sort_files(files, order="asc"):
    return sorted(files, key=lambda x: os.path.basename(x), reverse=(order == "desc"))
