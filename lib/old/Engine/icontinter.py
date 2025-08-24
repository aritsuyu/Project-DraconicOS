from PIL import Image

# Open the image and convert it to RGBA mode
img = Image.open("icon.png").convert("RGBA")
pixels = img.getdata()

# Define the new color (Example: pure white)
new_color = (255, 255, 255)  # RGB

# Replace all non-transparent pixels with the new color
updated_pixels = [
    (new_color[0], new_color[1], new_color[2], a) if a > 0 else (r, g, b, a)
    for r, g, b, a in pixels
]

# Apply the changes and save the result
img.putdata(updated_pixels)
img.save("icon_white.png")
