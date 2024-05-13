import random
import sys

import pygame

###################################################################
###################################################################
###################################################################
# set up some var
done=True
level=1
pixel_value = 4
dimension_value = 4
WIDTH,HEIGHT=600,600

SELECTED_COLOR = (255, 0, 0)
# Initialize the selected element
selected_element = "pixel"
pygame.display.set_caption("DHL-Maze")

#//////////////////////////////////           \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#////////////////////////////////// INTERFACE \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#//////////////////////////////////           \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
def draw_interface(screen):
    global pixel_value, dimension_value, selected_element

       # Clear the screen
    screen.fill((0,0,0))
    font=pygame.font.Font(None,48)
    # Draw the pixel label
    pixel_label = font.render(str(pixel_value), True, (255,255,255))
    pixel_rect = pixel_label.get_rect(center=(250, 400))
    bg=pygame.image.load("bg.png").convert()
    screen.blit(bg,(0,0))
    screen.blit(pixel_label, pixel_rect)

    # Draw the dimension label
    dimension_label = font.render(str(dimension_value), True, (255,255,255))
    dimension_rect = dimension_label.get_rect(center=(350, 400))
    screen.blit(dimension_label, dimension_rect)

    # Draw the up arrow for pixel
    up_arrow_pix = font.render("^", True, SELECTED_COLOR if selected_element == "pixel" else (255,255,255))
    up_arrow_pix_rect = up_arrow_pix.get_rect(center=(250, 350))
    screen.blit(up_arrow_pix, up_arrow_pix_rect)

    # Draw the down arrow for pixel
    down_arrow_pix = font.render("v", True, SELECTED_COLOR if selected_element == "pixel" else (255,255,255))
    down_arrow_pix_rect = down_arrow_pix.get_rect(center=(250, 450))
    screen.blit(down_arrow_pix, down_arrow_pix_rect)

    # Draw the up arrow for dimension
    up_arrow_dim = font.render("^", True, SELECTED_COLOR if selected_element == "dimension" else (255,255,255))
    up_arrow_dim_rect = up_arrow_dim.get_rect(center=(350, 350))
    screen.blit(up_arrow_dim, up_arrow_dim_rect)

    # Draw the down arrow for dimension
    down_arrow_dim = font.render("v", True, SELECTED_COLOR if selected_element == "dimension" else (255,255,255))
    down_arrow_dim_rect = down_arrow_dim.get_rect(center=(350, 450))
    screen.blit(down_arrow_dim, down_arrow_dim_rect)

    # Draw the cross label
    cross_label = font.render("X", True, (255,255,255))
    cross_rect = cross_label.get_rect(center=(WIDTH // 2, 400))
    screen.blit(cross_label, cross_rect)

    # Update the display
    pygame.display.flip()

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if selected_element == "pixel":
                    pixel_value += 1
                else:
                    dimension_value += 1
            elif event.key == pygame.K_DOWN:
                if selected_element == "pixel":
                    pixel_value -= 1
                    if pixel_value < 4:
                        pixel_value = 4
                else:
                    dimension_value -= 1
                    if dimension_value < 4:
                        dimension_value = 4
            elif event.key == pygame.K_RIGHT:
                if selected_element == "pixel":
                    selected_element = "dimension"
            elif event.key == pygame.K_LEFT:
                if selected_element == "dimension":
                    selected_element = "pixel"
            elif event.key == pygame.K_RETURN:
                done=False
                main(screen,pixel_value,dimension_value)
                print("APPUYEZ sur ENTREE pour CONFIRMER")
# def presse_entree():
    

#//////////////////////////////////             \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#////////////////////////////////// set up algo \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#//////////////////////////////////             \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
class Stack:
    def __init__(self):
        self.stack = []

    def __len__(self):
        return len(self.stack)

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        return self.stack.pop()

    def top(self):
        return self.stack[-1]


#//////////////////////////////////           \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#////////////////////////////////// MAIN LOOP \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#//////////////////////////////////           \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
def main(screen,pixel_value,dimension_value):

    global square_width, player_rect, border, level, yellow_square_generated, collected

    maze_width =pixel_value
    maze_height = dimension_value

    square_width = round(440 / max(maze_width, maze_height))
    player_rect = square_width - square_width / 5
    border = square_width / 5
    loop = True
    stack = Stack()
    stack.push(Square(0, 0, square_width, maze_width, maze_height, square_width, screen.get_size()))
    squares = [stack.top()]
    maze_generated = False

    clock = pygame.time.Clock()

    player_pos = pygame.Vector2(stack.top().square_x, stack.top().square_y)

    level = level
    police = pygame.font.Font("Wisscraft.ttf", 50)
    police2 = pygame.font.Font("Wisscraft.ttf", 25)
    level_text = police.render("LEVEL " + str(level), True, (255, 40, 0))
    taille_text = police2.render(str(maze_width) + "x" + str(maze_height), True, (255, 40, 0))

    yellow_square_generated = False
    collected = False

    ost=["ost/1.mp3","ost/2.mp3",'ost/3.mp3']
    while loop:

        if pygame.mixer.music.get_busy()==False:
                
            if maze_width * maze_height >=100:
                ost=[]
                ost.append('ost/amixem.mp3')
                ost.append('ost/A_Hundred_Truth.mp3')
                ost.append('ost/PIANO.mp3')
            if maze_width * maze_height >=324:
                ost.remove('ost/PIANO.mp3')
                ost.append('ost/CROSSEX.mp3')
                ost.append('ost/Dilema.mp3')

            music=random.choice(ost)
            pygame.mixer.music.load(music)
            print(music)
            pygame.mixer.music.play()
            print(ost)

            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                if screen.get_at((int(player_pos.x), int(player_pos.y - 1))) == (255, 255, 255) or screen.get_at((int(player_pos.x), int(player_pos.y - 1))) == (102, 102, 102) or screen.get_at((int(player_pos.x), int(player_pos.y - 1))) == (99,16,16):
                    player_pos.y -= player_rect + border
            elif keys[pygame.K_DOWN]:
                if screen.get_at((int(player_pos.x), int(player_pos.y + player_rect))) == (255, 255, 255) or screen.get_at((int(player_pos.x), int(player_pos.y + player_rect))) == (102, 102, 102) or screen.get_at((int(player_pos.x), int(player_pos.y + player_rect))) == (99, 16, 16):
                    player_pos.y += player_rect + border
            elif keys[pygame.K_LEFT]:
                if screen.get_at((int(player_pos.x - 1), int(player_pos.y))) == (255, 255, 255)  or screen.get_at((int(player_pos.x - 1), int(player_pos.y))) == (102, 102, 102) or screen.get_at((int(player_pos.x - 1), int(player_pos.y))) == (99, 16, 16):
                    player_pos.x -= player_rect + border
            elif keys[pygame.K_RIGHT]:
                if screen.get_at((int(player_pos.x + player_rect), int(player_pos.y))) == (255, 255, 255) or screen.get_at((int(player_pos.x + player_rect), int(player_pos.y))) == (102, 102, 102) or screen.get_at((int(player_pos.x + player_rect), int(player_pos.y))) == (99, 16, 16):
                    player_pos.x += player_rect + border

        draw_screen(screen, squares, maze_generated, screen.get_size(), player_pos, player_rect, border, level_text, taille_text,maze_width,maze_height)

        if collect_yellow_square(player_pos, squares):
            collected = True

        if is_on_red_square(player_pos, squares,maze_height,maze_width):
            if collected and all(square.is_collected for square in squares if square.is_yellow):  
                level += 1
                taille_text = police2.render(str(maze_width) + "x" + str(maze_height), True, (255, 40, 0))
                level_text = police.render("LEVEL " + str(level), True, (255, 40, 0))
                main(screen,random.choice([maze_width, maze_width + 1]),random.choice([maze_height, maze_height + 1]))

        while not next_square(stack, squares, maze_width, maze_height, square_width) and len(stack) != 1:
            stack.pop()
        if len(squares) == maze_width * maze_height and len(stack) == 1:
            maze_generated = True

        clock.tick(120)

        if maze_generated and not yellow_square_generated and not any(square.is_yellow for square in squares):
            yellow_squares_count = calculate_yellow_squares_count(maze_width, maze_height)
            available_squares = []
            for square in squares:
                # Pour les grilles de grande taille, inclure les carrés blancs et gris dans les carrés disponibles
                if square.color in [(255, 255, 255), (102, 102, 102),(99,16,16)] and not (square.x == 0 and square.y == 0) and not (square.x == maze_width - 1 and square.y == maze_height - 1):
                    available_squares.append(square)

            if available_squares:
                for _ in range(yellow_squares_count):
                    random_white_square = random.choice(available_squares)
                    yellow_square_x = random_white_square.square_x + (random_white_square.square_width - player_rect) / 2
                    yellow_square_y = random_white_square.square_y + (random_white_square.square_width - player_rect) / 2
                    yellow_square = Square(random_white_square.x, random_white_square.y, player_rect, maze_width, maze_height, player_rect, win_size)
                    yellow_square.square_x = yellow_square_x
                    yellow_square.square_y = yellow_square_y
                    yellow_square.change_to_yellow(player_rect)
                    squares.append(yellow_square)
                    yellow_square_generated = True
     


#//////////////////////////////////           \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#//////////////////////////////////    ALGO   \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#//////////////////////////////////           \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
class Square:
    def __init__(self, x, y, width, maze_width, maze_height, square_width, win_size):
        self.east = False
        self.south = False
        self.total_width = width
        self.square_width = width * 4/5
        self.square_x = (win_size[0] - maze_width * square_width) / 2 + width * x + width / 10
        self.square_y = (win_size[1] - maze_height * square_width) / 2 + width * y + width / 10
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.square_x, self.square_y, self.square_width, self.square_width)
        if maze_height*maze_width < 100:
            self.color = (255, 255, 255)  # Couleur par défaut (blanc)
        elif maze_height*maze_width < 324: 
            self.color=(102,102,102)
        else:
            self.color=(99,16,16)
        self.is_yellow = False  # Ajout d'un attribut pour vérifier si le carré est jaune
        self.is_collected = False  # Ajout d'un attribut pour suivre si le carré jaune a été collecté

    def draw(self, screen,maze_width,maze_height):
        
        vx = vy = 0
        if self.east:
            vx = self.total_width / 5
        if self.south:
            vy = self.total_width / 5
        rect_east = pygame.Rect(self.square_x, self.square_y, self.square_width + vx, self.square_width)
        rect_south = pygame.Rect(self.square_x, self.square_y, self.square_width, self.square_width + vy)
        pygame.draw.rect(screen, self.color, rect_east)
        pygame.draw.rect(screen, self.color, rect_south)

        if self.x == maze_width - 1 and self.y == maze_height - 1:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)
        if self.x == 0 and self.y == 0:
            pygame.draw.rect(screen, (0, 255, 0), self.rect)

        # Dessiner un indicateur visuel si le carré jaune a été collecté
        if self.is_yellow and self.is_collected:
            pygame.draw.circle(screen, (0, 255, 0), (int(self.square_x + self.square_width / 2), int(self.square_y + self.square_width / 2)), 5)

    def change_to_yellow(self, player_rect):
        self.color = (255, 255, 0)  # Jaune
        self.square_width = player_rect
        self.is_yellow = True  # Mettre à jour l'attribut pour indiquer que le carré est jaune
        self.is_collected = False  # Initialiser à False lors de la création

def draw_screen(screen, squares, maze_generated, win_size, player_pos, player_rect, border, level_text, taille_text,maze_width,maze_height):
    screen.fill((0, 0, 0))
    for square in squares:
        if not (square.is_yellow and square.is_collected):  # Ne dessiner que les carrés jaunes non récoltés
            square.draw(screen,maze_width,maze_height)
    if maze_generated:
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(player_pos.x, player_pos.y, player_rect, player_rect))

    # Calculer la position X pour le texte du niveau
    level_text_width, _ = level_text.get_size()
    level_text_x = (win_size[0] - level_text_width) // 2
    level_text_y = 10

    # Afficher le texte du niveau
    screen.blit(level_text, (level_text_x, level_text_y))

    # Positionner le texte de la taille dans le coin en bas à gauche
    taille_text_x = 10
    taille_text_y = win_size[1] - taille_text.get_height() - 10

    # Afficher le texte de la taille
    screen.blit(taille_text, (taille_text_x, taille_text_y))

    pygame.display.flip()

def next_square(stack, squares, maze_width, maze_height, square_width):
    visited = {(square.x, square.y) for square in squares}
    last = stack.top()
    x = last.x
    y = last.y
    possibility = [1, 1, 1, 1]
    if x == 0 or (x - 1, y) in visited:
        possibility[0] = 0
    if x == maze_width - 1 or (x + 1, y) in visited:
        possibility[1] = 0
    if y == 0 or (x, y - 1) in visited:
        possibility[2] = 0
    if y == maze_height - 1 or (x, y + 1) in visited:
        possibility[3] = 0

    if sum(possibility):
        index = random.randint(0, 3)
        while possibility[index] == 0:
            index = random.randint(0, 3)
        if index == 0:
            s = Square(x - 1, y, square_width, maze_width, maze_height, square_width, win_size)
            s.east = True
        elif index == 1:
            last.east = True
            s = Square(x + 1, y, square_width, maze_width, maze_height, square_width, win_size)
        elif index == 2:
            s = Square(x, y - 1, square_width, maze_width, maze_height, square_width, win_size)
            s.south = True
        else:
            last.south = True
            s = Square(x, y + 1, square_width, maze_width, maze_height, square_width, win_size)

        stack.push(s)
        squares.append(s)
        return True
    return False


#//////////////////////////////////                    \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#////////////////////////////////// Victory Conditions \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#//////////////////////////////////                    \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
def is_on_red_square(player_pos, squares,maze_height,maze_width):
    for square in squares:
        if square.x == maze_width - 1 and square.y == maze_height - 1:
            red_square_rect = pygame.Rect(square.square_x, square.square_y, square.square_width, square.square_width)
            if red_square_rect.collidepoint(player_pos.x, player_pos.y):
                return True
    return False

def collect_yellow_square(player_pos, squares):
    for square in squares:
        if square.is_yellow and not square.is_collected:  
            yellow_square_rect = pygame.Rect(square.square_x, square.square_y, square.square_width, square.square_width)
            if yellow_square_rect.collidepoint(player_pos.x, player_pos.y):
                square.is_collected = True  # Marquer le carré jaune comme collecté
    return all(square.is_collected for square in squares if square.is_yellow)  # Vérifier si tous les carrés jaunes ont été collectés

def calculate_yellow_squares_count(maze_width, maze_height):
    total_squares = maze_width * maze_height
    yellow_squares_percentage = 0.05
    yellow_squares_count = int(total_squares * yellow_squares_percentage)
    return yellow_squares_count



#//////////////////////////////////           \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#////////////////////////////////// GAME LOOP \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#//////////////////////////////////           \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


if __name__ == '__main__':
    pygame.init()
    win_size = (600, 600)
    win = pygame.display.set_mode(win_size)
    while done :
        draw_interface(win)
    pygame.quit()