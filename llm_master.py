import os
import random
import re
from typing import List, Tuple

from langchain_openai import ChatOpenAI
from rich.console import Console

console = Console()


def get_next_art_prompt(prompts_so_far: List[Tuple[str, str]], done_amount: str = "") -> Tuple[str, str]:
    previous_content = "\n".join(
        [f"Story: {story_text}\nArt: {art_prompt}" for story_text, art_prompt in prompts_so_far])

    prompt = """
I'm writing an illustrated picture book, and I want help with the next page.  {done_amount}

Here's the story so far. I'll show you the story on each page, and a description of the art. 

{previous_content}

I want you to help me out by filling out this form. 

Keep the header sections the same, but fill in the content with your own ideas.

# Story Ideas

Brainstorm several ideas about what could happen next in the story. It's a picture book, so the story should be visually engaging. Suggest several twists and turns that could happen. Don't be afraid to introduce new characters, ideas, or settings.

# Next Story Page

Choosing one of those ideas, write a short one-paragraph story about what happens next in the story. It should be evocative of a beautiful, fantastic world. Choose something exciting that will advance the plot!

# Art Ideas

Brainstorm several ideas about what the art could look like.

# Art Direction

A picture of [adjective] [central element] with [mood] lighting. The art is [style] and [technique], in the style of [artist]. 
""".format(previous_content=previous_content, done_amount=done_amount).strip()

    openai_llm = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"], model_name="gpt-4")
    response = openai_llm.invoke(
        prompt,
        max_tokens=2000,
        temperature=0.7,
    ).content

    pattern = r"#\s*(.*?)\n\n(.*?)(?=\n\n#|\Z)"
    # Use re.DOTALL to make '.' match any character including newline
    matches = re.findall(pattern, response, re.DOTALL)
    sections = {header.strip(): text.strip() for header, text in matches}

    # Default to something random
    story_idea = "Review the story so far"
    art_idea = random.choice(prompts_so_far)[1]

    for key in sections.keys():
        if "next story page" in key.lower():
            story_idea = sections[key]
        elif "art direction" in key.lower():
            art_idea = sections[key]

    return story_idea, art_idea


# I know this is duplicated code. Oh well!
def get_next_art_prompt_from_audio(audio: str, previous_context: str) -> str:
    prompt = """
I'm making art based on a conversation that I'm having. Here's a loose transcription of the conversation so far:

```
{audio}
```

I want you to help me out by filling out this form. 

Keep the header sections the same, but fill in the content with your own ideas.

# Imagery

Looking at the transcription of the conversation I showed you, brainstorm imagery that the words are evocative of. 
* Concrete object that was mentioned
* Descriptive adjective
* Abstract concept that was mentioned
* Emotion that was mentioned
* Concrete noun that this reminds you of
* A portrait or landscape scene description

# Art Ideas

Brainstorm a few ideas about what the art could look like. If the conversation references concrete images, stick closely to that. But if it's more abstract, think about how to represent the mood and style of the conversation. Not everything needs to be used in the prompt, but it's good to have a few ideas to choose from.

# Art Direction

A picture of [concrete adjective] [concrete noun] with [lighting]. The art is [concrete or realistic style] and [creative technique], in the style of [artist]. 
""".format(audio=audio, previous_content=previous_context).strip()

    openai_llm = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"], model_name="gpt-4")
    response = openai_llm.invoke(
        prompt,
        max_tokens=2000,
        temperature=0.7,
    ).content

    pattern = r"#\s*(.*?)\n\n(.*?)(?=\n\n#|\Z)"
    # Use re.DOTALL to make '.' match any character including newline
    matches = re.findall(pattern, response, re.DOTALL)
    sections = {header.strip(): text.strip() for header, text in matches}

    art_idea = ""
    for key in sections.keys():
        if "art direction" in key.lower():
            console.print(f"Art direction found: {sections[key]}")
            return sections[key]

    # Default to just returning the audio
    console.print("No art direction found, defaulting to audio")
    return audio
