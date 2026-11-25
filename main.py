"""Entry for make.fun competition
u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.

Writes the invitation image (entry.png, shipped in this repository)
byte-exact to /output/entry.png.
"""

import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    src = HERE / "entry.png"
    out_dir = Path("/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(src, dest)
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
