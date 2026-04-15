from PIL import Image
from utils import (
    get_multiplier,
    get_resize,
    apply_resize,
    collect_files,
    filter_supported,
    sort_files,
    group_files,
)
from extra import Progress
from config import SUPPORTED_FORMATS


class ImageToPDFConverter:
    def __init__(self, resize=None):
        self.resize = resize
        self.files = []
        self.global_mult = 1
        self.rules = []

    def load_images(self, paths, sort="asc", duplicate=None, group=None):
        files = collect_files(paths)
        files = filter_supported(files, SUPPORTED_FORMATS)
        if group is not None:
            files = group_files(files, group, sort_order=sort)
        else:
            files = sort_files(files, sort)
        self.files = files
        if duplicate:
            self.global_mult, self.rules = duplicate
        else:
            self.global_mult, self.rules = 1, []

    def estimate_total_pages(self):
        total = 0
        for i in range(len(self.files)):
            page = i + 1
            total += get_multiplier(page, self.rules)
        return total * self.global_mult

    def convert(self, output_path):
        tracker = Progress()
        first = None
        rest = []
        count = 0
        for _ in range(self.global_mult):
            for i, path in enumerate(self.files):
                page = i + 1
                mult = get_multiplier(page, self.rules)
                for _ in range(mult):
                    try:
                        img = Image.open(path)

                        if img.mode in ("RGBA", "P"):
                            img = img.convert("RGB")

                        size = get_resize(self.resize, page)
                        img = apply_resize(img, size)

                        if first is None:
                            first = img
                        else:
                            rest.append(img)

                    except Exception as e:
                        print(f"\n[SKIP] {path}: {e}")
                    count += 1
                    tracker.update()
        print()

        if first is None:
            raise ValueError("No valid images found")
        first.save(output_path, save_all=True, append_images=rest)

        tracker.finish(count)
        print(f"[DONE] Saved: {output_path}")
