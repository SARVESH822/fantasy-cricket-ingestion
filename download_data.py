import requests
import zipfile
import os
import shutil

# Cricsheet league ZIP URLs
leagues = {
    "ipl": "https://cricsheet.org/downloads/ipl_json.zip",
    "bbl": "https://cricsheet.org/downloads/bbl_json.zip",
    "psl": "https://cricsheet.org/downloads/psl_json.zip",
    "cpl": "https://cricsheet.org/downloads/cpl_json.zip",
    "sa20": "https://cricsheet.org/downloads/sa20_json.zip",
    "ilt20": "https://cricsheet.org/downloads/ilt20_json.zip",
    "lpl": "https://cricsheet.org/downloads/lpl_json.zip",
    "bpl": "https://cricsheet.org/downloads/bpl_json.zip"
}

# Create raw_data folder
os.makedirs("raw_data", exist_ok=True)

for league, url in leagues.items():

    print(f"\nDownloading {league} data...")

    zip_name = f"{league}.zip"

    # Download ZIP file
    response = requests.get(url)

    with open(zip_name, "wb") as f:
        f.write(response.content)

    print(f"{league} ZIP downloaded.")

    # Temporary extraction folder
    extract_folder = f"temp_{league}"

    # Extract ZIP
    with zipfile.ZipFile(zip_name, "r") as zip_ref:
        zip_ref.extractall(extract_folder)

    print(f"{league} ZIP extracted.")

    # Destination folder
    destination = os.path.join("raw_data", league)

    os.makedirs(destination, exist_ok=True)

    # Copy JSON files
    for file in os.listdir(extract_folder):

        if file.endswith(".json"):

            src = os.path.join(extract_folder, file)
            dst = os.path.join(destination, file)

            shutil.copy(src, dst)

    print(f"{league} JSON files copied.")

    # Cleanup
    os.remove(zip_name)
    shutil.rmtree(extract_folder)

print("\nAll downloads completed.")

# Upload new Kaggle dataset version
os.system(
    'kaggle datasets version -p . -m "Automatic daily Cricsheet update"'
)

print("\nKaggle dataset updated.")
