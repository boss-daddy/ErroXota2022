from PIL import Image
import os
images = [
    Image.open("/Users/mariopokemon/Desktop/rio/fotos/" + f)
    for f in sorted([k for k in os.listdir() if 'rio' in k])
]

pdf_path = "/Users/mariopokemon/Desktop/rio/fotos/mar26_mar27.pdf"
    
images[0].save(
    pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
)
