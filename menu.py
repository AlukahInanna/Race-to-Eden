import pygame
import sys
import os
import settings
import movement_system
# Initialize Pygame
pygame.init()
cript_dir = os.path.dirname(__file__)

master_volume = 1.0
music_volume = 0.75
sfx_volume = 0.8

def music(master_volume, music_volume):
    music_path = os.path.join(cript_dir, "music","GameMenuMusic.mp3") #music path
    try:
        pygame.mixer.music.load(music_path)
        
        pygame.mixer.music.play(-1) 
        
        
        pygame.mixer.music.set_volume(master_volume * music_volume) 
    except pygame.error:
        print("Error start menu music")

#default resolution
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Race to Eden")

# set up fonts
title_font = pygame.font.Font("fonts/letters.ttf", 160)
button_font = pygame.font.Font("fonts/letters.ttf", 50) 

# Load the background image and scale to 1080p
script_dir = os.path.dirname(__file__)
image_path = os.path.join(script_dir, "images/background.png") #path of the picture
bg_image = pygame.image.load(image_path).convert() 
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_button(screen, text, center_x, center_y, mouse_pos):
    
    # creates a temporary image of the text to measure size
    temp_surf = button_font.render(text, True, (255, 255, 255))
    #it makes a rectange exaclty centred where we want it
    button_rect = temp_surf.get_rect(center=(center_x, center_y))
    
    #check where if the mouse is in the rectange
    if button_rect.collidepoint(mouse_pos):
        color = (255, 215, 0)  
    else:
        color = (255, 255, 255)  
        
    # changes the  color
    final_text_surf = button_font.render(text, True, color)
    
    # draw the colored text to the screen
    screen.blit(final_text_surf, button_rect)
    
    return button_rect

def run_menu():
    global master_volume, music_volume, sfx_volume
    menu_running = True
    music(master_volume, music_volume)
    
    center_x = (SCREEN_WIDTH // 2) #center of the screen
    
    while menu_running:
        screen.blit(bg_image, (0, 0)) #loads the backgound to the screen
        mouse_pos = pygame.mouse.get_pos() 
        
        
        
        title_surf = title_font.render("Race to Eden", True, (255, 255, 255)) #  render it in white (255, 255, 255)
       
        title_rect = title_surf.get_rect(center=(center_x, 200)) #possition on the screen
        screen.blit(title_surf, title_rect)#output to the screen
       
        
        # buttons below the title
        start_button = draw_button(screen, "Start Game", center_x, 450, mouse_pos)
        settings_button = draw_button(screen, "Settings", center_x, 570, mouse_pos)
        exit_button = draw_button(screen, "Exit", center_x, 690, mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # so the x on the screen works
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: #mouse sellection
                if event.button == 1: 
                    if start_button.collidepoint(mouse_pos): #main game loads
                        print("Start Game clicked!")
                        pygame.mixer.music.stop()
                        movement_system.main(master_volume, music_volume, sfx_volume)
                    elif settings_button.collidepoint(mouse_pos):#seetings page loads
                        music_volume, sfx_volume, master_volume = settings.run(master_volume,music_volume,sfx_volume)
                        print("Settings clicked!")
                    elif exit_button.collidepoint(mouse_pos):#exit button on the screen
                        print("Exit clicked!")
                        pygame.quit()
                        sys.exit()
                        
        pygame.display.flip()

if __name__ == "__main__":
    run_menu()
    print("Transitioning to the main game...")
    pygame.quit()
