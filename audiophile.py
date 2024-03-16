import asyncio
import os
import random
from typing import Optional

import openai
from openai import OpenAI
from rich.console import Console
from scipy.io.wavfile import write
from sounddevice import rec, wait

from read_api_keys import read_api_keys

read_api_keys()

console = Console()

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()


# TODO Ways to improve this
# - Pass in the transcription history, to help it understand the context of the conversation
# - Concatenate 2 blocks at a time, to avoid errors that occur at the boundary of understanding


class AudioTranscriber:
    def __init__(self):
        # The current transcription is waiting to be processed by an external service
        self.current_transcription: str = ""

        self.transcription_history: list[str] = []
        self.currently_transcribing = False

        self.duration = 5  # seconds
        self.sample_rate = 44100  # Hz

        # Both of these should be in the "comms_files" dir.
        self.text_output_file: Optional[str] = None
        self.control_file: Optional[str] = None

    async def transcribe(self) -> None:
        console.print("Recording...")
        loop = asyncio.get_running_loop()
        # Run the blocking audio recording in a separate thread
        audio = await loop.run_in_executor(
            None,  # Uses the default executor (ThreadPoolExecutor)
            lambda: rec(int(self.duration * self.sample_rate), samplerate=self.sample_rate, channels=2, dtype='int16')
        )
        wait()  # This is blocking, but short-lived. Consider how critical this wait is.
        console.print("Recording finished.")

        audio_filename = 'output_audio.wav'
        write(audio_filename, self.sample_rate, audio)

        # Open the audio file in read-binary mode
        with open(audio_filename, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                prompt=" ".join(self.transcription_history[-4:]),
            )

        # console.print the transcribed text
        console.print("Transcribed Text:", transcription.text)
        console.print(transcription)
        self.current_transcription += " " + transcription.text

    async def start_transcribing(self) -> None:
        console.print("Starting to transcribe...")
        self.currently_transcribing = True
        while self.currently_transcribing:
            await self.transcribe()
            await asyncio.sleep(0)  # Yield control

    def transcribe_blocking(self) -> None:
        # console.print("Recording...")
        asyncio.run(self.start_transcribing())

    def stop_transcribing(self) -> None:
        self.currently_transcribing = False

    def get_current_transcription_and_reset(self) -> Optional[str]:
        """Saves the current transcription to history, returns it, and resets it."""
        current_transcription = self.current_transcription
        self.current_transcription = ""
        self.transcription_history.append(current_transcription)
        return current_transcription

    def transcribe_until_stopped(self) -> None:
        console.print("Starting to transcribe...")
        while True:
            if self.control_file is not None and os.path.exists(self.control_file):
                control = open(self.control_file, "r").read()
                if control.lower().strip() == "stop":
                    console.print("Stopping transcription...")
                    break

            asyncio.run(self.transcribe())

            if self.text_output_file is not None and self.current_transcription != "":
                console.print("Writing to file...")
                with open(self.text_output_file, "a") as file:
                    file.write(self.get_current_transcription_and_reset() + "\n")
            else:
                console.print(f"Output file: {self.text_output_file}")
                console.print(f"Current transcription: {self.current_transcription}")


def main_with_files():
    transcriber = AudioTranscriber()
    transcriber.text_output_file = "comms_files/transcription.txt"
    transcriber.control_file = "comms_files/control.txt"

    transcriber.transcribe_until_stopped()


async def main():
    transcriber = AudioTranscriber()

    # Start the transcribing task in the background
    task = asyncio.create_task(transcriber.start_transcribing())

    total_time = 0
    console.print("Starting to record audio...")
    for i in range(10):
        st = random.randint(3, 15)
        total_time += st
        console.print(f"Sleeping for {st} seconds...")
        # time.sleep(st)  # Sleep for a random time, blocking
        await asyncio.sleep(st)  # Sleep for a random time, non-blocking

        console.print(f"Slept for {st} seconds. Total time slept: {total_time} seconds.")
        console.print(transcriber.get_current_transcription_and_reset())

    transcriber.stop_transcribing()
    await task  # Ensure the background task has completed or been cancelled properly


# This isn't just for development, it's also important because app.py runs this file as a subprocess.
if __name__ == "__main__":
    # asyncio.run(main())
    main_with_files()
