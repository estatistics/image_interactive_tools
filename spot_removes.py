import os
import sys

# Silence Qt Font & QPA warnings completely before OpenCV imports
os.environ["QT_QPA_FONTDIR"] = "/usr/share/fonts"
os.environ["QT_LOGGING_RULES"] = "qt.qpa.fonts.warning=false;*.warning=false"

import cv2
import numpy as np
from pathlib import Path

# ==============================================================================
# CONFIGURATION SETTINGS
# ==============================================================================
CONFIG = {
    # Output format: "jpg", "webp", or "png"
    "OUTPUT_FORMAT": "jpg",

    # Quality settings:
    # - JPG / WEBP: 1 to 100 (higher = better quality)
    # - PNG: 0 to 9 (compression level)
    "QUALITY": 95,

    # Shadow Expansion Buffer (0.05 to 0.30):
    "EXPANSION_PCT": 0.10,

    # External Texture Options:
    "USE_EXTERNAL_TEXTURE": True,
    "TEXTURE_FILENAME": "./cloning_image/cloning.webp",

    # Pseudo Canvas Padding Percentage (e.g., 0.08 = 8% padding on all sides)
    # Allows seamless cloning to work smoothly along image borders and corners
    "PADDING_PCT": 0.08,

    # Output folder relative to script location
    "OUTPUT_FOLDER_NAME": "clean_pages_output",
}
# ==============================================================================


def load_unicode_image(filepath):
    path_str = str(filepath)
    if not os.path.exists(path_str):
        return None
    img_array = np.fromfile(path_str, dtype=np.uint8)
    return cv2.imdecode(img_array, cv2.IMREAD_COLOR)


class InteractiveFingerCleaner:
    def __init__(self, image_path, current_idx, total_count, config):
        self.image_path = image_path
        self.current_idx = current_idx
        self.total_count = total_count
        self.config = config

        self.original = load_unicode_image(image_path)
        if self.original is None:
            raise ValueError(f"Could not load image: {image_path}")

        self.h, self.w, _ = self.original.shape
        self.display_img = self.original.copy()

        self.shapes_history = []  # List of (center, axes)
        self.center = None
        self.axes = None
        self.drawing = False

        self.win_id = "FingerCleanerWindow"

        # Load external texture safely
        self.external_texture = None
        if self.config["USE_EXTERNAL_TEXTURE"]:
            tex_path = Path(__file__).parent / Path(self.config["TEXTURE_FILENAME"])
            self.external_texture = load_unicode_image(tex_path)
            if self.external_texture is None:
                print(f"Warning: Custom texture at '{tex_path}' not found. Falling back to auto-sampling.")

    def get_window_title(self):
        count = len(self.shapes_history)
        mode = "External Texture" if (self.config["USE_EXTERNAL_TEXTURE"] and self.external_texture is not None) else "Auto-Patch"
        return (
            f"[{self.current_idx}/{self.total_count}] {self.image_path.name} | "
            f"Circles: {count} | Mode: {mode} | ENTER=Save, U=Undo, R=Reset, S=Skip, ESC=Exit"
        )

    def redraw_display(self):
        self.display_img = self.original.copy()
        for center, axes in self.shapes_history:
            cv2.ellipse(self.display_img, center, axes, 0, 0, 360, (0, 255, 0), 2)

        cv2.setWindowTitle(self.win_id, self.get_window_title())
        cv2.imshow(self.win_id, self.display_img)

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.center = (x, y)
            self.axes = (0, 0)

        elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
            dx = abs(x - self.center[0])
            dy = abs(y - self.center[1])
            self.axes = (max(5, dx), max(5, dy))

            temp_display = self.display_img.copy()
            cv2.ellipse(temp_display, self.center, self.axes, 0, 0, 360, (0, 0, 255), 2)
            cv2.imshow(self.win_id, temp_display)

        elif event == cv2.EVENT_LBUTTONUP and self.drawing:
            self.drawing = False
            dx = abs(x - self.center[0])
            dy = abs(y - self.center[1])
            self.axes = (max(5, dx), max(5, dy))

            self.shapes_history.append((self.center, self.axes))
            self.redraw_display()

    def generate_expanded_mask(self, target_h, target_w, pad_x, pad_y):
        mask = np.zeros((target_h, target_w), dtype=np.uint8)
        exp_pct = self.config["EXPANSION_PCT"]

        for center, axes in self.shapes_history:
            # Shift center coordinates by padding offset
            padded_center = (center[0] + pad_x, center[1] + pad_y)
            exp_axes = (
                int(axes[0] * (1.0 + exp_pct)),
                int(axes[1] * (1.0 + exp_pct))
            )
            cv2.ellipse(mask, padded_center, exp_axes, 0, 0, 360, 255, -1)
        return mask

    def get_texture_patch(self, target_w, target_h, padded_img, min_x, max_x, min_y, max_y):
        if self.external_texture is not None:
            return cv2.resize(self.external_texture, (target_w, target_h), interpolation=cv2.INTER_CUBIC)

        # Fallback to auto-sampling nearby paper
        pad_h, pad_w = padded_img.shape[:2]
        src_min_y = min(pad_h - target_h - 1, max_y + int(target_h * 0.2))
        src_max_y = src_min_y + target_h
        src_min_x = min_x
        src_max_x = max_x

        if src_max_y >= pad_h:
            src_min_y = max(0, min_y - int(target_h * 1.2))
            src_max_y = src_min_y + target_h

        return padded_img[src_min_y:src_max_y, src_min_x:src_max_x]

    def heal_selection(self):
        if not self.shapes_history:
            return self.original.copy()

        # Step 1: Calculate pseudo-canvas padding dimensions
        pad_pct = self.config.get("PADDING_PCT", 0.08)
        pad_y = int(self.h * pad_pct)
        pad_x = int(self.w * pad_pct)

        # Step 2: Create Pseudo-Canvas with replicated edge padding
        padded_img = cv2.copyMakeBorder(
            self.original,
            pad_y, pad_y, pad_x, pad_x,
            cv2.BORDER_REPLICATE
        )
        pad_h, pad_w, _ = padded_img.shape

        # Step 3: Generate mask on padded canvas space
        mask = self.generate_expanded_mask(pad_h, pad_w, pad_x, pad_y)

        y_indices, x_indices = np.where(mask > 0)
        min_x, max_x = np.min(x_indices), np.max(x_indices)
        min_y, max_y = np.min(y_indices), np.max(y_indices)

        box_w = max_x - min_x
        box_h = max_y - min_y

        if box_w <= 0 or box_h <= 0:
            return self.original.copy()

        texture_patch = self.get_texture_patch(box_w, box_h, padded_img, min_x, max_x, min_y, max_y)

        canvas = padded_img.copy()
        if texture_patch.shape[:2] == (box_h, box_w):
            sub_mask = mask[min_y:max_y, min_x:max_x]
            target_roi = canvas[min_y:max_y, min_x:max_x]
            target_roi[sub_mask > 0] = texture_patch[sub_mask > 0]

        center_pt = (int((min_x + max_x) / 2), int((min_y + max_y) / 2))

        try:
            # Seamless clone inside padded space (border is no longer boundary edge)
            healed_padded = cv2.seamlessClone(
                canvas,
                padded_img,
                mask,
                center_pt,
                cv2.NORMAL_CLONE
            )
        except cv2.error:
            healed_padded = canvas

        # Step 4: Crop pseudo-canvas back to original size before saving
        healed_final = healed_padded[pad_y:pad_y + self.h, pad_x:pad_x + self.w]
        return healed_final

    def run(self):
        cv2.namedWindow(self.win_id, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.win_id, 1100, 850)
        cv2.setMouseCallback(self.win_id, self.mouse_callback)

        cv2.setWindowTitle(self.win_id, self.get_window_title())
        cv2.imshow(self.win_id, self.display_img)

        while True:
            key = cv2.waitKey(1) & 0xFF

            if key in [13, 32]:  # ENTER / SPACE
                healed_result = self.heal_selection()
                cv2.destroyWindow(self.win_id)
                return healed_result

            elif key == ord('u'):  # UNDO
                if self.shapes_history:
                    self.shapes_history.pop()
                    self.redraw_display()

            elif key == ord('r'):  # RESET
                self.shapes_history.clear()
                self.redraw_display()

            elif key == ord('s'):  # SKIP
                cv2.destroyWindow(self.win_id)
                return self.original.copy()

            elif key == 27:  # ESC
                cv2.destroyAllWindows()
                exit()


def save_image(filepath, img, out_format, quality):
    target_path = filepath.with_suffix(f".{out_format.lower()}")
    fmt = out_format.lower()
    encode_params = []

    if fmt in ["jpg", "jpeg"]:
        encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    elif fmt == "webp":
        encode_params = [int(cv2.IMWRITE_WEBP_QUALITY), quality]
    elif fmt == "png":
        encode_params = [int(cv2.IMWRITE_PNG_COMPRESSION), quality]

    is_success, buffer = cv2.imencode(f".{fmt}", img, encode_params)
    if is_success:
        with open(target_path, "wb") as f:
            f.write(buffer)


if __name__ == "__main__":
    current_dir = Path(__file__).parent.resolve()

    out_format = CONFIG["OUTPUT_FORMAT"].lower()
    quality = CONFIG["QUALITY"]

    output_dir = current_dir / CONFIG["OUTPUT_FOLDER_NAME"]
    output_dir.mkdir(exist_ok=True)

    valid_extensions = {".jpg", ".jpeg", ".png", ".webp"}

    # Resolve relative texture path
    texture_path = (current_dir / Path(CONFIG["TEXTURE_FILENAME"])).resolve()

    image_files = sorted([
        f for f in current_dir.iterdir()
        if f.is_file() and f.suffix.lower() in valid_extensions and f.resolve() != texture_path
    ])

    total_images = len(image_files)

    for idx, file_path in enumerate(image_files, start=1):
        cleaner = InteractiveFingerCleaner(
            file_path,
            current_idx=idx,
            total_count=total_images,
            config=CONFIG
        )
        result = cleaner.run()

        save_image(output_dir / file_path.name, result, out_format, quality)
        print(f"[{idx}/{total_images}] Saved -> {output_dir / file_path.with_suffix('.' + out_format).name}")
