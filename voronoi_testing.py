from typing import Tuple
import numpy as np
from PIL import Image, ImageDraw
from scipy.spatial import Voronoi
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class ImageData:
    path: str
    array: np.ndarray = None
    size: Tuple[int, int] = (0, 0)
    voronoi: Voronoi = None

    def load_image(self):
        """Load an image and update the object with its array and size."""
        with Image.open(self.path) as img:
            self.array = np.array(img)
            self.size = img.size

def generate_voronoi_cells(image_data: ImageData, num_points: int) -> Voronoi:
    """Generate random points and create a Voronoi diagram based on these points, then store it in the image data."""
    height, width = image_data.size
    points = np.random.rand(num_points, 2) * [width, height]
    image_data.voronoi = Voronoi(points)
    return image_data.voronoi

def display_random_voronoi_cell(vor: Voronoi, image_size: Tuple[int, int]) -> Image:
    """Display a random Voronoi cell as a black and white image."""
    region_index = np.random.randint(0, len(vor.point_region))
    region = vor.regions[vor.point_region[region_index]]

    if -1 in region:
        print("Selected region touches the border, choosing another.")
        return display_random_voronoi_cell(vor, image_size)

    img = Image.new('L', image_size, "white")
    draw = ImageDraw.Draw(img)
    polygon = [(vor.vertices[i][0], vor.vertices[i][1]) for i in region if i != -1]
    draw.polygon(polygon, outline="black", fill="black")

    return img

def display_image_with_matplotlib(img):
    """Display an image using matplotlib in a minimal window."""
    plt.figure(figsize=(10, 6))
    plt.imshow(img, cmap='gray')
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    image_path = 'images/test_image.jpg'
    image_data = ImageData(path=image_path)
    image_data.load_image()

    vor = generate_voronoi_cells(image_data, num_points=100)
    img = display_random_voronoi_cell(vor, image_data.size)
    display_image_with_matplotlib(img)
