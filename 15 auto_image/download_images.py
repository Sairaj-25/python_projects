import os
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from rapidfuzz import process, fuzz
from tqdm import tqdm

# ==========================================
# CONFIG
# ==========================================

SHOP_CSV = "shop_product.csv"
BIGBASKET_CSV = "BigBasket.csv"

MEDIA_FOLDER = "media/products"
BASE_URL = "https://www.bigbasket.com"

RESIZE_SIZE = (300, 300)
MIN_MATCH_SCORE = 80
TIMEOUT = 15

os.makedirs(MEDIA_FOLDER, exist_ok=True)

# ==========================================
# LOAD CSV FILES
# ==========================================

print("📂 Loading CSV files...")

shop_df = pd.read_csv(SHOP_CSV)
bb_df = pd.read_csv(BIGBASKET_CSV)

# Normalize column names
shop_df.columns = shop_df.columns.str.strip().str.lower()
bb_df.columns = bb_df.columns.str.strip().str.lower()

required_shop_cols = {"name", "image"}
required_bb_cols = {"productname", "image_url"}


# Normalize names for matching
shop_df["name"] = shop_df["name"].astype(str).str.strip().str.lower()
bb_df["productname"] = bb_df["productname"].astype(str).str.strip().str.lower()

# ==========================================
# MATCHING FUNCTION
# ==========================================

def find_best_match(shop_name):
    # 1️⃣ Exact match
    exact_matches = bb_df[bb_df["productname"] == shop_name]
    if not exact_matches.empty:
        return exact_matches.index[0], 100

    # 2️⃣ Contains match
    contains_matches = bb_df[bb_df["productname"].str.contains(shop_name, na=False)]
    if not contains_matches.empty:
        return contains_matches.index[0], 95

    # 3️⃣ Fuzzy fallback
    match = process.extractOne(
        shop_name,
        bb_df["productname"].tolist(),
        scorer=fuzz.token_sort_ratio
    )

    if match:
        matched_name, score, _ = match
        index = bb_df[bb_df["productname"] == matched_name].index[0]
        return index, score

    return None, 0


# ==========================================
# DOWNLOAD FUNCTION
# ==========================================

def download_and_resize(image_url, save_path):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = requests.get(image_url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content)).convert("RGB")
        img = img.resize(RESIZE_SIZE)

        img.save(save_path, format="WEBP", quality=85)

        return True

    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


# ==========================================
# MAIN PROCESS
# ==========================================

print("🔎 Matching & Downloading Images...")

success_count = 0
failed_count = 0
skipped_count = 0

for _, row in tqdm(shop_df.iterrows(), total=len(shop_df)):

    shop_name = row["name"]
    image_filename = str(row["image"]).strip()

    if not image_filename or image_filename.lower() == "nan":
        skipped_count += 1
        continue

    final_path = os.path.join(MEDIA_FOLDER, image_filename)

    # Skip if already exists
    if os.path.exists(final_path):
        skipped_count += 1
        continue

    index, score = find_best_match(shop_name)

    if index is None or score < MIN_MATCH_SCORE:
        print(f"⚠ No good match for: {shop_name} (score: {score})")
        failed_count += 1
        continue

    image_url = bb_df.loc[index, "image_url"]

    if pd.isna(image_url) or not str(image_url).strip():
        print(f"⚠ No image URL for: {shop_name}")
        failed_count += 1
        continue

    image_url = str(image_url)

    # Fix relative URLs
    if image_url.startswith("/"):
        image_url = BASE_URL + image_url

    print(f"📥 Downloading: {shop_name} (score: {score})")

    success = download_and_resize(image_url, final_path)

    if success:
        success_count += 1
    else:
        failed_count += 1


# ==========================================
# SUMMARY
# ==========================================

print("\n🎉 PROCESS COMPLETED")
print(f"✅ Success: {success_count}")
print(f"⚠ Failed: {failed_count}")
print(f"⏭ Skipped: {skipped_count}")
