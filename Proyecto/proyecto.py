# Materia   :   Laboratorio
# Profesor  :   Javier Balmaceda
# Proyecto  :   "SPACE BATTLES"
# Alumnos   :   Nicolas Batista - Luciano Cossia
# Contacto  :   cossialuciano@gmail.com 

#librerias
import pygame
import os

pygame.init()
pygame.font.init()
pygame.mixer.init()

# display del juego
WIDTH, HEIGHT = 900, 500 # constantes de alto y ancho
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT)) # se asigna el método pasando las dimensiones
pygame.display.set_caption("Space Battles") # titulo de la ventana

# definicion RGB de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT) # objeto para dividir pantalla

# metodo os.path.join para evitar problemas con el criterio del so para dividir el path de los archivos
# concatena los strings
HIT_SOUND = pygame.mixer.Sound(os.path.join("Proyecto Laboratorio I", "Proyecto", "Assets", "hit.mp3"))
FIRE_SOUND = pygame.mixer.Sound(os.path.join("Proyecto Laboratorio I","Proyecto", "Assets", "fire.mp3"))

# fuente del texto
HEALTH_FONT = pygame.font.SysFont("arial", 30)
WINNER_FONT = pygame.font.SysFont("comicsans", 60)
TIMER_FONT = pygame.font.SysFont("arial", 30)

FPS = 60 # constante para que la velocidad de refresco no dependa de la velocidad de la pc

VEL = 5 # velocidad jugador
FAST_VEL = VEL * 2 # hurry up!
BULLET_VEL = 15 # velocidad disparo
FAST_BULLET = BULLET_VEL * 2 # hurry up!
MAX_BULLETS = 3 # enfriamiento del disparo, 3 disparos en pantalla

# eventos
TIMER_COUNT = pygame.USEREVENT + 1 # representa el código (ID) de evento para diferenciarlos
YELLOW_HIT = pygame.USEREVENT + 2
RED_HIT = pygame.USEREVENT + 3

# players setup
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Proyecto Laboratorio I", "Proyecto", "Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Proyecto Laboratorio I", "Proyecto", "Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join("Proyecto Laboratorio I", "Proyecto", "Assets", "background.png")), (WIDTH, HEIGHT))

# funcion para mostrar los objetos en pantalla
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, timer):
    SCREEN.fill(BLACK) # llenado de pantalla para que no haya estela residual
    SCREEN.blit(SPACE, (0, 0)) # muestra background
    pygame.draw.rect(SCREEN, BLACK, BORDER) # dibuja divisor de pantalla
    SCREEN.blit(timer, (WIDTH//2 - timer.get_width(), 10))
    red_health_text = HEALTH_FONT.render("Rojo: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Amarillo: " + str(yellow_health), 1, WHITE)
    SCREEN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10)) # toma el ancho del texto
    SCREEN.blit(yellow_health_text, (10, 10))
    SCREEN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) # muestra la nave en su posicion actual
    SCREEN.blit(RED_SPACESHIP, (red.x, red.y))
    
    for bullet in red_bullets:
        pygame.draw.rect(SCREEN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(SCREEN, YELLOW, bullet)

    pygame.display.update()

# funcion de movimiento del jugador
def yellow_movement(VEL, keys_pressed, yellow, counter):
    if counter <= 10:
        VEL = FAST_VEL
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # mueve hacia la izquierda
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x + 15: # mueve hacia la derecha
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 50: # mueve hacia arriba
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: # mueve hacia abajo
        yellow.y += VEL

def red_movement(VEL, keys_pressed, red, counter):
    if counter <= 10:
        VEL = FAST_VEL
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # mueve hacia la izquierda
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH + 15: # mueve hacia la derecha
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 50: # mueve hacia arriba
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15: # mueve hacia abajo
        red.y += VEL

# funcion del movimiento de los disparos
def handle_bullets(yellow_bullets, red_bullets, yellow, red, counter):
    for bullet in yellow_bullets:
        if counter <= 10:
            bullet.x += FAST_BULLET
        else:
            bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        if counter <= 10:
            bullet.x -= FAST_BULLET
        else:
            bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

# funcion para mostrar el resultado en pantalla       
def draw_result(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    SCREEN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

# funcion principal del juego     
def main():

    yellow = pygame.Rect(100, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_bullets = [] # lista vacia donde se almacenan las balas
    yellow_bullets = []
    red_health = 5 # puntos de salud
    yellow_health = 5
    
    clock = pygame.time.Clock() # se llama la funcion clock de pygame para FPS y Timer
    counter = 20
    timer = TIMER_FONT.render(str(counter), 1, WHITE) # tiempo en pantalla
    DELAY = 1000 # 1 segundo
    pygame.time.set_timer(TIMER_COUNT, DELAY)

    # loop principal
    run = True
    while run:
        clock.tick(FPS) # controla la velocidad del loop en 60 veces por segundo

        for event in pygame.event.get(): # recorre la lista de eventos
            if event.type == pygame.QUIT: # permite al usuario cerrar la ventana
                run = False
                pygame.quit()
                
            if event.type == TIMER_COUNT:
                counter -= 1
                timer = TIMER_FONT.render(str(counter), 1, WHITE)

            if event.type == pygame.KEYDOWN: # teclas disparo
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width//2, yellow.y + yellow.height//2 + 5, 10, 5)
                    yellow_bullets.append(bullet)
                    FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 + 5, 10, 5)
                    red_bullets.append(bullet)
                    FIRE_SOUND.play()

            if event.type == RED_HIT: # evento de salud
                red_health -= 1
                HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                HIT_SOUND.play()
                        
        end_text = ""
        if counter == 0 and yellow_health > red_health or red_health == 0:
            end_text = "Gano Amarillo!"
        
        elif counter == 0 and red_health > yellow_health or yellow_health == 0:
            end_text = "Gano Rojo!"

        elif counter == 0 and yellow_health == red_health:
            end_text = "Empate!"

        if end_text != "":
            draw_result(end_text) # muestra resultado
            break # rompe el bucle

        keys_pressed = pygame.key.get_pressed()
        yellow_movement(VEL, keys_pressed, yellow, counter)
        red_movement(VEL, keys_pressed, red, counter)
        handle_bullets(yellow_bullets, red_bullets, yellow, red, counter)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, timer)
    
    main()

"""
Variable __name__: solamente se llamara a la funcion main() de este archivo.
Evita que se inicie main() perteneciente a una función que se importa.
"""

if __name__ == "__main__":
    main()