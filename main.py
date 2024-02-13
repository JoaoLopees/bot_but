import pyautogui as pg
from PIL import Image

IMG_SUPERIOR = [(1648, 678), (1716,680), (1788, 682)]
IMG_INFERIOR = [(1649, 748), (1716, 750), (1777, 750)]
DESAFIO_REGIAO = (1611, 718, 220, 61)
BOTAO_CONFIRMAR = (1777,803)

def tirar_foto(posicao):
    x, y = posicao
    foto =  pg.screenshot(region=(x - 25, y - 23, 50, 50))
    return foto

def rotacionar_foto(imagem, grau):
    print(grau)
    imagem_rotacionada = imagem.rotate(grau, Image.BICUBIC)
    return imagem_rotacionada

def procurar_imagem(caminho_da_imagem, my_confidence, my_region=None):
    box = pg.locateOnScreen(caminho_da_imagem, confidence=my_confidence, region=my_region)
    if box: 
        return box
    return None



while True:
    captcha_na_tela = procurar_imagem('inicio_captcha.png', 0.8)
    imagem_encontrada = []
    imagem_nao_encontrada = []
    if captcha_na_tela != None:
        for posicao in IMG_SUPERIOR:
            imagem_carregada = tirar_foto(posicao)
            imagem_procurada = False
            for grau in range(361):
                imagem_rotacionada = rotacionar_foto(imagem_carregada, grau)
                box = procurar_imagem(imagem_rotacionada, 0.6, my_region=DESAFIO_REGIAO)
                if box:
                    print('BOX - IMAGEM ENCONTRADA', box)
                    x, y = pg.center(box)
                    imagem_encontrada.append([posicao, (x, y)])
                    imagem_procurada = True
                    break
            if not imagem_procurada:
                imagem_nao_encontrada.append(posicao)
        for posicao in imagem_encontrada:
            pg.moveTo(posicao[0])
            pg.click()
            pg.sleep(0.5)            
            pg.moveTo(posicao[1])
            pg.click()
            pg.sleep(0.5)
        if len(imagem_nao_encontrada) > 0:
            for posicao in imagem_nao_encontrada:
                pg.moveTo(posicao)
                pg.click()
                pg.sleep(0.5)
                for tentativa in IMG_INFERIOR:
                    pg.moveTo(tentativa)
                    pg.click()
                    pg.sleep(0.5)
        pg.moveTo(BOTAO_CONFIRMAR)
        pg.click

