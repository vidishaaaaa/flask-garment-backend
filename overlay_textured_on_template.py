from PIL import Image

def overlay_on_template(base_img_path, overlay_img_path, output_path):
    base = Image.open(base_img_path).convert("RGBA")
    overlay = Image.open(overlay_img_path).convert("RGBA")
    overlay = overlay.resize(base.size)

    composite = Image.alpha_composite(base, overlay)
    composite.save(output_path)
    composite.show()

if __name__ == "__main__":
    base_img = "static/shirt_template.png"             # Transparent shirt outline
    overlay_img = "static/fabric_texture.jpg"     # From Step 2
    output_img = "static/final_preview.png"

    overlay_on_template(base_img, overlay_img, output_img)
