import sys
import pygame
from pygame.locals import *
from Player import Player
from Scene import Scene
import asyncio
import time

#TODO: create multiple scenes for diff rooms
#TODO: function to initiate all sprites
#TODO: async function to load game modes

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

# #initiate sprites
# home_player = Player(RESOLUTION, (RESOLUTION[0]/2, 480), [all_sprites])

### game mode functions ###
async def home_mode():
    #initialize mode
    current_mode = "home"
    #TODO: fix
    home_player = Player(RESOLUTION, (RESOLUTION[0]/2, 480), [all_sprites])
    display.blit(home_old.background, (0,0))
    
    home_player.move(5, current_mode)
    display.blit(home_player.image, home_player.rect)
    # #load sprites
    # for sprite in all_sprites:
    #     display.blit(sprite.image, sprite.rect)

    pygame.display.update()
    fps_clock.tick(fps)

    #check for game mode change
    if dance_game_entry.colliderect(home_player.rect):
        return "dance game"
    elif shop_game_entry.colliderect(home_player.rect):
        return "shop game"

async def dance_game():
    current_mode = "dance game"
    #TODO: fix
    dance_player = Player(RESOLUTION, (300, 300), [all_sprites])

    while True:
        display.blit(dance_scene.background, (0,0))
        #TODO: change the player according to game mode
        dance_player.move(5, current_mode)

        for sprite in all_sprites:
            display.blit(sprite.image, sprite.rect)

        pygame.display.update()
        fps_clock.tick(fps)
            
### game update loop ###

async def main():
    while True:
        #quit game 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        change_mode = await home_mode()
        print(change_mode)

        if change_mode == "dance game":
            time.sleep(1)
            await dance_game()
        
    


# def main():
#     current_mode = "home"
#     while True:
#         #quit game 
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()

#         #change background based on game mode
#         #TODO: HINT change here
#         if current_mode == "home":
#             display.blit(home_old.background, (0,0))
#         elif current_mode == "dance game":
#             display.blit(dance_scene.background, (0,0))
#         elif current_mode == "shop game":
#             display.blit(shop_scene.background, (0,0))

#         #load sprites
#         for sprite in all_sprites:
#             display.blit(sprite.image, sprite.rect)

#         #update
#         player.move(5, current_mode)
#         # update game mode if player rect collides with game rect
#         #TODO: HINT change here
#         if current_mode == "home":
#             if dance_game_entry.colliderect(player.rect):
#                 current_mode = "dance game"
#             elif shop_game_entry.colliderect(player.rect):
#                 current_mode = "shop game"

#         pygame.display.update()
#         fps_clock.tick(fps)


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
    # main()
    asyncio.run(main())