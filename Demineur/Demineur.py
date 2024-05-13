import pygame
import numpy as np

pygame.init()

COVERD = 0
UNCOVERD = 1
FLAG = 2
BOMBE = 9
COLOR = ((10,21,236),(20,124,32),(236,10,13),(9,10,130),(121,5,17),(2,133,127),(6,6,6),(149,149,149))

taille_case = 25
#Gestion de la difficultée
colonne = 50
ligne = 50
bombe = 500

tab_bombe   = [[]]
tab_jeu     = [[]]

width, height = colonne*taille_case,ligne*taille_case
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Démineur')
police = pygame.font.SysFont("Arial",int(taille_case/1.7),True) 

jeu_en_cours = False
run = True

def init_level():
    for col in range(colonne) :
        for lig in range(ligne):
            pygame.draw.rect(screen,(153,153,153),((col)*taille_case,(lig)*taille_case,taille_case,taille_case),1)
            pygame.draw.rect(screen,(237,237,237),((col)*taille_case+1,(lig)*taille_case+1,taille_case-2,taille_case-2),2)
            pygame.draw.rect(screen,(192,192,192),((col)*taille_case+3,(lig)*taille_case+3,taille_case-6,taille_case-6))
    pygame.display.update()

def inside(col:int, lig:int)->bool:
    return 0 <= col < colonne and 0 <= lig < ligne

def around(col:int,lig:int)->list[tuple:int]:
    return [(col+x,lig+y) for x in range(-1,2) for y in range(-1,2) if inside(col+x,lig+y) and not (x,y)==(0,0)]

def random_grid(col:int,lig:int):
    np.random.seed()
    n = bombe
    while n > 0 :
        rand_col = np.random.randint(colonne)
        rand_lig = np.random.randint(ligne)       
        if tab_bombe[rand_col][rand_lig] != BOMBE and (rand_col,rand_lig) not in around(col,lig) and not (rand_col,rand_lig) == (col,lig):
            tab_bombe[rand_col][rand_lig] = BOMBE
            #Incremente voisins
            for coord in around(rand_col,rand_lig):
                if tab_bombe[coord[0],coord[1]] != BOMBE : tab_bombe[coord[0],coord[1]] +=1          
            n -= 1
    update_game(col,lig)

def update_game(col:int,lig:int):
    if inside(col,lig):
        if tab_bombe[col][lig] == 0 and tab_jeu[col][lig] == 0:
            tab_jeu[col][lig] = 1
            update_game(col-1,lig)
            update_game(col+1,lig)
            update_game(col,lig-1)
            update_game(col,lig+1)
            update_game(col-1,lig-1)
            update_game(col-1,lig+1)
            update_game(col+1,lig-1)
            update_game(col+1,lig+1)
        else:
            tab_jeu[col][lig] = 1
        show_case(col,lig)

def show_if_flag(col:int,lig:int):
    val = 0
    tab_around = around(col,lig)
    for coord in tab_around:
        if tab_jeu[coord[0],coord[1]] == FLAG : val += 1
    
    if val == tab_bombe[col,lig]:
        for coord in tab_around :
            if tab_jeu[coord[0],coord[1]] == COVERD:
                update_game(coord[0],coord[1])

def win():
    if np.count_nonzero(tab_jeu == UNCOVERD) == colonne * ligne - bombe:        
        return True #Gagné 
    else :
        return False

def lose():
    global jeu_en_cours
    jeu_en_cours = False
    for i in range(0,colonne):
        for j in range(0,ligne):
            if tab_jeu[i][j] == 0: 
                tab_jeu[i][j] = 1
                show_case(i,j)

def draw_number(col:int,lig:int):
    pygame.draw.rect(screen,(153,153,153),((col)*taille_case,(lig)*taille_case,taille_case,taille_case),1)
    pygame.draw.rect(screen,(192,192,192),((col)*taille_case+1,(lig)*taille_case+1,taille_case-1,taille_case-1))
    if tab_bombe[col,lig] != 0 :
        screen.blit(police.render(str(int(tab_bombe[col][lig])),True,COLOR[int(tab_bombe[col,lig])-1]), ((col)*taille_case+taille_case/3,(lig)*taille_case+taille_case/5))

def draw_bomb(col:int,lig:int):
    pygame.draw.rect(screen,(153,153,153),((col)*taille_case,(lig)*taille_case,taille_case,taille_case),1)
    pygame.draw.rect(screen,(250,0,0),((col)*taille_case+1,(lig)*taille_case+1,taille_case-1,taille_case-1))
    if jeu_en_cours == True:
        lose()
    pygame.draw.rect(screen,(255,0,0),(0,0,width,height),1)

def draw_flag(col:int,lig:int):
    pygame.draw.rect(screen,(153,153,153),((col)*taille_case,(lig)*taille_case,taille_case,taille_case),1)
    pygame.draw.rect(screen,(152,251,152),((col)*taille_case+1,(lig)*taille_case+1,taille_case-1,taille_case-1))

def draw_none(col:int,lig:int):
    pygame.draw.rect(screen,(153,153,153),((col)*taille_case,(lig)*taille_case,taille_case,taille_case),1)
    pygame.draw.rect(screen,(237,237,237),((col)*taille_case+1,(lig)*taille_case+1,taille_case-2,taille_case-2),2)
    pygame.draw.rect(screen,(192,192,192),((col)*taille_case+3,(lig)*taille_case+3,taille_case-6,taille_case-6))

def show_case(col:int,lig:int):
    match tab_jeu[col][lig]:
        case 0 : #Pas Découvert
            draw_none(col,lig)
        case 1 : #Découvert
            if tab_bombe[col][lig] == 9 : #Bombe
                draw_bomb(col,lig)
            else : #Numero
                draw_number(col,lig)
                    
        case 2: #Drapeau
            draw_flag(col,lig)

init_level()              
while run:

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEWHEEL:
            print(str(event.y))

        if event.type == pygame.MOUSEBUTTONUP:

            souris_pos = event.pos 
            souris_X = int(souris_pos[0]/taille_case)
            souris_Y = int(souris_pos[1]/taille_case)
            if inside(souris_X,souris_Y): 

                if event.button == 1 :        
                    if jeu_en_cours == False : #début de partie
                        tab_bombe   = np.zeros((int(colonne),int(ligne)))
                        tab_jeu     = np.zeros((int(colonne),int(ligne)))
                        init_level()
                        random_grid(souris_X,souris_Y)
                        jeu_en_cours = True  
                    else: #jeu en cours 
                        if tab_jeu[souris_X,souris_Y] == 0 :    
                            update_game(souris_X,souris_Y)
                        elif tab_jeu[souris_X,souris_Y] == 1:   
                            show_if_flag(souris_X,souris_Y) 

                if event.button == 3 and jeu_en_cours == True : 
                    if tab_jeu[souris_X,souris_Y] == 0 : tab_jeu[souris_X,souris_Y] = 2 
                    elif tab_jeu[souris_X,souris_Y] == 2 : tab_jeu[souris_X,souris_Y] = 0
                    show_case(souris_X,souris_Y)

                if event.button in (1,3) and jeu_en_cours == True and win():
                    pygame.draw.rect(screen,(0,255,0),(0,0,width,height),1)
                    pygame.display.update() 
                    jeu_en_cours = False

                pygame.display.update() 
pygame.QUIT