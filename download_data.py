import requests
import zipfile
import os
import shutil

# VERIFIED Cricsheet leagues
leagues = {

    "ipl": "https://cricsheet.org/downloads/ipl_json.zip",

    "bbl": "https://cricsheet.org/downloads/bbl_json.zip",

    "psl": "https://cricsheet.org/downloads/psl_json.zip",

    "cpl": "https://cricsheet.org/downloads/cpl_json.zip",

    "bpl": "https://cricsheet.org/downloads/bpl_json.zip",

    "lpl": "https://cricsheet.org/downloads/lpl_json.zip",

    "blast": "https://cricsheet.org/downloads/t20blast_male_json.zip",

    "smat": "https://cricsheet.org/downloads/sma_male_json.zip",

    "t20i": "https://cricsheet.org/downloads/t20s_json.zip",

    "sa20": "https://cricsheet.org/downloads/sa20_male_json.zip",

    "ilt20": "https://cricsheet.org/downloads/ilt20_male_json.zip",

    "hundred": "https://cricsheet.org/downloads/hundred_male_json.zip",

    "supersmash": "https://cricsheet.org/downloads/super_smash_male_json.zip",

    "abu_dhabi_t10": "https://cricsheet.org/downloads/abt10_male_json.zip"
}

# Create raw_data folder
os.makedirs("raw_data", exist_ok=True)

# Download each league
for league, url in leagues.items():

    print(f"\nDownloading {league}...")

    zip_name = f"{league}.zip"

    # Download ZIP
    response = requests.get(url)

    with open(zip_name, "wb") as f:
        f.write(response.content)

    # Temporary extraction folder
    extract_folder = f"temp_{league}"

    # Validate ZIP
    if zipfile.is_zipfile(zip_name):

        with zipfile.ZipFile(zip_name, "r") as zip_ref:
            zip_ref.extractall(extract_folder)

        print(f"{league} ZIP extracted.")

    else:

        print(f"Invalid ZIP for {league}. Skipping.")

        # Remove invalid file
        os.remove(zip_name)

        continue

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
    'kaggle datasets version -p raw_data --dir-mode zip -m "Automatic update"'
)

print("\nKaggle dataset updated.")
