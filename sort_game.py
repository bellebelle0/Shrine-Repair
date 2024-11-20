import random

# Questions and Answers Database
qa_data = [
    {"question": "Is the main deity of Japanese shrines referred to as 'Kami'?", "answer": True},
    {"question": "Are Komainu in shrines regarded as decorations rather than guardians?", "answer": False},
    {"question": "Is the traditional Japanese festival 'Hatsuha' held on New Year's Day, January 1st?", "answer": True},
    {"question": "Does the 'Torii' in a shrine symbolize the connection between humans and gods?", "answer": True},
    {"question": "Are harvest festivals and Shichi-Go-San unrelated to Japanese shrines?", "answer": False},
    {"question": "Are common offerings in shrines limited to money and flowers?", "answer": False},
]

# Display function for QA game
def display_qa_game(score, question_data):
    # Draw background and score
    display.blit(sorting_scene.background, (0, 0))
    score_text = f"Score: {score}"
    score_display = font.render(score_text, True, RED)
    display.blit(score_display, (24, 24))

    # Display question
    question_display = font.render(question_data["question"], True, WHITE)
    display.blit(question_display, (50, 50))

    pygame.display.update()
    fps_clock.tick(fps)

# QA game logic
def qa_game():
    score = 0
    asked_questions = set()

    while score < 10 and len(asked_questions) < len(qa_data):
        # Randomly select a question that hasn't been asked
        question_index = random.choice([i for i in range(len(qa_data)) if i not in asked_questions])
        current_question = qa_data[question_index]
        asked_questions.add(question_index)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                # Handle user input for True/False
                if event.type == KEYDOWN:
                    if event.key == K_t:  # 'T' for True
                        user_answer = True
                    elif event.key == K_f:  # 'F' for False
                        user_answer = False
                    else:
                        continue  # Skip if other keys are pressed

                    # Check answer
                    if user_answer == current_question["answer"]:
                        print("Correct!")
                        score += 1
                    else:
                        print(f"Incorrect! The correct answer was {current_question['answer']}.")

                    # Move to the next question
                    break

            # Display question
            display_qa_game(score, current_question)

    # Game completion logic
    if score >= 6:
        print("Congratulations! You've completed the game.")
    else:
        print("Game over! Better luck next time.")

# Add to main game loop
if current_mode == "qa game":
    qa_game()
    current_mode = "home"


# 题目随机化： 每次随机抽题，确保同一局游戏不会重复出题。
# 玩家交互：
# 使用键盘按键 T 和 F 分别表示 True 和 False。
# 根据输入立即反馈答案，并展示正确与否。
# 分数机制：
# 玩家答对一题加一分。
# 达到6分或完成所有题目后游戏结束。
