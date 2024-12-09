import random
from mm import *

def print_message(value, wMsg, lMsg):
    if result < 0:
        print(wMsg + '\n')
    else:
        print(lMsg + '\n')
  
dot = '●'
face_lines = {}
face_lines[1] = ["+-------+", f"       ",         f"   {dot}   ",     f"       ", "+-------+"]
face_lines[2] = ["+-------+", f" {dot}     ",     f"       ",         f"     {dot} ", "+-------+"]
face_lines[3] = ["+-------+", f" {dot}     ",     f"   {dot}   ",     f"     {dot} ", "+-------+"]
face_lines[4] = ["+-------+", f" {dot}   {dot} ", f"       ",         f" {dot}   {dot} ", "+-------+"]
face_lines[5] = ["+-------+", f" {dot}   {dot} ", f"   {dot}   ",     f" {dot}   {dot} ", "+-------+"]
face_lines[6] = ["+-------+", f" {dot}   {dot} ", f" {dot}   {dot} ", f" {dot}   {dot} ", "+-------+"]

for num in range(1,7):
  for li in range(1,len(face_lines[num])-1):
     face_lines[num][li] = '|' + face_lines[num][li] + '|'

num_lines = {}
num_lines[1] = [
    " ██",    
    "███",    
    " ██",    
    " ██",   
    " ██"
]

num_lines[2] = [
    "███████",
    "     ██", 
    " █████ ", 
    "██     ", 
    "███████"
] 

num_lines[3] = [
    "██████ ", 
    "     ██", 
    " █████ ", 
    "     ██", 
    "██████ " 
] 

num_lines[4] = [
    "██   ██", 
    "██   ██", 
    "███████", 
    "     ██", 
    "     ██", 
]

num_lines[5] = [
    "███████",
    "██     ", 
    "███████", 
    "     ██", 
    "███████", 
]

num_lines[6] = [
    " ██████ ",  
    "██      ",  
    "███████ ", 
    "██    ██",
    " ██████ " 
]

num_lines[7] = [
    "███████",
    "     ██", 
    "    ██ ", 
    "   ██  ", 
    "   ██  " 
]

num_lines[8] = [
    " █████ ", 
    "██   ██",
    " █████ ", 
    "██   ██", 
    " █████ ", 
]

num_lines[9] = [
    " █████ ",
    "██   ██", 
    " ██████", 
    "     ██", 
    " █████ ", 
]

num_lines[0] = [
    " ██████ ", 
    "██  ████", 
    "██ ██ ██", 
    "████  ██", 
    " ██████ " 
]

moves = {}
moves[1] = [2,3,4,5]
moves[2] = [1,3,4,6]
moves[3] = [1,2,5,6]
moves[4] = [1,2,5,6]
moves[5] = [1,3,4,6]
moves[6] = [2,3,4,5]

limit_suma = 21
position_cache = {}

class Position:
    def __init__(self, suma, face):
        self.suma = suma
        self.face = face
    
    def get_possible_moves(self):
        return moves[self.face]
    
    def make_move(self, move):
        return Position(self.suma + move, move)
    
    def is_terminal(self):
        return self.suma > limit_suma
    
    def add(self, new_face):
        self.suma += new_face
        self.face = new_face
        
    def print(self):
        nSpaces = 2
        nDisp = 30
        #print("Actual points:", self.face)
        #draw_dice_face(self.face)
        #print("SUMA:", self.suma)
        strSuma = str(self.suma)
        new_lines = []
        for li in range(5):    
            new_line = face_lines[self.face][li] + 2*" "
            for num in strSuma:
                new_line += num_lines[int(num)][li] + 2*" "
            new_lines.append(new_line)
            
        for di in range(2): print(nDisp*"*")
        print()
        for line in new_lines: print(line) 
        print()
        for di in range(2): print(nDisp*"*")

def MinMax(position, depth, is_maximizing_player):
    cache_key = (position.suma, position.face, is_maximizing_player)
    # Check if we've seen this position before
    if cache_key in position_cache:
        return position_cache[cache_key]
        
    scores = {}
    for move in position.get_possible_moves():
        new_position = position.make_move(move)
        
        if new_position.is_terminal():
            if is_maximizing_player:
                scores[move] = -1 - (1/depth)
            else:
                scores[move] = 1 + (1/depth)
        else:    
            eval, next_move = MinMax(new_position, depth + 1, not is_maximizing_player)
            scores[move] = eval

    best_move = max(scores, key=scores.get) if is_maximizing_player else min(scores, key=scores.get)
    result = (scores[best_move], best_move)
    
    position_cache[cache_key] = result
    return result

is_playing = True

#initial_face = random.randint(1, 6)
winning_numbers = [1, 2, 5, 6]
initial_face = random.choice(winning_numbers)

actPos = Position(initial_face, initial_face)
actPos.print()

result, found_move = MinMax(actPos, 1, True)
print_message(result, "I SHOULD WIN", "IF YOU PLAY GOOD, YOU CAN WIN")
if result < 0:
    has_chance = False
else:
    has_chance = True

actual_face = initial_face
while is_playing:
    respond = input("Enter some of these numbers '" + ",".join([str(move) for move in moves[actual_face]]) + "'\n")
    if respond.isdigit():
        respond_int = True
        put_move = int(respond)
    else:
        respond_int = False
        put_move = -1

    if respond_int and put_move in moves[actual_face]:
        actPos.add(put_move)
        #print(f"Your move {put_move}")
        actPos.print()
        if actPos.is_terminal():
          print("You have lost. FINITO!!!")
          is_playing = False
        else:
          result, found_move = MinMax(actPos, 1, False)
          if result < 0:
            if has_chance:
                print_message(result, "YOUR MOVE WAS NOT GOOD", "")
                has_chance = False
          else:
            if has_chance:
                print_message(result, "", "WELL DONE, YOU CAN STILL WIN")

          actual_face = found_move
          #print("MY MOVE", found_move, result)
          actPos.add(found_move)
          if actPos.is_terminal():
            print("I LOST. FINITO!!!")
            is_playing = False
          else:      
            print(f"My move {found_move}")
            actPos.print()
    else:
        print(f"Your respond '{respond}' is invalid!")
        print("Please, Enter some of these numbers: '" + ",".join([str(move) for move in moves[actual_face]]) + "'\n")
    
