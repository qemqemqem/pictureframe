# from torchvision.transforms import GaussianBlur

from rich.console import Console

from image_maker import update_image
from llm_master import get_next_art_prompt
from movify import create_animated_gif
from old_tracker import OldnessTracker
from read_api_keys import read_api_keys
from utils import load_image

read_api_keys()

console = Console(width=160)

story_so_far = [
    ("Once upon a time there was a castle by the sea, with boats in the harbor and birds in the air",
     "Image of a castle in a Russian style, by a sea, very peaceful and picturesque, flock of birds in the sky"),
]


def main():
    filename = "images/example_image.jpg"
    image = load_image(filename)

    oldness = OldnessTracker(image.width, image.height)

    # Baseline for the gif
    image.save(f"images/neutral_0.png")

    num_images = 20

    for i in range(num_images):
        # Get next art prompt
        next_prompt = get_next_art_prompt(story_so_far)
        story_so_far.append(next_prompt)
        art_description = next_prompt[1]

        save_loc = update_image(i, image, oldness, art_description)

        print(f"Saved image {i + 1} to {save_loc}")

    # Finished
    save_name = "gifs/neutral.gif"
    print(f"Creating gif... at {save_name}")
    create_animated_gif('images', save_name, 600, num_images + 1)


if __name__ == "__main__":
    main()
