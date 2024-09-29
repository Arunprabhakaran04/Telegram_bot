# here we use hugging face end points to generate an image as per the user query.

from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv
import uuid
import requests
from PIL import Image
from io import BytesIO
import os
import time
# def generate_image():
#
#     load_dotenv()
#     api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
#     headers = {
#         "Authorization": f"Bearer {api_key}"
#     }
#     model_id = "CompVis/stable-diffusion-v1-4"
#     api_url = f"https://api-inference.huggingface.co/models/{model_id}"
#     prompt = input("enter an text that you want to get as an image. ")
#     data = {"inputs" : prompt}
#     response = requests.post(api_url, headers=headers, json=data)
#     if response.status_code == 200:
#         image = Image.open(BytesIO(response.content))
#         image.show()
#
#         output_folder = "./Generated_Images"
#         os.makedirs(output_folder, exist_ok=True)
#         filename = "image"+ ".png"
#
#         # Save the generated image using the dynamic filename
#         image_path = os.path.join(output_folder, filename)
#         image.save(image_path)
#
#         print(f"Image saved as: {image_path}")
#
#     else:
#         print(f"Error: {response.status_code}, {response.text}")

def generate_image(prompt: str) -> str:
    """
    Function to generate an image using Hugging Face endpoint based on the given prompt.
    Returns the path to the generated image.
    """
    load_dotenv()
    api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    model_id = "CompVis/stable-diffusion-v1-4"
    api_url = f"https://api-inference.huggingface.co/models/{model_id}"

    data = {"inputs": prompt}
    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))

        # Ensure the output folder exists
        output_folder = "./Generated_Images"
        os.makedirs(output_folder, exist_ok=True)

        # Create a unique filename using uuid and current timestamp
        unique_id = uuid.uuid4()
        timestamp = int(time.time())
        filename = f"image_{unique_id}_{timestamp}.png"

        # Save the generated image
        image_path = os.path.join(output_folder, filename)
        image.save(image_path)

        print(f"Image saved as: {image_path}")
        return image_path

    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# if __name__ == "__main__":
#     generate_image()