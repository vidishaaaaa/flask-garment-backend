from PIL import Image, ImageChops
import os

# ==== PATHS ====
garment_path = "assets/wts.png"           # Transparent PNG with garment details
fabric_path = "uploads/f3.jpg"              # Fabric uploaded by user
output_dir = "output"
output_file = "shirt_with_fabric.png"
output_path = os.path.join(output_dir, output_file)

def apply_fabric_to_garment(garment_path, fabric_path, output_path):
    
    garment = Image.open(garment_path).convert("RGBA")
    fabric = Image.open(fabric_path).convert("RGBA")

# ==== RESIZE FABRIC TO MATCH GARMENT ====
    fabric_resized = fabric.resize(garment.size)

# ==== BLEND FABRIC WITH GARMENT (PRESERVE DETAILS) ====
    blended = ImageChops.multiply(fabric_resized, garment)

# ==== PRESERVE ORIGINAL SHIRT SHAPE (MASK) ====
    alpha_mask = garment.getchannel("A")  # Get transparency mask
    blended.putalpha(alpha_mask)

# ==== SAVE RESULT ====
    os.makedirs(output_dir, exist_ok=True)
    blended.save(output_path)

    return output_path




