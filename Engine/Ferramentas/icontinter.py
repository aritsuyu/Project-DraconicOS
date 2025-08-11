from PIL import Image

# Abre a imagem
img = Image.open("icone.png").convert("RGBA")
pixels = img.getdata()

# Define a nova cor (exemplo: verde vibrante)
nova_cor = (255, 255, 255)  # RGB 

novos_pixels = []
for r, g, b, a in pixels:
    if a > 0:  # Se não for transparente
        novos_pixels.append((nova_cor[0], nova_cor[1], nova_cor[2], a))
    else:
        novos_pixels.append((r, g, b, a))

# Aplica as mudanças
img.putdata(novos_pixels)
img.save("icone_verde.png")
