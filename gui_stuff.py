from typing import Tuple

import pygame


class GuiInfo:
    def __init__(self):
        # Full-screen display mode
        self.infoObject = pygame.display.Info()
        self.screen = pygame.display.set_mode((self.infoObject.current_w, self.infoObject.current_h), pygame.FULLSCREEN)

        self.fading = False
        self.fade_alpha = 0
        self.new_image = None

        self.running = True
        self.visible = True

    def load_image(self, path: str, size: Tuple[int, int]) -> pygame.Surface:
        return pygame.transform.scale(pygame.image.load(path), size)

    # Show new image with fade effect
    def show_new_image(self, new_image_path: str) -> None:
        new_image = self.load_image(new_image_path, (self.infoObject.current_w, self.infoObject.current_h))
        for alpha in range(0, 255, 2):
            new_image.set_alpha(alpha)
            self.screen.blit(new_image, (0, 0))
            pygame.display.flip()
            pygame.time.delay(10)  # Adjust delay for smoother fade effect

    # Function to initiate fade effect
    def initiate_fade(self, new_image_path: str) -> None:
        self.fade_alpha = 0  # Reset alpha to 0
        self.fading = True  # Start fading
        self.new_image = self.load_image(new_image_path, (self.infoObject.current_w, self.infoObject.current_h))

    def display_recording_text(self) -> None:
        font_size = 40
        text = "RECORDING AUDIO"
        position = (75, 45)
        if pygame.time.get_ticks() % 1500 > 500:
            font = pygame.font.Font(None, font_size)
            text_surf = font.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(topleft=position)
            pygame.draw.circle(self.screen, (255, 0, 0), (text_rect.left - 25, text_rect.centery), 15)
            self.screen.blit(text_surf, text_rect)

    # For transcription subtitles
    def display_text_with_background(self, text: str, position: Tuple[int, int], font_size: int = 30,
                                     bg_color: Tuple[int, int, int] = (192, 192, 192), bg_alpha: int = 128) -> None:
        font = pygame.font.Font(None, font_size)
        text_surf = font.render(text, True, (0, 0, 0))  # Black text
        text_rect = text_surf.get_rect(center=(position[0], position[1]))

        # Create a translucent background surface
        bg_surf = pygame.Surface((text_rect.width + 20, text_rect.height + 10))  # Padding around text
        bg_surf.set_alpha(bg_alpha)  # Set transparency
        bg_surf.fill(bg_color)  # Fill with grey color
        self.screen.blit(bg_surf, (text_rect.left - 10, text_rect.top - 5))  # Positioning background with padding
        self.screen.blit(text_surf, text_rect)  # Draw the text on top of the background

    def display_text(self, text: str, position: Tuple[int, int], font_size: int = 30, visible: bool = True) -> None:
        font = pygame.font.Font(None, font_size)
        text_surf = font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surf, position)
