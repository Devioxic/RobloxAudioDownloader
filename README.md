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
Run the script with the Roblox asset ID as an argument:

```sh
python main.py <asset_id>
```

Replace <asset_id> with the ID of the Roblox asset you want to download the audio from.

## License
This project is licensed under the terms of the MIT license.