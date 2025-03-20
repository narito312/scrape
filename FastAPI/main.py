# # from flask import Flask, request, jsonify, send_from_directory
# # import os
# # import requests
# # from bs4 import BeautifulSoup
# # from selenium import webdriver
# # from selenium.webdriver.chrome.service import Service
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.chrome.options import Options
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC

# # app = Flask(__name__)


# # SAVE_DIR = 'scraped_files'
# # os.makedirs(SAVE_DIR, exist_ok=True)


# # def setup_selenium():
# #     chrome_options = Options()
# #     chrome_options.add_argument("--headless")
# #     chrome_options.add_argument("--no-sandbox")
# #     chrome_options.add_argument("--disable-dev-shm-usage")
# #     service = Service('/usr/local/bin/chromedriver')
# #     return webdriver.Chrome(service=service, options=chrome_options)

# # def download_image_with_selenium(page_url, filename):
# #     driver = setup_selenium()
# #     driver.get(page_url)

# #     try:
# #         image_element = WebDriverWait(driver, 10).until(
# #             EC.presence_of_element_located((By.XPATH, '//img[contains(@src, "blob:")]'))
# #         )

# #         blob_url = image_element.get_attribute('src')

# #         js = f"return fetch('{blob_url}').then(response => response.blob()).then(blob => {{return URL.createObjectURL(blob);}});"
# #         image_url = driver.execute_script(js)

# #         png_response = requests.get(image_url)
# #         if png_response.status_code == 200:
# #             file_path = os.path.join(SAVE_DIR, filename)
# #             with open(file_path, 'wb') as file:
# #                 file.write(png_response.content)
# #             return file_path, None
# #         else:
# #             return None, "Failed to download the image"
# #     finally:
# #         driver.quit()


# # def download_image_with_selenium(page_url, filename):
# #     driver = setup_selenium()
# #     driver.get(page_url)


# # def download_image_with_selenium(page_url, filename):
# #     driver = setup_selenium()
# #     driver.get(page_url)

# #     try:
# #         png_element = driver.find_element(By.TAG_NAME, 'png')
# #         png_url = png_element.get_attribute('src')

# #         png_response = requests.get(png_url)
# #         if png_response.status_code == 200:
# #             file_path = os.path.join(SAVE_DIR, filename)
# #             with open(file_path, 'wb') as file:
# #                 file.write(png_response.content)
# #             return file_path, None
# #         else:
# #             return None, "Failed to download the image"
# #     finally:
# #         driver.quit()

# # def download_image_from_url(page_url, filename):
# #     headers = {"User-Agent": "Mozilla/5.0"}
# #     response = requests.get(page_url, headers=headers)
# #     if response.status_code != 200:
# #         return None, "Failed to retrieve the page"

# #     soup = BeautifulSoup(response.content, 'html.parser')
    
  
# #     img_tag = soup.find('img')
    
# #     if not img_tag or 'src' not in img_tag.attrs:
# #         return None, "Image URL not found on page"

# #     png_url = img_tag['src']
# #     if not png_url.startswith("http"):
# #         png_url = f"https://mangadex.org{png_url}"

# #     png_response = requests.get(png_url, headers=headers)
# #     if png_response.status_code == 200:
# #         file_path = os.path.join(SAVE_DIR, filename)
# #         with open(file_path, 'wb') as file:
# #             file.write(png_response.content)
# #         return file_path, None
# #     else:
# #         return None, "Failed to download the image"


# # @app.route('/scrape', methods=['POST'])
# # def scrape_file():
# #     data = request.get_json()
# #     url = data.get('url')
# #     filename = data.get('filename')

# #     if not url or not filename:
# #         return jsonify({"error": "URL and filename are required"}), 400

# #     try:
# #         response = requests.get(url)
# #         response.raise_for_status()

# #         file_path = os.path.join(SAVE_DIR, filename)
# #         with open(file_path, 'wb') as file:
# #             file.write(response.content)

# #         return jsonify({"message": f"File saved as {filename}"}), 201
# #     except requests.exceptions.RequestException as e:
# #         return jsonify({"error": str(e)}), 500


# # @app.route('/list-files', methods=['GET'])
# # def list_files():
# #     files = os.listdir(SAVE_DIR)
# #     return jsonify({"files": files})

# # @app.route('/download/<filename>', methods=['GET'])
# # def download_file(filename):
# #     try:
# #         return send_from_directory(SAVE_DIR, filename, as_attachment=True)
# #     except FileNotFoundError:
# #         return jsonify({"error": "File not found"}), 404
    

# # if __name__ == '__main__':
# #     app.run(debug=True)

# import requests
# import os

# secret_data_url = "https://api.mangadex.org/at-home/server/"
# media_url = "https://cmdxd98sb0x3yprd.mangadex.network/data/"
# book_id = "1178415e-f2ec-4e98-94df-9c1e91751738/"


# # url = "https://mangadex.org/chapter/1178415e-f2ec-4e98-94df-9c1e91751738/5"  # Replace with the target webpage URL


# # go out to JSON server to get book resources based on the Book ID:
# response = requests.get(f"{secret_data_url}{book_id}?forcePort443=false")
# data = response.json()

# # extract the hash and the links to each image:
# hash = data.get("chapter").get("hash")
# image_urls = data.get("chapter").get("data")

# # loop through each image, build the url, and download the image
# for image_url in image_urls:
#     full_url = f"{media_url}{hash}/{image_url}"
#     print(full_url)
#     img_response = requests.get(full_url)
#     if img_response.status_code == 200:
#         # Save the image
#         img_name = os.path.basename(full_url)  # Extract filename from URL
#         with open(img_name, "wb") as file:
#             file.write(img_response.content)
#         print(f"Image downloaded: {img_name}")
#     else:
#         print("Failed to download the image.")

        
# def getBookByTitle(title):
#     response = requests.get(f"https://api.mangadex.org/manga?title={title}&limit=1")
#     data = response.json()
#     print(data)


from fastapi import FastAPI, Query, HTTPException
import requests

app = FastAPI()

def search_titles(title: str, limit: int):
    url = "https://api.mangadex.org/manga"
    params = {
        "limit": limit,
        "title": title,
        "includedTagsMode": "AND",
        "excludedTagsMode": "OR",
        "contentRating[]": ["safe", "suggestive", "erotica"],
        "order[latestUploadedChapter]": "desc",
    }
    
    headers = {"accept": "application/json"}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None

@app.get("/search/")
def search(title: str = Query(..., description="Title of the manga"), 
           limit: int = Query(10, description="Number of results to return")):
    
    data = search_titles(title, limit)

    if not data:
        raise HTTPException(status_code=500, detail="Failed to fetch data from MangaDex API")

    if "data" not in data:
        raise HTTPException(status_code=404, detail="No results found")

    results = []
    for manga in data["data"]:
        title = manga["attributes"]["title"].get("en", "N/A")
        description = manga["attributes"].get("description", {}).get("en", "No description available")
        results.append({"title": title, "description": description})

    return {"results": results}
    
