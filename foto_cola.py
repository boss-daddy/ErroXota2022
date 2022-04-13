from PIL import Image, ImageFont, ImageDraw, ImageOps
import os
import textwrap

PAD=1000
title_size = 125
conteudo_size = 100

def padronizar_conteudo(conteudo,width):
    wrapper = textwrap.TextWrapper(width=width) 
    word_list = wrapper.wrap(text=conteudo) 
    caption_new = ''
    for ii in word_list[:-1]:
        caption_new = caption_new + ii + '\n'
    caption_new += word_list[-1]
    return(caption_new)

    # lineas = []
    # inword = 0 
    # linea = ""
    # # how many chars per line are possible?
    # gross_size = img_size[0] // conteudo_size
    # gross_size *=2
    # for i,c in enumerate(conteudo):
    #     linea += c
    #     if i and i%gross_size==0:
    #         lineas.append(linea)
    #         linea = ""
    # lineas.append(conteudo[-(len(conteudo)%gross_size-1):])
    # # print(lineas)
    # lineas = '\n'.join(lineas)
    # # print(lineas)
    # return lineas



def junta_texto(img, titulo, conteudo):
    conteudo = padronizar_conteudo(conteudo, 60)
    print(titulo)
    titulo = padronizar_conteudo(titulo, 50)
    print(titulo)
    PAD = len(conteudo.split('\n')+titulo.split('\n'))*200
    file = img.filename.split('/')  
    img = ImageOps.pad(img, (img._size[0],img._size[1]+PAD))
    draw = ImageDraw.Draw(img)
    title_font = ImageFont.truetype("/Library/Fonts/Heuristica-Regular.otf", title_size)
    conteudo_font = ImageFont.truetype("/Library/Fonts/Heuristica-Regular.otf", conteudo_size)
    draw.text((img._size[0]//2,title_size),titulo,(255,255,255),font=title_font,anchor="mm")
    draw.text((img._size[0]//2,title_size+40),conteudo,(255,200,255),font=conteudo_font,anchor="ma")
    filename = ('/'.join(file[:-1]) + '/legendado/legendada_' + file[-1])
    img.save(filename)

def pega_legendas(main_path):
    legendas = {}
    with open(main_path) as f:
        wait = 0
        key,val='',''
        for x in f.readlines():
            if '**' in x:
                wait = 1
                key = x[3:].strip()
            elif wait:
                assert '->' not in x
                val = x.strip()
                legendas[key] = val
                wait = 0
    return legendas

if __name__=='__main__':
    main_path = "/Users/mariopokemon/Desktop/erroxota/fotos/"
    imagens = [
        Image.open(main_path + f)
        for f in sorted([k for k in os.listdir() if 'rio' in k and '.jpg' in k])
    ]
    leg = pega_legendas(main_path+'/rio_comentario.txt')
    # pdf_path = "/Users/mariopokemon/Desktop/rio/fotos/mar26_mar27.pdf"
    # images[0].save(
    #     pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
    # )
    for img,texto in list(zip(imagens,list(leg.items()))):
        print(img.filename.split('/')[-1])
        junta_texto(img, *texto)
