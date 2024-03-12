import cv2
import numpy as np


class OldnessTracker:
    def __init__(self, image_width: int, image_height: int) -> None:
        # Define the subsampling factor.
        self.subsample_factor = 10
        # Calculate the dimensions of the subsampled grid.
        self.grid_width = image_width // self.subsample_factor
        self.grid_height = image_height // self.subsample_factor
        self.grid = np.random.randint(0, 2, (self.grid_height, self.grid_width), dtype=np.int32)

    def zero_polygon_area(self, polygon: np.ndarray) -> None:
        # Ensure the polygon is in the correct format and dtype.
        if polygon.ndim != 2 or polygon.shape[1] != 2 or polygon.dtype != np.int32:
            raise ValueError("Polygon must be a 2D ndarray with shape (?, 2) and dtype np.int32.")

        # Create an empty mask with the same dimensions as the grid.
        mask = np.zeros((self.grid_height, self.grid_width), dtype=np.uint8)
        # Adjust polygon points to the subsampled grid.
        subsampled_polygon = (polygon // self.subsample_factor).astype(np.int32)
        # Fill the polygon in the mask.
        cv2.fillPoly(mask, [subsampled_polygon], 1)
        # Increment the grid values where the mask is filled.
        self.grid[mask == 1] += 1

    def increment_all(self, increment_size: int = 1) -> None:
        # Increment all grid values by a given size.
        self.grid += increment_size
        # Cap all ages at 255.
        self.grid[self.grid > 255] = 255

    def average_age_within(self, polygon: np.ndarray) -> float:
        # Ensure the polygon is in the correct format and dtype.
        if polygon.ndim != 2 or polygon.shape[1] != 2 or polygon.dtype != np.int32:
            raise ValueError("Polygon must be a 2D ndarray with shape (?, 2) and dtype np.int32.")

        # Create an empty mask with the same dimensions as the grid.
        mask = np.zeros((self.grid_height, self.grid_width), dtype=np.uint8)
        # Adjust polygon points to the subsampled grid.
        subsampled_polygon = (polygon // self.subsample_factor).astype(np.int32)
        # Fill the polygon in the mask.
        cv2.fillPoly(mask, [subsampled_polygon], 1)
        # Compute the average value of the grid cells within the polygon.
        if np.sum(mask) == 0:  # Avoid division by zero if the polygon does not cover any grid cells.
            return 0.0
        return np.sum(self.grid[mask == 1]) / np.sum(mask)
