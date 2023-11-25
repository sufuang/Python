import requests, re
import pandas as pd

url_end_points = "http://10.177.213.119:5002"
remote_api_text_prompt = url_end_points + "/api/v1/chat/completions"

sample_file = pd.read_csv("Flavor_Item_Sample_with_Link.csv", encoding='unicode_escape')
url = sample_file[sample_file.Link.notnull()]['Link'].tolist()

def TXT_ONLY_API_CALL(prompt_text):
    return eval(requests.post(remote_api_text_prompt, 
                              json={"model": "Llama-2-70b-chat-hf",
                              "messages": "<s>[INST]<<SYS>>Do not include brand name of the item.<</SYS>>" + prompt_text + ". Dont answer in sentence. Give only flavor name[/INST]",
                              "temperature": 0.7,
                              "top_p": 0.8,
                              "n": 1,
                              "max_tokens": 100,
                              "stop": [
                                  "</s>"
                              ]})\
                                .text).get('choices')[0].get('message').get('content')

sample_file['Item Name - Using Link'] = ''
sample_file['Flavor Name - Using Link']  = ''
print("Total URLs: ", len(url), "\n")
scent_flavour = 1
# scent_flavour = int(input("1. Flavor\n2. Scent\n\n"))

for i in range(20):
    item_name_link = TXT_ONLY_API_CALL("what is the name of the item in this link " + url[i]).strip()
    sample_file.at[i, 'Item Name - Using Link'] = item_name_link

    if scent_flavour == 1: # For Flavour detection
        flavor_name_link = TXT_ONLY_API_CALL("What are the flavour names of the item in this link - " + url[i])
        sample_file.at[i, 'Flavor Name - Using Link'] = flavor_name_link
        print(i, sample_file.Link.iloc[i] ,item_name_link.split(':')[-1].strip(), flavor_name_link.split(':')[-1], sep=' == ', end='\n\n')
    
    elif scent_flavour == 2:  # For Scent Detection
        break

    else:
        print("Invalid input. Try again..\n")

print("EXPORTING TO CSV...")
sample_file.to_csv('GenAI_Results_LLaMA_txt.csv')
print("DONE")

