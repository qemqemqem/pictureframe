import asyncio
import subprocess

import pygame
from rich.console import Console

from gui_stuff import GuiInfo
from read_api_keys import read_api_keys

read_api_keys()

console = Console()

# Initialize Pygame
pygame.init()


# Main function to run the game loop
async def main():
    gui_info = GuiInfo()

    # Run audio in the background
    # You might want to use a different python here idk
    with open('comms_files/control.txt', 'w') as file:
        file.write('record')
    subprocess.Popen(["venv/bin/python", "audiophile.py"])
    most_recent_transcription = ""
    transcription_history = []
    transcriptions_not_yet_imaged = []

    # Draw images in the background
    subprocess.Popen(["venv/bin/python", "image_maker.py"])

    background_image_path = 'images/example_image.jpg'
    background_image = gui_info.load_image(background_image_path,
                                           (gui_info.infoObject.current_w, gui_info.infoObject.current_h))
    gui_info.background_image = background_image
    gui_info.screen.blit(gui_info.background_image, (0, 0))

    # i = 1
    while gui_info.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gui_info.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gui_info.running = False
                # elif event.key == pygame.K_SPACE:
                #     gui_info.initiate_fade(f'images/example_{i}.png')
                #     i += 1

        gui_info.fade_and_show()

        # Read the transcription file
        with open('comms_files/transcription.txt', 'r') as file:
            recent_transcriptions = [l.strip() for l in file.readlines()]
        current_transcription = " ".join(recent_transcriptions)
        if current_transcription != most_recent_transcription and current_transcription.strip() != "":
            most_recent_transcription = current_transcription
            transcription_history.append(current_transcription)
            transcriptions_not_yet_imaged.append(current_transcription)
            with open('comms_files/transcription.txt', 'w') as file:
                file.write('')  # Clear the file

        # Display text
        gui_info.display_text_with_background(most_recent_transcription,
                                              (gui_info.infoObject.current_w // 2, gui_info.infoObject.current_h - 50),
                                              font_size=50)

        # Commission an image
        with open('comms_files/image_progress.txt', 'r') as file:
            image_progress = file.read().strip()

        if image_progress.strip().startswith("ready"):
            with open('comms_files/image_progress.txt', 'w') as file:
                file.write(" ".join(transcriptions_not_yet_imaged))
            transcriptions_not_yet_imaged = []
            image_file = image_progress.strip()[5:].strip()
            if image_file != "":
                console.print(f"Fading image file: {image_file}")
                gui_info.initiate_fade(image_file)

        pygame.display.flip()

        await asyncio.sleep(0)  # Yield control

    with open('comms_files/control.txt', 'w') as file:
        # This stops the background audio and image processes
        file.write('stop')

    pygame.quit()


if __name__ == '__main__':
    asyncio.run(main())
