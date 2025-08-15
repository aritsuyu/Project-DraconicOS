from PIL import Image

# Define o quanto de "preto próximo" você quer remover
TOLERANCIA = 30  # 0 = só preto puro, 30 = preto e tons bem escuros

img = Image.open("icon.png").convert("RGBA")
data = img.getdata()
new_data = []

for item in data:
    r, g, b, a = item
    if r <= TOLERANCIA and g <= TOLERANCIA and b <= TOLERANCIA:
        # transforma em transparente
        new_data.append((0, 0, 0, 0))
    else:
        new_data.append(item)

img.putdata(new_data)
img.save("output.png")
