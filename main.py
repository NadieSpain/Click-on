import pygame 
from pygame.locals import *
import random
import winsound

#El juego trata de tornar todos los recuadros a 0 sin dar al ultimo nivolver a pulsar los 0   


pygame.init()

#aqui se almacenan los puntos de la ronda
pts_round=0
#puntos totales
pts=0

#numero de cuadrados en el eje ...
#x
N_squarex= 10
#y
N_squarey= 10

#cuadricula 
#key: f"{x}-{y}"
#info: numero de intentos 
_grid_={}
#mayor numero que puede aparecer en un cuadrado
Maxtries=5


#convierte un color a negativo
negative = lambda t: (255-t[0],255-t[1],255-t[2])
#elige un color aleatorio
random_color=lambda: (random.randint(0,255),random.randint(0,255),random.randint(0,255))

#crea otra lista de colores, resetea la cuadricula y quita el ultimo click
def reset():
    global bg, lastclick
    lastclick=""
    bg=[(random_color()) for i in range(Maxtries+1)]
    for x in range(N_squarex):
        for y in range(N_squarey):
            _grid_[f"{x}-{y}"]=random.randint(0,Maxtries)
reset()




relief=(0,0,0)
bg=[(random_color()) for i in range(Maxtries+1)]


#tamaño del cuadrado
size_square = 50
SIZE_SCREEN = ((size_square*N_squarex), (size_square*N_squarey))
screen = pygame.display.set_mode((SIZE_SCREEN[0],SIZE_SCREEN[1]+100), pygame.DOUBLEBUF, 32)

#hace falta reseteo 
isreset=False
#si esta encendida la ventana
_ON_=True
#ultimo click -> f"{x}-{y}"
lastclick=""
while _ON_:
    screen.fill(relief)
    #si todos los cuadros son 0 lo reinicia y suma los puntos de esa ronda
    if isreset:
        pts+=pts_round
        pts_round=0
        reset()

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            _ON_=not _ON_

        # detecto el evento que se genera cuando sube el botón del mouse
        elif(event.type == pygame.MOUSEBUTTONUP):
            # si el botón presionado es 1...
            if(event.button == 1):
                # obtengo la posición xy del cursor
                curx, cury = event.pos

                #si las coordenadas son dentro del tablero
                if cury<=SIZE_SCREEN[1]:
                    # obtengo las coordenadas del cuadrado
                    x = curx // size_square
                    y = cury // size_square

                    try:
                        #si pulsa uno valido
                        if (_grid_[f"{x}-{y}"]) and lastclick!=f"{x}-{y}":
                            _grid_[f"{x}-{y}"] -= 1
                            lastclick=f"{x}-{y}"
                            pts_round+=1
                        #si pulsa el ultimo
                        elif lastclick==f"{x}-{y}":
                            winsound.Beep(500, 10)
                            winsound.Beep(500, 10)
                        #si pulsa un 0
                        elif not (_grid_[f"{x}-{y}"]):
                            winsound.Beep(500, 10)
                            winsound.Beep(500, 10)

                    except KeyError:
                        pass

                else:
                    #si pulsa fuera y en el centro del eje y del tablero
                    if curx>=(SIZE_SCREEN[0]//2-25) and curx<=(SIZE_SCREEN[0]//2+25) and cury>=(SIZE_SCREEN[1]+25) and cury<=(SIZE_SCREEN[1]+50):
                        reset()
                        pts_round=0
            

    isreset=True

    #lista de diccionarios con cada cuadrado
    #args: num, coords, color 
    message_list=[]
    for x in range(N_squarex):
        for y in range(N_squarey):
            coord=[
                (x + x * size_square, y + y *size_square),# 0,0
                (x + (x + 1) * size_square, y + y * size_square),#1,0
                (x + (x + 1) * size_square, y + (y + 1)*size_square),#1,1
                (x + x * size_square, y + (y + 1) * size_square)#0,1
                ]

            #si algo es mayor que 0 no hace falta reseteo
            if _grid_[f"{x}-{y}"]!=0:
                isreset=False                
            
            pygame.draw.polygon(screen, bg[_grid_[f"{x}-{y}"]], coord)
            message_list.append( {
                    "num":str(_grid_[f"{x}-{y}"]), "coords":(x,y), 
                    "color":negative(bg[_grid_[f"{x}-{y}"]]) 
                                    } )
    for x in range(N_squarex):
        for y in range(N_squarey):
            coord=[
                (x + x * size_square, y + y *size_square),# 0,0
                (x + (x + 1) * size_square, y + y * size_square),#1,0
                (x + (x + 1) * size_square, y + (y + 1)*size_square),#1,1
                (x + x * size_square, y + (y + 1) * size_square)#0,1
                ]
            if f"{x}-{y}"==lastclick:
                pygame.draw.polygon(screen, negative(bg[_grid_[f"{x}-{y}"]]), coord, 3)

    font = pygame.font.SysFont("Helvetica Neue", 20)
    #numeros de cada cadrado 
    for i in message_list:
        x, y= i["coords"][0], i["coords"][1]
        message= font.render(i["num"], 0, i["color"])
        screen.blit(message, (x*size_square+(size_square//2), (y*size_square)+(size_square//2)))

    #puntos 
    font= pygame.font.SysFont("Helvetica Neue", 20)
    message= font.render(f"Pts: {pts}", 1, (255,255,255))
    screen.blit(message, (20,SIZE_SCREEN[1]+10))

    #puntos de esa ronda
    message= font.render(f"Round Pts: {pts_round}", 1, (255,255,255))
    screen.blit(message, (SIZE_SCREEN[0]-100,SIZE_SCREEN[1]+10))
    pygame.display.flip()
