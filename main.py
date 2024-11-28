import sys
import pygame
import random
from pygame.locals import *
from Player import Player
from Scene import Scene
from DanceSpotlight import DanceSpotlight
from ShopItem import ShopItem

#TODO: refactor

#initialize pygame engine
pygame.init()

### pygame configurations ###
#refresh rate configs
fps = 60
fps_clock = pygame.time.Clock()

# display config
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)

#font config
font = pygame.font.SysFont("Verdana", 60)
small_font = pygame.font.SysFont("Verdana", 24)

# color config
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# load all scenes
home_old = Scene(RESOLUTION, "art/home_old.PNG")
home_new = Scene(RESOLUTION, "art/home_new.PNG")
dance_scene = Scene(RESOLUTION, "art/dance_game.PNG")
shop_scene = Scene(RESOLUTION, "art/shop_game.PNG")
sorting_scene = Scene(RESOLUTION, "art/sort_game.PNG")


#configure display window
display = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Shrine Repair")

#initiate sprite groups
all_sprites = pygame.sprite.Group()

#initiate sprites
home_player = Player(RESOLUTION, (RESOLUTION[0]/2, 480), [all_sprites], "art/home_player.PNG")
dance_player = Player(RESOLUTION, (0, 275), [all_sprites], "art/dance_player.PNG")
shop_player = Player(RESOLUTION, (320, 400), [all_sprites], "art/shop_player.PNG")
sorting_player = Player(RESOLUTION, (320, 450), [all_sprites], "art/sort_player.PNG")

# minigame events
SCORE_UP = pygame.USEREVENT + 1 # create new user defined event
GAMEPLAY_TIMER = pygame.USEREVENT + 2

dance_flag = False
shop_flag = False
sort_flag = False
completion_status = False

### utility functions ###
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text

### game modes ###
# home mode gameplay loop
def home_mode():
    # if all games have been completed draw new bg
    if completion_status:
        display.blit(home_new.background, (0,0))
    else:
        # draw old bg
        display.blit(home_old.background, (0,0))
        
    #move and draw player
    home_player.move(5, "home")
    display.blit(home_player.image, home_player.rect)

    pygame.display.update()
    fps_clock.tick(fps)

# dance mode gameplay loop
def dance_game(score, spotlight, live_spotlight):
    #show score in corner and draw bg
    score_text = f"Score: {score}"
    score_display = small_font.render(score_text, True, WHITE)
    display.blit(dance_scene.background, (0,0))
    display.blit(score_display, (24, 8))

    #variable to hold spotlight status
    spotlight_status = live_spotlight
    #if a spotlight is currently live
    if live_spotlight:
        #draw spotlight and player
        display.blit(spotlight.image, spotlight.rect)
        dance_player.move(move_speed=5, mode="dance game")
        display.blit(dance_player.image, dance_player.rect)

        #add score when player reaches spotlight and kill spotlight
        if dance_player.rect.colliderect(spotlight.rect):
            spotlight.kill()
            # indicate that a SCORE_UP event has occured
            inc_score = pygame.event.Event(SCORE_UP) 
            pygame.event.post(inc_score)
            spotlight_status = False

    #if spotlight is not live
    else:
        #kill it to prevent the sprite rect from being created
        spotlight.kill()
        spotlight_status = False

        dance_player.move(5, "dance game")
        display.blit(dance_player.image, dance_player.rect)


    pygame.display.update()
    fps_clock.tick(fps)

    return spotlight_status

# shop mode gameplay loop          
def shop_game(score, item_group):
    #show score in corner and draw bg
    score_text = f"Score: {score}"
    score_display = small_font.render(score_text, True, WHITE)
    display.blit(shop_scene.background, (0,0))
    display.blit(score_display, (24, 8))
    shop_player.move(5, "shop game")
    
    #for each item created
    for item in item_group:
        #draw and move item
        item.move()
        display.blit(item.image, item.rect)

        #add score when player collides with item
        if shop_player.rect.colliderect(item.rect):
            item.kill()
            inc_score = pygame.event.Event(SCORE_UP)
            pygame.event.post(inc_score)

    display.blit(shop_player.image, shop_player.rect)

    pygame.display.update()
    fps_clock.tick(fps)

# QA game logic
def sort_game(current_question, score, question_status):
    # Draw background and score
    display.blit(sorting_scene.background, (0, 0))
    score_text = f"Score: {score}"
    score_display = small_font.render(score_text, True, WHITE)
    display.blit(score_display, (24, 8))
    
    #  question display
    # question_display = small_font.render(current_question["question"], True, WHITE)
    # display.blit(question_display, (24, 60))
    text_display = pygame.Rect((120,40,418, 200))
    drawText(display, current_question["question"], BLACK, text_display, small_font)

    user_answer = ''

    # user input true or false by moving
    true_rect = pygame.Rect((0, 161, SCREEN_WIDTH/3, SCREEN_HEIGHT-161))
    false_rect = pygame.Rect(((640*2/3), 161, SCREEN_WIDTH/3, SCREEN_HEIGHT-161))

    sorting_player.move(5, "sort game")
    display.blit(sorting_player.image, sorting_player.rect)

    if question_status == True:
        if true_rect.colliderect(sorting_player.rect):
            user_answer = 'True'
            sorting_player.spawn()
        elif false_rect.colliderect(sorting_player.rect):
            user_answer = 'False'
            sorting_player.spawn()
    
    # check user input correct or not
    if not len(user_answer) == 0:
        if user_answer == current_question["answer"]:
            print("Correct!")
            inc_score = pygame.event.Event(SCORE_UP) 
            pygame.event.post(inc_score)
            question_status = False
        else:
            print(f"Incorrect! The correct answer was {current_question['answer']}.")
            question_status = False
    

    pygame.display.update()
    fps_clock.tick(fps)

    return question_status


### game update loop ###
def main():
    # access completion flags
    global completion_status
    global sort_flag, shop_flag, dance_flag

    current_mode = "home"
    # scene entry points aka rect
    scene_entries = []
    dance_game_entry = pygame.Rect((154.1, 0, 300.1, 211)) #(left top x, left top y, width, height)
    scene_entries.append(dance_game_entry)
    shop_game_entry = pygame.Rect((0, 84, 84, 161))
    scene_entries.append(shop_game_entry)
    sorting_game_entry = pygame.Rect((444, 0, 184, 218))
    scene_entries.append(sorting_game_entry)

    while True:
        #check for minigame completion status
        if shop_flag and dance_flag and sort_flag:
            completion_status = True
        else:
            completion_status = False
        # start game in home loop
        if current_mode == "home":
            home_player.spawn()
            while True:
                #check for quit
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                home_mode()

                # update game mode if player rect collides with game rect
                if dance_game_entry.colliderect(home_player.rect):
                    current_mode = "dance game"
                    break
                elif shop_game_entry.colliderect(home_player.rect):
                    current_mode = "shop game"
                    break
                elif sorting_game_entry.colliderect(home_player.rect): 
                    current_mode = "sort game"
                    break

        # enter dance game loop
        if current_mode == "dance game":
            #create a spotlight instance
            spotlight = DanceSpotlight()
            #respawn the spotlight every second
            pygame.time.set_timer(GAMEPLAY_TIMER, 1000)
            live_spotlight = False

            score = 0
            while score < 10:
                for event in pygame.event.get():
                    #check for quit
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    #check for increase in score
                    if event.type == SCORE_UP:
                        score += 1

                    #check for event to spawn spot
                    if event.type == GAMEPLAY_TIMER:
                        live_spotlight = True
                        spotlight.spawn()
                        
                #update spotlight status
                live_spotlight = dance_game(score, spotlight, live_spotlight)

            # update dance completion status
            dance_flag = True
            # return to home mode after minigame
            current_mode = "home"

        # enter shop game loop
        if current_mode == "shop game":
            #sprite group to hold items
            item_group = pygame.sprite.Group()
            pygame.time.set_timer(GAMEPLAY_TIMER, 1000)

            score = 0
            while score < 10:
                #check for quit
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    #check for increase in score
                    if event.type == SCORE_UP:
                        score += 1

                    #create a new shop item every second
                    if event.type == GAMEPLAY_TIMER:
                        item_group.add(ShopItem())
                        print(item_group)

                shop_game(score, item_group)

            # update dance completion status
            shop_flag = True
            # return to home mode after minigame
            current_mode = "home"
            
        if current_mode == "sort game":
            # Questions and Answers Database
            qa_data = [
                {"question": "The main deity of a Japanese shrine is referred to as 'Kami'.", "answer": 'True'},
                {"question": "Komainu in shrines are regarded as decorations rather than guardians.", "answer": 'False'},
                {"question": "The traditional Japanese festival 'Hatsuha' is held on New Year's Day, January 1st.", "answer": 'True'},
                {"question": "The 'Torii' in a shrine symbolizes the connection between humans and gods.", "answer": 'True'},
                {"question": "Harvest festivals and Shichi-Go-San are unrelated to Japanese shrines.", "answer": 'False'},
                {"question": "Common offerings in shrines are limited to money and flowers.", "answer": 'False'},
            ]
            asked_questions = []
            # Randomly select a question that hasn't been asked
            question_index = random.choice([i for i in range(len(qa_data)) if i not in asked_questions])
            current_question = qa_data[question_index]
            asked_questions.append(question_index)

            #track question status and score
            question_status = True
            score=0
            while len(asked_questions) <= len(qa_data):
                #check for quit
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == SCORE_UP:
                        score += 1

                # if there is an existing question
                if question_status:
                    print(current_question)
                else:
                    #check if it is the last question
                    if not len(asked_questions) == len(qa_data):
                        question_index = random.choice([i for i in range(len(qa_data)) if i not in asked_questions])
                        current_question = qa_data[question_index]
                        asked_questions.append(question_index)
                        question_status = True
                        print(current_question)
                    else:
                        # if last question has been answered or not
                        if question_status:
                            continue
                        else:
                            break

                question_status = sort_game(current_question, score, question_status)

            if score >= 6:
                print("Congratulations! You've completed the game.")
                sort_flag = True
            else:
                print("Game over! Better luck next time.")
            # return to home mode after minigame
            current_mode = "home"

if __name__ == '__main__':
    main()