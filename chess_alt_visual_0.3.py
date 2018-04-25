try:
    from colorama import init
    from termcolor import colored, cprint
    init()
except ValueError:
    colour_init=False
else:
    colour_init=True

ascii_opt = True
import os


    
## these lists are essentail to making any of this work, these are the basic setups and coordinates for the pieces on the board
black=[('pawn',['a7','b7','c7','d7','e7','f7','g7','h7']),('rook',['a8','h8']),('knight',['b8','g8']),('bishop',['c8','f8']),('queen',['d8']),('king',['e8'])]
white=[('pawn',['a2','b2','c2','d2','e2','f2','g2','h2']),('rook',['a1','h1']),('knight',['b1','g1']),('bishop',['c1','f1']),('queen',['d1']),('king',['e1'])]

## For identifying is a peice belongs to a certain player
def player_check(player,coords):
    found =False
    for (piece,coordinates) in player:
        for c in coordinates:
            if c==coords:
                found=True
    if found:
        return True
    else:
        return False

##  To be used to identifying which piece is in the given coordinates, knowing whos player it is
def piece_check(player,coords):
    for (piece,coordinates) in player:
        for c in coordinates:
            if c==coords:
                return piece


##collision detection, False if no piece occupying space, True if own piece already there and 'Taken' if its other team's piece
def collision(player,altplayer, newcoords):
    collided = 'False'
    for (piece,coordinates) in player:
        for c in coordinates:
            if c == newcoords:
                collided = 'True'
    for (piece,coordinates) in altplayer:
        for c in coordinates:
            if c == newcoords:
                collided = 'Taken'
    return collided



## this bloody pawn bit i swear to god took me so long to work out dont touch it and dont ask why pawns for some bloody reason are the hardest piece to program ffs fockin pawns
def pawn_moveset_non_col(oldcoords,player):
    if (int(oldcoords[1]) == 7) and (player == black):
        moveset = [oldcoords[0] + '6',oldcoords[0] +'5']
    elif (int(oldcoords[1]) == 2) and (player == white):
        moveset = [oldcoords[0] + '3',oldcoords[0] +'4']
    elif player == white:
        moveset = [oldcoords[0]+str(int(oldcoords[1])+1)]
    elif player == black:
        moveset = [oldcoords[0]+str(int(oldcoords[1])-1)]
    return moveset
        

def pawn_moveset_col(player,oldcoords):
    letter=oldcoords[0]
    num = str(oldcoords[1])
    if player==white:
        moveset =[((ord(letter)+1)+(int(num)+1)),((ord(letter)-1)+(int(num)+1))]
    else:
        moveset = [((ord(letter)+1)+(int(num)-1)),((ord(letter)-1)+(int(num)-1))]
    return moveset




##this function's purpose is calculating the moveset (where a piece can go) when given the piece name and original coordinates(it all works i promise(i checked), this took a very long time)
def piece_moveset(name,coords):
    letter=coords[0]
    num = str(coords[1])
    moveset=[]
    if name =='rook':
        for r in range(8):
            moveset.append(letter+str(r+1))
        for r in range(8):
            moveset.append(chr(ord('a')+r)+num)
    elif name == 'knight':
        for (a,b) in [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]:
            moveset.append(chr(ord(letter)+a)+str(int(num)+b))
    elif name == 'bishop':
        for r in range(4):
            x=0
            if (r+2)%2 == 0:
                y=0
                for x in range(7):
                    y+=(r-1)
                    moveset.append(chr(ord(letter)+y)+str(int(num)+y))
            else:
                y=0
                for x in range(7):
                    y+=r-2
                    moveset.append(chr(ord(letter)+y)+str(int(num)-y))

    elif name == 'queen':
        for r in range(8):
            moveset.append(letter+str(r+1))
        for r in range(8):
            moveset.append(chr(ord('a')+r)+num)
        for r in range(4):
            x=0
            if (r+2)%2 == 0:
                y=0
                for x in range(7):
                    y+=(r-1)
                    moveset.append(chr(ord(letter)+y)+str(int(num)+y))
            else: 
                y=0
                for x in range(7):
                    y+=r-2
                    moveset.append(chr(ord(letter)+y)+str(int(num)-y))        
    else:
        for o in range(-1,2):
            for i in range(-1,2):
                print(o,i,moveset)
                moveset.append(chr(ord(letter)+o)+(str(int(num)+i)))
        moveset.remove(coords)
    tempread=[] 
    for c in moveset:
        if (105>ord(c[0])>96) and (9>int(c[1:])>0):
            tempread.append(c)
    moveset=tempread
    return moveset





p=' ----------------------------------- \n ----------------------------------- \n [8],a8,b8,c8,d8,e8,f8,g8,h8,¦ \n ----------------------------------- \n [7],a7,b7,c7,d7,e7,f7,g7,h7,¦ \n ----------------------------------- \n [6],a6,b6,c6,d6,e6,f6,g6,h6,¦ \n ----------------------------------- \n [5],a5,b5,c5,d5,e5,f5,g5,h5,¦ \n ----------------------------------- \n [4],a4,b4,c4,d4,e4,f4,g4,h4,¦ \n ----------------------------------- \n [3],a3,b3,c3,d3,e3,f3,g3,h3,¦ \n ----------------------------------- \n [2],a2,b2,c2,d2,e2,f2,g2,h2,¦ \n ----------------------------------- \n [1],a1,b1,c1,d1,e1,f1,g1,h1,¦ \n ----------------------------------- '
pre_list=p.replace(",","¦")

##This string gives a table that resembles a chessboard like this:
## --------------------------- 
## ¦¦a8¦b8¦c8¦d8¦e8¦f8¦g8¦h8¦¦ 
## --------------------------- 
## ¦¦a7¦b7¦c7¦d7¦e7¦f7¦g7¦h7¦¦ 
## --------------------------- 
## ¦¦a6¦b6¦c6¦d6¦e6¦f6¦g6¦h6¦¦ 
## --------------------------- 
## ¦¦a5¦b5¦c5¦d5¦e5¦f5¦g5¦h5¦¦ 
## --------------------------- 
## ¦¦a4¦b4¦c4¦d4¦e4¦f4¦g4¦h4¦¦ 
## --------------------------- 
## ¦¦a3¦b3¦c3¦d3¦e3¦f3¦g3¦h3¦¦ 
## --------------------------- 
## ¦¦a2¦b2¦c2¦d2¦e2¦f2¦g2¦h2¦¦ 
## --------------------------- 
## ¦¦a1¦b1¦c1¦d1¦e1¦f1¦g1¦h1¦¦ 
## ---------------------------

def symbol_allow(name):
    if option=='ascii' or option=='colour':
        if name == 'pawn':
            return ' p '
        elif name == 'rook':
            return ' h '
        elif name == 'knight':
            return ' z '
        elif name == 'bishop':
            return ' b '
        elif name == 'queen':
            return ' q '
        else:
            return ' k '
    else:
        if name == 'pawn':
            return '♙'
        elif name == 'rook':
            return '♖'
        elif name == 'knight':
            return '♘'
        elif name == 'bishop':
            return '♗'
        elif name == 'queen':
            return '♕'
        else:
            return '♔'

def symbol_allob(name):
    if option=='ascii' or option=='colour':
        if name == 'pawn':
            return ' P '
        elif name == 'rook':
            return ' H '
        elif name == 'knight':
            return ' Z '
        elif name == 'bishop':
            return ' B '
        elif name == 'queen':
            return ' Q '
        else:
            return ' K '
    else:
        if name == 'pawn':
            return '♟'
        elif name == 'rook':
            return '♜'
        elif name == 'knight':
            return '♞'
        elif name == 'bishop':
            return '♝'
        elif name == 'queen':
            return '♛'
        else:
            return '♚'

##The 'Visualiser' is a little hard to explain.  It generates coordinates from a1,b1,c1... to ...f8,g8,h8.
##When it generates them, it checks all the coordinates in each player's list to see if any match.
##If they do match, it the replaces the coordinates in the table list with a representative symbol of the piece.
##if they dont match, it replaces the coordinate with a blank space
##
##well i mean thats what its meant to do
##
##for some reason it on does the Rook at h8
##--------------------------- 
## ¦¦a8¦b8¦c8¦d8¦e8¦f8¦g8¦ R ¦¦ 
## --------------------------- 
## ¦¦a7¦b7¦c7¦d7¦e7¦f7¦g7¦h7¦¦ 
## --------------------------- 
## ¦¦a6¦b6¦c6¦d6¦e6¦f6¦g6¦h6¦¦ 
## --------------------------- 
## ¦¦a5¦b5¦c5¦d5¦e5¦f5¦g5¦h5¦¦ 
## --------------------------- 
## ¦¦a4¦b4¦c4¦d4¦e4¦f4¦g4¦h4¦¦ 
## --------------------------- 
## ¦¦a3¦b3¦c3¦d3¦e3¦f3¦g3¦h3¦¦ 
## --------------------------- 
## ¦¦a2¦b2¦c2¦d2¦e2¦f2¦g2¦h2¦¦ 
## --------------------------- 
## ¦¦a1¦b1¦c1¦d1¦e1¦f1¦g1¦h1¦¦ 
## --------------------------- 
##
##If you could provide some help on whats going wrong that would be strongly appreciated!!



def visualiser():
    d=pre_list
    t=0
    for y in range(1,9):
        for x in ['a','b','c','d','e','f','g','h']:
            for (piece,coords) in black:
                for c in coords:
                    if c==(x+str(y)):
                        f= d.replace(c,symbol_allob(piece))
                        d=f
                        t=1
            for (piece,coords) in white:
                for c in coords:
                    if c==(x+str(y)):
                        f= d.replace(c,symbol_allow(piece))
                        d=f
                        t=1

            try:
                if option=='piece':
                    f= d.replace((x+str(y)),' ')
                else:
                    f= d.replace((x+str(y)),'   ')
            except ValueError:
                'nah'
            else:
                d=f
    return d

post_list=' [-],[a],[b],[c],[d],[e],[f],[g],[h],, \n ----------------------------------- '.replace(",","¦")

def altfinalprint():
    print(visualiser())
    print(post_list)
    print('P = pawn  H = rook  Z = knight  B = bishop  Q = queen  K = king')


def finalprint():
    newlist= visualiser()
    final_string=''
    for x in list(newlist):
        if x=='p' or x=='z' or x=='q' or x=='k' or x=='b' or x=='h':
            final_string +=colored(x.upper(),'cyan','on_grey')
        elif x=='\n':
            final_string +=x
        else:
            final_string +=colored(x,'white','on_grey')
    print(final_string)
    almost=''
    for x in list(post_list):
        if x=='\n':
            almost +=x
        else:
            almost +=colored(x,'white','on_grey')
    print(almost)
    print('P = pawn  H = rook  Z = knight  B = bishop  Q = queen  K = king')

def question1():
    if os.name == 'nt':
        option='ascii'
    else:
        inp=input('Use ascii chracters? [P - pawn, H - rook, etc] (y/n) ')
        if inp == 'y':
            option='ascii'
        else:
            option = 'piece'
    return option

match_result='ongoing'
turn=1
currentp=white
altp=black

option = 'none'
if colour_init:
    inp=str(input('Would you like to use the multi-coloured version? (y/n) '))
    if inp=='y' :
        option = 'colour'
    else:
        option=question1()
else:
    option=question1()

if option== 'colour':
    finalprint()
else:
    altfinalprint()   


while match_result =='ongoing':
    restart= False
    collided=False
    if turn%2==1:
        currentp=white
        altp=black
    else:
        currentp=black
        altp=white

    if currentp ==white:
        if option=='colour':
            displayp='Cyan'
        elif option== 'ascii':
            displayp='Lowercase'
        else:
            displayp='White'
    else:
        if option =='colour':
            displayp='White'
        elif option=='ascii':
            displayp='Uppercase'
        else:
            displayp='Black'
    print(displayp + ' goes now')
    bigcheck = True
    (old,new)=(input('Type in old and new coordinates: ')).split()
    if option== 'colour':
        finalprint()
    else:
        altfinalprint()
            
    for y in range(1,9):
        if new[0] ==str(y):
            new=(new[1]+new[0])
        elif old[0]==str(y):
            old=(old[1]+old[0])

    if player_check(currentp,old):
        if collision(currentp,altp,new) =='False' or collision(currentp,altp,new) =='Taken':
            if collision(currentp,altp,new) == 'Taken':
                collided = True
            dapiece=piece_check(currentp,old)
            if dapiece=='pawn':
                if collided:
                    moves = pawn_moveset_col(currentp,old)
                else:
                    moves = pawn_moveset_non_col(old,currentp)
            else:
                moves= piece_moveset(dapiece,old)
            if new in moves:
                if collided:
                    newlst=[]
                    for c in altp:
                        edit=list(c)
                        for t in edit[1]:
                            if t==new:
                                edit[1].remove(new)
                        newlst.append(tuple(edit))
                    altp=newlst
                lst=[]
                for r in currentp:
                    edi=list(r)
                    try:
                        ind=edi[1].index(old)
                    except ValueError:
                        'keep going'
                    else:
                        edi[1].insert(ind,new)
                        edi[1].remove(old)
                    lst.append(tuple(edi))
                currentp=lst
            else:
                print('Move not possible')
                restart =True
            
        else:
            print('A piece is in the way')
            restart = True
    else:
        print('No piece currently at this position')
        restart = True

    if turn%2==1:
        white=currentp
        black=altp
    else:
        black=currentp
        white=altp
    if restart :
        'do nothing'
    else:
        turn+= 1













##Notes:

##    collision detection doesn't draw lines, only from point to point


    


##input two co-ords
##check correct player v
##check which piece v
##check if move is viable (piece and collision)
##change list data on current player
##check if other player has piece in spot:
##    if yes then remove piece
##    otherwise ignore
##print board
##cycle turn
