
import pygame
import pgzrun
import random

WIDTH = 800
HEIGHT = 600
TITLE = "sweet pororo run"
PONTOS_VITORIA = 100
VIDAS_INICIAIS = 3
VELOCIDADE_JOGADOR = 3
VELOCIDADE_BASE_INIMIGO = 0.8

TAM_INIMIGO = 80
TAM_ITEM = 36

HITBOX_MARGEM = 16


def redimensionar(ator, altura):
    """Redimensiona um Actor mantendo a proporção original (sem esticar)."""
    escala = altura / ator.height
    nova_largura = max(1, int(ator.width * escala))
    novo_surf = pygame.transform.smoothscale(ator._orig_surf, (nova_largura, altura))
    ator._orig_surf = ator._surf = novo_surf
    ator._update_pos()


def colidiu(a, b, margem=HITBOX_MARGEM):
    """Colisão com hitbox reduzida (mais justa que o retângulo da imagem inteira)."""
    rect_a = a._rect.inflate(-margem * 2, -margem * 2)
    rect_b = b._rect.inflate(-margem * 2, -margem * 2)
    return rect_a.colliderect(rect_b)


class Personagem(Actor):
    """Actor de jogador: guarda pontuação própria e pode 'atravessar' as bordas."""

    def __init__(self, image, pos):
        super().__init__(image, pos)
        self.pontos_coletados = 0

    def atravessar_bordas(self):
        if self.x > WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = WIDTH

        if self.y > HEIGHT:
            self.y = 0
        elif self.y < 0:
            self.y = HEIGHT


eddy = Personagem("eddy", (120, 120))
redimensionar(eddy, TAM_JOGADOR)

hanmang = Personagem("hanmang", (WIDTH - 120, 120))
redimensionar(hanmang, TAM_JOGADOR)

crong = Actor("crong", (700, 500))
redimensionar(crong, TAM_INIMIGO)

petty = Actor("petty", (100, 500))
redimensionar(petty, TAM_INIMIGO)

moeda = Actor("moeda", (400, 300))
redimensionar(moeda, TAM_ITEM)

moedas_extra = []

vidas = VIDAS_INICIAIS
estado_jogo = "JOGANDO"


def reiniciar_jogo():
    global pontos, vidas, estado_jogo
    pontos = 0
    vidas = VIDAS_INICIAIS
    eddy.pos = (120, 120)
    hanmang.pos = (WIDTH - 120, 120)
    crong.pos = (700, 500)
    petty.pos = (100, 500)
    moeda.pos = (400, 300)
    moedas_extra.clear()
    estado_jogo = "JOGANDO"


def mover_inimigo(inimigo, alvo):
    vel = VELOCIDADE_BASE_INIMIGO + (pontos // 20) * 0.4

    if inimigo.x < alvo.x:
        inimigo.x += vel
    elif inimigo.x > alvo.x:
        inimigo.x -= vel

    if inimigo.y < alvo.y:
        inimigo.y += vel
    elif inimigo.y > alvo.y:
        inimigo.y -= vel


def spawn_moeda_extra():
    if estado_jogo != "JOGANDO" or len(moedas_extra) >= 5:
        return
    nova = Actor("moeda", (random.randint(60, WIDTH - 60), random.randint(60, HEIGHT - 200)))
    redimensionar(nova, TAM_ITEM - 6)
    moedas_extra.append(nova)


clock.schedule_interval(spawn_moeda_extra, 3)

def draw():
    screen.fill((255, 182, 193))

    if estado_jogo == "JOGANDO":
        eddy.draw()
        hanmang.draw()
        crong.draw()
        petty.draw()
        moeda.draw()
        for m in moedas_extra:
            m.draw()

        screen.draw.text(f"Pontos: {pontos}/{PONTOS_VITORIA}", topleft=(20, 20),
                          fontsize=32, color="crimson", shadow=(1, 1), scolor="pink")

        cor_vida = "crimson" if vidas > 1 else "pink"
        texto_vidas = "Vidas: " + ("+" * vidas)
        screen.draw.text(texto_vidas, topright=(WIDTH - 20, 20),
                          fontsize=28, color=cor_vida, shadow=(1, 1), scolor="pink")

        nivel = (pontos // 20) + 1
        screen.draw.text(f"Nível de Ameaça: {nivel}", midbottom=(WIDTH // 2, HEIGHT - 15),
                          fontsize=22, color="pink")

        screen.draw.text("Eddy: WASD   |   Hanmang: Setas", midtop=(WIDTH // 2, 20),
                          fontsize=18, color="crimson")

    elif estado_jogo == "VITORIA":
        screen.draw.text("PARABÉNS, VOCÊS VENCERAM!", center=(WIDTH // 2, 220),
                          fontsize=56, color="brown", shadow=(2, 2), scolor="crimson")
        screen.draw.text(f"Pontuação Final: {pontos}", center=(WIDTH // 2, 300),
                          fontsize=32, color="indianred")
        screen.draw.text("Pressione [R] para Jogar Novamente", center=(WIDTH // 2, 400),
                          fontsize=26, color="pink")

    elif estado_jogo == "GAMEOVER":
        screen.draw.text("GAME OVER", center=(WIDTH // 2, 220),
                          fontsize=64, color="crimson", shadow=(2, 2), scolor="rgba(246 53 104 / 0.71)")
        screen.draw.text(f"Vocês fizeram {pontos} pontos antes de serem capturados!",
                          center=(WIDTH // 2, 300), fontsize=26, color="palevioletred")
        screen.draw.text("Pressione [R] para Tentar Novamente", center=(WIDTH // 2, 400),
                          fontsize=26, color="palevioletred")
def update():
    global pontos, vidas, estado_jogo

    if estado_jogo in ("VITORIA", "GAMEOVER"):
        if keyboard.r:
            reiniciar_jogo()
        return
        eddy.x -= VELOCIDADE_JOGADOR
    if keyboard.d:
        eddy.x += VELOCIDADE_JOGADOR
    if keyboard.w:
        eddy.y -= VELOCIDADE_JOGADOR
    if keyboard.s:
        eddy.y += VELOCIDADE_JOGADOR
    if keyboard.left:
        hanmang.x -= VELOCIDADE_JOGADOR
    if keyboard.right:
        hanmang.x += VELOCIDADE_JOGADOR
    if keyboard.up:
        hanmang.y -= VELOCIDADE_JOGADOR
    if keyboard.down:
        hanmang.y += VELOCIDADE_JOGADOR
    eddy.atravessar_bordas()
    hanmang.atravessar_bordas()
    mover_inimigo(crong, eddy)
    mover_inimigo(petty, hanmang)
    if colidiu(eddy, moeda) or colidiu(hanmang, moeda):
        moeda.x = random.randint(50, WIDTH - 50)
        moeda.y = random.randint(50, HEIGHT - 50)
        pontos += 1
        try:
            sounds.coleta.play()
        except Exception:
            pass
    for m in moedas_extra[:]:
        if colidiu(eddy, m) or colidiu(hanmang, m):
            moedas_extra.remove(m)
            pontos += 2
            try:
                sounds.coleta.play()
            except Exception:
                pass
    if pontos >= PONTOS_VITORIA:
        estado_jogo = "VITORIA"

    
    if colidiu(eddy, crong) or colidiu(hanmang, petty) or colidiu(eddy, petty) or colidiu(hanmang, crong):
        vidas -= 1
        if vidas <= 0:
            estado_jogo = "GAMEOVER"
        else:
            crong.x, crong.y = random.choice([60, WIDTH - 60]), random.choice([60, HEIGHT - 60])
            petty.x, petty.y = random.choice([60, WIDTH - 60]), random.choice([60, HEIGHT - 60])


pgzrun.go()

