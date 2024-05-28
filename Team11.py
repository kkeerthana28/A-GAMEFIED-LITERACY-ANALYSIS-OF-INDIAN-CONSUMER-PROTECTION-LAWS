import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Consumer Rights Puzzle Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# Fonts
font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 30)

# Load heart image for lives display
heart_img = pygame.image.load('/Users/anushbharathwaj/Downloads/pngegg (2).png')  # Make sure you have a 'heart.png' file in your project directory
heart_img = pygame.transform.scale(heart_img, (30, 30))  # Scale the heart image

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    click = False
    while True:
        screen.fill(BLACK)
        draw_text('Main Menu', font, WHITE, screen, (screen_width - font.size('Main Menu')[0]) // 2, 50)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect((screen_width - 200) // 2, 200, 200, 50)
        button_2 = pygame.Rect((screen_width - 200) // 2, 300, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                num_players = ask_for_players()
                return num_players
        if button_2.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        pygame.draw.rect(screen, RED, button_1)
        draw_text('Start', small_font, WHITE, screen, (screen_width - small_font.size('Start')[0]) // 2, 210)
        pygame.draw.rect(screen, RED, button_2)
        draw_text('Quit', small_font, WHITE, screen, (screen_width - small_font.size('Quit')[0]) // 2, 310)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Ensure this is the left mouse button
                    click = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Ensure this is the left mouse button
                    click = False

        pygame.display.update()


def ask_for_players():
    running = True
    number = ''
    while running:
        screen.fill(BLACK)
        draw_text('Enter number of players:', font, WHITE, screen, (screen_width - font.size('Enter number of players:')[0]) // 2, 20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if number.isdigit():
                        return int(number)
                elif event.key == pygame.K_BACKSPACE:
                    number = number[:-1]
                else:
                    number += event.unicode

        draw_text(number, font, WHITE, screen, (screen_width - font.size(number)[0]) // 2, 100)
        pygame.display.update()

def get_player_names(num_players):
    player_names = []
    for i in range(num_players):
        running = True
        name = ''
        while running:
            screen.fill(BLACK)
            prompt = f'Enter name for Player {i+1}:'
            draw_text(prompt, font, WHITE, screen, (screen_width - font.size(prompt)[0]) // 2, 20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if name:
                            player_names.append(name)
                            running = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode

            draw_text(name, font, WHITE, screen, (screen_width - font.size(name)[0]) // 2, 100)
            pygame.display.update()
    return player_names

# Start the game
num_players = main_menu()
player_names = get_player_names(num_players)

# Initialize players
players = [{'name': name, 'score': 0, 'level': 1, 'lives': 3} for name in player_names]
current_player_index = 0

# Your game code continues from here...

# Your game code continues from here...

# Player
player_speed = 10
player_image = pygame.Surface((50, 50))
player_image.fill(WHITE)
player_rect = player_image.get_rect(center=(screen_width // 2, screen_height // 2))

# Obstacles
obstacles = []
obstacle_size = 50

def add_obstacles(level):
    global obstacles
    obstacles.clear()  # Clear existing obstacles for a new level
    grid_width = screen_width // obstacle_size
    grid_height = (screen_height // obstacle_size) - 1
    grid = set()

    while len(obstacles) < level:
        # Pick a random grid cell that is not already occupied
        x = random.randint(0, grid_width - 1) * obstacle_size
        y = random.randint(1, grid_height) * obstacle_size  # Start y at 1 to avoid placing at the top edge

        if (x, y) not in grid:
            grid.add((x, y))
            obstacles.append(pygame.Rect(x, y - screen_height, obstacle_size, obstacle_size))  # Place off-screen

# Dashboard variables
timing = 0
score = 0
level = 1

# Sample quiz questions
consumer_law_data = {
  "question": [
    "Which law provides consumers with the right to dispute billing errors on their credit card statements?",
    "What federal agency is responsible for enforcing laws related to consumer credit?",
    "Which law requires lenders to provide borrowers with clear and accurate information about loan terms and costs?",
    "Which act in India aims to prevent consumers from exploitation by traders and manufacturers?", 
    "What is the legal remedy available to consumers in India for resolving disputes under consumer protection laws? ",
    "What is the maximum penalty for a first-time offense of selling adulterated food under the Food Safety and Standards Act, 2006?", 
    "Under the Consumer Protection Act, 2019, what is the maximum amount of compensation that can be awarded by a District Commission?",
    "In India, what is the statutory cooling-off period for cancelling a contract made during door-to-door sales?", 
    "As per the Legal Metrology Act, 2009, what is the maximum punishment for selling goods using incorrect weights or measures?", 
    "What is the period within which a consumer complaint should be filed from the date of the cause of action under the Consumer Protection Act, 2019? ",
    "Which court handles appeals against the orders of the National Consumer Disputes Redressal Commission (NCDRC)? ",
    "Under the Real Estate (Regulation and Development) Act, 2016, what percentage of the amount received from the buyer must be deposited in a separate bank account for the construction of the project? "
  ],
  "answer": [
    "Fair Credit Billing Act",
    "Consumer Financial Protection Bureau",
    "Truth in Lending Act",
    "Consumer Protection Act, 2019",
    "Filing a complaint in the appropriate consumer forum", 
    "Imprisonment for up to 6 months and a fine of up to Rs. 1 lakh",
    "Rs. 1 crore", 
    "7 days",
    "Imprisonment for up to 1 year and a fine of up to Rs. 1 lakh",
    "Within 1 year",
    "Supreme Court of India",
    "70% to 100%"
  ],
  "options": [
    ["Fair Credit Reporting Act", "Truth in Lending Act", "Fair Credit Billing Act"],
    ["Federal Trade Commission", "Consumer Financial Protection Bureau", "Securities and Exchange Commission"],
    ["Truth in Lending Act", "Fair Debt Collection Practices Act", "Fair Credit Reporting Act"],
    ["Consumer Protection Act, 2019", "Sale of Goods Act, 1930", "Indian Contract Act, 1872"],
    ["Filing a complaint in the appropriate consumer forum", "Filing a police complaint", "Seeking arbitration"],
    ["Imprisonment for up to 6 months and a fine of up to Rs. 1 lakh", "Imprisonment for up to 1 year and a fine of up to Rs. 5 lakhs", "Revocation of business license"],
    ["Rs. 1 lakh", "Rs. 10 lakhs", "Rs. 1 crore"],
    ["3 days", "7 days", "14 days"],
    ["Imprisonment for up to 1 year and a fine of up to Rs. 1 lakh", "Imprisonment for up to 3 years and a fine of up to Rs. 5 lakhs", "Revocation of business license"],
    ["Within 90 days", "Within 180 days", "Within 1 year"],
    ["Supreme Court of India", "High Court", "District Court"],
    ["50%", "70%", "70% to 100%"]
  ]
}

# Convert consumer_law_data into scenarios
scenarios = []
for question, answer, options in zip(consumer_law_data["question"], consumer_law_data["answer"], consumer_law_data["options"]):
    scenarios.append({"question": question, "correct_answer": answer, "options": options})

current_question = None
previous_questions = []  # To keep track of the previous two questions
answer_selected = -1
game_state = "running"

# Function Definitions
def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    while words:
        line = ''
        while words and font.size(line + words[0])[0] <= max_width:
            line += (words.pop(0) + ' ')
        lines.append(line)
    return lines

def display_quiz(quiz, selected_index=-1, correct_index=-1, answer_feedback=""):
    screen.fill(BLACK)
    max_width = screen_width - 100

    question_lines = wrap_text(quiz["question"], font, max_width)
    y_offset = 100
    for line in question_lines:
        question_text = font.render(line, True, WHITE)
        screen.blit(question_text, (50, y_offset))
        y_offset += font.get_height() + 10

    y_offset += 20

    for i, option in enumerate(quiz["options"]):
        option_lines = wrap_text(option, font, max_width)
        option_y_offset = y_offset
        for line in option_lines:
            option_color = WHITE
            if i == selected_index:
                option_color = YELLOW  # Set the selected option to YELLOW
            elif i == correct_index:
                option_color = GREEN  # Set the correct option to GREEN
            elif i == selected_index and quiz["options"][i] != quiz["correct_answer"]:
                option_color = RED
            option_text = font.render(line, True, option_color)
            screen.blit(option_text, (50, option_y_offset))
            option_y_offset += font.get_height() + 5
            y_offset += font.get_height() + 10  

    feedback_text = font.render(answer_feedback, True, WHITE)
    screen.blit(feedback_text, (50, y_offset + 20))

def check_answer(quiz, option_index):
    global score, game_state, level, current_question, previous_questions
    Naive_Bayes = quiz["options"] == quiz["correct_answer"]
    correct = quiz["options"][option_index] == quiz["correct_answer"]
    if correct:
        feedback = "Correct!"
        score += 1
        level += 1
        players[current_player_index]['score'] += 1
        add_obstacles(level)
        # Remove the current question from the list of scenarios
        scenarios.remove(current_question)
    else:
        feedback = "Wrong answer!"
        players[current_player_index]['lives'] -= 1  # Reduce lives for the current player
        score -= 1
        if level > 1:  # Ensure level doesn't go below 1
            level -= 1
        add_obstacles(level)  # Add obstacles for the previous level or existing level

    display_quiz(quiz, option_index, quiz["options"].index(quiz["correct_answer"]), feedback)
    pygame.display.flip()
    pygame.time.delay(2000)  # Show the feedback for 2 seconds
    game_state = "running"

def get_new_question():
    global current_question, previous_questions, scenarios
    while True:
        new_question = random.choice(scenarios)
        if new_question not in previous_questions and new_question != current_question:  
            # Ensure it's not the same as the previous two questions and not the current question
            current_question = new_question
            previous_questions.append(new_question)
            if len(previous_questions) > 2:
                previous_questions.pop(0)  # Keep only the latest two questions in the list
            break

# Main loop setup
clock = pygame.time.Clock()
add_obstacles(level)  # Initialize first level obstacle
get_new_question()  # Get the first question
current_player_index = 0
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and game_state == "running":
            if event.key == pygame.K_LEFT:
                player_rect.x -= player_speed
            elif event.key == pygame.K_RIGHT:
                player_rect.x += player_speed
            elif event.key == pygame.K_UP:
                player_rect.y -= player_speed
            elif event.key == pygame.K_DOWN:
                player_rect.y += player_speed
        elif event.type == pygame.KEYDOWN and game_state == "quiz":
            if event.key == pygame.K_UP:
                answer_selected -= 1
                if answer_selected < 0:
                    answer_selected = len(current_question["options"]) - 1
            elif event.key == pygame.K_DOWN:
                answer_selected += 1
                if answer_selected >= len(current_question["options"]):
                    answer_selected = 0
            elif event.key == pygame.K_RETURN:
                check_answer(current_question, answer_selected)
                get_new_question()  # Get a new question after answering the current one
                if players[current_player_index]['lives'] == 0:
                    current_player_index = (current_player_index + 1) % num_players  # Move to the next player
                    if all(player['lives'] == 0 for player in players):
                        # If all players have lost all their lives, end the game
                        running = False

    screen.fill(BLACK)

    if game_state == "running":
        for obstacle in obstacles:
            pygame.draw.rect(screen, RED, obstacle)
            obstacle.y += 2
            if obstacle.y > screen_height:
                obstacle.y = -50
                obstacle.x = random.randint(50, screen_width - 50)
            if player_rect.colliderect(obstacle):
                game_state = "quiz"

        screen.blit(player_image, player_rect)

    elif game_state == "quiz" and current_question:
        display_quiz(current_question, answer_selected)

    # Dashboard updates
    timing += clock.tick(60) / 1000
    
    screen.blit(font.render(f"Time: {timing:.2f} sec", True, WHITE), (20, 20))
    screen.blit(font.render(f"Score: {score}", True, WHITE), (20, 40))
    screen.blit(font.render(f"Level: {level}", True, WHITE), (20, 60))

    # Display current player's name and remaining lives in the top left corner
    current_player = players[current_player_index]
    draw_text(current_player['name'], font, WHITE, screen, (screen_width - font.size(current_player['name'])[0]) // 2, 10)
    for i in range(current_player['lives']):
        screen.blit(heart_img, (screen_width - (i+1) * 40, 10))

    pygame.display.flip()

# Display final dashboard for all players
# Display final dashboard for all players
# Load trophy image
trophy_img = pygame.image.load('/Users/anushbharathwaj/Downloads/l22as1uemua37h5ktkt1iclo55.png')  # Replace 'trophy_image.png' with the path to your trophy image
trophy_img = pygame.transform.scale(trophy_img, (30, 30))  # Scale the trophy image

# Display final dashboard for all players
screen.fill(BLACK)
y_offset = 100
winner_score = max(player['score'] for player in players)
for player in players:
    final_text = f"{player['name']}: Score = {player['score']}, Level = {player['level']}, Time = {timing:.2f} sec"
    if player['score'] == winner_score:
        screen.blit(trophy_img, (20, y_offset))  # Blit trophy image
        final_text += " Winner!"
    draw_text(final_text, font, GREEN if player['score'] == winner_score else WHITE, screen, 60, y_offset)
    y_offset += 50
pygame.display.flip()



# Wait for a few seconds before quitting
pygame.time.delay(5000)

# Quit Pygame
pygame.quit()
