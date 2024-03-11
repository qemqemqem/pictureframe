# from torchvision.transforms import GaussianBlur

from rich.console import Console

from stability_inpainting import inpaint_image
from utils import zoom_and_resize, create_random_polygon_mask, load_image

console = Console(width=160)

if __name__ == "__main__":
    filename = "images/example_image.jpg"
    image = load_image(filename)
    image = image.resize((1024, 1024))

    # Baseline for the gif
    image.save(f"images/example_0.jpg")

    for i in range(10):
        console.log(f"Editing Image {i + 1}")
        mask, vertices = create_random_polygon_mask(image.width, image.height)

        resized_image, resized_mask, x_min, y_min, x_max, y_max = zoom_and_resize(image, vertices)
        # console.log("x_min, y_min, x_max, y_max:", x_min, y_min, x_max, y_max)

        # Show the resized image and mask
        # display_image_with_matplotlib(resized_image)
        # display_image_with_matplotlib(resized_mask)

        # inpainted_image = inpaint_image(image, mask)
        inpainted_image = inpaint_image(resized_image, resized_mask)
        # display_image_with_matplotlib(inpainted_image)
        inpainted_image.save("images/inpainted_image.jpg")

        # Resize inpainted_image back to its original size
        # console.log("New size:", x_max - x_min, y_max - y_min)
        # inpainted_image = inpainted_image.resize(((x_max - x_min) // 2, (y_max - y_min) // 2))
        inpainted_image = inpainted_image.resize((x_max - x_min, y_max - y_min))
        # display_image_with_matplotlib(inpainted_image)

        # display_image_with_matplotlib(image)
        image.paste(inpainted_image, (x_min, y_min))
        # display_image_with_matplotlib(image)

        image.save(f"images/example_{i + 1}.jpg")
