from typing import List

from PIL import Image


def create_animated_gif(directory: str, output_filename: str, duration: int = 500) -> None:
    """
    Creates an animated GIF from a series of JPEG images in a specified directory.

    :param directory: The path to the directory containing the images.
    :param output_filename: The path where the animated GIF should be saved.
    :param duration: The duration each frame should be displayed for, in milliseconds.
    """
    # Build the list of image file paths in the format `example_{i}.jpg` for i in range(10)
    image_files: List[str] = [f"{directory}/example_{i}.png" for i in range(10)]

    # Load the images into a list
    images: List[Image.Image] = [Image.open(image_file) for image_file in image_files]

    # Ensure there's more than one image to animate
    if len(images) > 1:
        # Create the animated GIF
        images[0].save(output_filename, save_all=True, append_images=images[1:], optimize=False, duration=duration,
                       loop=0)
    else:
        print("Need more than one image to create an animation.")


if __name__ == "__main__":
    create_animated_gif('images', 'creatures.gif', 700)
