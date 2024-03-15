import pygame

from gui_stuff import GuiInfo

# Initialize Pygame
pygame.init()


# Main function to run the game loop
def main():
    gui_info = GuiInfo()

    background_image_path = 'images/example_image.jpg'
    background_image = gui_info.load_image(background_image_path,
                                           (gui_info.infoObject.current_w, gui_info.infoObject.current_h))
    gui_info.screen.blit(background_image, (0, 0))

    # blink_event = pygame.USEREVENT + 1
    # pygame.time.set_timer(blink_event, 1000)  # ms

    i = 1
    while gui_info.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gui_info.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gui_info.running = False
                elif event.key == pygame.K_SPACE:
                    gui_info.initiate_fade(f'images/example_{i}.png')
                    i += 1
            # elif event.type == blink_event:
            #     visible = not visible

        # Fade effect logic
        if gui_info.fading:
            if gui_info.fade_alpha < 255:
                gui_info.fade_alpha += 5  # Increment alpha
                if gui_info.new_image is not None:
                    gui_info.new_image.set_alpha(gui_info.fade_alpha)
                    gui_info.screen.blit(background_image, (0, 0))  # Draw the old image
                    gui_info.screen.blit(gui_info.new_image, (0, 0))  # Draw the new image on top with increasing alpha
                    gui_info.display_recording_text()
                # pygame.display.flip()
            else:
                gui_info.fading = False  # Stop fading
                background_image = gui_info.new_image  # Set new image as the background

        if not gui_info.fading:
            gui_info.screen.blit(background_image, (0, 0))
            gui_info.display_recording_text()

        # Display text
        gui_info.display_text_with_background("This is a story all about how, my world got flip turned upside down",
                                              (gui_info.infoObject.current_w // 2, gui_info.infoObject.current_h - 50),
                                              font_size=50)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
