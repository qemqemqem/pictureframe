import asyncio
import subprocess

import pygame

from gui_stuff import GuiInfo
from read_api_keys import read_api_keys

read_api_keys()

# Initialize Pygame
pygame.init()


# Main function to run the game loop
async def main():
    gui_info = GuiInfo()

    # transcriber = AudioTranscriber()
    # current_transcription = "This is a story all about how, my world got flip turned upside down"

    # You might want to use a different python here idk
    with open('comms_files/audio_control.txt', 'w') as file:
        file.write('record')
    subprocess.Popen(["venv/bin/python", "audiophile.py"])
    most_recent_transcription = ""
    transcription_history = []

    # Start the transcribing task in the background
    # task = asyncio.create_task(transcriber.start_transcribing())
    # loop = asyncio.get_running_loop()
    #
    # recv_queue = multiprocessing.Queue()
    # with concurrent.futures.ProcessPoolExecutor() as pool:
    #     await loop.run_in_executor(pool, run_in_process, transcriber.start_transcribing, recv_queue)

    background_image_path = 'images/example_image.jpg'
    background_image = gui_info.load_image(background_image_path,
                                           (gui_info.infoObject.current_w, gui_info.infoObject.current_h))
    gui_info.background_image = background_image
    gui_info.screen.blit(gui_info.background_image, (0, 0))

    i = 1
    while gui_info.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gui_info.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gui_info.running = False
                elif event.key == pygame.K_SPACE:
                    gui_info.initiate_fade(f'images/example_{i}.png')
                    i += 1

        gui_info.fade_and_show()

        # Display text
        with open('comms_files/transcription.txt', 'r') as file:
            recent_transcriptions = [l.strip() for l in file.readlines()]
        current_transcription = "\n".join(recent_transcriptions)
        if current_transcription != most_recent_transcription and current_transcription.strip() != "":
            most_recent_transcription = current_transcription
            transcription_history.append(current_transcription)
        gui_info.display_text_with_background(most_recent_transcription,
                                              (gui_info.infoObject.current_w // 2, gui_info.infoObject.current_h - 50),
                                              font_size=50)
        with open('comms_files/transcription.txt', 'w') as file:
            file.write('')  # Clear the file

        pygame.display.flip()

        # # Audio
        # new_transcription = transcriber.get_current_transcription_and_reset()
        # if new_transcription:
        #     current_transcription = new_transcription

        await asyncio.sleep(0)  # Yield control

    pygame.quit()

    with open('comms_files/audio_control.txt', 'w') as file:
        file.write('stop')

    # Kill the task
    # task.cancel()
    # await task


if __name__ == '__main__':
    asyncio.run(main())
