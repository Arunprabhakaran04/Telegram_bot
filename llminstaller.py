from transformers import AutoTokenizer, AutoModelForCausalLM

def model_installer(model_name:str):
    """
    This function block downloads and returns the model and its tokenizer as per the model name mentioned by the user.
    The format of the return value of this function is -
    'tokenizer': 'tokenizer of the corresponding model'
    'model': 'model installed locally.'
    """
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)

        return {"tokenizer": tokenizer, "model": model}
    except Exception as e:
        print(f"Error downloading model '{model_name}': {e}")
        return None


if __name__ == "__main__":
    name = input("enter the model configuration name ")
    model_installer(name)
