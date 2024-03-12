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


def adjust_and_maintain_square_bbox(image_size: Tuple[int, int], vertices: np.ndarray, buffer: int) -> Tuple[
    int, int, int, int]:
    """
    Adjusts a bounding box to make it square, adds a buffer, pushes it into the image if it exceeds bounds,
    and ensures it remains square by reducing the buffer if necessary.

    Args:
    - image_size: A tuple containing the width and height of the image.
    - vertices: A NumPy array of shape (N, 2) containing the vertices of the bounding box.
    - buffer: An integer representing the buffer size to add around the bounding box.

    Returns:
    - A tuple of integers (x_min, y_min, x_max, y_max) representing the adjusted bounding box.
    """
    image_width, image_height = image_size

    # Find the original bounding box
    x_min, y_min = np.min(vertices, axis=0)
    x_max, y_max = np.max(vertices, axis=0)
    # print("Original Bounding Box:", x_min, y_min, x_max, y_max)

    # Determine the size of the square bounding box, including the initial buffer
    initial_bbox_size = max(x_max - x_min, y_max - y_min) + 2 * buffer

    # If initial_bbox_size exceeds either the width or height of the image, set it to the minimum of the two
    initial_bbox_size = min(initial_bbox_size, image_width, image_height)

    # Calculate the center of the original bounding box
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2

    # Adjust center if the bounding box exceeds the image bounds
    half_size = initial_bbox_size // 2
    center_x = max(half_size, min(center_x, image_width - half_size))
    center_y = max(half_size, min(center_y, image_height - half_size))

    # Recalculate the bounding box with the adjusted center
    x_min = int(center_x - half_size)
    y_min = int(center_y - half_size)
    x_max = int(center_x + half_size)
    y_max = int(center_y + half_size)

    # Ensure the bounding box does not exceed image boundaries
    x_min = max(0, x_min)
    y_min = max(0, y_min)
    x_max = min(image_width, x_max)
    y_max = min(image_height, y_max)

    return x_min, y_min, x_max, y_max


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
    buffer = min(image_width, image_height) // 8  # PARAMETER
    x_min, y_min, x_max, y_max = adjust_and_maintain_square_bbox((image_width, image_height), vertices, buffer)
    # print("Bounding box:", x_min, y_min, x_max, y_max)

    # Crop the image and mask to the bounding box
    cropped_image = image.crop((x_min, y_min, x_max, y_max))
    cropped_mask = mask.crop((x_min, y_min, x_max, y_max))

    # console.log("Cropped image:", cropped_image.size, cropped_image.mode)
    # console.log("Cropped mask:", cropped_mask.size, cropped_mask.mode)

    # Resize both image and mask
    resized_image = cropped_image.resize(desired_size)  # , Image.ANTIALIAS)
    resized_mask = cropped_mask.resize(desired_size)  # , Image.ANTIALIAS)

    return resized_image, resized_mask, x_min, y_min, x_max, y_max


def create_random_polygon(image_width: int, image_height: int) -> np.ndarray:
    """Creates a random polygon mask as a NumPy array."""
    num_vertices = np.random.randint(8, 20)

    vertices_x_center = np.random.randint(0, image_width)
    vertices_y_center = np.random.randint(0, image_height)
    vertices_radius = min(image_width, image_height) // 3  # PARAMETER

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

    return hull


def create_mask_from_vertices(image_width, image_height, vertices: np.ndarray) -> Image.Image:
    mask = np.zeros((image_height, image_width), dtype=np.uint8)
    cv2.fillPoly(mask, [vertices], (255, 255, 255))
    mask = Image.fromarray(mask).convert("L")  # L is for grayscale
    mask = ImageOps.invert(mask)
    return mask


def load_image(filename: str) -> Image.Image:
    """Loads an image from the given file."""
    return Image.open(filename)
