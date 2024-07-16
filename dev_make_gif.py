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
    ("Once upon a time there was the void, filled only with chaos and potential.",
     "Image of outer space, full of stars and galaxies"),
]


def main():
    filename = "images/example_image.jpg"
    image = load_image(filename)

    oldness = OldnessTracker(image.width, image.height)

    # Baseline for the gif
    image.save(f"images/neutral_0.png")

    num_images = 20
    num_generated = 0

    try:
        for i in range(num_images):
            # Get next art prompt
            next_prompt = get_next_art_prompt(story_so_far)
            story_so_far.append(next_prompt)
            art_description = next_prompt[1]

            previous_context = "\n".join([story[0] for story in story_so_far])

            save_loc = update_image(i, image, oldness, art_description, previous_context)

            print(f"Saved image {i + 1} to {save_loc}")
            num_generated = i + 1
    except KeyboardInterrupt:
        print("Interrupted, creating gif anyway...")

    # Finished
    save_name = "gifs/space.gif"
    print(f"Creating gif... at {save_name}")
    create_animated_gif('images', save_name, 600, num_generated + 1)


if __name__ == "__main__":
    main()
