import sys
import pygame
from pygame.locals import *
from Player import Player
from Scene import Scene
from DanceSpotlight import DanceSpotlight
from ShopItem import ShopItem

#TODO: add flag for completion of minigames

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

# color config
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# load all scenes
home_old = Scene(RESOLUTION, "Draft/home-old.jpg")
home_new = Scene(RESOLUTION, "Draft/home-new.jpg")
dance_scene = Scene(RESOLUTION, "Draft/Game1.jpg")
shop_scene = Scene(RESOLUTION, "Draft/Game2.jpg")
sorting_scene = Scene(RESOLUTION, "Draft/Game3.jpg")

# scene entry points aka rect
#TODO: HINT change here
scene_entries = []
dance_game_entry = pygame.Rect((154.1, 0, 300.1, 211)) #(left top x, left top y, width, height)
scene_entries.append(dance_game_entry)
shop_game_entry = pygame.Rect((0, 84, 84, 161))
scene_entries.append(shop_game_entry)
sorting_game_entry = pygame.Rect((444, 0, 184, 218))
scene_entries.append(sorting_game_entry)

#configure display window
display = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Shrine Repair")

#initiate sprite groups
all_sprites = pygame.sprite.Group()

#initiate sprites
#TODO: HINT change here
home_player = Player(RESOLUTION, (RESOLUTION[0]/2, 480), [all_sprites], "Draft/player-sprite.png")
dance_player = Player(RESOLUTION, (0, 255), [all_sprites], "Draft/dance_sprite.png")
shop_player = Player(RESOLUTION, (320, 400), [all_sprites], "Draft/shop_game_sprite.png")
sorting_player = Player(RESOLUTION, (320, 400), [all_sprites], "sorting_game_sprite.jpg")

# minigame events
SCORE_UP = pygame.USEREVENT + 1 # create new user defined event
GAMEPLAY_TIMER = pygame.USEREVENT + 2

dance_flag = False
shop_flag = False
sort_flag = False
completion_status = False

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
#TODO: clean up logic
def dance_game(score, spotlight, live_spotlight):
    #show score in corner and draw bg
    score_text = f"Score: {score}"
    score_display = font.render(score_text, True, RED)
    display.blit(dance_scene.background, (0,0))
    display.blit(score_display, (24, 24))

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
    score_display = font.render(score_text, True, RED)
    display.blit(shop_scene.background, (0,0))
    display.blit(score_display, (24, 24))
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


### game update loop ###
def main():
    current_mode = "home"
    while True:
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
                #TODO: HINT change here
                if dance_game_entry.colliderect(home_player.rect):
                    current_mode = "dance game"
                    break
                elif shop_game_entry.colliderect(home_player.rect):
                    current_mode = "shop game"
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
            while True:
                #check for quit
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

            #TODO: put sort game function here

            # return to home mode after minigame
            current_mode = "home"

#main():
# load home map
# current mode = home
# player moves
# if player collides with rect
# change mode to game
# await game to play out
# after game check whether completion flag for each game has been raised
# if yes, change background to new
# else pass

if __name__ == '__main__':
    main()