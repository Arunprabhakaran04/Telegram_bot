# here we use hugging face end points to generate an image as per the user query.

from langchain_huggingface import HuggingFaceEndpoint
# from dotenv import load_dotenv
# import uuid
# import requests
# from PIL import Image
# from io import BytesIO
# import os
# import time
# def generate_image(prompt: str) -> str:
#     """
#     Function to generate an image using Hugging Face endpoint based on the given prompt.
#     Returns the path to the generated image.
#     """
#     load_dotenv()
#     api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
#     headers = {
#         "Authorization": f"Bearer {api_key}"
#     }
#
#     model_id = "CompVis/stable-diffusion-v1-4"
#     api_url = f"https://api-inference.huggingface.co/models/{model_id}"
#
#     data = {"inputs": prompt}
#     response = requests.post(api_url, headers=headers, json=data)
#
#     if response.status_code == 200:
#         image = Image.open(BytesIO(response.content))
#
#         # Ensure the output folder exists
#         output_folder = "./Generated_Images"
#         os.makedirs(output_folder, exist_ok=True)
#
#         # Create a unique filename using uuid and current timestamp
#         unique_id = uuid.uuid4()
#         timestamp = int(time.time())
#         filename = f"image_{unique_id}_{timestamp}.png"
#
#         # Save the generated image
#         image_path = os.path.join(output_folder, filename)
#         image.save(image_path)
#
#         print(f"Image saved as: {image_path}")
#         return image_path
#
#     else:
#         print(f"Error: {response.status_code}, {response.text}")
#         return None

from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv
import uuid
import requests
from PIL import Image
from io import BytesIO
import os
import time


def generate_image(prompt: str, max_retries: int = 5, initial_wait: int = 10) -> str:
    """
    Function to generate an image using Hugging Face endpoint based on the given prompt.
    Implements retry logic in case the model is still loading.
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

    retries = 0
    wait_time = initial_wait

    while retries < max_retries:
        try:
            # Make the request with a timeout
            response = requests.post(api_url, headers=headers, json=data, timeout=480)  # 2-minute timeout

            # Check for successful response
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

            elif response.status_code == 503 and "loading" in response.text:
                print(f"Model is still loading. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                retries += 1
                wait_time *= 2  # Exponential backoff

            else:
                print(f"Error: {response.status_code}, {response.text}")
                return None

        except requests.exceptions.Timeout:
            print("Error: The request timed out.")
            return None

        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            return None

    print("Error: Max retries exceeded. Unable to generate image.")
    return None


# if __name__ == "__main__":
#     generate_image()