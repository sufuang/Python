import requests, re
import pandas as pd

url_end_points = "http://10.177.213.119:8081"
remote_api_url_p = url_end_points+"/set_prompt"
remote_api_url_img = url_end_points+"/inference"

sample_file = pd.read_csv("Flavor_Item_Sample_with_Link.csv", encoding='unicode_escape')
url = sample_file['Link'].tolist()

def API_CALL(promt_text, image_pth=None):
    with open(image_pth, 'rb') as image_file:
        r = requests.post(remote_api_url_p, json={'prompt': promt_text})
        response = requests.post(remote_api_url_img, files={'image': image_file})

    if response.status_code == 200:
        return re.sub(r'</s>','',response.text)
    else:
        print(f"FailCode:{response.status_code}")


sample_file['Name - Using Link'] = ''
sample_file['Name - Using Product Image'] = ''
sample_file['Flavor - Using Link'] = ''
sample_file['Flavor - Using Product Image'] = ''
print("Length: ", len(url))
print()

cnt=-1
for url in url:
    cnt+=1
    print(cnt)
    # scent_flavour = int(input("1. Flavor\n2. Scent\n\n"))
    scent_flavour = 1    # Temporary
    
    if scent_flavour == 1: # For Flavor detection
        product_image = "https://www.kroger.com/product/images/large/front/" + str(url.split('/')[-1].split('?')[0])
        respons = requests.get(product_image)
        if respons.status_code:
            fp = open('flavour_img.jpg', 'wb')
            fp.write(respons.content)
            fp.close()
        
        item_name_link = API_CALL("what is the name of the item in this URL " + url + ". Answer in short", "flavour_img.jpg")
        item_name_img = API_CALL("what is the name of the item in this image. Answer in short", "flavour_img.jpg")
        flavor_name_link = API_CALL("what is the flavor name of the item in this URL " + url + ". Answer in short", "flavour_img.jpg")
        flavor_name_img = API_CALL("what is the flavor name of the item in this image. Answer in short", "flavour_img.jpg")

        sample_file.at[cnt, 'Name - Using Link'] = item_name_link
        sample_file.at[cnt, 'Name - Using Product Image'] = item_name_img
        sample_file.at[cnt, 'Flavor - Using Link'] = flavor_name_link
        sample_file.at[cnt, 'Flavor - Using Product Image'] = flavor_name_img
        print("Item name-link:", item_name_link)
        print("Item name-img :", item_name_img)
        print("Flavor-link:", flavor_name_link)
        print("Flavor-img :", flavor_name_img)
        print("Product Details:", API_CALL("what is product details of the item in this page" + url, "flavour_img.jpg"))
        print("Flavor:", API_CALL("what is product details of the item in this page" + url, "flavour_img.jpg"))
        print()

    elif scent_flavour == 2: 
        pass  # For Scent Detection
    else:
        print("Invalid input. Try again..")

# sample_file.to_csv("GenAI_Results.csv", index=False)

