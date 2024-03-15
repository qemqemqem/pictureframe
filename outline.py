import pygame

# Initialize Pygame
pygame.init()


# Main function to run the game loop
def main():
    init_gui()

    while running:
        update_gui()  # Needs to update every frame

        # I need help multi-threading these
        if need_network_update():
            update_over_network()  # This takes a while, it needs to wait for network calls and also do expensive computation

        if need_record_audio():
            record()  # This needs to be run every 5s. It's a network call, so it also takes a while

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
