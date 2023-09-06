import pygame
import random
from shapely.geometry import Point, Polygon
pygame.init()
TOTALBASE=700
TOTALHEIGHT=400
SCRBASE=200
SCRHEIGHT=400
GRIDDIM=20
gb=pygame.display.set_mode((TOTALBASE,TOTALHEIGHT))
pygame.display.set_caption("Tetris game")
logo=pygame.image.load("tetris game logo.jpg")
pygame.display.set_icon(logo)
def grid():
    for run in range(0,SCRBASE,GRIDDIM):
        for run2 in range(0,SCRHEIGHT,GRIDDIM):
            pygame.draw.rect(gb,(100,0,100),pygame.Rect(run,run2,GRIDDIM,GRIDDIM),1)
def draw_block(delx,dely,l,colour):
    for run in range(0,len(l)):
        l[run][0]+=delx
        l[run][1]+=dely
        l[run][0],l[run][1]=round(l[run][0],0),round(l[run][1],1)
    pygame.draw.polygon(gb,colour,l)
    return l
def rotate90anti(l,colour):
    for run in range(0,len(l)):
        l[run][1],l[run][0]=l[0][0]+l[0][1]-l[run][0],l[run][1]+l[0][0]-l[0][1]
        l[run][0],l[run][1] = round(l[run][0],0),round(l[run][1],1)
    pygame.draw.polygon(gb,colour,l)
    return (l)
flag=True
def initialize():
    global x,y,listT,listS,listL,listSq,listR,colourT,colourS,colourL,colourSq,colourR,coord,n
    x,y=SCRBASE/2,0
    listT = [[x, y], [x + 60, y], [x + 60, y + 20], [x + 40, y + 20], [x + 40, y + 40], [x + 20, y + 40],
             [x + 20, y + 20], [x, y + 20]]
    listS = [[x, y], [x + 40, y], [x + 40, y + 20], [x + 60, y + 20], [x + 60, y + 40], [x + 20, y + 40],
             [x + 20, y + 20], [x, y + 20]]
    listL = [[x, y], [x + 20, y], [x + 20, y + 40], [x + 40, y + 40], [x + 40, y + 60], [x, y + 60]]
    listSq = [[x, y], [x + 40, y], [x + 40, y + 40], [x, y + 40]]
    listR = [[x, y], [x + 20, y], [x + 20, y + 80], [x, y + 80]]
    colourT, colourS, colourL, colourSq, colourR = (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 128, 64)
    coord = [[listT, colourT], [listS, colourS], [listL, colourL], [listSq, colourSq], [listR, colourR]]
    n=random.randrange(0,len(coord))
initialize()
text=pygame.font.Font("freesansbold.ttf",20)
shape,col=[],[]
flag=True
while flag:
    gb.fill((0,0,0))
    rules=[None,None,None,None,None,None,None,None,None]
    rules[0]=text.render("WELCOME TO FALLING BLOCKS GAME. THE RULES ARE:",True,(255,255,255))
    rules[1]=text.render("1)TO MOVE THE BLOCKS LEFT, PRESS LEFT ARROW KEY", True, (255, 255, 255))
    rules[2]=text.render("2)TO MOVE THE BLOCKS RIGHT, PRESS RIGHT ARROW KEY", True, (255, 255, 255))
    rules[3] = text.render("3)TO ROTATE THE BLOCKS PRESS SPACE BAR", True, (255, 255, 255))
    rules[4] = text.render("4)IF A BLOCK FALLS SUCCESSFULLY, THE PLAYER GETS 5 POINTS", True, (255, 255, 255))
    rules[5] = text.render("5)IF A HORIZONTAL ROW IS FULL, THE PLAYER GETS EXTRA POINTS ", True, (255, 255, 255))
    rules[6] = text.render("   AND THAT ROW ALONG WITH ALL ROWS BELOW GET CLEARED", True, (255, 255, 255))
    rules[7] = text.render("6)GAME ENDS WHEN THE BLOCKS FILL THE FULL SCREEN", True, (255, 255, 255))
    rules[8] = text.render("---------------PRESS ANY KEY TO BEGIN------------", True, (255, 255, 255))
    for run in range(0,8):
        gb.blit(rules[run],(0,run*30+40))
    gb.blit(rules[8],(0,300))
    for run in pygame.event.get():
        if run.type==pygame.KEYDOWN:
            flag=False
    pygame.display.update()
flag,flag2=True,True
full=False
point,level=0,1
count,fr=0,600
while flag2:
    flag=True
    moveblock=pygame.USEREVENT+1
    pygame.time.set_timer(moveblock,fr)
    while flag:
        row=[]
        breakdown,rowfill,blockfill=False,False,False
        rotate=False
        up,stop=False,False
        overlap,overlapy=False,False
        chx,chy=0,0
        gb.fill((0, 0, 0))
        grid()
        if count==5:
            count=0
            if fr==200:
                fr,level=80,level+1
            elif fr==80:
                fr=80
            else:
                fr,level=fr-200,level+1
            break
        for run3 in pygame.event.get():
            if (run3.type == pygame.QUIT):
                flag,flag2=False,False
            if (run3.type == pygame.KEYDOWN and run3.key == pygame.K_LEFT):
                chx=-20
                break
            if (run3.type == pygame.KEYDOWN and run3.key == pygame.K_RIGHT):
                chx=20
                break
            if (run3.type==moveblock):
                chy=20
            if (run3.type == pygame.KEYDOWN and run3.key == pygame.K_SPACE):
                coord[n][0]=rotate90anti(coord[n][0],coord[n][1])
                rotate=True
        for run in coord[n][0]:
            if run[0]<0:
                chx=-run[0]
                break
            if run[0]>SCRBASE:
                chx=SCRBASE-run[0]
                break
        for run in coord[n][0]:
            if round(run[1],1)==SCRHEIGHT:
                chy=0
                stop=True
                break
        for run in coord[n][0]:
            if round(run[1],1)>SCRHEIGHT:
                chy=SCRHEIGHT-round(run[1],1)
                up=True
                break
        draw_block(chx, chy, coord[n][0], coord[n][1])
        mov=Polygon(coord[n][0])
        for run in shape:
            ex=Polygon(run)
            if mov.overlaps(ex) and chx==20:
                chx=-20
                overlap=True
                break
            if mov.overlaps(ex) and chx==-20:
                chx=20
                overlap=True
                break
            if mov.overlaps(ex) and chx==0 and rotate==False:
                chy=-20
                stop,up,overlapy=True,False,True
                break
            if mov.overlaps(ex) and chx==0 and rotate==True:
                overlapy=True
                chy=-60
                break
        if overlap==True or overlapy==True:
            gb.fill((0, 0, 0))
            grid()
            draw_block(chx, chy, coord[n][0], coord[n][1])
        for run in range(int(GRIDDIM/2),int(SCRHEIGHT+(GRIDDIM/2)),GRIDDIM):
            rowfill=False
            for run2 in range(int(GRIDDIM/2),int(SCRBASE+(GRIDDIM/2)),GRIDDIM):
                for run3 in shape:
                    sh=Polygon(run3)
                    if Point(run2,run).within(sh):
                        blockfill=True
                        break
                    else:
                        blockfill=False
                if blockfill==False:
                    rowfill=False
                    break
            if blockfill==True:
                rowfill=True
                row.append((run+GRIDDIM/2)/GRIDDIM)
        if stop==True and up==False:
            count+=1
            point+=5
            shape.append(coord[n][0])
            col.append(coord[n][1])
            initialize()
        isfull=False
        if row!=[]:
            isfull=True
            for run in range(0,len(row)):
                for run2 in shape:
                    for run3 in range(0,len(run2)):
                        if run2[run3][1]<=(row[run]-1)* GRIDDIM:
                            run2[run3][1] += GRIDDIM
                            for run4 in range(0, len(row)):
                                row[run4]+=1
        if isfull==True:
            point+=10
        score = text.render("SCORE : " + str(point), True, (255, 255, 255))
        levelt=text.render("LEVEL : "+str(level), True, (255,255,255))
        gb.blit(score, (TOTALBASE / 2, 40))
        gb.blit(levelt, (TOTALBASE/2, 80))
        full=False
        for run in shape:
            for run2 in run:
                if run2[1]<0:
                    full=True
                    flag,flag2=False,False
                    break
        for run in range(0, len(shape)):
            draw_block(0, 0, shape[run], col[run])
        pygame.display.update()
while full:
    gb.fill((0,0,0))
    end=text.render("GAME OVER. YOUR SCORE: "+str(point)+". PRESS ANY KEY TO EXIT",True,(255,255,255))
    gb.blit(end, (40,40))
    for run in pygame.event.get():
        if run.type==pygame.KEYDOWN:
           full=False
    pygame.display.update()



























































































