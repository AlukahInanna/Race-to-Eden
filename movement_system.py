import pygame
import sys
from simple_pause import PauseMenu # Import your pause menu class from simple_pause.py

def build_default_background(screen):
    """Create a simple full-screen fallback background for gameplay."""
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    return background

def run_game(screen, bg_image=None, master_volume=1.0, music_volume=0.8, sfx_volume=0.8):
    
    clock = pygame.time.Clock()
    game_running = True
    game_bg = bg_image if bg_image is not None else build_default_background(screen)
    
    # --- 1. PLAYER SETUP ---
    # Start the player in the middle of the screen
    player_pos = pygame.math.Vector2(screen.get_width() // 2, screen.get_height() // 2)
    player_speed = 300 # Pixels per second
    player_size = 40
    
    # Create a simple red square to represent the player for now
    player_image = pygame.Surface((player_size, player_size))
    player_image.fill((200, 50, 50))
    player_rect = player_image.get_rect(center=(player_pos.x, player_pos.y))
    # -----------------------

    while game_running:
        # Calculate Delta Time (dt) to ensure smooth movement regardless of framerate
        dt = clock.tick(60) / 1000 

        # --- 2. EVENT HANDLING ---
        for event in pygame.event.get():
            
                
            if event.type == pygame.KEYDOWN:
        
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p :
                    
                    # 1. Create the pause menu object
                    pause_menu = PauseMenu(screen)
                    
                    # 2. Open the menu. The game loop FREEZES here!
                    action = pause_menu.display()
                    
                    # 3. Handle what the player clicked in the pause menu
                    if action == "menu":
                        return "menu"
                    
                    if action == "settings":
                        pass
                    
                    elif action == "resume":
                        # They clicked 'Resume' or pressed ESC again.
                        # Do nothing, the game loop just continues!
                        pass
                # -------------------------

        # --- 3. GAME LOGIC & MOVEMENT ---
        # Get all keys currently being held down
        keys = pygame.key.get_pressed()
        
        # Create a movement vector starting at (0, 0)
        direction = pygame.math.Vector2(0, 0)
        
        # Check WASD keys
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            direction.y = -1 # Up
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            direction.y = 1  # Down
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction.x = -1 # Left
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction.x = 1  # Right

        # Normalize the vector so diagonal movement isn't faster
        if direction.length() > 0:
            direction = direction.normalize()
            
        # Update player position
        player_pos += direction * player_speed * dt
        player_rect.center = (int(player_pos.x), int(player_pos.y))
        
        # --- 4. DRAWING ---
        # Draw the background first
        screen.blit(game_bg, (0, 0))
            
        # Draw the player on top of the background
        screen.blit(player_image, player_rect)
        
        pygame.display.flip()
       


def main(master_volume, music_volume, sfx_volume):
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Movement & Pause Test")
    
    # Fake font and background for testing
    test_bg = build_default_background(screen)
    
    print("Use WASD or Arrows to move. Press ESC to Pause.")
    
    # Run the game loop
    result = run_game(screen, test_bg, master_volume, music_volume, sfx_volume)
    
    if result == "menu":
        import menu
        menu.run_menu()
        return

    print(f"Game ended. Returning to: '{result}'")
    pygame.quit()
    sys.exit()
