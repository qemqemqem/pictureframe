from typing import Tuple
import numpy as np
from PIL import Image, ImageDraw
from scipy.spatial import Voronoi, cKDTree
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class ImageData:
    path: str
    array: np.ndarray = None
    age_array: np.ndarray = None
    size: Tuple[int, int] = (0, 0)
    voronoi: Voronoi = None

    def load_image(self):
        """Load an image and update the object with its array and size."""
        with Image.open(self.path) as img:
            self.array = np.array(img)
            self.size = img.size

    def create_age_array(self):
        """Initialize the age array for the image with random values."""
        self.age_array = np.random.randint(0, 256, self.size)

    def generate_voronoi_cells(self, num_points: int):
        """Generate random points and create a Voronoi diagram based on these points, then store it in the object."""
        points = np.random.rand(num_points, 2) * [self.size[0], self.size[1]]
        self.voronoi = Voronoi(points)

def calculate_average_ages(image_data: ImageData) -> np.ndarray:
    """Calculate the average age of pixels within each Voronoi cell."""
    tree = cKDTree(image_data.voronoi.points)
    sum_ages = np.zeros(len(image_data.voronoi.points))
    count = np.zeros(len(image_data.voronoi.points))

    gap_size = 100 # Skip most pixels, for speed

    for x in range(image_data.age_array.shape[1], gap_size):  # Width
        for y in range(image_data.age_array.shape[0], gap_size):  # Height
            dist, point_index = tree.query([x, y])
            sum_ages[point_index] += image_data.age_array[y, x]
            count[point_index] += 1

    count[count == 0] = 1
    average_ages = sum_ages / count
    return average_ages

def select_cell_with_highest_average_age(image_data: ImageData, average_ages: np.ndarray) -> int:
    """Select the Voronoi cell with the highest average age."""
    return np.argmax(average_ages)

def display_selected_voronoi_cell(image_data: ImageData, cell_index: int) -> Image:
    """Display the selected Voronoi cell as a black and white image."""
    region = image_data.voronoi.regions[image_data.voronoi.point_region[cell_index]]
    img = Image.new('L', image_data.size, "white")
    draw = ImageDraw.Draw(img)

    if -1 not in region:
        polygon = [(image_data.voronoi.vertices[i][0], image_data.voronoi.vertices[i][1]) for i in region]
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
    image_data.create_age_array()
    image_data.generate_voronoi_cells(num_points=100)

    # For displaying a random Voronoi cell, you'll need to modify `display_random_voronoi_cell` to work directly with `ImageData` as well.

    average_ages = calculate_average_ages(image_data)
    highest_avg_age_cell_index = select_cell_with_highest_average_age(image_data, average_ages)
    img = display_selected_voronoi_cell(image_data, highest_avg_age_cell_index)
    display_image_with_matplotlib(img)
