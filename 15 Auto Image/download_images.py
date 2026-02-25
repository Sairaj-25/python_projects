import os
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from rapidfuzz import process, fuzz
from tqdm import tqdm

# ================= CONFIG =================
SHOP_PRODUCT_CSV = "shop_product.csv"
SHOP_CATEGORY_CSV = "shop_category.csv"
BIGBASKET_CSV = "bigbasket.csv"

MEDIA_FOLDER = "media/products"
BASE_URL = "https://www.bigbasket.com"

RESIZE_SIZE = (300, 300)
MIN_MATCH_SCORE = 90
TIMEOUT = 15
MAX_IMAGES_PER_PRODUCT = 5

os.makedirs(MEDIA_FOLDER, exist_ok=True)

print("Loading CSV files...")

# ================= LOAD FILES =================
shop_product_df = pd.read_csv(SHOP_PRODUCT_CSV)
shop_category_df = pd.read_csv(SHOP_CATEGORY_CSV)
bb_df = pd.read_csv(BIGBASKET_CSV)

# Normalize column names
shop_product_df.columns = shop_product_df.columns.str.strip().str.lower()
shop_category_df.columns = shop_category_df.columns.str.strip().str.lower()
bb_df.columns = bb_df.columns.str.strip().str.lower()

# Normalize text fields
shop_product_df["name"] = shop_product_df["name"].astype(str).str.strip().str.lower()
shop_category_df["name"] = shop_category_df["name"].astype(str).str.strip().str.lower()
bb_df["productname"] = bb_df["productname"].astype(str).str.strip().str.lower()
bb_df["category"] = bb_df["category"].astype(str).str.strip().str.lower()

# ================= JOIN PRODUCTS WITH CATEGORY =================
# Merge product with category table using category_id
shop_df = shop_product_df.merge(
    shop_category_df,
    left_on="category_id",
    right_on="id",
    how="left",
    suffixes=("", "_category")
)

# Rename category name column
shop_df.rename(columns={"name_category": "category_name"}, inplace=True)

print("Join completed.")


# ================= MATCH FUNCTION =================
def find_matches(shop_name, shop_category):

    # Filter bigbasket by category name
    category_filtered = bb_df[
        bb_df["category"].str.contains(str(shop_category), na=False)
    ]

    if category_filtered.empty:
        category_filtered = bb_df

    matches = []

    # Exact match
    exact_matches = category_filtered[
        category_filtered["productname"] == shop_name
    ]
    for idx in exact_matches.index:
        matches.append((idx, 100))

    # Contains match
    contains_matches = category_filtered[
        category_filtered["productname"].str.contains(shop_name, na=False)
    ]
    for idx in contains_matches.index:
        matches.append((idx, 90))

    # Fuzzy match
    fuzzy_results = process.extract(
        shop_name,
        category_filtered["productname"].tolist(),
        scorer=fuzz.token_sort_ratio,
        score_cutoff=MIN_MATCH_SCORE
    )

    for matched_name, score, _ in fuzzy_results:
        index = category_filtered[
            category_filtered["productname"] == matched_name
        ].index[0]
        matches.append((index, score))

    return list(set(matches))


# ================= DOWNLOAD FUNCTION =================
def download_and_resize(image_url, save_path):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(image_url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content)).convert("RGB")
        img = img.resize(RESIZE_SIZE)
        img.save(save_path, format="WEBP", quality=85)

        return True

    except Exception as e:
        print(f"Download Failed: {image_url} | Error: {e}")
        return False


# ================= MAIN PROCESS =================
print("🔎 Matching & Downloading Images...")

success_count = 0
failed_count = 0

for _, row in tqdm(shop_df.iterrows(), total=len(shop_df)):

    shop_name = row["name"]
    shop_category = row["category_name"]
    image_filename = str(row["image"]).strip()

    if not image_filename or image_filename.lower() == "nan":
        continue

    name_without_ext = os.path.splitext(image_filename)[0]

    matches = find_matches(shop_name, shop_category)

    if not matches:
        print(f"⚠ No matches found for: {shop_name}")
        continue

    matches = matches[:MAX_IMAGES_PER_PRODUCT]

    for i, (index, score) in enumerate(matches):

        image_url = bb_df.loc[index, "image_url"]

        if pd.isna(image_url) or not str(image_url).strip():
            continue

        image_url = str(image_url)

        if image_url.startswith("/"):
            image_url = BASE_URL + image_url

        new_filename = f"{name_without_ext}_{i}.webp"
        final_path = os.path.join(MEDIA_FOLDER, new_filename)

        if os.path.exists(final_path):
            continue

        print(f"Downloading: {shop_name} | score={score}")

        success = download_and_resize(image_url, final_path)

        if success:
            success_count += 1
        else:
            failed_count += 1

print("\nPROCESS COMPLETED")
print(f"Success: {success_count}")
print(f"Failed: {failed_count}")
