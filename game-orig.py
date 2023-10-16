# Biblioteca PyGame
import pygame
# Biblioteca para geracao de numeros pseudoaleatorios
import random
# Modulo da biblioteca PyGame que permite o acesso as teclas utilizadas
from pygame.locals import *

# Classe que representar o jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        image_player = pygame.image.load("freeza-removebg-preview.png")
        scaled_image_player = pygame.transform.scale(image_player, (image_player.get_width() / 5, image_player.get_height() / 5))
        
        super(Player, self).__init__()
        self.surf = scaled_image_player
        self.rect = self.surf.get_rect()

    # Determina acao de movimento conforme teclas pressionadas
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -1)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 1)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-1, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(1, 0)

        # Mantem o jogador nos limites da tela do jogo
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600

# Classe que representa os inimigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        image_inimigo = pygame.image.load("poder rosa.png")
        scaled_image_inimigo = pygame.transform.scale(image_inimigo, (image_inimigo.get_width() / 3, image_inimigo.get_height() / 5))

        super(Enemy, self).__init__()
        self.surf = scaled_image_inimigo
        self.rect = self.surf.get_rect( #Coloca na extrema direita (entre 820 e 900) e sorteia sua posicao em relacao a coordenada y (entre 0 e 600)
            center=(random.randint(820, 900), random.randint(0, 600))
            
        )
        self.speed = random.uniform(1, 1) #Sorteia sua velocidade, entre 1 e 15

    # Funcao que atualiza a posiçao do inimigo em funcao da sua velocidade e termina com ele quando ele atinge o limite esquerdo da tela (x < 0)
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Inicializa pygame
pygame.init()

# Cria a tela com resolução 800x600px
screen = pygame.display.set_mode((800, 600))

# Cria um evento para adicao de inimigos
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 700) #Define um intervalo para a criacao de cada inimigo (milisegundos)

# Cria o jogador (nosso retangulo)
player = Player()

# Define o plano de fundo
x=800
y=600
screen = pygame.display.set_mode((x,y))
pygame.display.set_caption("Torneio do poder")

backgroud = pygame.image.load ("areana2.jpeg")
backgroud = pygame.transform.scale(backgroud, (x, y))



#adicionar vida
total_lives = 3
remaining_lives = total_lives
font = pygame.font.Font(None, 38)  # Escolha a fonte e o tamanho desejados
total_lives_text = font.render(f"LIVE: {total_lives}", True, (196, 0, 255))  # Renderiza o texto da pontuação




#criar tela de game over 

game_over_surface = pygame.Surface((800, 600))
game_over_surface.fill((0, 0, 0))  # Preencha a superfície com uma cor de fundo (neste caso, preto)

game_over_font = pygame.font.Font(None, 64)
game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
game_over_rect = game_over_text.get_rect(center=(400, 300))



enemies = pygame.sprite.Group() #Cria o grupo de inimigos
all_sprites = pygame.sprite.Group() #Cria o grupo de todos os Sprites
all_sprites.add(player) #Adicionar o player no grupo de todos os Sprites


running = True #Flag para controle do jogo

while running:

     #Laco para verificacao do evento que ocorreu
    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: #Verifica se a tecla ESC foi pressionada
                running = False
        elif event.type == QUIT: #Verifica se a janela foi fechada
            running = False
        elif(event.type == ADDENEMY): #Verifica se e o evento de criar um inimigo
            new_enemy = Enemy() #Cria um novo inimigo
            enemies.add(new_enemy) #Adiciona o inimigo no grupo de inimigos
            all_sprites.add(new_enemy) #Adiciona o inimigo no grupo de todos os Sprites
    rel_x = x % backgroud.get_rect().width
    screen.blit(backgroud, (0, 0)) #Atualiza a exibicao do plano de fundo do jogo (neste caso nao surte efeito)
    screen.blit(backgroud, (rel_x - backgroud.get_rect().width,0))#cria background

    if rel_x < 800:
         screen.blit(backgroud, (rel_x, 0))

         x-=0.2
    screen.blit(total_lives_text, (10, 10))  # Define a posição do texto na tela
    pressed_keys = pygame.key.get_pressed() #Captura as as teclas pressionadas
    player.update(pressed_keys) #Atualiza a posicao do player conforme teclas usadas
    enemies.update() #Atualiza posicao dos inimigos


    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect) #Atualiza a exibicao de todos os Sprites

    if pygame.sprite.spritecollideany(player, enemies): #Verifica se ocorreu a colisao do player com um dos inimigos
        player.kill() #Se ocorrer a colisao, encerra o player
    if pygame.sprite.spritecollideany(player, enemies):
    # A colisão ocorreu. Você pode tratar isso como preferir.
    # Por exemplo, aumentar a pontuação e recriar o inimigo.
        total_lives -= 1
        total_lives_text = font.render(f"Live: {total_lives}", True, (196, 0, 255))

    if remaining_lives <= 0:
        game_over = True  # O jogador perdeu todas as vidas, definimos o estado de game over

    
    


    #Mostrar a tela de game over quando o jogo terminar:
    if pygame.sprite.spritecollideany(player, enemies):
        # A colisão ocorreu.
        # Encerrar o jogo e mostrar a tela de game over.
        running = False
        # Exibir a tela de game over

        screen.blit(game_over_surface, (0, 0))
        screen.blit(game_over_text, game_over_rect)

    
    
    
    pygame.display.flip() #Atualiza a projecao do jogo
