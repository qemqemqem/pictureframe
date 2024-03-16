# from torchvision.transforms import GaussianBlur

from rich.console import Console

from image_maker import update_image
from movify import create_animated_gif
from old_tracker import OldnessTracker
from read_api_keys import read_api_keys
from utils import load_image

read_api_keys()

console = Console(width=160)

story_so_far = [("Once upon a time there was a castle by the sea, with boats in the harbor and birds in the air",
                 "Image of a castle in a Russian style, by a sea, very peaceful and picturesque, flock of birds in the sky")]


def main():
    filename = "images/example_image.jpg"
    image = load_image(filename)

    oldness = OldnessTracker(image.width, image.height)

    # Baseline for the gif
    image.save(f"images/example_0.png")

    num_images = 10

    for i in range(num_images):
        update_image(i, image, oldness)

    # Finished
    create_animated_gif('images', 'gifs/story.gif', 600, num_images + 1)


if __name__ == "__main__":
    main()
