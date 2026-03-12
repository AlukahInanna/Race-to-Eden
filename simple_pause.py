import os
import sys
import pygame


SCRIPT_DIR = os.path.dirname(__file__)
FONT_PATH = os.path.join(SCRIPT_DIR, "fonts", "letters.ttf")
BACKGROUND_PATH = os.path.join(SCRIPT_DIR, "images", "background.png")
# so the path also works windows and unix based systems

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.center_x = screen.get_width() // 2
        self.center_y = screen.get_height() // 2

        self.font = pygame.font.Font(FONT_PATH, 50)
        self.title_font = pygame.font.Font(FONT_PATH, 85)

        self.menu_rect = pygame.Rect(0, 0, 720, 380)
        self.menu_rect.center = (self.center_x, self.center_y)

        try:
            background = pygame.image.load(BACKGROUND_PATH).convert()
            self.background_image = pygame.transform.scale(background, screen.get_size())
        except pygame.error:
            self.background_image = pygame.Surface(screen.get_size())
            self.background_image.fill((20, 30, 40))

        self.overlay = pygame.Surface(screen.get_size())
        self.overlay.set_alpha(120)
        self.overlay.fill((0, 0, 0))

    def draw_button(self, text, y_pos, mouse_pos):
        text_surf = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(self.center_x, y_pos))
        button_rect = text_rect.inflate(100, 30)

        if button_rect.collidepoint(mouse_pos):
            box_color = (255, 215, 0)
        else:
            box_color = (70, 70, 70)

        pygame.draw.rect(self.screen, box_color, button_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 2, border_radius=10)
        self.screen.blit(text_surf, text_rect)

        return button_rect

    def display(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.overlay, (0, 0))

            pygame.draw.rect(self.screen, (25, 25, 25), self.menu_rect, border_radius=18)
            pygame.draw.rect(self.screen, (255, 215, 0), self.menu_rect, 3, border_radius=18)

            title_surf = self.title_font.render("PAUSED", True, (255, 215, 0))
            title_rect = title_surf.get_rect(center=(self.center_x, self.center_y - 110))
            self.screen.blit(title_surf, title_rect)

            mouse_pos = pygame.mouse.get_pos()
            resume_btn = self.draw_button("Resume", self.center_y + 10, mouse_pos)
            quit_btn = self.draw_button("Quit to Menu", self.center_y + 120, mouse_pos)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "resume"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if resume_btn.collidepoint(event.pos):
                        return "resume"
                    if quit_btn.collidepoint(event.pos):
                        return "menu"

