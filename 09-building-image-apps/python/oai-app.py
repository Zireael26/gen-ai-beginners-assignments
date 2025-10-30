from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI
from openai.resources.images import ImagesResponse
import base64
from datetime import datetime

load_dotenv()
client = OpenAI()

def generate_image_with_responses_api(prompt: str) -> str:
    response = client.responses.create(
        model="gpt-5-nano",
        input=prompt,
        reasoning={"effort": "low"},
        tools=[
            {
                "type": "image_generation",
                "quality": "low",
            }
        ],
        service_tier="flex"
    )
    image_data = [
        output.result
        for output in response.output
        if output.type == "image_generation_call"
    ]
    return image_data[0]

def generate_image(prompt: str) -> str:
    image_response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        quality="standard",
        n=1,
        size="1024x1024",
        response_format="b64_json"
    )
    return image_response.data[0].b64_json

def save_image(image_data: str, filename: str):
    if image_data:
        image_bytes = base64.b64decode(image_data)
        with open(filename, "wb") as image_file:
            image_file.write(image_bytes)

if __name__ == "__main__":
    prompt = input("Enter a prompt for the image: ")
    image_base64 = generate_image(prompt)
    
    output_dir = Path("09-building-image-apps/generated_images")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = int(datetime.now().timestamp())
    output_path = output_dir / f"image_{timestamp}.png"
    save_image(image_base64, output_path)
    print(f"Image saved to {output_path}")