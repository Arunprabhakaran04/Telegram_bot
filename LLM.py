from dotenv import load_dotenv
from llminstaller import model_installer
from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import ChatPromptTemplate
# model creation :
def generate_text(query:str):
    load_dotenv()
    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.3", # using an instruct model which has been finetuned to perform well on instruction tasks.
        # repo_id = "meta-llama/Llama-2-7b-chat-hf", # this model needs to be installed locally requiring a lot of computational resource.
        temperature=0.6, # setting the creativity of the model.
        max_new_tokens=512
    )
    # query = input("what do you want to ask the model ?")

    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're a knowledgeable Assistant. Provide concise, accurate answers to user questions without creating a dialogue format. Focus solely on the question asked. Dont make up scenerios on your own. If the question is unclear, ask for clarification."
        ),
        ("human", "{query}"),
    ]
    )

    """The following below code could be used to downland llama-chat model which is specifically trained on text conversation
    which would help our telegram bot to chat with the user.
    But due to the computation cost and lack of gpu, we are sticking with mistral model which is not specifically trained for convesation 
    but it serves the purpose."""


    """    
    model_name = "meta-llama/Llama-2-7b-chat-hf"
    model_para = model_installer(model_name=model_name)
    tokenizer = model_para["tokenizer"]
    model = model_para["model"]

    query = input("hi what do you want to ask the model ? : ")
    inputs = tokenizer(query, return_tensors="pt")

    output = model.generate(**inputs, max_new_tokens = 512, temperature = 0.6)
    result = tokenizer.decode(output, skip_special_tokens=True)
    """

    formatted_prompt = prompt.format(query=query)
    result = llm.invoke(formatted_prompt)

    return result

# if __name__ == "__main__":
#     generate_text(query)

