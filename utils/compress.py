import subprocess
import os
import shutil
import platform


def get_gs_command():
    for cmd in ("gs", "gswin64c", "gswin32c"):
        path = shutil.which(cmd)
        if path:
            return path

    if platform.system() == "Windows":
        base = r"C:\Program Files\gs"
        if os.path.exists(base):
            for folder in os.listdir(base):
                bin_path = os.path.join(base, folder, "bin")
                for exe in ("gswin64c.exe", "gswin32c.exe"):
                    full_path = os.path.join(bin_path, exe)
                    if os.path.exists(full_path):
                        return full_path

    return None


def parse_compress_args(level):
    if not level:
        return "none"

    level = level.lower()
    valid_levels = {"none", "low", "medium", "high"}

    if level not in valid_levels:
        raise ValueError(f"--compress has invalid value: '{level}'")

    return level


def fallback_compress_pdf(file_path, level):
    try:
        import fitz  # pymupdf
    except ImportError:
        raise RuntimeError(
            "pymupdf is required for fallback compression but is not installed. For more info refer to the documentation."
        )

    doc = fitz.open(file_path)

    zoom_map = {"low": 2.0, "medium": 1.5, "high": 1.0}

    zoom = zoom_map.get(level, 1.5)

    new_doc = fitz.open()

    for page in doc:
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        new_page = new_doc.new_page(width=pix.width, height=pix.height)
        new_page.insert_image(new_page.rect, pixmap=pix)

    temp_output = file_path + ".tmp.pdf"
    new_doc.save(temp_output)
    new_doc.close()
    doc.close()

    os.replace(temp_output, file_path)
    return file_path


def compress_pdf(file_path: str, level: str):
    if level == "none":
        return file_path

    gs_cmd = get_gs_command()

    temp_output = file_path + ".tmp.pdf"

    if gs_cmd:
        quality_map = {"low": "/printer", "medium": "/ebook", "high": "/screen"}

        command = [
            gs_cmd,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS={quality_map[level]}",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={temp_output}",
            file_path,
        ]

        try:
            subprocess.run(command, check=True)
            os.replace(temp_output, file_path)
            return file_path

        except Exception as e:
            if os.path.exists(temp_output):
                os.remove(temp_output)
            raise RuntimeError(f"Ghostscript compression failed: {e}")

    try:
        return fallback_compress_pdf(file_path, level)

    except Exception as e:
        raise RuntimeError(
            f"Compression failed (no Ghostscript + fallback failed): {e}"
        )
