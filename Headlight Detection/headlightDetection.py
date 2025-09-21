import cv2
import numpy as np
import time
from pathlib import Path
from matplotlib import pyplot as plt

# ---- Settings ----
SHOW_FIGS = True   # Set False if you don’t want matplotlib popups
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# 🔑 Your folder (searched RECURSIVELY)
IMAGE_DIR = Path("/Users/brandonr/Documents/CPSC_2735 copy")

# Accepted image extensions (case-insensitive)
EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp", ".heic"}

def wait(t: float):
    time.sleep(t)

def list_dir_quick(folder: Path, limit: int = 40):
    """Print a quick listing to help debug when no images are found."""
    print(f"\nQuick listing for: {folder}")
    entries = sorted(folder.rglob("*"))
    shown = 0
    for p in entries:
        if shown >= limit:
            print(f"... ({len(entries) - shown} more)")
            break
        kind = "DIR " if p.is_dir() else "FILE"
        print(f"{kind:4} {p}")
        shown += 1
    if not entries:
        print("(Folder is empty)")

def get_images_recursive(folder: Path):
    """Return all image files (recursively) in the given folder."""
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")
    images = [p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in EXTS]
    if not images:
        list_dir_quick(folder)
        raise FileNotFoundError(f"No images with extensions {sorted(EXTS)} found in {folder}")
    return images

def scenario(image_path: Path, show: bool = SHOW_FIGS):
    image = cv2.imread(str(image_path))
    if image is None:
        # Some OpenCV builds can’t read HEIC; suggest converting.
        raise ValueError(f"Failed to read image: {image_path} "
                         f"(If this is .heic, consider converting: "
                         f'sips -s format jpeg "{image_path}" --out "{image_path}.jpg")')

    # --- Processing ---
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (15, 15), 0)
    _, thresh = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)

    found = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(found) == 3:
        _img, contours, hierarchy = found
    else:
        contours, hierarchy = found

    vis = image.copy()
    cv2.drawContours(vis, contours, -1, (0, 255, 0), 2)

    centroids = []
    for cnt in contours:
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centroids.append((cx, cy))
            cv2.circle(vis, (cx, cy), 3, (0, 0, 255), -1)

    # --- Save outputs ---
    stem = image_path.stem
    out_gray   = OUTPUT_DIR / f"{stem}_gray.png"
    out_blur   = OUTPUT_DIR / f"{stem}_blur.png"
    out_thresh = OUTPUT_DIR / f"{stem}_thresh.png"
    out_vis    = OUTPUT_DIR / f"{stem}_contours.png"

    cv2.imwrite(str(out_gray), gray)
    cv2.imwrite(str(out_blur), blur)
    cv2.imwrite(str(out_thresh), thresh)
    cv2.imwrite(str(out_vis), vis)

    # --- Show results ---
    if show:
        try:
            vis_rgb = cv2.cvtColor(vis, cv2.COLOR_BGR2RGB)
            plt.figure(figsize=(7, 5))
            plt.title(f"{stem}: Contours + Centroids")
            plt.imshow(vis_rgb)
            plt.axis("off")
            plt.show()

            plt.figure(figsize=(7, 5))
            plt.title(f"{stem}: Threshold")
            plt.imshow(thresh, cmap="gray")
            plt.axis("off")
            plt.show()
        except Exception as e:
            print(f"(Display skipped) {e}")

    return {
        "image": str(image_path),
        "num_contours": len(contours),
        "centroids": centroids[:50],
        "saved": {
            "gray": str(out_gray.resolve()),
            "blur": str(out_blur.resolve()),
            "thresh": str(out_thresh.resolve()),
            "contours": str(out_vis.resolve())
        }
    }

if __name__ == "__main__":
    print("Starting macOS-safe image processing…")
    try:
        images = get_images_recursive(IMAGE_DIR)
        print(f"Found {len(images)} image(s).")
        for p in images:
            print(f"\nProcessing {p} …")
            stats = scenario(p, show=SHOW_FIGS)
            print(f"Contours: {stats['num_contours']}")
            print("Saved files:")
            for k, v in stats["saved"].items():
                print(" ", k, "->", v)
            wait(0.1)
    except Exception as e:
        print(f"Setup error: {e}")
