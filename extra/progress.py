import sys
import time


class Progress:
    def __init__(self):
        self.start = time.time()
        self.frames = ["|", "/", "-", "\\"]
        self.i = 0

    def update(self):
        frame = self.frames[self.i % 4]
        self.i += 1
        sys.stdout.write(f"\r{frame} Processing...")
        sys.stdout.flush()

    def finish(self, count):
        elapsed = time.time() - self.start
        speed = count / elapsed if elapsed > 0 else 0
        sys.stdout.write(
            f"\r✔ Converted {count} pages in {elapsed:.1f}s | {speed:.2f} img/s\n"
        )
        sys.stdout.flush()
