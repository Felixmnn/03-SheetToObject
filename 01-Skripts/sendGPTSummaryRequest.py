#The GPTData gets processed by GPT
#The GPT Summary gets saved in the GPTSummary folder

import os
from openai import OpenAI
from config import api_key


    
def createOpenAiRequest (anfrage): 
        
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key= api_key,  # use your API key here
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "",
            },
            {
                "role": "user",
                "content": f"{anfrage}",
            }
        ],
        model="gpt-4o",
        temperature=1,
        max_tokens=4096,
        top_p=1
    )
    response = response.choices[0].message.content
    print (response)
    return(response)
