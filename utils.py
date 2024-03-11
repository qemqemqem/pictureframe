from typing import Tuple

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps
from rich.console import Console

console = Console(width=160)


def display_image_with_matplotlib(img):
    """Display an image using matplotlib in a minimal window."""
    plt.figure(figsize=(10, 6))
    plt.imshow(img, cmap='gray')
    plt.axis('off')
    plt.show()


def zoom_and_resize(image: Image.Image, vertices: np.ndarray, desired_size: Tuple[int, int] = (1024, 1024)) -> Tuple[
    Image.Image, Image.Image, int, int, int, int]:
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

    # # Make the bounding box a square
    # max_width = x_max - x_min
    # max_height = y_max - y_min
    # max_dim = max(max_width, max_height)
    # x_max = x_min + max_dim // 2
    # y_max = y_min + max_dim // 2
    # x_min = x_max - max_dim // 2
    # y_min = y_max - max_dim // 2

    # Crop the image and mask to the bounding box
    cropped_image = image.crop((x_min, y_min, x_max, y_max))
    cropped_mask = mask.crop((x_min, y_min, x_max, y_max))

    console.log("Cropped image:", cropped_image.size, cropped_image.mode)
    console.log("Cropped mask:", cropped_mask.size, cropped_mask.mode)

    # Resize both image and mask
    resized_image = cropped_image.resize(desired_size)  # , Image.ANTIALIAS)
    resized_mask = cropped_mask.resize(desired_size)  # , Image.ANTIALIAS)

    return resized_image, resized_mask, x_min, y_min, x_max, y_max


def create_random_polygon_mask(image_width: int, image_height: int) -> Tuple[Image.Image, np.ndarray]:
    """Creates a random polygon mask as a NumPy array."""
    mask = np.zeros((image_height, image_width), dtype=np.uint8)
    num_vertices = np.random.randint(8, 10)

    vertices_x_center = np.random.randint(0, image_width)
    vertices_y_center = np.random.randint(0, image_height)
    vertices_radius = min(image_width, image_height) // 4

    # Generate the vertices, generating the X values within vertices_radius of the vertices_x_center, and the Y values within vertices_radius of the vertices_y_center
    vertices = np.zeros((num_vertices, 2), dtype=int)
    for i in range(num_vertices):
        # Generate points within a circle logic
        angle = np.random.uniform(0, 2 * np.pi)
        radius = vertices_radius * np.sqrt(np.random.uniform(0, 1))
        x = int(vertices_x_center + radius * np.cos(angle))
        y = int(vertices_y_center + radius * np.sin(angle))
        vertices[i] = [x, y]

    # vertices = np.random.randint(0, min(image_width, image_height), size=(num_vertices, 2))
    hull = cv2.convexHull(vertices)
    hull = np.squeeze(hull, axis=1)
    cv2.fillPoly(mask, [hull], (255, 255, 255))
    mask = Image.fromarray(mask).convert("L")  # L is for grayscale
    mask = ImageOps.invert(mask)
    return mask, hull


def load_image(filename: str) -> Image.Image:
    """Loads an image from the given file."""
    return Image.open(filename)
