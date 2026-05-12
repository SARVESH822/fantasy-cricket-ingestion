import requests
import zipfile
import os
import shutil

# League URLs
leagues = {
    "ipl": "https://cricsheet.org/downloads/ipl_json.zip",
    "bbl": "https://cricsheet.org/downloads/bbl_json.zip",
    "psl": "https://cricsheet.org/downloads/psl_json.zip",
    "cpl": "https://cricsheet.org/downloads/cpl_json.zip",
    "lpl": "https://cricsheet.org/downloads/lpl_json.zip",
    "bpl": "https://cricsheet.org/downloads/bpl_json.zip"
}

# Create folders
os.makedirs("raw_data", exist_ok=True)

for league, url in leagues.items():

    print(f"\nDownloading {league}...")

    zip_name = f"{league}.zip"

    # Download ZIP
    response = requests.get(url)

    with open(zip_name, "wb") as f:
        f.write(response.content)

    # Extract ZIP
    extract_folder = f"temp_{league}"

    with zipfile.ZipFile(zip_name, "r") as zip_ref:
        zip_ref.extractall(extract_folder)

    # Destination
    destination = os.path.join("raw_data", league)

    os.makedirs(destination, exist_ok=True)

    # Copy JSONs
    for file in os.listdir(extract_folder):

        if file.endswith(".json"):

            shutil.copy(
                os.path.join(extract_folder, file),
                os.path.join(destination, file)
            )

    # Cleanup
    os.remove(zip_name)
    shutil.rmtree(extract_folder)

print("\nAll JSON files downloaded.")

# Upload to Kaggle
os.system(
    'kaggle datasets version -p raw_data --dir-mode zip -m "Automatic update"'
)
print("\nKaggle dataset updated.")
