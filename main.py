import sys
import pygame
from pygame.locals import *
from Player import Player
from Scene import Scene
import asyncio
import time

#TODO: create multiple scenes for diff rooms

#initialize pygame engine
pygame.init()

### pygame configurations ###
#refresh rate configs
fps = 60
fps_clock = pygame.time.Clock()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)

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

display = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Shrine Repair")

#initiate sprite groups
all_sprites = pygame.sprite.Group()

#initiate sprites
#TODO: HINT change here
home_player = Player(RESOLUTION, (RESOLUTION[0]/2, 480), [all_sprites], "Draft/player-sprite.png")
dance_player = Player(RESOLUTION, (300, 300), [all_sprites], "Draft/dance_sprite.png")
shop_player = Player(RESOLUTION, (300, 300), [all_sprites], "Draft/shop_game_sprite.png")

### game modes ###
# home mode gameplay loop
def home_mode():
    #initialize mode
    display.blit(home_old.background, (0,0))
    home_player.move(5, "home")
    display.blit(home_player.image, home_player.rect)

    pygame.display.update()
    fps_clock.tick(fps)

# dance mode gameplay loop
#TODO: update
def dance_game():
    #TODO: change to button exit after minigame finish or auto finish
    display.blit(dance_scene.background, (0,0))
    dance_player.move(5, "dance game")
    display.blit(dance_player.image, dance_player.rect)

    pygame.display.update()
    fps_clock.tick(fps)

# shop mode gameplay loop          
def shop_game():
    #TODO: change to button exit after minigame finish or auto finish
    display.blit(shop_scene.background, (0,0))
    shop_player.move(5, "shop game")
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
                    break

        # enter dance game loop
        if current_mode == "dance game":
            while True:
                #check for quit
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                dance_game()
                
                exit_rect = pygame.Rect(200, 380, 100, 100)
                if exit_rect.colliderect(dance_player.rect):
                    # return to home loop after finishing minigame
                    current_mode = "home"
                    break

        # enter shop game loop
        if current_mode == "shop game":
            while True:
                #check for quit
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                shop_game()

                exit_rect = pygame.Rect(200, 380, 100, 100)
                if exit_rect.colliderect(shop_player.rect):
                    # return to home loop after finishing minigame
                    current_mode = "home"
                    break




# def main():
#     while True:
#         #quit game 
#         i = 0 
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == PLAY_MINIGAME:
#                 if event.mode == 'dance':
#                     print("dance game" + str(time.time()))
#                     dance_game()
#                     # display.blit(dance_scene.background, (0,0))
#                     i+=1

#         change_mode = home_mode()
        # print(change_mode)

        # if change_mode == "dance game":
        #     dance_game()


# async def main():
#     while True:
#         #quit game 
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()
#         change_mode = await home_mode()
#         print(change_mode)

#         if change_mode == "dance game":
#             await dance_game()
        


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
    # asyncio.run(main())