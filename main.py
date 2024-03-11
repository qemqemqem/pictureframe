# from torchvision.transforms import GaussianBlur
from typing import Tuple

import cv2
import numpy as np
from PIL import Image
from PIL import ImageOps
from rich.console import Console
from rich.markdown import Markdown

from stability_inpainting import inpaint_image
from utils import display_image_with_matplotlib

console = Console(width=160)


def load_image(filename: str) -> Image.Image:
    """Loads an image from the given file."""
    return Image.open(filename)


def create_random_polygon_mask(image_width: int, image_height: int) -> Tuple[Image.Image, np.ndarray]:
    """Creates a random polygon mask as a NumPy array."""
    mask = np.zeros((image_height, image_width), dtype=np.uint8)
    num_vertices = np.random.randint(8, 10)
    # Generate random vertices within image bounds
    vertices = np.random.randint(0, min(image_width, image_height), size=(num_vertices, 2))
    hull = cv2.convexHull(vertices)
    hull = np.squeeze(hull, axis=1)
    cv2.fillPoly(mask, [hull], (255, 255, 255))
    mask = Image.fromarray(mask).convert("L")  # L is for grayscale
    mask = ImageOps.invert(mask)
    return mask, hull


def zoom_and_resize(image_path: str, vertices: np.ndarray, desired_size: Tuple[int, int] = (1024, 1024)) -> Tuple[
    Image.Image, Image.Image]:
    """
    Zoom into the area defined by vertices on the original image, and resize the zoomed image and mask to 1024x1024.

    Args:
    - image_path (str): Path to the image file.
    - vertices (np.ndarray): Array of vertices defining the polygon. Shape should be (num_vertices, 2).
    - desired_size (Tuple[int, int]): The desired size to resize to. Default is (1024, 1024).

    Returns:
    Tuple[Image.Image, Image.Image]: The resized image and mask.
    """
    # Load the original image
    image = load_image(image_path)
    image_width, image_height = image.size

    # Create the mask
    mask = np.zeros((image_height, image_width), dtype=np.uint8)
    cv2.fillPoly(mask, [vertices], (255, 255, 255))

    # Convert mask to PIL Image
    mask = Image.fromarray(mask).convert("L")
    mask = ImageOps.invert(mask)

    # Find bounding box
    x_min, y_min = np.min(vertices, axis=0)
    x_max, y_max = np.max(vertices, axis=0)

    # Crop the image and mask to the bounding box
    cropped_image = image.crop((x_min, y_min, x_max, y_max))
    cropped_mask = mask.crop((x_min, y_min, x_max, y_max))

    # Resize both image and mask
    resized_image = cropped_image.resize(desired_size)  # , Image.ANTIALIAS)
    resized_mask = cropped_mask.resize(desired_size)  # , Image.ANTIALIAS)

    return resized_image, resized_mask


if __name__ == "__main__":
    filename = "images/example_image.jpg"
    image = load_image(filename)
    image = image.resize((1024, 1024))
    mask, vertices = create_random_polygon_mask(image.width, image.height)

    resized_image, resized_mask = zoom_and_resize(filename, vertices)

    # known_good_image = Image.open('images/rocket.png')
    # known_good_mask2 = Image.open('images/rocket-mask.png')

    # Print details of the image and mask
    console.log(Markdown("# Image and mask details"))
    console.log("Image:", image.size, image.mode)
    console.log("Mask:", mask.size, mask.mode)
    console.log("Resized image:", resized_image.size, resized_image.mode)
    console.log("Resized mask:", resized_mask.size, resized_mask.mode)

    # Show the resized image and mask
    display_image_with_matplotlib(resized_image)
    display_image_with_matplotlib(resized_mask)

    # inpainted_image = inpaint_image(image, mask)
    inpainted_image = inpaint_image(resized_image, resized_mask)
    # inpainted_image.show()
    display_image_with_matplotlib(inpainted_image)
    inpainted_image.save("images/inpainted_image.jpg")
