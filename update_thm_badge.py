import requests
import base64
from html2image import Html2Image
import numpy as np
from PIL import Image


def remove_transparent_background_and_save(input_path, output_path):
    # Read input image, and convert to NumPy array.
    img = np.array(Image.open(input_path))  # img is 1080 rows by 1920 cols and 4 color channels, the 4'th channel is alpha.

    # Find indices of non-transparent pixels (indices where alpha channel value is above zero).
    idx = np.where(img[:, :, 3] > 0)

    # Get minimum and maximum index in both axes (top left corner and bottom right corner)
    x0, y0, x1, y1 = idx[1].min(), idx[0].min(), idx[1].max(), idx[0].max()

    # Crop rectangle and convert to Image
    out = Image.fromarray(img[y0:y1+1, x0:x1+1, :])

    # Save the result (RGBA color format).
    out.save(output_path)


if __name__ == "__main__":
    image_path = "https://tryhackme.com/badge/1309194"
    img_data = requests.get("https://tryhackme.com/badge/1309194").content
    img_data = img_data.decode("utf-8")
    img_data = img_data.split('\"')[1]
    img_data = img_data.encode("utf-8")

    hti = Html2Image()
    decoded_html = base64.b64decode(img_data)
    decoded_html = decoded_html.decode("utf-8")
    hti.screenshot(html_str=decoded_html, save_as='thm_profile_pic_screenshot.png')
    remove_transparent_background_and_save('thm_profile_pic_screenshot.png', './assets/thm_propic.png')
