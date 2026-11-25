"""Entry for make.fun competition
u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.

Writes the invitation image (entry.png, shipped in this repository)
byte-exact to /output/entry.png.

Before copying, the entry is validated against the kit gate
(RULES.txt): PNG or JPEG, at most 1 MiB (1,048,576 bytes) and at most
1024x1024 pixels. A file the gate would refuse fails loudly here
instead of being shipped as a doomed entry.
"""

import shutil
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent

MAX_BYTES = 1_048_576
MAX_DIMENSION = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_dimensions(data: bytes) -> tuple[int, int]:
    """Return (width, height) from a PNG header; raise if not a PNG."""
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("entry.png is not a PNG file")
    # IHDR chunk: 8-byte signature, 4-byte length, 4-byte type,
    # then width and height as big-endian uint32.
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise ValueError("entry.png has no valid IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def validate_gate(src: Path) -> None:
    """Fail loudly if the entry would be refused by the kit gate."""
    size = src.stat().st_size
    if size > MAX_BYTES:
        raise ValueError(
            f"entry.png is {size} bytes, over the 1 MiB gate limit"
        )
    width, height = png_dimensions(src.read_bytes())
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise ValueError(
            f"entry.png is {width}x{height}, over the 1024x1024 gate limit"
        )
    print(f"gate ok: {width}x{height}, {size} bytes")


def main() -> None:
    src = HERE / "entry.png"
    validate_gate(src)
    out_dir = Path("/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(src, dest)
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
