

A fast cli tool I made to make faster pdfs from images.

## Supported Image File Types
- jpeg (jpg)
- png
- webp
- bmp
- tiff
- heic
- heif
- avif

## USAGE:


## Options

| Argument         | Description                                                                 | Example                              |
| :--------------: | :-------------------------------------------------------------------------- | :----------------------------------- |
| `inputs`         | Input files (multiple), folders, or wildcard patterns (`*`)                            | `img1.jpeg images/ *.jpg folder/*`              |
| `-o, --output`   | Output PDF file (required)                                                  | `-o output.pdf`                       |
| `-s, --sort`     | Sort images by `file`, `name`, or `date` + `asc/desc`                       | `--sort name desc`                    |
| `-r, --resize`   | Resize images globally and/or per page                                          | `--resize 800x600 1=400x300`     |
| `-d, --duplicate`| Duplicate images globally and/or per page                                       | `--duplicate 2 3=4`               |
| `-g, --group`    | Group images by extensions (supports wildcard `*` patterns)                 | `--group jpg png *`                   |
| `--compress`     | Compression level (`none`, `low`, `medium`, `high`)                         | `--compress high`                     |      |
