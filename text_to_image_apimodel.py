# here we use hugging face end points to generate an image as per the user query.

from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv
import requests
from PIL import Image
from io import BytesIO
import os

def generate_image():

    load_dotenv()
    api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    model_id = "CompVis/stable-diffusion-v1-4"
    api_url = f"https://api-inference.huggingface.co/models/{model_id}"
    prompt = input("enter an text that you want to get as an image. ")
    data = {"inputs" : prompt}
    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image.show()

        output_folder = "./Generated_Images"
        os.makedirs(output_folder, exist_ok=True)
        filename = "image"+ ".png"

        # Save the generated image using the dynamic filename
        image_path = os.path.join(output_folder, filename)
        image.save(image_path)

        print(f"Image saved as: {image_path}")

    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    generate_image()