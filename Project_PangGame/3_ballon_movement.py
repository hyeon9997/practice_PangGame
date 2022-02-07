import os
import pygame
##################################################################
# 기본 초기화 (반드시 해야 하는 것들)


pygame.init() # 초기화 (반드시 필요)

# 화면 크기 설정
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height ))

# 화면 타이틀 설정
pygame.display.set_caption("Nado Pang")

# FPS(프레임)
clock = pygame.time.Clock()

##################################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 캐릭터, 좌표, 폰트 등)
current_path = os.path.dirname(__file__) #현재 파일의 위치 반환
image_path = os.path.join(current_path, "images") #images 폴더 위치 반환

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - stage_height - character_height

# 캐릭터 이동 방향
character_to_x = 0

# 캐릭터 이동 속도
character_speed = 5

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = character.get_rect().size
weapon_width = weapon_size[0]
weapon_height = weapon_size[1]

# 무기는 한 번에 여러 발 발사 가능
weapons = []

# 무기 이동 속도
weapon_speed = 10

# 공 만들기 (4개 크기에 대해 따로 처리)
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))
]

# 공 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -9]

# 공들
balls = []

balls.append({
    "pos_x" : 50, # 공의 x좌표
    "pos_y" : 50, # 공의 y좌표
    "img_idx" : 0,
    "to_x" : 3, # x축 이동방향
    "to_y" : -6, # y축 이동방향
    "init_spe_y" : ball_speed_y[0] }) # y 최초 속도
    


# 이벤트 루프
running = True #게임 진행 여부 확인
while running:
    dt = clock.tick(10) #게임화면 초당 프레임 수 설정

    # 2. 이벤트 처리(키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key ==  pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3. 게임 캐릭터 위치 정의    
    character_x_pos += character_to_x

    # 캐릭터 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos == screen_width - character_width:
        character_x_pos = screen_width - character_width

    #  무기 위치 정의 : 무기 위치를 위로 이동
    weapons = [[w[0], w[1] - weapon_speed]  for w in weapons] ##반드시 찾아볼것!!

    # 천장에 닿은 무기 없애기
    weapons = [[w[0], w[1] - weapon_speed]  for w in weapons if w[1] > 0] #만약 w[1](y좌표)가 0보다 크면 리스트로 만든다?

    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls): #enumerate() : 리스트 번호/값 뽑아옴
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 가로벽에 닿았을 때 공 이동 위치 변경(튕겨 나오는 효과)
        if ball_pos_x <= 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * - 1

        # 세로 위치
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spe_y"] # 처음 바닥에 닿았을 때 튕겨 올라가는 부분
        else:
            ball_val["to_y"] += 0.5 # 속도를 증가하면서 위로 올라가게됨
        
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # 4. 충돌 처리

    # 5. 화면에 그리기 (작성 순서대로 화면에 표시됨)    
    screen.blit(background, (0, 0))
    
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos ))   
    
    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))
    
    screen.blit(stage, (0, screen_height - stage_height))

    screen.blit(character, (character_x_pos, character_y_pos))
    
    


    pygame.display.update() # 게임화면을 다시 그리기


# 종료 전 대기
pygame.time.dalay(2000) #2초 정도 대기

# 게임 종료
pygame.quit()