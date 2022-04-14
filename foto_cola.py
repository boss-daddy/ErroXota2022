from PIL import Image, ImageFont, ImageDraw, ImageOps
import os
import textwrap

PAD = 1000
title_size = 125
conteudo_size = 100


def padronizar_conteudo(conteudo, width, e_titulo=False):
    wrapper = textwrap.TextWrapper(width=width)
    word_list = wrapper.wrap(text=conteudo)
    caption_new = ""
    for ii in word_list[:-1]:
        caption_new = caption_new + ii + "\n" + ("" if e_titulo else "\n")
    caption_new += word_list[-1]
    return caption_new


def adicionar_margem(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result


def junta_texto(img, titulo, conteudo, title, content):
    conteudo = padronizar_conteudo(conteudo, 38)
    titulo = padronizar_conteudo(titulo, 33, e_titulo=True)

    content = padronizar_conteudo(content, 38)
    title = padronizar_conteudo(title, 33, e_titulo=True)

    PAD = len(conteudo.split("\n") + titulo.split("\n")) * 200
    file = img.filename.split("/")

    img = adicionar_margem(img, 0, 2000, 0, 2000, (0, 0, 0))
    abs_size = img._size    
    draw = ImageDraw.Draw(img)
    title_font = ImageFont.truetype("/Library/Fonts/Heuristica-Italic.otf", title_size)
    conteudo_font = ImageFont.truetype(
        "/Library/Fonts/Heuristica-Regular.otf", conteudo_size
    )
    english_line_cnt = len(title.split("\n") + content.split('\n'))
    draw.text(
        (title_size // 2, title_size),
        titulo,
        (255, 255, 255),
        font=title_font,
        anchor="lm",
    )
    draw.text(
        (title_size // 2, title_size + 100 * len(titulo.split("\n"))),
        conteudo,
        (255, 200, 255),
        font=conteudo_font,
        anchor="la",
    )
    draw.text(
        (abs_size[0] - 2000 + title_size // 2, abs_size[1] - 100 * english_line_cnt),
        title,
        (255, 255, 255),
        font=title_font,
        anchor="lm",
    )
    draw.text(
        (abs_size[0] - 2000 + title_size // 2, abs_size[1] - 100 * english_line_cnt + title_size),
        content,
        (255, 200, 255),
        font=conteudo_font,
        anchor="la",
    )
    filename = "/".join(file[:-1]) + "/legendado/legendada_" + file[-1]
    img.save(filename)


def pega_legendas(main_path):
    legendas = {}
    captions = {}
    with open(main_path) as f:
        wait = 0
        key, val = "", ""
        fudase = list(f.readlines())
        for x in fudase:
            if "**" in x:
                wait = 1
                key = x[2:].strip()
            elif wait:
                assert "->" not in x
                val = x.strip()
                legendas[key] = val
                wait = 0
        for x in fudase:
            if "->" in x:
                wait = 1
                key = x[2:].strip()
            elif wait:
                assert "**" not in x
                val = x.strip()
                captions[key] = val
                wait = 0
    return [(*u, *j) for u, j in zip(legendas.items(), captions.items())]


def export_to_pdf():
    main_path = "/Users/mariopokemon/Desktop/erroxota/sachete_de_férias/ErroXota2022/legendado/"
    imagens = [
        Image.open(main_path + 'legendada_'+f)
        for f in sorted([k for k in os.listdir() if "rio" in k and ".jpg" in k])
    ]
    pdf_path = "/Users/mariopokemon/Desktop/erroxota/sachete_de_férias/ErroXota2022/RDJ2022.pdf"
    imagens[0].save(
        pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=imagens[1:]
    )

def constroi_fotos_legendadas():
    main_path = "/Users/mariopokemon/Desktop/erroxota/sachete_de_férias/ErroXota2022/"
    imagens = [
        Image.open(main_path +f)
        for f in sorted([k for k in os.listdir() if "rio" in k and ".jpg" in k])
    ]
    todo = pega_legendas(main_path + "rio_comentario.txt")
    for img, texto in list(zip(imagens, todo)):
        print(img.filename.split("/")[-1])
        junta_texto(img, *texto)

if __name__ == "__main__":
    constroi_fotos_legendadas()
    export_to_pdf()
