import sys, cv2, numpy as np
from PIL import Image
from rembg import remove, new_session

def prep(in_path, out_path="source-prepped.png"):
    with open(in_path, "rb") as f:
        input_bytes = f.read()
    session = new_session("u2net_human_seg")  # lighter model, tuned for people
    out_bytes = remove(input_bytes, session=session)  # remove bg -> RGBA
    img = Image.open(__import__("io").BytesIO(out_bytes)).convert("RGBA")

    # composite onto pure white
    bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    bg.paste(img, (0, 0), img)
    rgb = bg.convert("RGB")

    # grayscale + CLAHE for real contrast
    arr = cv2.cvtColor(np.array(rgb), cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    arr = clahe.apply(arr)

    Image.fromarray(arr).save(out_path)
    print("wrote", out_path)

if __name__ == "__main__":
    prep(sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg")
