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

if __name__ == "__main__":
    filename = "images/example_image.jpg"
    image = load_image(filename)
    # image = image.resize((1024, 1024))  # Pretty sure this isn't broken

    oldness = OldnessTracker(image.width, image.height)

    # Baseline for the gif
    image.save(f"images/example_0.png")

    num_images = 30

    for i in range(num_images):
        console.log(f"Editing Image {i + 1}")

        # vertices = create_random_polygon(image.width, image.height)
        potential_vertices = [create_random_polygon(image.width, image.height) for _ in range(10)]
        # TODO Shouldn't this be max? It seems to work as min, though...
        vertices = min(potential_vertices, key=lambda v: oldness.average_age_within(v))

        # mask = create_mask_from_vertices(image.width, image.height, vertices)

        oldness.increment_all()
        oldness.zero_polygon_area(vertices)

        resized_image, resized_mask, x_min, y_min, x_max, y_max = zoom_and_resize(image, vertices)
        # console.log("x_min, y_min, x_max, y_max:", x_min, y_min, x_max, y_max)

        # Show the resized image and mask
        # display_image_with_matplotlib(resized_image)
        # display_image_with_matplotlib(resized_mask)

        story_idea, art_idea = get_next_art_prompt(story_so_far, done_amount=f"This is page {i + 1}/{num_images}.")
        story_so_far.append((story_idea, art_idea))
        console.log(f"Story idea: {story_idea}\nArt idea: {art_idea}")

        # inpainted_image = inpaint_image(image, mask)
        inpainted_image = inpaint_image(resized_image, resized_mask,
                                        prompt=art_idea)
        # display_image_with_matplotlib(inpainted_image)
        # inpainted_image.save("images/inpainted_image.jpg")

        inpainted_image = Image.composite(resized_image, inpainted_image, resized_mask)
        # display_image_with_matplotlib(inpainted_image)

        # Resize inpainted_image back to its original size
        # console.log("New size:", x_max - x_min, y_max - y_min)
        # inpainted_image = inpainted_image.resize(((x_max - x_min) // 2, (y_max - y_min) // 2))
        inpainted_image = inpainted_image.resize((x_max - x_min, y_max - y_min))
        # display_image_with_matplotlib(inpainted_image)

        image.paste(inpainted_image, (x_min, y_min))
        # display_image_with_matplotlib(image)

        image.save(f"images/example_{i + 1}.png")

    # Finished
    create_animated_gif('images', 'gifs/story.gif', 600, num_images + 1)
