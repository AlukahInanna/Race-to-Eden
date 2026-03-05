import pygame
import sys


class Button:
    """A blueprint for all clickable text buttons."""
    def __init__(self, text, center_x, center_y, font):
        self.text = text
        self.font = font
        
        # Pre-calculate the button's invisible hitbox (rect)
        temp_surf = self.font.render(self.text, True, (255, 255, 255))
        self.rect = temp_surf.get_rect(center=(center_x, center_y))

    def draw(self, screen, mouse_pos):
        """Draws the text and changes color if the mouse hovers over it."""
        if self.rect.collidepoint(mouse_pos):
            color = (255, 215, 0)  # Gold for hover
        else:
            color = (255, 255, 255)  # White for normal
            
        text_surf = self.font.render(self.text, True, color)
        screen.blit(text_surf, self.rect)

    def handle_event(self, event):
        """Checks if this specific button was clicked."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True # The button was clicked!
        return False

# Volume Sliders
class Slider:
    """A blueprint for interactive volume sliders."""
    def __init__(self, x, y, width, label, font, initial_val=1.0):
        self.x = x
        self.y = y
        self.width = width
        self.label = label
        self.font = font
        self.val = initial_val  
        self.grabbed = False    
        
        self.track_rect = pygame.Rect(x, y, width, 10)
        self.update_knob()

    def update_knob(self):
        """Calculates exactly where the knob should sit."""
        knob_x = self.x + (self.width * self.val)
        self.knob_rect = pygame.Rect(0, 0, 20, 40)
        self.knob_rect.center = (knob_x, self.y + 5)

    def draw(self, screen):
        """Draws the slider, track, and label."""
        # Label text
        text = f"{self.label}: {int(self.val * 100)}%"
        text_surf = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(self.x + (self.width // 2), self.y - 40))
        screen.blit(text_surf, text_rect)

        # Empty grey track
        pygame.draw.rect(screen, (100, 100, 100), self.track_rect)
        
        # Filled gold track
        filled_rect = pygame.Rect(self.x, self.y, self.width * self.val, 10)
        pygame.draw.rect(screen, (255, 215, 0), filled_rect)

        # Draggable Knob
        color = (255, 215, 0) if self.grabbed else (255, 255, 255)
        pygame.draw.rect(screen, color, self.knob_rect)

    def handle_event(self, event):
        """Checks for mouse clicks and dragging."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.knob_rect.collidepoint(event.pos) or self.track_rect.collidepoint(event.pos):
                self.grabbed = True
                self.update_val(event.pos[0])
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.grabbed = False
            
        elif event.type == pygame.MOUSEMOTION:
            if self.grabbed:
                self.update_val(event.pos[0])

    def update_val(self, mouse_x):
        """Updates the internal volume percentage."""
        relative_x = mouse_x - self.x
        self.val = max(0.0, min(relative_x / self.width, 1.0))
        self.update_knob()



# SCREEN MANAGER


class SettingsScreen:
    """Manages the entire settings menu loop, drawing, and events."""
    def __init__(self, screen, bg_image, title_font, button_font):
        self.screen = screen
        self.bg_image = bg_image
        self.title_font = title_font
        self.running = True
        
        center_x = self.screen.get_width() // 2
        slider_x = center_x - 200 
        
        # Create all our UI elements once
        self.sliders = [
            Slider(slider_x, 400, 400, "Master Volume", button_font, 1.0),
            Slider(slider_x, 520, 400, "Music Volume", button_font, 0.8),
            Slider(slider_x, 640, 400, "SFX Volume", button_font, 0.8)
        ]
        
        self.back_button = Button("Back To Main Menu", center_x, 800, button_font)

    def handle_events(self):
        """Processes all user inputs."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Let the UI elements check if they were interacted with
            for slider in self.sliders:
                slider.handle_event(event)
                
            if self.back_button.handle_event(event):
                self.running = False # Clicking back breaks the loop!

    def draw(self):
        """Draws everything to the screen."""
        self.screen.blit(self.bg_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        center_x = self.screen.get_width() // 2
        
        # Draw Title
        title_surf = self.title_font.render("Settings", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(center_x, 200)) 
        self.screen.blit(title_surf, title_rect)
        
        # Draw UI
        for slider in self.sliders:
            slider.draw(self.screen)
            
        self.back_button.draw(self.screen, mouse_pos)

    def start(self):
        """The main loop that keeps the screen alive."""
        while self.running:
            self.handle_events()
            
            # --- NEW: APPLY VOLUMES IN REAL-TIME ---
            # sliders[0] is Master, sliders[1] is Music
            master_vol = self.sliders[0].val
            music_vol = self.sliders[1].val
            
            # Final volume is Master multiplied by Music 
            # (e.g., 50% Master * 50% Music = 25% actual output)
            final_music_volume = master_vol * music_vol
            
            # Send the new volume directly to Pygame's global DJ!
            pygame.mixer.music.set_volume(final_music_volume)
           
            
            self.draw()
            pygame.display.flip()


# ENTRY POINT

def run(screen, bg_image, title_font, button_font): 
    settings_menu = SettingsScreen(screen, bg_image, title_font, button_font)
    settings_menu.start()