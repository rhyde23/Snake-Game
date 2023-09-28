import pygame, random, pickle

pygame.init()

platform = pygame.display.set_mode((340, 300))
pygame.display.set_caption('Snake')

red = (255, 0, 0, 100)
dark_green = (20, 20, 20)
light_green = (0, 200, 0, 100)
green = (0, 75, 0, 100)
black = (0, 0, 0)

def initialize_transparent_surface(color) :
    image = pygame.Surface([20, 20], pygame.SRCALPHA, 32)
    image = image.convert_alpha()
    image.fill(color)
    return image

head = initialize_transparent_surface(light_green)
body = initialize_transparent_surface(green)
apple = initialize_transparent_surface(red)

display_coordinates = []
for x in range(0, 340, 20) :
    for y in range(0, 300, 20) :
        display_coordinates.append([x, y])

def display_snake(snake) :
    for i, s in enumerate(snake) :
        if i == len(snake) - 1 :
            platform.blit(head, (s[0], s[1]))
        else :
            platform.blit(body, (s[0], s[1]))

def randomize_apple_coordinates() :
    return random.choice([pos for pos in display_coordinates if pos not in snake])

def get_difference(pos1, pos2) :
    return [pos1[0]-pos2[0], pos1[1]-pos2[1]]

highscore = pickle.load(open('/home/pi/Desktop/Snake/gameData.dat', 'rb'))

loop = True
game = False
menu = True

font = pygame.font.SysFont('Arial', 15)
menu_texts = [font.render('Press any key to play.', True, black), font.render('Highscore: ' + str(highscore), True, black)]

while loop :
    while game :
        platform.fill(dark_green)
        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                key = pygame.key.name(event.key)
                if key in motions :
                    motion = motions[key]
                    if key in motions_horizontal :
                        motions = motions_vertical
                    else :
                        motions = motions_horizontal
        if motion != [0, 0] :
            if delay == 0 :
                snake.pop(0)
                snake.append([snake[-1][0]+motion[0], snake[-1][1]+motion[1]])
                delay = 100
                if snake[-1] == apple_coordinates :
                    apple_coordinates = randomize_apple_coordinates()
                    difference = get_difference(snake[0], snake[1])
                    snake.insert(0, [snake[0][0]+difference[0], snake[0][1]+difference[1]])
                    score += 1
            delay -= 1
        display_snake(snake)
        platform.blit(apple, (apple_coordinates[0], apple_coordinates[1]))
        if snake[-1] not in display_coordinates or 2 in [snake.count(s) for s in snake] :
            game = False
            menu = True
            if score > highscore :
                pickle.dump(score, open('/home/pi/Desktop/Snake/gameData.dat', 'wb'))
                highscore = score
                menu_texts = [font.render('Press any key to play.', True, black), font.render('Highscore: ' + str(highscore), True, black), font.render('Score: ' + str(score), True, black), font.render('New Highscore!', True, black)]
            else :
                menu_texts = [font.render('Press any key to play.', True, black), font.render('Highscore: ' + str(highscore), True, black), font.render('Score: ' + str(score), True, black)]
        pygame.display.update()
    while menu :
        platform.fill(red)
        for y, menu_text in enumerate(menu_texts) :
            platform.blit(menu_text, (0, y*50))
        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                menu = False
                game = True
                snake = [[80, 160], [100, 160]]
                apple_coordinates = [200, 160]
                motions_horizontal = {'right':[20, 0], 'left':[-20, 0]}
                motions_vertical = {'down':[0, 20], 'up':[0, -20]}
                motions = {'right':[20, 0], 'left':[-20, 0], 'down':[0, 20], 'up':[0, -20]} 
                motion = [0, 0]
                delay = 0
                score = 0
        pygame.display.update()
                
