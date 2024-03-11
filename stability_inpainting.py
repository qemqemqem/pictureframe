import io
import os
from typing import List

import numpy as np
import requests
from PIL import Image, ImageOps
from stability_sdk import client
from PIL import Image
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
# from torchvision.transforms import GaussianBlur
import cv2
import rich
from rich.markdown import Markdown
from rich.console import Console

from utils import display_image_with_matplotlib

console = Console(width=160)

# os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

api_host = os.getenv('API_HOST', 'https://api.stability.ai')
url = f"{api_host}/v1/engines/list"

api_key = os.getenv("STABILITY_KEY")
if api_key is None:
    raise Exception("Missing Stability API key.")

response = requests.get(url, headers={
    "Authorization": f"Bearer {api_key}"
})

if response.status_code != 200:
    raise Exception("Non-200 response: " + str(response.text))

# Do something with the payload...
payload = response.json()
console.log(Markdown("# Details about the API"))
console.log(payload)

# Create a Stability client instance
stability_api = client.StabilityInference(
    key=os.environ["STABILITY_KEY"],
    verbose=True,  # Print debug messages.
    engine="stable-diffusion-xl-1024-v0-9",
)

def load_image(filename: str) -> Image.Image:
    """Loads an image from the given file."""
    return Image.open(filename)

def create_random_polygon_mask(image_width: int, image_height: int) -> np.ndarray:
    """Creates a random polygon mask as a NumPy array."""
    mask = np.zeros((image_height, image_width), dtype=np.uint8)
    num_vertices = np.random.randint(3, 8)  # Choose a random number of vertices
    # Generate random vertices within image bounds
    vertices = np.random.randint(0, min(image_width, image_height), size=(num_vertices, 2))
    # Fill the polygon using OpenCV or a similar library (not shown for brevity)
    cv2.fillPoly(mask, [vertices], (255, 255, 255))  # Assuming OpenCV is used
    return mask

def inpaint_image(image: Image.Image, mask: Image.Image) -> Image.Image:
    """Inpaints the masked region of the image using the Stability API."""

    # Print details of the image and mask
    console.log(Markdown("# Image and mask details"))
    console.log("Image:", image.size, image.mode)
    console.log("Mask:", mask.size, mask.mode)

    answers = stability_api.generate(
        prompt="Photorealistic futuristic dragon",
        init_image=image,
        mask_image=mask,
    )
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                print("Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img2 = Image.open(io.BytesIO(artifact.binary))
                return img2
    console.log("No image!", log_locals=True)


if __name__ == "__main__":
    filename = "images/example_image.jpg"
    # image = load_image(filename)
    # mask = create_random_polygon_mask(image.width, image.height)
    # mask_image = Image.fromarray(mask).convert("RGB")  # Convert to grayscale (L mode)
    # # Invert the mask (optional, depends on Stability API usage)
    # mask_image = ImageOps.invert(mask_image)  # May be needed based on API behavior
    # # Display the mask_image
    # mask_image.show()

    image = Image.open('images/rocket.png')
    mask = Image.open('images/rocket-mask.png')

    inpainted_image = inpaint_image(image, mask)
    # inpainted_image.show()
    display_image_with_matplotlib(inpainted_image)
    inpainted_image.save("images/inpainted_image.jpg")