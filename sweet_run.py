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

Rect((380,80), (20,180))
  
]

waypoints= [
    (450,365),
    (365,449)
]
global waypoint_atual
waypoint_atual=0


PASSO_RAIO=10
RAIO_VISAO=150
def bola(maus, bons, obs, RAIO_VISAO):

    lx = bons.x-maus.x
    ly = maus.y-bons.y
    longe = math.hypot(lx,ly)

    if RAIO_VISAO < longe:
        return False


    if RAIO_VISAO > longe:
        return True
    
    if longe == 0:
        return True


    dir_x = dx / longe 
    dir_y = dy / longe


    andos =int(longe / PASSO_RAIO)

    for p in range (1 , passos):
        ponto_x = maus.x + dir_x * (p * PASSO_RAIO)
        ponto_y = maus.y + dir_y * (p * PASSO_RAIO)

        for retangulo in obs:
            if retangulo.collidepoint((ponto_x, ponto_y)):
                return False


    return True






    

def draw():

    screen.fill((255, 182, 193))

    if estado_jogo == "JOGANDO":
        for retangulo in obstaculos:
            screen.draw.rect(retangulo, "brown")



        
        eddy.draw()
        loopy.draw()
        crong.draw()
        petty.draw()
        moeda.draw()

        for i,wp in enumerate(waypoints):
            screen.draw.filled_circle(wp,14, "darkred")
        prox_wp = waypoints[(i+1)% len(waypoints)]
        screen.draw.line(wp, prox_wp, ("darkgreen"))

        screen.draw.circle((crong.x, crong.y),RAIO_VISAO, "olivedrab")
        screen.draw.circle((petty.x, petty.y),RAIO_VISAO, "olivedrab")

        if bola(crong,eddy,obstaculos, RAIO_VISAO):
            screen.draw.line((crong.x, crong.y), (eddy.x,eddy.y),"darkkhaki")

        if bola(petty,loopy,obstaculos, RAIO_VISAO):
            screen.draw.line((petty.x, petty.y), (loopy.x,loopy.y),"purple")
        
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
            color="palevioletred")

    
  
  
  
  
        





def colidiu(objeto1, objeto2):
    return objeto1.colliderect(objeto2)


def mover_inimigo(inimigo,heroi):
    global waypoint_atual
    vendo_heroi = bola(inimigo, heroi, obstaculos, RAIO_VISAO)

    if vendo_heroi==True:
        alvo_x= heroi.x
        alvo_y = heroi.y

    else:
        alvo_x, alvo_y = waypoints[waypoint_atual]
        longe_waypoints = math.hypot(alvo_x - inimigo.x, alvo_y - inimigo.y )
        if longe_waypoints  < 5:
            waypoint_atual = (waypoint_atual + 1 ) % 2 

    if alvo_x < inimigo.x:
        inimigo.x -= 1.0
    else:
        inimigo.x += 1.0

    if alvo_y < inimigo.y:
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