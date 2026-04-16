import os
import glob


def collect_files(paths):
    out = []
    for p in paths:
        matches = glob.glob(p, recursive=True)

        if matches:
            for match in matches:
                if os.path.isdir(match):
                    out.extend(os.path.join(match, f) for f in os.listdir(match))
                else:
                    out.append(match)
        elif os.path.isdir(p):
            out.extend(os.path.join(p, f) for f in os.listdir(p))
        else:
            out.append(p)

    return out


def normalize_ext(p):
    e = os.path.splitext(p)[1].lower()
    return ".jpg" if e == ".jpeg" else e


def filter_supported(files, supported_formats):
    return [f for f in files if normalize_ext(f) in supported_formats]


def sort_files(files, sort=("name", "asc")):
    field, order = sort

    reverse = order == "desc"

    def key_func(path):
        if field == "name":
            return os.path.basename(path).lower()

        elif field == "file":
            return os.path.splitext(path)[1].lower()

        elif field == "date":
            return os.path.getmtime(path)

        else:
            raise ValueError(f"Unsupported sort field: {field}")

    return sorted(files, key=key_func, reverse=reverse)
