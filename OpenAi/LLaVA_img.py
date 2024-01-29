import requests, re
import pandas as pd

url_end_points = "http://10.177.213.119:8081"
remote_api_url_prompt = url_end_points+"/set_prompt"
remote_api_url_img = url_end_points+"/inference"

sample_file = pd.read_csv("Flavor_Item_Sample_with_Link.csv", encoding='unicode_escape')
url = sample_file[sample_file.Link.notnull()]['Link'].tolist()

def IMG_TXT_API_CALL(prompt_text, image_path='download_img.jpg'):
    with open(image_path, 'rb') as image_file:
        r = requests.post(remote_api_url_prompt, json={'prompt': prompt_text, "temperature": 0.7, "top_p": 0.8})
        response = requests.post(remote_api_url_img, files={'image': image_file})
    if response.status_code == 200:
        return re.sub(r'</s>', '', response.text)
    else:
        print(f"ServerFailCode:{response.status_code}")

sample_file['Item Name - Using Link']            = ''
sample_file['Item Name - Using Product Image']   = ''
sample_file['Flavor - Using Link']          = ''
sample_file['Flavor - Using Product Image'] = ''
print("Total URLs: ", len(url), "\n")
scent_flavour = 1    # Temporary
# scent_flavour = int(input("1. Flavor\n2. Scent\n\n"))

for i in range(len(url)):
    product_image = "https://www.kroger.com/product/images/large/front/" + str(url[i].split('/')[-1].split('?')[0])
    respons = requests.get(product_image)
    if respons.status_code == 200:
        fp = open('download_img.jpg', 'wb')
        fp.write(respons.content)
        fp.close()
    else:
        print("No images found in the link. Skipping ", url[i])
        print("Image Link: ",product_image)
        continue

    item_name_link = IMG_TXT_API_CALL("what is item name in this page " + url[i] + ". Dont answer in sentence. Give only flavor name. If there are more than one flavor names, separate them with a comma")
    print("URL PROMPT          :", requests.get(url_end_points+'/get_prompt').text)
    item_name_img = IMG_TXT_API_CALL("What is item name in this image? Give answer only.", "download_img.jpg")
    print("IMAGE PROMPT        :", requests.get(url_end_points+'/get_prompt').text, "\n")

    print("Item name from link :", item_name_link)
    print("Item name from img  :", item_name_img)

    if scent_flavour == 1: # For Flavour detection
        flavor_name_link = IMG_TXT_API_CALL("what are the flavor names of the product in this link" + url[i] + ". Exclude brand names. Dont answer in sentence. Give only flavor name. Consider special flavors")
        flavor_name_img = IMG_TXT_API_CALL("What is the flavor name of the item in this image. Give answer only", "download_img.jpg")

        sample_file.at[i, 'Item Name - Using Link']            = item_name_link
        sample_file.at[i, 'Item Name - Using Product Image']   = item_name_img
        sample_file.at[i, 'Flavor - Using Link']          = flavor_name_link
        sample_file.at[i, 'Flavor - Using Product Image'] = flavor_name_img

        print("Flavor from link    :", flavor_name_link)
        print("Flavor from img     :", flavor_name_img)
        print()

    elif scent_flavour == 2:  # For Scent Detection
        scent_name_link = IMG_TXT_API_CALL("scent name of the item in this URL " + url[i] + ". Give short answer", "download_img.jpg")
        print("URL PROMPT          :", requests.get(url_end_points+'/get_prompt').text)
        scent_name_img = IMG_TXT_API_CALL("scent name of the item in this image. Give answer only", "download_img.jpg")
        print("IMAGE PROMPT        :", requests.get(url_end_points+'/get_prompt').text)
        print()

        sample_file.at[i, 'Name - Using Link']           = item_name_link
        sample_file.at[i, 'Name - Using Product Image']  = item_name_img
        sample_file.at[i, 'scent - Using Link']          = scent_name_link
        sample_file.at[i, 'scent - Using Product Image'] = scent_name_img
        
        print("Scent from link     :", scent_name_link)
        print("Scent from img      :", scent_name_img)
        print("Product Details     :", IMG_TXT_API_CALL("Product details of the item in this page " + url[i], "download_img.jpg"))
        print()
        break # FOR TESTING PURPOSES ONLY
    else:
        print("Invalid input. Try again..\n")

print("EXPORTING TO CSV...")
sample_file.to_csv('GenAI_Results_LLaVA_img.csv')
print("DONE")