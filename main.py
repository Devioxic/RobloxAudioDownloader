from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import argparse
import os
import random
import string

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def create_folder(folder_name):
    os.makedirs(folder_name, exist_ok=True)

def create_temp_folder():
    temp_folder_name = generate_random_string(10)
    create_folder(temp_folder_name)
    return temp_folder_name

def remove_temp_folder(folder_name):
    os.rmdir(folder_name)

def transfer_files(folder_name, asset_id):
    for filename in os.listdir(folder_name):
        os.rename(f"{folder_name}\{filename}", f"Audio\{asset_id}.mp3")


def extract_audio_src(asset_id):
    url = f"https://create.roblox.com/marketplace/asset/{asset_id}"

    name = create_temp_folder()
    print(f"{os.getcwd()}/{name}")

    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
    "download.default_directory": f"{os.getcwd()}\{name}",
    })
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)  # Replace with the path to your chromedriver if not in PATH

    driver.get(url)
    time.sleep(2)  # Give time for the audio to load

    audio_element = driver.find_element(By.TAG_NAME, 'audio')

    if audio_element:
        src = audio_element.get_attribute('src')
        print(f"The source for the first <audio> tag is: {src}")
        create_folder('Audio')
        driver.get(src)
        time.sleep(2) # Give time for the audio to download, you might want to increase this if you have a slow internet connection
        transfer_files(name, asset_id)
        remove_temp_folder(name)
    else:
        print("No <audio> tag found on the page.")

    driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract SRC attribute from the first <audio> tag of a Roblox asset page and download the audio file.')
    parser.add_argument('asset_id', type=int, help='Roblox asset ID')

    args = parser.parse_args()
    asset_id = args.asset_id

    # Check if the asset ID is valid
    if type(asset_id) != int:
        print("The asset ID must be an integer.")
    elif len(str(asset_id)) != 10:
        print("The asset ID must be 10 digits long.")

    extract_audio_src(asset_id)