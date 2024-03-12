# from torchvision.transforms import GaussianBlur

from PIL import Image
from rich.console import Console

from old_tracker import OldnessTracker
from stability_inpainting import inpaint_image
from utils import zoom_and_resize, load_image, create_mask_from_vertices, create_random_polygon

console = Console(width=160)

if __name__ == "__main__":
    filename = "images/example_image.jpg"
    image = load_image(filename)
    # image = image.resize((1024, 1024))  # Pretty sure this isn't broken

    oldness = OldnessTracker(image.width, image.height)

    # Baseline for the gif
    image.save(f"images/example_0.png")

    for i in range(10):
        console.log(f"Editing Image {i + 1}")

        # TODO Use these vertices to update oldness in an array
        # TODO Generate 10 different vertices
        # TODO Use a function to rank the vertices from oldness
        # TODO Split up mask generation because it's slow
        # vertices = create_random_polygon(image.width, image.height)
        potential_vertices = [create_random_polygon(image.width, image.height) for _ in range(10)]
        vertices = min(potential_vertices, key=lambda v: oldness.average_age_within(v))

        mask = create_mask_from_vertices(image.width, image.height, vertices)

        oldness.increment_all()
        oldness.zero_polygon_area(vertices)

        resized_image, resized_mask, x_min, y_min, x_max, y_max = zoom_and_resize(image, vertices)
        # console.log("x_min, y_min, x_max, y_max:", x_min, y_min, x_max, y_max)

        # Show the resized image and mask
        # display_image_with_matplotlib(resized_image)
        # display_image_with_matplotlib(resized_mask)

        # inpainted_image = inpaint_image(image, mask)
        inpainted_image = inpaint_image(resized_image, resized_mask,
                                        prompt="the scene contains a fantastic animal, inspired by medieval illuminations, Renaissance watercolor style")
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
