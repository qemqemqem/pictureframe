# from torchvision.transforms import GaussianBlur

from rich.console import Console

from stability_inpainting import inpaint_image
from utils import display_image_with_matplotlib, zoom_and_resize, create_random_polygon_mask, load_image

console = Console(width=160)

if __name__ == "__main__":
    filename = "images/example_image.jpg"
    image = load_image(filename)
    image = image.resize((1024, 1024))
    mask, vertices = create_random_polygon_mask(image.width, image.height)

    resized_image, resized_mask, x_min, y_min, x_max, y_max = zoom_and_resize(image, vertices)
    console.log("x_min, y_min, x_max, y_max:", x_min, y_min, x_max, y_max)

    # known_good_image = Image.open('images/rocket.png')
    # known_good_mask2 = Image.open('images/rocket-mask.png')

    # Print details of the image and mask
    # console.log(Markdown("# Image and mask details"))
    # console.log("Image:", image.size, image.mode)
    # console.log("Mask:", mask.size, mask.mode)
    # console.log("Resized image:", resized_image.size, resized_image.mode)
    # console.log("Resized mask:", resized_mask.size, resized_mask.mode)

    # Show the resized image and mask
    display_image_with_matplotlib(resized_image)
    display_image_with_matplotlib(resized_mask)

    # inpainted_image = inpaint_image(image, mask)
    inpainted_image = inpaint_image(resized_image, resized_mask)
    display_image_with_matplotlib(inpainted_image)
    inpainted_image.save("images/inpainted_image.jpg")

    # Resize inpainted_image back to its original size
    console.log("New size:", x_max - x_min, y_max - y_min)
    # inpainted_image = inpainted_image.resize(((x_max - x_min) // 2, (y_max - y_min) // 2))
    inpainted_image = inpainted_image.resize((x_max - x_min, y_max - y_min))
    display_image_with_matplotlib(inpainted_image)

    display_image_with_matplotlib(image)
    image.paste(inpainted_image, (x_min, y_min))
    display_image_with_matplotlib(image)
