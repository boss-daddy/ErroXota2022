from PIL import Image, ImageFont, ImageDraw, ImageOps
import os
images = [
    Image.open("/Users/mariopokemon/Desktop/rio/fotos/" + f)
    for f in sorted([k for k in os.listdir() if 'rio' in k])
]

pdf_path = "/Users/mariopokemon/Desktop/rio/fotos/mar26_mar27.pdf"
    
images[0].save(
    pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
)


def junta_texto():
    img = Image.open("SAMPLE-IN.png")
    img = ImageOps.expand(img, border=10, fill=(255,255,255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("FONTS/arial.ttf", 36)
    draw.text((0,0),"Sample Text",(0,255,255),font=font)
    img.save('sample-out.jpg')