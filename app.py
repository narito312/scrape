from flask import Flask, request, jsonify, send_from_directory
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)


SAVE_DIR = 'scraped_files'
os.makedirs(SAVE_DIR, exist_ok=True)


def setup_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service('/usr/local/bin/chromedriver')
    return webdriver.Chrome(service=service, options=chrome_options)

def download_image_with_selenium(page_url, filename):
    driver = setup_selenium()
    driver.get(page_url)

    try:
        image_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//img[contains(@src, "blob:")]'))
        )

        blob_url = image_element.get_attribute('src')

        js = f"return fetch('{blob_url}').then(response => response.blob()).then(blob => {{return URL.createObjectURL(blob);}});"
        image_url = driver.execute_script(js)

        png_response = requests.get(image_url)
        if png_response.status_code == 200:
            file_path = os.path.join(SAVE_DIR, filename)
            with open(file_path, 'wb') as file:
                file.write(png_response.content)
            return file_path, None
        else:
            return None, "Failed to download the image"
    finally:
        driver.quit()


def download_image_with_selenium(page_url, filename):
    driver = setup_selenium()
    driver.get(page_url)


def download_image_with_selenium(page_url, filename):
    driver = setup_selenium()
    driver.get(page_url)

    try:
        png_element = driver.find_element(By.TAG_NAME, 'png')
        png_url = png_element.get_attribute('src')

        png_response = requests.get(png_url)
        if png_response.status_code == 200:
            file_path = os.path.join(SAVE_DIR, filename)
            with open(file_path, 'wb') as file:
                file.write(png_response.content)
            return file_path, None
        else:
            return None, "Failed to download the image"
    finally:
        driver.quit()

def download_image_from_url(page_url, filename):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(page_url, headers=headers)
    if response.status_code != 200:
        return None, "Failed to retrieve the page"

    soup = BeautifulSoup(response.content, 'html.parser')
    
  
    img_tag = soup.find('img')
    
    if not img_tag or 'src' not in img_tag.attrs:
        return None, "Image URL not found on page"

    png_url = img_tag['src']
    if not png_url.startswith("http"):
        png_url = f"https://mangadex.org{png_url}"

    png_response = requests.get(png_url, headers=headers)
    if png_response.status_code == 200:
        file_path = os.path.join(SAVE_DIR, filename)
        with open(file_path, 'wb') as file:
            file.write(png_response.content)
        return file_path, None
    else:
        return None, "Failed to download the image"


@app.route('/scrape', methods=['POST'])
def scrape_file():
    data = request.get_json()
    url = data.get('url')
    filename = data.get('filename')

    if not url or not filename:
        return jsonify({"error": "URL and filename are required"}), 400

    try:
        response = requests.get(url)
        response.raise_for_status()

        file_path = os.path.join(SAVE_DIR, filename)
        with open(file_path, 'wb') as file:
            file.write(response.content)

        return jsonify({"message": f"File saved as {filename}"}), 201
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route('/list-files', methods=['GET'])
def list_files():
    files = os.listdir(SAVE_DIR)
    return jsonify({"files": files})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory(SAVE_DIR, filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    

if __name__ == '__main__':
    app.run(debug=True)