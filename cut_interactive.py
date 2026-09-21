import os
import sys
import cv2
import numpy as np

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff')

# Interactive global variables
pts = []
drag_idx = -1
active_img = None
padded_img = None
BASE_WIN_NAME = "Crop Tool"
PAD_RATIO = 0.05  # 20% extra canvas padding on all sides
JPG_QUAL = 100
WEBP_QUAL = 95

# --- SAVE SETTINGS ---
# Options: "JPG", "WEBP_LOSSY", "WEBP_LOSSLESS", "PNG"
SAVE_FORMAT = "JPG"

def order_points(points):
    rect = np.zeros((4, 2), dtype="float32")
    s = points.sum(axis=1)
    rect[0] = points[np.argmin(s)]  # Top-Left
    rect[2] = points[np.argmax(s)]  # Bottom-Right

    diff = np.diff(points, axis=1)
    rect[1] = points[np.argmin(diff)] # Top-Right
    rect[3] = points[np.argmax(diff)] # Bottom-Left
    return rect

def get_page_background_color(image):
    """Samples pixel colors near margins to fill padded canvas."""
    h, w = image.shape[:2]
    sample_tl = image[10:30, 10:30]
    sample_tr = image[10:30, w-30:w-10]
    sample_bl = image[h-30:h-10, 10:30]
    sample_br = image[h-30:h-10, w-30:w-10]

    samples = np.vstack([sample_tl, sample_tr, sample_bl, sample_br])
    mean_color = np.mean(samples, axis=(0, 1)).astype(int)
    return tuple(map(int, mean_color))

def add_canvas_padding(image, pad_ratio=PAD_RATIO):
    """Pads image canvas with 20% extra space filled with sampled page color."""
    h, w = image.shape[:2]
    pad_h = int(h * pad_ratio)
    pad_w = int(w * pad_ratio)

    bg_color = get_page_background_color(image)
    padded = cv2.copyMakeBorder(
        image,
        pad_h, pad_h, pad_w, pad_w,
        cv2.BORDER_CONSTANT,
        value=bg_color
    )
    return padded, pad_w, pad_h

def draw_overlay():
    display = padded_img.copy()
    if len(pts) == 4:
        rect = order_points(np.array(pts, dtype="float32"))
        poly_pts = rect.astype(np.int32).reshape((-1, 1, 2))

        cv2.polylines(display, [poly_pts], isClosed=True, color=(0, 255, 0), thickness=2)

        labels = ["TL", "TR", "BR", "BL"]
        for idx, (x, y) in enumerate(rect.astype(int)):
            cv2.circle(display, (x, y), 8, (0, 0, 255), -1)
            cv2.circle(display, (x, y), 12, (255, 255, 255), 2)
            cv2.putText(display, labels[idx], (x + 12, y + 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    cv2.imshow(BASE_WIN_NAME, display)

def mouse_callback(event, x, y, flags, param):
    global pts, drag_idx

    if len(pts) < 4 or padded_img is None:
        return

    h, w = padded_img.shape[:2]

    if event == cv2.EVENT_LBUTTONDOWN:
        distances = [np.hypot(x - px, y - py) for px, py in pts]
        min_idx = np.argmin(distances)
        if distances[min_idx] < 40:
            drag_idx = min_idx

    elif event == cv2.EVENT_MOUSEMOVE and drag_idx != -1:
        clamped_x = max(0, min(x, w - 1))
        clamped_y = max(0, min(y, h - 1))
        pts[drag_idx] = [clamped_x, clamped_y]
        draw_overlay()

    elif event == cv2.EVENT_LBUTTONUP:
        drag_idx = -1

def crop_and_warp(padded_image, src_pts):
    rect = order_points(src_pts)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    return cv2.warpPerspective(padded_image, M, (maxWidth, maxHeight))

def save_image(out_path_base, cropped_img):
    """Saves output image with configured format parameters."""
    if SAVE_FORMAT == "JPG":
        out_path = out_path_base + ".jpg"
        cv2.imwrite(out_path, cropped_img, [int(cv2.IMWRITE_JPEG_QUALITY), JPG_QUAL])
    elif SAVE_FORMAT == "WEBP_LOSSY":
        out_path = out_path_base + ".webp"
        cv2.imwrite(out_path, cropped_img, [int(cv2.IMWRITE_WEBP_QUALITY), WEBP_QUAL])
    elif SAVE_FORMAT == "WEBP_LOSSLESS":
        out_path = out_path_base + ".webp"
        cv2.imwrite(out_path, cropped_img, [int(cv2.IMWRITE_WEBP_QUALITY), 101])
    elif SAVE_FORMAT == "PNG":
        out_path = out_path_base + ".png"
        cv2.imwrite(out_path, cropped_img, [int(cv2.IMWRITE_PNG_COMPRESSION), 6])
    return out_path


def get_default_box(pw, ph, pad_w, pad_h):
    return [
        [pad_w, pad_h],
        [pw - pad_w, pad_h],
        [pw - pad_w, ph - pad_h],
        [pad_w, ph - pad_h]
    ]

def main():
    global active_img, padded_img, pts

    files = [f for f in os.listdir('.') if f.lower().endswith(IMAGE_EXTENSIONS) and os.path.isfile(f)]
    if not files:
        print("No images found in current folder.")
        return

    output_dir = "cropped_unwarped"
    os.makedirs(output_dir, exist_ok=True)

    cv2.namedWindow(BASE_WIN_NAME, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(BASE_WIN_NAME, mouse_callback)

    print("--- INSTRUCTIONS ---")
    print("1. Drag handles into padded areas to align edges.")
    print("2. Press ENTER / SPACE to save and open next image.")
    print("3. Press 'R' to RESET current box.")
    print("4. Press ESC to skip current image.\n")

    relative_pts = None

    for idx, file_name in enumerate(files):
        image = cv2.imread(file_name)
        if image is None:
            continue

        active_img = image
        padded_img, pad_w, pad_h = add_canvas_padding(image, PAD_RATIO)
        ph, pw = padded_img.shape[:2]

        # UPDATE TOP BAR TITLE WITH IMAGE NAME
        window_title = f"[{idx+1}/{len(files)}] {file_name} | ENTER=Save  R=Reset  ESC=Skip"
        cv2.setWindowTitle(BASE_WIN_NAME, window_title)

        if relative_pts is None:
            pts = get_default_box(pw, ph, pad_w, pad_h)
        else:
            pts = [[int(rx * pw), int(ry * ph)] for rx, ry in relative_pts]

        draw_overlay()

        while True:
            key = cv2.waitKey(20) & 0xFF

            # ENTER or SPACE
            if key in (13, 32):
                relative_pts = [[p[0] / pw, p[1] / ph] for p in pts]
                cropped = crop_and_warp(padded_img, np.array(pts, dtype="float32"))

                base_name = os.path.splitext(file_name)[0]
                out_path_base = os.path.join(output_dir, base_name)
                saved_path = save_image(out_path_base, cropped)

                print(f"[{idx+1}/{len(files)}] Processed & Saved: {saved_path}")
                break

            # RESET ('R')
            elif key in (ord('r'), ord('R')):
                pts = get_default_box(pw, ph, pad_w, pad_h)
                draw_overlay()

            # ESC
            elif key == 27:
                print(f"[{idx+1}/{len(files)}] Skipped: {file_name}")
                break

    cv2.destroyAllWindows()
    print(f"\nDone! Saved images to '{output_dir}/'.")

if __name__ == "__main__":
    main()
