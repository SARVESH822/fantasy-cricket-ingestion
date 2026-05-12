import requests
import zipfile
import os
import shutil

leagues = {

    # IPL
    "ipl": "https://cricsheet.org/downloads/ipl_json.zip",

    # Big Bash League
    "bbl": "https://cricsheet.org/downloads/bbl_json.zip",

    # Pakistan Super League
    "psl": "https://cricsheet.org/downloads/psl_json.zip",

    # Caribbean Premier League
    "cpl": "https://cricsheet.org/downloads/cpl_json.zip",

    # Bangladesh Premier League
    "bpl": "https://cricsheet.org/downloads/bpl_json.zip",

    # Lanka Premier League
    "lpl": "https://cricsheet.org/downloads/lpl_json.zip",

    # Vitality Blast (England)
    "blast": "https://cricsheet.org/downloads/vitalityblast_json.zip",

    # Syed Mushtaq Ali Trophy
    "smat": "https://cricsheet.org/downloads/sma_male_json.zip",

    # International T20s
    "t20i": "https://cricsheet.org/downloads/t20s_json.zip",

    # SA20
    "sa20": "https://cricsheet.org/downloads/sa20_male_json.zip",

    # ILT20
    "ilt20": "https://cricsheet.org/downloads/ilt20_male_json.zip",

    # The Hundred
    "hundred": "https://cricsheet.org/downloads/hundred_male_json.zip",

    # Super Smash (New Zealand)
    "supersmash": "https://cricsheet.org/downloads/super_smash_male_json.zip",

    # T10 leagues
    "abu_dhabi_t10": "https://cricsheet.org/downloads/abt10_male_json.zip"
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
