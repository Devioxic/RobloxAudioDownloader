from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import argparse
import os
import random
import string
import base64

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def create_folder(folder_name : str):
    os.makedirs(folder_name, exist_ok=True)

def create_temp_folder():
    temp_folder_name = generate_random_string(10)
    create_folder(temp_folder_name)
    return temp_folder_name

def remove_temp_folder(folder_name : str):
    os.rmdir(folder_name)

def transfer_files(folder_name : str, file_name : str):
    for filename in os.listdir(folder_name):
        os.rename(f"{folder_name}\{filename}", f"Audio\{file_name}.mp3")

def save_alt_file(data : bytearray, file_name : str, folder_name : str = "Audio"):
    with open(f"{folder_name}/{file_name}.ogg", "wb") as fh:
        fh.write(data)

def get_file_content_chrome(driver, uri):
  result = driver.execute_async_script("""
    var uri = arguments[0];
    var callback = arguments[1];
    var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
    var xhr = new XMLHttpRequest();
    xhr.responseType = 'arraybuffer';
    xhr.onload = function(){ callback(toBase64(xhr.response)) };
    xhr.onerror = function(){ callback(xhr.status) };
    xhr.open('GET', uri);
    xhr.send();
    """, uri)
  if type(result) == int :
    raise Exception("Request failed with status %s" % result)
  return base64.b64decode(result)


def extract_audio_src(asset_id : int, file_name : str):
    url = f"https://create.roblox.com/marketplace/asset/{asset_id}"

    name = create_temp_folder()
    print(f"{os.getcwd()}/{name}")

    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
    "download.default_directory": f"{os.getcwd()}\{name}",
    })
    #options.add_argument('--headless') # Won't work with some assets
    driver = webdriver.Chrome(options=options)  # Replace with the path to your chromedriver if not in PATH

    driver.get(url)
    time.sleep(2)  # Give time for the audio to load

    audio_element = driver.find_element(By.TAG_NAME, 'audio')

    if audio_element:
        src = audio_element.get_attribute('src')
        print(f"The source for the first <audio> tag is: {src}")
        create_folder('Audio')
        print(f"Downloading audio")
        driver.get(src)
        try: # In case the audio is an ogg file and plays instead of downloading
            data = get_file_content_chrome(driver, src)
            save_alt_file(data, file_name, "Audio")
        except:
            print("Regular file, proceeding with download")

        time.sleep(2) # Give time for the audio to download, you might want to increase this if you have a slow internet connection
        transfer_files(name, file_name)
        remove_temp_folder(name)
    else:
        print("No <audio> tag found on the page.")

    driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract SRC attribute from the first <audio> tag of a Roblox asset page and download the audio file.')
    parser.add_argument('asset_id', type=int, help='Roblox asset ID')
    parser.add_argument('name', type=str, help='Name of the audio file', nargs='?', default=None)

    args = parser.parse_args()
    asset_id = args.asset_id

    if not args.name:
        name = str(asset_id)
    else:
        name = args.name

    extract_audio_src(asset_id, name)