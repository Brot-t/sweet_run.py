import pygame, pgzrun, random,os,math
from PIL import Image

WIDTH = 800
HEIGHT = 600
TITLE = "sweet_run"

VIDAS_INICIAIS = 3
VELOCIDADE_JOGADOR = 5
PONTOS_VITORIA = 20
TAM_ITEM = 35

class Sumir(Actor):

    def __init__(self, image):
        super().__init__(image)
        self.ponto = 0

    def parede(self):
        if self.x >= 790:
            self.x -= 200
        if self.x <= 10:
            self.x += 200
        if self.y >= 590:
            self.y -= 200
        if self.y <= 10:
            self.y += 200

    def pontos(self):
        self.ponto += 1


def redimensionar_arquivo(nome_imagem, nova_largura, nova_altura):

    caminho_original = f"images/{nome_imagem}.png"
    caminho_redimensionado = f"images/{nome_imagem}_{nova_largura}x{nova_altura}_r.png"
    precisa_gerar = True
    if os.path.exists(caminho_redimensionado):
        with Image.open(caminho_redimensionado) as img_existente:
            if img_existente.size == (nova_largura, nova_altura):
                precisa_gerar = False
    if precisa_gerar:
        img = Image.open(caminho_original).convert("RGBA")
        alpha = img.split()[-1]
        mascara = alpha.point(lambda p: 255 if p > 25 else 0)
        bbox = mascara.getbbox()

        if bbox:
            img = img.crop(bbox)

        img = img.resize((nova_largura, nova_altura), Image.LANCZOS)
        img.save(caminho_redimensionado)

    return f"{nome_imagem}_{nova_largura}x{nova_altura}_r"


eddy = Sumir(redimensionar_arquivo("eddy", 100, 100))
loopy = Sumir(redimensionar_arquivo("loopy", 100, 100))
crong = Actor(redimensionar_arquivo("crong", 100, 100))
moeda = Actor(redimensionar_arquivo("moeda", 35, 35))
petty = Actor(redimensionar_arquivo("petty", 100, 100))

moedas_extra = []

pontos = 0
vidas = VIDAS_INICIAIS
estado_jogo = "JOGANDO"
HITCODESPHERE=10
RAIO_VISAO=150

obstaculos=[



]



def bola(maus, bons, obs, RAIO_VISAO):

    lx = bons.x-maus.x
    ly = maus.y-bons.y
    longe = math.hypot(lx,ly)




    if RAIO_VISAO < longe:
        return False
    






    

def draw():

    screen.fill((255, 182, 193))

    if estado_jogo == "JOGANDO":

        eddy.draw()
        loopy.draw()
        crong.draw()
        petty.draw()
        moeda.draw()

        for m in moedas_extra:
            m.draw()

        screen.draw.text(
            f"Pontos: {pontos}/{PONTOS_VITORIA}",
            topleft=(20, 20),
            fontsize=32,
            color="crimson",
            shadow=(1, 1),
            scolor="pink"
        )

        cor_vida = "crimson" if vidas > 1 else "pink"
        texto_vidas = "Vidas: " + ("+" * vidas)

        screen.draw.text(
            texto_vidas,
            topright=(WIDTH - 20, 20),
            fontsize=28,
            color=cor_vida,
            shadow=(1, 1),
            scolor="pink"
        )

        nivel = (pontos // 20) + 1

        screen.draw.text(
            f"Nível de Ameaça: {nivel}",
            midbottom=(WIDTH // 2, HEIGHT - 15),
            fontsize=22,
            color="pink"
        )

        screen.draw.text(
            "Eddy: WASD   |   loopy: Setas",
            midtop=(WIDTH // 2, 20),
            fontsize=18,
            color="crimson"
        )

    elif estado_jogo == "VITORIA":

        screen.draw.text(
            "PARABÉNS, VOCÊS VENCERAM!",
            center=(WIDTH // 2, 220),
            fontsize=56,
            color="brown",
            shadow=(2, 2),
            scolor="crimson"
        )

        screen.draw.text(
            f"Pontuação Final: {pontos}",
            center=(WIDTH // 2, 300),
            fontsize=32,
            color="indianred"
        )

        screen.draw.text(
            "Pressione [R] para Jogar Novamente",
            center=(WIDTH // 2, 400),
            fontsize=26,
            color="pink"
        )

    elif estado_jogo == "GAMEOVER":

        screen.draw.text(
            "GAME OVER",
            center=(WIDTH // 2, 220),
            fontsize=64,
            color="crimson",
            shadow=(2, 2),
            scolor="pink"
        )

        screen.draw.text(
            f"Vocês fizeram {pontos} pontos antes de serem capturados!",
            center=(WIDTH // 2, 300),
            fontsize=26,
            color="palevioletred"
        )

        screen.draw.text(
            "Pressione [R] para Tentar Novamente",
            center=(WIDTH // 2, 400),
            fontsize=26,
            color="palevioletred"
        )


def colidiu(objeto1, objeto2):
    return objeto1.colliderect(objeto2)


def mover_inimigo(inimigo, alvo):

    if alvo.x < inimigo.x:
        inimigo.x -= 1.0
    else:
        inimigo.x += 1.0

    if alvo.y < inimigo.y:
        inimigo.y -= 1.0
    else:
        inimigo.y += 1.0


def spawn_moeda_extra():

    if estado_jogo != "JOGANDO" or len(moedas_extra) >= 5:
        return

    nova = Actor(
        redimensionar_arquivo("moeda", TAM_ITEM - 6, TAM_ITEM - 6)
    )

    nova.x = random.randint(60, WIDTH - 60)
    nova.y = random.randint(60, HEIGHT - 200)

    moedas_extra.append(nova)


def reiniciar_jogo():

    global pontos, vidas, estado_jogo

    pontos = 0
    vidas = VIDAS_INICIAIS
    estado_jogo = "JOGANDO"

    eddy.x = 400
    eddy.y = 200

    loopy.x = 400
    loopy.y = 400

    crong.x = 100
    crong.y = 100

    petty.x = 700
    petty.y = 500

    moeda.x = random.randint(50, WIDTH - 50)
    moeda.y = random.randint(50, HEIGHT - 50)

    moedas_extra.clear()


def update():

    global pontos, vidas, estado_jogo

    if estado_jogo in ("VITORIA", "GAMEOVER"):

        if keyboard.r:
            reiniciar_jogo()

        return

    if keyboard.a:
        eddy.x -= VELOCIDADE_JOGADOR

    if keyboard.d:
        eddy.x += VELOCIDADE_JOGADOR

    if keyboard.w:
        eddy.y -= VELOCIDADE_JOGADOR

    if keyboard.s:
        eddy.y += VELOCIDADE_JOGADOR

    if keyboard.left:
        loopy.x -= VELOCIDADE_JOGADOR

    if keyboard.right:
        loopy.x += VELOCIDADE_JOGADOR

    if keyboard.up:
        loopy.y -= VELOCIDADE_JOGADOR

    if keyboard.down:
        loopy.y += VELOCIDADE_JOGADOR

    eddy.parede()
    loopy.parede()

    mover_inimigo(crong, eddy)
    mover_inimigo(petty, loopy)

    if colidiu(eddy, moeda) or colidiu(loopy, moeda):

        moeda.x = random.randint(50, WIDTH - 50)
        moeda.y = random.randint(50, HEIGHT - 50)

        pontos += 1

        try:
            sounds.coleta.play()
        except Exception:
            pass

    for m in moedas_extra[:]:

        if colidiu(eddy, m) or colidiu(loopy, m):

            moedas_extra.remove(m)
            pontos += 2


    if pontos >= PONTOS_VITORIA:
        estado_jogo = "VITORIA"

    if (
        colidiu(eddy, crong)
        or colidiu(loopy, petty)
        or colidiu(eddy, petty)
        or colidiu(loopy, crong)
    ):

        vidas -= 1

        if vidas <= 0:
            estado_jogo = "GAMEOVER"

        else:

            crong.x, crong.y = random.choice(
                [60, WIDTH - 60]
            ), random.choice(
                [60, HEIGHT - 60]
            )

            petty.x, petty.y = random.choice(
                [60, WIDTH - 60]
            ), random.choice(
                [60, HEIGHT - 60]
            )


clock.schedule_interval(spawn_moeda_extra, 3)

pgzrun.go()