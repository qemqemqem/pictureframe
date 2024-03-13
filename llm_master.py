import os
import random
import re
from typing import List, Tuple

from langchain_openai import ChatOpenAI


def get_next_art_prompt(prompts_so_far: List[Tuple[str, str]]) -> Tuple[str, str]:
    previous_content = "\n".join(
        [f"Story: {story_text}\nArt: {art_prompt}" for story_text, art_prompt in prompts_so_far])

    prompt = """
I'm writing an illustrated picture book, and I want help with the next page. 

Here's the story so far. I'll show you the story on each page, and a description of the art:

{previous_content}

I want you to help me out by filling out this form:

# Story Ideas

Brainstorm several ideas about what could happen next in the story. It's a picture book, so the story should be visually engaging. Suggest several twists and turns that could happen. Don't be afraid to introduce new characters, ideas, or settings.

# Next Story Page

Choosing one of those ideas, write a short one-paragraph story about what happens next in the story. It should be evocative of a fantastic world.

# Art Ideas

Brainstorm several ideas about what the art could look like.

# Art Direction

A picture of [adjective] [central element] with [mood] lighting. The art is [style] and [technique], in the style of [artist]. 
""".format(previous_content=previous_content).strip()

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
