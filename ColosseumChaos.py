import pygame
import random
import time

# Initialize pygame
pygame.init()

# Set up game window
WIDTH, HEIGHT = 1792, 1024
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Colosseum Chaos')

# Colors
WHITE = (255, 255, 255)
PURPLE = (77, 25, 77)
BLACK = (0, 0, 0)

# Load assets
background = pygame.image.load('images/background.jpg')  # Background image
enemy_img = pygame.image.load('images/Enemy1.png')  # Enemy image
scaled_enemy_img = pygame.transform.scale(enemy_img, (200, 200))  # Scale the enemy image
innocent_img = pygame.image.load('images/Innocent1.png')  # Innocent image
scaled_innocent_img = pygame.transform.scale(innocent_img, (200, 200))  # Scale the innocent image
success_sound = pygame.mixer.Sound('sounds/Cheer.mp3')  # Success sound
penalty_sound = pygame.mixer.Sound('sounds/Boo.mp3')  # Penalty sound

# Font setup
font = pygame.font.Font('fonts/BLKCHCRY.ttf', 32)

# Create a clock object to control frame rate
clock = pygame.time.Clock()

# Game state variables
score = 0
timer = 30  # Seconds to play
current_image = None
current_position = (0, 0)
image_display_time = 0  # Time when the image was displayed
clickable_area_size = 150  # Size of the clickable area around the image (larger than the image)


# Function to draw buttons
def draw_button(text, x, y, width, height, color, text_color=WHITE):
    pygame.draw.rect(screen, color, (x, y, width, height))
    label = font.render(text, True, text_color)
    screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))


# Function to check if mouse is over the button
def is_mouse_over_button(x, y, width, height):
    mouse_pos = pygame.mouse.get_pos()
    return x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height

# Main menu screen
def main_menu():
    running = True
    while running:
        screen.fill(BLACK)


        pygame.draw.rect(screen, PURPLE, (0, 0, WIDTH, 50))

        # Draw instructions
        instruction_text1 = font.render("Click on the enemies to score points!", True, WHITE)
        instruction_text2 = font.render("Avoid clicking the innocents!", True, WHITE)
        screen.blit(instruction_text1, (WIDTH // 2 - instruction_text1.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(instruction_text2, (WIDTH // 2 - instruction_text2.get_width() // 2, HEIGHT // 2 - 50))

        # New sizes for the images
        NEW_WIDTH, NEW_HEIGHT = 200, 200

        # Rescale the images
        resized_enemy_img = pygame.transform.scale(enemy_img, (NEW_WIDTH, NEW_HEIGHT))
        resized_innocent_img = pygame.transform.scale(innocent_img, (NEW_WIDTH, NEW_HEIGHT))

        # Display the resized images on the screen
        screen.blit(resized_enemy_img, (WIDTH // 4 - NEW_WIDTH // 2, HEIGHT // 2 - NEW_HEIGHT // 2))
        screen.blit(resized_innocent_img, (3 * WIDTH // 4 - NEW_WIDTH // 2, HEIGHT // 2 - NEW_HEIGHT // 2))

        enemy_label = font.render("Enemy", True, WHITE)
        innocent_label = font.render("Innocent", True, WHITE)
        screen.blit(enemy_label, (WIDTH // 4 - enemy_label.get_width() // 2, HEIGHT // 2 + 110))
        screen.blit(innocent_label, (3 * WIDTH // 4 - innocent_label.get_width() // 2, HEIGHT // 2 + 110))

        #Play Game button
        button_width = 200
        button_height = 50
        draw_button("Play Game", WIDTH // 2 - button_width // 2, HEIGHT // 2 + 100, button_width, button_height, PURPLE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if is_mouse_over_button(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 100, button_width, button_height):
                    running = False
                    main_game_loop()  # Start the game loop when button is clicked

        pygame.display.update()

# Initialize a variable to store the last time the timer was updated
last_timer_update = pygame.time.get_ticks()

def countdown_timer():
    global timer, last_timer_update
    current_time = pygame.time.get_ticks()
    # Check if 1 second (1000 milliseconds) has passed
    if current_time - last_timer_update >= 1000:
        timer -= 1
        last_timer_update = current_time

def display_countdown():
    # Create a larger font for the countdown
    large_font = pygame.font.Font('fonts/BLKCHCRY.ttf', 64)  # Double the original size (32 → 64)

    for i in range(5, 0, -1):
        screen.fill((0, 0, 0))
        countdown_text = large_font.render(str(i), True, WHITE)
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(1000)  # Wait 1 second

    # Show "GO!" after the countdown
    screen.fill((0, 0, 0))
    go_text = large_font.render("GO!", True, WHITE)
    screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    pygame.time.delay(1000)  # Wait 1 second


def display_score_and_timer():
    score_text = font.render(f"Score: {score}", True, WHITE)
    timer_text = font.render(f"Time: {timer}s", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(timer_text, (WIDTH - timer_text.get_width() - 10, 10))


# Display "Game Over"
def display_game_over():
    game_over_text = font.render(f"Game Over! Final Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))

    # Draw Play Again and Close Game buttons
    button_width = 200
    button_height = 50
    draw_button("Play Again", WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height, PURPLE)
    draw_button("Close Game", WIDTH // 2 - button_width // 2, HEIGHT // 2 + 60, button_width, button_height, BLACK)


# Randomly choose image
def choose_image():
    global current_image, current_position, image_display_time
    choice = random.choice([1, 2])  # 1 for enemy, 2 for innocent
    if choice == 1:
        current_image = scaled_enemy_img
    else:
        current_image = scaled_innocent_img
    current_position = (random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100))
    image_display_time = time.time()  # Record the time the image was shown


# Check for mouse click on image
def check_click(mouse_pos):
    global score
    if current_image:
        image_rect = current_image.get_rect(topleft=current_position)

        # Create a larger clickable area around the image
        clickable_area_rect = pygame.Rect(current_position[0] - (clickable_area_size - 200) // 2,
                                          current_position[1] - (clickable_area_size - 200) // 2,
                                          clickable_area_size, clickable_area_size)

        if clickable_area_rect.collidepoint(mouse_pos):  # Check if the click is within the clickable area
            if current_image == scaled_enemy_img:  # If it's an enemy
                score += 10
                success_sound.play()
            else:  # If it's an innocent
                score -= 5
                penalty_sound.play()
            choose_image()  # Load next image
        return Trueg
    return False


# Main game loop
def main_game_loop():
    global score, timer
    running = True
    display_countdown()
    choose_image()  # Choose the first image to display
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                check_click(mouse_pos)  # Check if the mouse clicked on the current image

        # Update timer
        if timer > 0:
            countdown_timer()

        # Draw everything
        screen.fill(PURPLE)


        pygame.draw.rect(screen, PURPLE, (0, 0, WIDTH, 50))  # Bar height of 50 pixels

        screen.blit(background, (0, 50))  # Draw the background starting below the bar
        display_score_and_timer()

        # Check if 2 seconds have passed since the image was last updated
        if current_image and time.time() - image_display_time >= 2:
            choose_image()  # Choose a new image after 2 seconds

        if current_image:
            screen.blit(current_image, current_position)  # Draw the current image (enemy or innocent)

        # Check if the game is over
        if timer <= 0:
            display_game_over()
            pygame.display.update()
            pygame.time.delay(2000)  # Wait 2 seconds before displaying the game over screen
            break  # Exit the game loop after game over

        pygame.display.update()

        # Control the frame rate
        clock.tick(60)  # 60 FPS


# Main loop for game over screen
def game_over_screen():
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check if Play Again button was clicked
                if is_mouse_over_button(WIDTH // 2 - 100, HEIGHT // 2, 200, 50):
                    global score, timer
                    score = 0
                    timer = 30  # Reset timer for new game
                    main_game_loop()  # Restart game loop
                    return
                # Check if Close Game button was clicked
                elif is_mouse_over_button(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50):
                    running = False

        pygame.display.update()


# Start the game
main_menu()  # Start the main game loop
game_over_screen()  # Show the game over screen when the game ends

# Quit the game
pygame.quit()
