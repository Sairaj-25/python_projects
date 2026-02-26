from pathlib import Path
from PIL import Image
import logging


# config

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR/"input_images"
OUTPUT_DIR = BASE_DIR/"optimized_images"


SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png", ".webp")

# Ecommerce image sizes for production

SIZES = {
    "thumbnail": (150, 150),
    "medium": (500, 500),
    "large": (1000, 1000),
}

WEBP_QUALITY = 85

# logging

logging.basicConfig(
    filename="image_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# functions

def validate_image(image_path: Path):
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True
    except Exception:
        logging.error(f"Invalid image: {image_path}")
        return False
    

def process_image(image_path: Path):
    try:
        with Image.open(image_path) as img:

            # convert torgb (webp compatibility)
            if img.mode in ("RGBA" , "P"):
                img = img.convert("RGB")

            for size_name, dimensions in SIZES.items():

                resized_img = img.copy()
                resized_img.thumbnail(dimensions)

                output_folder = OUTPUT_DIR / size_name
                output_folder.mkdir(parents=True, exist_ok=True)

                output_path = output_folder / f"{image_path.stem}.webp"

                resized_img.save(
                    output_path,
                    "webp",
                    quality=WEBP_QUALITY,
                    optimize=True,
                )

            logging.info(f"Processed: {image_path.name}")
            return True

    except Exception as e:
        logging.error(f"Failed processing {image_path.name}: {e}")
        return False


def run_pipeline():
    if not INPUT_DIR.exists():
        print("Input folder not found")
        return

    total_files = 0
    total_supported = 0
    total_success = 0
    total_failed = 0

    for image_path in INPUT_DIR.rglob("*"):
        if image_path.is_file():
            total_files += 1

            if image_path.suffix.lower() in SUPPORTED_FORMATS:
                total_supported += 1

                if validate_image(image_path):
                    if process_image(image_path):
                        total_success += 1
                    else:
                        total_failed +=1
                else:
                    total_failed += 1



    print("Image pipeline completed")
    print("\nImage Pipeline Report")
    print("----------------------")
    print("Total files found:", total_files)
    print("Supported images:", total_supported)
    print("Successfully processed:", total_success)
    print("Failed:", total_failed)


if __name__ == "__main__":
    run_pipeline()
