import pygame
import sys
import random
import time

# Pygame 초기화
pygame.init()

# 한글 폰트 설정
pygame.font.init()
font_path = "source\Font.ttf"  # 'Arial' 폰트 대신 사용할 한글 폰트 경로를 지정해주세요.
font = pygame.font.Font(font_path, 36)
input_font = pygame.font.Font(font_path, 48)
time_font = pygame.font.Font(font_path, 24)

# 게임 창 설정
WIDTH, HEIGHT = 800, 600
WINDOW_SIZE = (WIDTH, HEIGHT)
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Quiz Game")
clock = pygame.time.Clock()

# 버튼 클래스 정의
class Button:
    def __init__(self, text, position, size, color, hover_color, action):
        self.text = text
        self.position = position
        self.size = size
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if self.position[0] < mouse_x < self.position[0] + self.size[0] and \
           self.position[1] < mouse_y < self.position[1] + self.size[1]:
            pygame.draw.rect(screen, self.hover_color, (self.position[0], self.position[1], self.size[0], self.size[1]))
            if pygame.mouse.get_pressed()[0] == 1:
                self.action()
        else:
            pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], self.size[0], self.size[1]))

        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=(self.position[0] + self.size[0] // 2, self.position[1] + self.size[1] // 2))
        screen.blit(text_surface, text_rect)

# 게임 변수 초기화
score = 0
combo = 0
max_combo = 0
questions = questions = [
        {"question": "아파트 가격은 금리와 비례한다.\n(o/x)", "answer": "x"},
        {"question": "아파트 분양을 받기 위해서는\n 청약점수가 필요하다.\n(o/x)", "answer": "o"},
        {"question": "아파트 평을 제곱미터로 환산하면 \n 3.6mx3.6m이다.\n(o/x)", "answer": "x"},
        {"question": "월세'는 매월 지불하는 임대료이고, \n '전세'는 전체 보증금을 지불하고  \n 일정 기간 동안 주거하는 형태이다.\n(o/x)", "answer": "o"},
        {"question": "건물의 유지보수, 공동 시설 사용, 경비원\n 비용 등  아파트에서 공동으로 \n 부담하는 비용을 \n '관리비'라 부른다.\n(o/x)", "answer": "o"},
        {"question": "아파트를 구입할 때는 부동산 시장의 \n향후 전망, 인프라 개발 계획, \n인근 지역의 경제적 발전 가능성 \n 등을 고려해야 합니다.\n(o/x)", "answer": "o"},
    ]

question_time_limit = 10  # 문제당 제한 시간 (초)
def render_multiline_text(surface, text, font, color, position):
    lines = text.split('\n')  # 개행 문자를 기준으로 문자열을 나눕니다.

    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (position[0], position[1] + i * text_rect.height)
        surface.blit(text_surface, text_rect)

# 기타 설정
input_text = ""
start_time = None
game_duration = 180  # 3 minutes

# 게임 상태 정의
class GameState:
    START_MENU = 0
    GAME_IN_PROGRESS = 1
    GAME_OVER = 2

game_state = GameState.START_MENU

# 현재 문제에 대한 초기 설정
def initialize_question():
    return {
        "question": "",
        "answer": "",
        "time_limit": question_time_limit,
        "start_time": None
    }

current_question = initialize_question()
current_question["start_time"] = time.time()  # Initialize start_time for the first question
# 버튼 초기화
def restart_game():
    global questions, question_time_limit, score, combo, max_combo
    questions = [
        {"question": "아파트 가격은 금리와 비례한다.\n(o/x)", "answer": "x"},
        {"question": "아파트 분양을 받기 위해서는\n 청약점수가 필요하다.\n(o/x)", "answer": "o"},
        {"question": "아파트 평을 제곱미터로 환산하면 \n 3.6mx3.6m이다.\n(o/x)", "answer": "x"},
        {"question": "월세'는 매월 지불하는 임대료이고, \n '전세'는 전체 보증금을 지불하고  \n 일정 기간 동안 주거하는 형태이다.\n(o/x)", "answer": "o"},
        {"question": "건물의 유지보수, 공동 시설 사용, 경비원\n 비용 등  아파트에서 공동으로 \n 부담하는 비용을 \n '관리비'라 부른다.\n(o/x)", "answer": "o"},
        {"question": "아파트를 구입할 때는 부동산 시장의 \n향후 전망, 인프라 개발 계획, \n인근 지역의 경제적 발전 가능성 \n 등을 고려해야 합니다.\n(o/x)", "answer": "o"},
    ]
    question_time_limit = 10  # 문제당 제한 시간 (초)
    score = 0
    combo = 0
    max_combo = 0
    game_state = GameState.GAME_IN_PROGRESS

def return_to_menu():
    restart_game()
    global game_state
    game_state = GameState.START_MENU

restart_button = Button("다시하기", (WIDTH // 2 - 100, HEIGHT // 2 + 50), (200, 50), WHITE, (200, 200, 200), return_to_menu)
# 음악 파일 로드 및 재생
pygame.mixer.music.load("source\happy_jazz.mp3")
pygame.mixer.music.play(-1)  # -1은 반복 재생을 의미

# 효과음 로드
success_sound = pygame.mixer.Sound("source/성공.mp3")
fail_sound = pygame.mixer.Sound("source/실패.mp3")


# 게임 루프
running = True
while running:
    screen.fill("#ece6cc")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == GameState.START_MENU:
                if event.key == pygame.K_RETURN:
                    # 제한 시간 초기화
                    current_question["start_time"] = time.time()
                    game_state = GameState.GAME_IN_PROGRESS
                    start_time = time.time()
            elif game_state == GameState.GAME_IN_PROGRESS:
                if event.key == pygame.K_RETURN:
                    # 답 체크
                    answer = input_text.strip()
                    if answer.lower() == questions[0]["answer"].lower():
                        score += 10
                        combo += 1
                        if combo > max_combo:
                            max_combo = combo
                            if(max_combo>1):
                                score +=5
                         # 성공 효과음 재생
                        success_sound.play()
                    else:
                        
                        combo = 0
                        # 실패 효과음 재생
                        fail_sound.play()
                    input_text = ""  # 답을 처리하고 입력 초기화

                    # 다음 문제
                    questions.pop(0)
                    if questions:
                        current_question = initialize_question()
                        current_question["start_time"] = time.time()  # Update start_time for the new question
                    else:
                        # 모든 문제 풀이 완료
                        game_state = GameState.GAME_OVER

                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    # 게임 상태에 따른 처리
    if game_state == GameState.START_MENU:
        text = font.render("토아 아파트 퀴즈 게임",True,BLACK)
        text2 = font.render("Press Enter to Start", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 -100))
        screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 - text2.get_height() // 2))
    elif game_state == GameState.GAME_IN_PROGRESS:
        if questions:
            # 문제 표시
            question_number = len(questions) - len(questions) + 1  # Calculate question number
            multiline_text = f"[문제{question_number}] {questions[0]['question']}"
            render_multiline_text(screen, multiline_text, font, BLACK, (10, 200))

            # 입력창 표시
            pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 100, HEIGHT - 100, 200, 50))
            input_surface = input_font.render(input_text, True, BLACK)
            screen.blit(input_surface, (WIDTH // 2 - input_surface.get_width() // 2, HEIGHT - 100))

            # 점수 표시
            score_text = font.render(f"점수 {score}", True, BLACK)
            screen.blit(score_text,(WIDTH//2 -score_text.get_width(),10))

            # 시간 표시
            elapsed_time = int(time.time() - current_question["start_time"])
            time_text = time_font.render(f"시간: {elapsed_time}/{current_question['time_limit']} 초", True, BLACK)
            screen.blit(time_text, (WIDTH - time_text.get_width() - 10, 10))

            # 콤보 표시
            combo_text = font.render(f"콤보 {combo}", True, BLACK)
            screen.blit(combo_text, (10, 10))

            # 제한 시간 초과 처리
            if elapsed_time > current_question["time_limit"]:
                # 시간 초과로 인한 오답 처리
                combo = 0
                fail_sound.play()
                input_text = ""  # 입력 초기화

                # 다음 문제
                questions.pop(0)
                if questions:
                    current_question = initialize_question()
                    current_question["start_time"] = time.time()  # Update start_time for the new question
                else:
                    # 모든 문제 풀이 완료
                    game_state = GameState.GAME_OVER
        else:
            # 모든 문제 풀이 완료
            game_state = GameState.GAME_OVER

    elif game_state == GameState.GAME_OVER:
        elapsed_time = int(time.time() - start_time)
        text = font.render(f"최종점수: {score} 최대콤보: {max_combo}",True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        # 다시하기 버튼 그리기
        restart_button.draw()
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = GameState.START_MENU

    pygame.display.flip()
    clock.tick(FPS)

# Pygame 종료
pygame.quit()
sys.exit()

# Music by 
# <a href="https://pixabay.com/ko/users/music_for_videos-26992513/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=110855">
# Oleg Kyrylkovv</a> from <a href="https://pixabay.com/music//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=110855">Pixabay</a>
