# Roblox Audio Extractor

This Python script extracts the SRC attribute from the first `<audio>` tag of a Roblox asset page and downloads the audio file.

## Requirements

- Python 3
- Selenium
- Chrome WebDriver

## Installation

1. Clone this repository.
2. Install the required Python packages using pip:

```sh
pip install -r requirements.txt
```

## Usage
Run the script with the Roblox asset ID as a required argument and the name of the output file as an optional argument.

```sh
python main.py <asset_id> [name]
```

Replace <asset_id> and [name] with the asset ID and the name of the output file respectively.

## Download multiple files

If you want to download multiple files at once, you can use the `multiple_download.py` script.

1. Open the `multiple_download.py` file
2. Add each id to the `ids` list separated by a comma
3. Add each name to the `names` list separated by a comma (optional)
4. Simply run the script

## License
This project is licensed under the terms of the MIT license.