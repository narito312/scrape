import requests
import pprint
import os

#set up chapter url
chapter_id = "a54c491c-8e4c-4e97-8873-5b79e59da210"

base_url = "https://api.mangadex.org/at-home/server/"

chapter_url = f"{base_url}{chapter_id}"
media_url = "https://uploads.mangadex.org/data/"
#print (chapter_url)

#send the requests to get chapter info:

chapter_response= requests.get(chapter_url).json()

hash = chapter_response.get("chapter").get("hash")

png_list = chapter_response.get("chapter").get("data")

png_url = f"{media_url}{hash}/{png_list[0]}"

print(png_url)

for png in png_list:
    png_url = f"{media_url}{hash}/{png}"
    print(png_url)

    img_response = requests.get(png_url)
    if img_response.status_code == 200:
        # Save the image
        img_name = os.path.basename(png_url)  # Extract filename from URL
        with open(img_name, "wb") as file:
            file.write(img_response.content)
        print(f"Image downloaded: {img_name}")
    else:
        print("Failed to download the image.")

