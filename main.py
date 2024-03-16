# from torchvision.transforms import GaussianBlur

from PIL import Image
from rich.console import Console

from llm_master import get_next_art_prompt
from movify import create_animated_gif
from old_tracker import OldnessTracker
from stability_inpainting import inpaint_image
from utils import zoom_and_resize, load_image, create_random_polygon

console = Console(width=160)

story_so_far = [("Once upon a time there was a castle by the sea, with boats in the harbor and birds in the air",
                 "Image of a castle in a Russian style, by a sea, very peaceful and picturesque, flock of birds in the sky")]


def main():
    filename = "images/example_image.jpg"
    image = load_image(filename)

    oldness = OldnessTracker(image.width, image.height)

    # Baseline for the gif
    image.save(f"images/example_0.png")

    num_images = 4

    for i in range(num_images):
        update_image(i, image, oldness)

    # Finished
    create_animated_gif('images', 'gifs/story.gif', 600, num_images + 1)


def update_image(i, image, oldness):
    console.log(f"Editing Image {i + 1}")

    potential_vertices = [create_random_polygon(image.width, image.height) for _ in range(10)]
    # TODO Shouldn't this be max? It seems to work as min, though...
    vertices = min(potential_vertices, key=lambda v: oldness.average_age_within(v))

    oldness.increment_all()
    oldness.zero_polygon_area(vertices)
    resized_image, resized_mask, x_min, y_min, x_max, y_max = zoom_and_resize(image, vertices)

    story_idea, art_idea = get_next_art_prompt(story_so_far)
    story_so_far.append((story_idea, art_idea))
    console.log(f"Story idea: {story_idea}\nArt idea: {art_idea}")

    inpainted_image = inpaint_image(resized_image, resized_mask, prompt=art_idea)
    inpainted_image = Image.composite(resized_image, inpainted_image, resized_mask)
    inpainted_image = inpainted_image.resize((x_max - x_min, y_max - y_min))
    image.paste(inpainted_image, (x_min, y_min))

    image.save(f"images/example_{i + 1}.png")


if __name__ == "__main__":
    main()

    #call tool to do image segmentation
    #or at least do segmentation on objects, and colors 

    '''
    1. get segmented image
    2. only replace areas of segmentation that haven't been replaced
    3. Try to make segmentation
    '''