import asyncio
import os
import random

import openai
from openai import OpenAI
from scipy.io.wavfile import write
from sounddevice import rec, wait

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()


# TODO Ways to improve this
# - Pass in the transcription history, to help it understand the context of the conversation
# - Concatenate 2 blocks at a time, to avoid errors that occur at the boundary of understanding


class Transcriber:
    def __init__(self):
        self.current_transcription: str = ""
        self.transcription_history: list[str] = []
        self.currently_transcribing = False

        self.duration = 5  # seconds
        self.sample_rate = 44100  # Hz

    async def transcribe(self) -> None:
        print("Recording...")
        loop = asyncio.get_running_loop()
        # Run the blocking audio recording in a separate thread
        audio = await loop.run_in_executor(
            None,  # Uses the default executor (ThreadPoolExecutor)
            lambda: rec(int(self.duration * self.sample_rate), samplerate=self.sample_rate, channels=2, dtype='int16')
        )
        wait()  # This is blocking, but short-lived. Consider how critical this wait is.
        print("Recording finished.")

        audio_filename = 'output_audio.wav'
        write(audio_filename, self.sample_rate, audio)

        # Open the audio file in read-binary mode
        with open(audio_filename, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                prompt=" ".join(self.transcription_history[-4:]),
            )

        # Print the transcribed text
        print("Transcribed Text:", transcription.text)
        print(transcription)
        self.current_transcription += " " + transcription.text

    async def start_transcribing(self) -> None:
        self.currently_transcribing = True
        while self.currently_transcribing:
            await self.transcribe()
            await asyncio.sleep(0)  # Yield control

    def stop_transcribing(self) -> None:
        self.currently_transcribing = False

    def get_current_transcription_and_reset(self) -> str:
        """Saves the current transcription to history, returns it, and resets it."""
        current_transcription = self.current_transcription
        self.current_transcription = ""
        self.transcription_history.append(current_transcription)
        return current_transcription


async def main():
    transcriber = Transcriber()

    # Start the transcribing task in the background
    task = asyncio.create_task(transcriber.start_transcribing())

    total_time = 0
    print("Starting to record audio...")
    for i in range(10):
        st = random.randint(3, 15)
        total_time += st
        print(f"Sleeping for {st} seconds...")
        # time.sleep(st)  # Sleep for a random time, blocking
        await asyncio.sleep(st)  # Sleep for a random time, non-blocking

        print(f"Slept for {st} seconds. Total time slept: {total_time} seconds.")
        print(transcriber.get_current_transcription_and_reset())

    transcriber.stop_transcribing()
    await task  # Ensure the background task has completed or been cancelled properly


if __name__ == "__main__":
    asyncio.run(main())
