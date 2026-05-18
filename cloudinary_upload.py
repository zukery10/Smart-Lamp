import cloudinary
import cloudinary.uploader
import os

# Configure Cloudinary connection (fill these in from your dashboard)
cloudinary.config(
    cloud_name="dlci24gt7",   # e.g. " dhnsqvfn8p"
    api_key="889738317595178",         # e.g. "123456789012345"
    api_secret="BEtuE3PjkdN8b_km8VTphgtv5Wo",   # long secret string
)
# Choose the local image file to upload
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
IMAGE_PATH = os.path.join(STATIC_DIR, "last_visitor.jpg")

# Upload the image. Returns a public URL for the image 
def upload_image(image_path,
                 folder = "smart-doorbell-lab",
                 public_id = "last_visitor"):
    result = cloudinary.uploader.upload(
        image_path,
        folder="Smart-Lamp",  # optional logical folder name
        public_id="last_visitor",      # <-- always upload with same ID
        overwrite=True,                # <-- overwrite existing image
        invalidate=True,               # <-- (optional) clear cached copies
    )
    url = result["secure_url"]
    #print(url)
    return url

def main():
    url = upload_image(IMAGE_PATH)
    print("Upload complete.")
    print(f"Public URL:{url}")


