SUPPORTED_BASE = (".jpg", ".png", ".webp", ".bmp", ".tiff")
SUPPORTED_FORMATS: set[str] = set(SUPPORTED_BASE)

try:
    import pillow_heif

    pillow_heif.register_heif_opener()
    SUPPORTED_FORMATS.update({".heic", ".heif"})
except ImportError:
    pass

try:
    import pillow_avif

    SUPPORTED_FORMATS.add(".avif")
except ImportError:
    pass
