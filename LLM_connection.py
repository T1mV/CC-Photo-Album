import os
import base64  # for images using OpenRouter
import mimetypes  # to detect the image type (jpeg, png, etc)
from google import genai
from google.genai import types
import ollama
from openai import OpenAI
from PIL import Image
from dotenv import load_dotenv


load_dotenv()

prompt = "Write a very short caption for this image."
image = "duck.png"


def choose_LLM_connection(choice, image, prompt, model):
    # Google AI studio connection:
    if choice == "GoogleAI":
        print(f"Using Google AI Studio and {model}.")
        client = genai.Client(api_key=os.environ["GOOGLEAI_API_KEY"])

        img = Image.open(image)

        response = client.models.generate_content(
            model = model,
            contents = [img, prompt],
            config = types.GenerateContentConfig(temperature = 0),
        )
        print(f"LLM caption: {response.text}")

    # Ollama connection:
    elif choice == "Ollama":
        print(f"Using Ollama and {model}.")
        # client = ollama.Client(
        #     host = "https://ollama.com",
        #     headers = {"Authorization": "Bearer " + os.environ["OLLAMA_API_KEY"]},
        # )

        # response = client.chat(
        response = ollama.chat(
            model = model, 
            messages = [{
                "role": "user",
                "content": prompt,
                "images": [image],
            }],
            options = {"temperature": 0},
        )
        print(f"LLM caption: {response['message']['content']}")

    # OpenRouter connection:
    elif choice == "OpenRouter":
        print(f"Using OpenRouter and {model}.")
        client = OpenAI(
            base_url = "https://openrouter.ai/api/v1",
            api_key = os.environ["OPENROUTER_API_KEY"],
        )

        with open(image, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()

        mime = mimetypes.guess_type(image)[0]  # to be flexible with png, jpg etc

        response = client.chat.completions.create(
            model = model, 
            messages = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                ],
            }],
            temperature = 0 
        )
        print(f"LLM caption: {response.choices[0].message.content}")

    else:
        print("Input either 'GoogleAI', 'Ollama', or 'OpenRouter' as the choice.")

print("FIRST LLM CALL")
choose_LLM_connection("GoogleAI", image, prompt, "gemini-3.5-flash-lite")
print("")
print("SECOND LLM CALL")
choose_LLM_connection("OpenRouter", image, prompt, "anthropic/claude-haiku-5.5")
# choose_LLM_connection("Ollama", image, prompt, "gemma4:e4b")

# one tests for the else
# choose_LLM_connection("GoogleAI", image, prompt, "test") 
# this one ^ still errors because it never enters the else, fix later or make sure to use correct model name
