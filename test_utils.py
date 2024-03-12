import numpy as np
import pytest

from utils import adjust_and_maintain_square_bbox


@pytest.mark.parametrize(
    "image_size, vertices, buffer, expected_output",
    [
        # Simple case with no adjustments needed
        ((100, 100), np.array([[10, 10], [20, 20]]), 10, (0, 0, 30, 30)),
        # Pushed out from side
        ((100, 100), np.array([[10, 10], [20, 20]]), 20, (0, 0, 50, 50)),
        # Buffer exceeds image dimensions
        ((100, 100), np.array([[10, 10], [80, 80]]), 30, (0, 0, 100, 100)),
        # Square bounding box exceeds image dimensions
        ((100, 100), np.array([[10, 10], [90, 90]]), 20, (0, 0, 100, 100)),
        # Bounding box near the edge of the image
        ((100, 100), np.array([[80, 80], [90, 90]]), 10, (70, 70, 100, 100)),
        # Bounding box corner case
        ((100, 100), np.array([[0, 0], [10, 10]]), 5, (0, 0, 20, 20)),
    ],
)
def test_adjust_and_maintain_square_bbox(
        image_size, vertices, buffer, expected_output
):
    result = adjust_and_maintain_square_bbox(image_size, vertices, buffer)
    assert result == expected_output

    assert result[2] - result[0] == result[3] - result[1]  # Square
