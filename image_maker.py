import time
from typing import Optional

from PIL import Image
from rich.console import Console

from llm_master import get_next_art_prompt_from_audio
# from dev_make_gif import story_so_far
from old_tracker import OldnessTracker
from read_api_keys import read_api_keys
from stability_inpainting import inpaint_image
from utils import create_random_polygon, zoom_and_resize

read_api_keys()

console = Console()


def update_image(i, image, oldness, audio: Optional[str] = None,
                 previous_context: str = "A wizard playing poker in a realistic style") -> str:
    console.log(f"Editing Image {i + 1}")

    potential_vertices = [create_random_polygon(image.width, image.height) for _ in range(10)]
    # TODO Shouldn't this be max? It seems to work as min, though...
    vertices = min(potential_vertices, key=lambda v: oldness.average_age_within(v))

    oldness.increment_all()
    oldness.zero_polygon_area(vertices)
    resized_image, resized_mask, x_min, y_min, x_max, y_max = zoom_and_resize(image, vertices)

    assert audio is not None, "Need to implement"
    # if art_idea is None:
    #     story_idea, art_idea = get_next_art_prompt(story_so_far)
    #     story_so_far.append((story_idea, art_idea))
    #     console.log(f"Story idea: {story_idea}\nArt idea: {art_idea}")

    # TODO Track previous art
    art_idea = get_next_art_prompt_from_audio(audio, previous_context)

    with open("art_log.txt", 'a') as f:
        f.write(f"Art {i}: {time.time()}\n")
        f.write(f"Audio: {audio}\n")
        f.write(f"Art Idea: {art_idea}\n\n")

    # TODO For post
    save_intermediate = True
    # [] Save resized_image to file
    if save_intermediate:
        resized_image.save(f"images/intermediate_{i + 1}.png")
    # [] Save resized_mask to file
    if save_intermediate:
        resized_mask.save(f"images/mask_{i + 1}.png")

    inpainted_image = inpaint_image(resized_image, resized_mask, prompt=art_idea)
    # [] Save inpainted_image to file
    if save_intermediate:
        inpainted_image.save(f"images/inpainted_{i + 1}.png")
    inpainted_image = Image.composite(resized_image, inpainted_image, resized_mask)
    inpainted_image = inpainted_image.resize((x_max - x_min, y_max - y_min))
    image.paste(inpainted_image, (x_min, y_min))
    # [] Save inpainted_image to file again
    if save_intermediate:
        image.save(f"images/inpainted_final_{i + 1}.png")

    save_loc = f"images/example_{i + 1}.png"
    image.save(save_loc)

    return save_loc


def update_image_in_background(starting_image_file: str) -> None:
    image = Image.open(starting_image_file)

    oldness = OldnessTracker(image.width, image.height)

    image_num = 0
    while True:
        with open('comms_files/image_progress.txt', 'r') as file:
            instructions = file.read()
            if instructions.strip().startswith("ready"):
                time.sleep(1)
                continue
            else:
                audio = instructions

        console.log(f"Generating with art idea: {audio}")
        saved_file_loc = update_image(image_num, image, oldness, audio)

        # TODO Record that the image has been updated

        image_num += 1

        with open("comms_files/control.txt", 'r') as f:
            if f.read() == 'stop':
                break

        with open('comms_files/image_progress.txt', 'w') as file:
            file.write(f"ready {saved_file_loc}")

    console.log("Stopping image creation.")


# This isn't just for development, it's also important because app.py runs this file as a subprocess.
if __name__ == "__main__":
    # asyncio.run(main())
    update_image_in_background("images/start_image.png")
