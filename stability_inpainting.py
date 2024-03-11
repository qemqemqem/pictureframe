import io
import os

import requests
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from PIL import Image
from rich.console import Console
# from torchvision.transforms import GaussianBlur
from stability_sdk import client

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
# console.log(Markdown("# Details about the API"))
# console.log(payload)

# Create a Stability client instance
stability_api = client.StabilityInference(
    key=os.environ["STABILITY_KEY"],
    verbose=True,  # Print debug messages.
    engine="stable-diffusion-xl-1024-v0-9",
)


def inpaint_image(image: Image.Image, mask: Image.Image) -> Image.Image:
    """Inpaints the masked region of the image using the Stability API."""

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
