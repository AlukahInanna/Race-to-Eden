import pygame
import sys
import os
import settings
# Initialize Pygame
pygame.init()
cript_dir = os.path.dirname(__file__)

# --- NEW: LOAD AND PLAY MUSIC ---
music_path = os.path.join(cript_dir, "GameMenuMusic.mp3")
try:
    pygame.mixer.music.load(music_path)
    # Play the music. The '-1' tells Pygame to loop it infinitely!
    pygame.mixer.music.play(-1) 
    
    # Set default starting volume (Master 1.0 * Music 0.8)
    pygame.mixer.music.set_volume(0.8) 
except pygame.error:
    print("WARNING: Could not load 'music.mp3'. Check the file name!")
# 1. Set up the 1080p display
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Race to Eden")

# 2. Set up our fonts
# We use a huge font for the title and a smaller one for the buttons
title_font = pygame.font.Font("letters.ttf", 160)
button_font = pygame.font.Font("letters.ttf", 50) 

# Load the background image and scale it to fit 1080p
script_dir = os.path.dirname(__file__)
image_path = os.path.join(script_dir, "background.png") 
bg_image = pygame.image.load(image_path).convert() 
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_button(screen, text, center_x, center_y, mouse_pos):
    """Draws clickable text that changes color on hover."""
    # 1. Render the text temporarily to get its exact dimensions and create a hitbox
    temp_surf = button_font.render(text, True, (255, 255, 255))
    button_rect = temp_surf.get_rect(center=(center_x, center_y))
    
    # 2. Check if the mouse is hovering over the text's invisible hitbox
    if button_rect.collidepoint(mouse_pos):
        color = (255, 215, 0)  # Gold/Yellow for hover state
    else:
        color = (255, 255, 255)  # White for normal state
        
    # 3. Render the text again with the correct color
    final_text_surf = button_font.render(text, True, color)
    
    # 4. Draw the colored text to the screen
    screen.blit(final_text_surf, button_rect)
    
    return button_rect

def run_menu():
    menu_running = True
    
    button_width = 480
    button_height = 110
    
    # Math to find the exact horizontal center of the screen
    center_x = (SCREEN_WIDTH // 2)
    
    while menu_running:
        screen.blit(bg_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos() 
        
        # --- NEW: Draw the Game Title ---
        # We render it in white (255, 255, 255), but you can change these RGB numbers!
        title_surf = title_font.render("Race to Eden", True, (255, 255, 255))
        # Center the title at X = middle of screen, Y = 200 (near the top)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 200)) 
        screen.blit(title_surf, title_rect)
        # --------------------------------
        
        # Draw buttons below the title (Starting at Y = 450 to give the title breathing room)
        start_button = draw_button(screen, "Start Game", center_x, 450, mouse_pos)
        settings_button = draw_button(screen, "Settings", center_x, 570, mouse_pos)
        exit_button = draw_button(screen, "Exit", center_x, 690, mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if start_button.collidepoint(mouse_pos):
                        print("Start Game clicked!")
                        menu_running = False 
                    elif settings_button.collidepoint(mouse_pos):
                        settings.run(screen, bg_image, title_font, button_font)
                        print("Settings clicked!")
                    elif exit_button.collidepoint(mouse_pos):
                        print("Exit clicked!")
                        pygame.quit()
                        sys.exit()
                        
        pygame.display.flip()

if __name__ == "__main__":
    run_menu()
    print("Transitioning to the main game...")
    pygame.quit()