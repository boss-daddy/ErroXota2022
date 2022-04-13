from PIL import Image, ImageFont, ImageDraw, ImageOps
import os

PAD=1000
title_size = 125
conteudo_size = 100

def padronizar_conteudo(conteudo,img_size):
    lineas = []
    inword = 0 
    linea = ""
    # how many chars per line are possible?
    gross_size = img_size[0] // conteudo_size
    gross_size *=2
    for i,c in enumerate(conteudo):
        linea += c
        if i and i%gross_size==0:
            lineas.append(linea)
            linea = ""
    lineas.append(conteudo[-(len(conteudo)%gross_size-1):])
    print(lineas)
    lineas = '\n'.join(lineas)
    print(lineas)
    return lineas



def junta_texto(img, titulo, conteudo):
    conteudo = padronizar_conteudo(conteudo,img._size)
    file = img.filename.split('/')  
    img = ImageOps.pad(img, (img._size[0],img._size[1]+PAD))
    draw = ImageDraw.Draw(img)
    title_font = ImageFont.truetype("/Library/Fonts/Heuristica-Regular.otf", title_size)
    conteudo_font = ImageFont.truetype("/Library/Fonts/Heuristica-Regular.otf", conteudo_size)
    draw.text((img._size[0]//2,title_size),titulo,(255,255,255),font=title_font,anchor="mm")
    draw.text((img._size[0]//2,title_size*2),conteudo,(255,0,255),font=conteudo_font,anchor="ma")
    filename = ('/'.join(file[:-1]) + '/legendado/legendada_' + file[-1])
    img.save(filename)

def pega_legendas(main_path):
    legendas = {}
    with open(main_path) as f:
        wait = 0
        key,val='',''
        for x in f.readlines():
            if 'RDJ 2022' in x:
                wait = 1
                key = x.strip()
            elif wait:
                assert '->' not in x
                val = x.strip()
                legendas[key] = val
                wait = 0
    return legendas

if __name__=='__main__':
    main_path = "/Users/mariopokemon/Desktop/erroxota/fotos/"
    images = [
        Image.open(main_path + f)
        for f in sorted([k for k in os.listdir() if 'rio' in k and '.jpg' in k])
    ]
    leg = pega_legendas(main_path+'/rio_comentario.txt')
    # pdf_path = "/Users/mariopokemon/Desktop/rio/fotos/mar26_mar27.pdf"
    # images[0].save(
    #     pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
    # )
    texto = list(leg.items())[0]
    print(texto)
    junta_texto(images[0], *texto)
