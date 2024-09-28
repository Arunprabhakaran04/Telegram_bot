import torch.cuda
from diffusers import StableDiffusionPipeline

device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)

def model_creation():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(device)
    model_id =  "CompVis/stable-diffusion-v1-4"
    device = device
    temperature = 0.6

    ##creating a pipeling for our project

    pipe = StableDiffusionPipeline.from_pretrained(model_id, use_auth_toke=True, torch_dtype=torch.float16)
    pipe = pipe.to(device)
    pipe.enable_attention_slicing()

    prompt = "comical book reading rat"
    image = pipe(prompt).images[0]
    image.show()

    image.save("./Generated Images")

if __name__ == "__main__":
    model_creation()