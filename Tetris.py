import pygame
import random
import os

# 初始化
pygame.init()

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
BG_COLOR = (20, 20, 40)
COLORS = [
    (30, 215, 230),  # I - 更柔和的青色
    (30, 90, 210),    # J - 深蓝色
    (255, 180, 60),   # L - 橙色
    (255, 225, 60),   # O - 亮黄色
    (50, 220, 100),   # S - 亮绿色
    (180, 60, 220),   # T - 紫色
    (240, 60, 60)     # Z - 红色
]

# 游戏设置
CELL_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * (GRID_WIDTH + 6)
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
GAME_AREA_LEFT = CELL_SIZE

# 方块形状
SHAPES = [
    [[1, 1, 1, 1]],  # I
    
    [[1, 0, 0],
     [1, 1, 1]],     # J
     
    [[0, 0, 1],
     [1, 1, 1]],     # L
     
    [[1, 1],
     [1, 1]],        # O
     
    [[0, 1, 1],
     [1, 1, 0]],     # S
     
    [[0, 1, 0],
     [1, 1, 1]],     # T
     
    [[1, 1, 0],
     [0, 1, 1]]      # Z
]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('俄罗斯方块')
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.game_started = False
        self.paused = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.font = pygame.font.Font(None, 25)  # 使用pygame默认字体
        self.big_font = pygame.font.Font(None, 40)  # 使用pygame默认字体
        # 初始化音效
        pygame.mixer.init()
        self.move_sound = pygame.mixer.Sound('move.wav') if os.path.exists('move.wav') else None
        self.rotate_sound = pygame.mixer.Sound('rotate.wav') if os.path.exists('rotate.wav') else None
        self.clear_sound = pygame.mixer.Sound('clear.wav') if os.path.exists('clear.wav') else None
        
    def new_piece(self):
        # 随机选择一种方块
        shape = random.choice(SHAPES)
        color = COLORS[SHAPES.index(shape)]
        # 初始位置在顶部中间
        x = GRID_WIDTH // 2 - len(shape[0]) // 2
        y = 0
        return {'shape': shape, 'color': color, 'x': x, 'y': y}
        
    def valid_move(self, piece, x_offset=0, y_offset=0):
        for y, row in enumerate(piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece['x'] + x + x_offset
                    new_y = piece['y'] + y + y_offset
                    if (new_x < 0 or new_x >= GRID_WIDTH or 
                        new_y >= GRID_HEIGHT or 
                        (new_y >= 0 and self.grid[new_y][new_x])):
                        return False
        return True
        
    def rotate_piece(self):
        # 转置矩阵实现旋转
        rotated = list(zip(*self.current_piece['shape'][::-1]))
        # 检查旋转后是否有效
        old_shape = self.current_piece['shape']
        self.current_piece['shape'] = rotated
        if not self.valid_move(self.current_piece):
            self.current_piece['shape'] = old_shape
        
    def lock_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece['y'] + y][self.current_piece['x'] + x] = self.current_piece['color']
        # 检查是否有完整的行
        self.clear_lines()
        # 生成新方块
        self.current_piece = self.new_piece()
        # 检查游戏是否结束
        if not self.valid_move(self.current_piece):
            self.game_over = True
            
    def clear_lines(self):
        lines_cleared = 0
        for y in range(GRID_HEIGHT):
            if all(self.grid[y]):
                lines_cleared += 1
                # 移动上面的行下来
                for y2 in range(y, 0, -1):
                    self.grid[y2] = self.grid[y2-1][:]
                self.grid[0] = [0 for _ in range(GRID_WIDTH)]
        # 计分
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared == 4:
            self.score += 800
            
    def draw_grid(self):
        # 绘制渐变背景
        for y in range(SCREEN_HEIGHT):
            color = (max(20, min(60, y//10)), 
                    max(20, min(60, y//10)), 
                    max(40, min(80, y//5)))
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
        
        # 绘制游戏区域背景
        pygame.draw.rect(self.screen, BG_COLOR, 
                        (GAME_AREA_LEFT, 0, CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT))
        # 绘制网格线
        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(self.screen, GRAY, 
                            (GAME_AREA_LEFT + x * CELL_SIZE, 0), 
                            (GAME_AREA_LEFT + x * CELL_SIZE, CELL_SIZE * GRID_HEIGHT))
        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(self.screen, GRAY, 
                            (GAME_AREA_LEFT, y * CELL_SIZE), 
                            (GAME_AREA_LEFT + GRID_WIDTH * CELL_SIZE, y * CELL_SIZE))
                            
    def draw_piece(self, piece):
        for y, row in enumerate(piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    # 绘制方块主体
                    pygame.draw.rect(self.screen, piece['color'], 
                                    (GAME_AREA_LEFT + (piece['x'] + x) * CELL_SIZE, 
                                     (piece['y'] + y) * CELL_SIZE, 
                                     CELL_SIZE, CELL_SIZE))
                    # 绘制高光效果
                    highlight = tuple(min(255, c + 40) for c in piece['color'])
                    pygame.draw.rect(self.screen, highlight, 
                                    (GAME_AREA_LEFT + (piece['x'] + x) * CELL_SIZE + 2, 
                                     (piece['y'] + y) * CELL_SIZE + 2, 
                                     CELL_SIZE - 4, CELL_SIZE//3))
                    # 绘制边框
                    pygame.draw.rect(self.screen, WHITE, 
                                    (GAME_AREA_LEFT + (piece['x'] + x) * CELL_SIZE, 
                                     (piece['y'] + y) * CELL_SIZE, 
                                     CELL_SIZE, CELL_SIZE), 1)
                                     
    def draw_matrix(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    pygame.draw.rect(self.screen, self.grid[y][x], 
                                    (GAME_AREA_LEFT + x * CELL_SIZE, 
                                     y * CELL_SIZE, 
                                     CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.screen, WHITE, 
                                    (GAME_AREA_LEFT + x * CELL_SIZE, 
                                     y * CELL_SIZE, 
                                     CELL_SIZE, CELL_SIZE), 1)
                                     
    def draw_score(self):
        score_text = self.font.render(f'分数: {self.score}', True, WHITE)
        level_text = self.font.render(f'等级: {self.level}', True, WHITE)
        lines_text = self.font.render(f'行数: {self.lines_cleared}', True, WHITE)
        self.screen.blit(score_text, (GAME_AREA_LEFT + GRID_WIDTH * CELL_SIZE + 20, 30))
        self.screen.blit(level_text, (GAME_AREA_LEFT + GRID_WIDTH * CELL_SIZE + 20, 70))
        self.screen.blit(lines_text, (GAME_AREA_LEFT + GRID_WIDTH * CELL_SIZE + 20, 110))
        
    def draw_start_screen(self):
        title = self.big_font.render('俄罗斯方块', True, WHITE)
        start_text = self.font.render('按任意键开始游戏', True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//3))
        self.screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, SCREEN_HEIGHT//2))

    def draw_pause_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        pause_text = self.big_font.render('游戏暂停', True, WHITE)
        continue_text = self.font.render('按P键继续', True, WHITE)
        self.screen.blit(pause_text, (SCREEN_WIDTH//2 - pause_text.get_width()//2, SCREEN_HEIGHT//3))
        self.screen.blit(continue_text, (SCREEN_WIDTH//2 - continue_text.get_width()//2, SCREEN_HEIGHT//2))

    def draw_game_over(self):
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            game_over_text = self.big_font.render('游戏结束!', True, WHITE)
            score_text = self.font.render(f'最终分数: {self.score}', True, WHITE)
            restart_text = self.font.render('按R键重新开始', True, WHITE)
            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//3))
            self.screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 50))
            
    def run(self):
        fall_time = 0
        fall_speed = 0.5  # 初始下落速度(秒)
        last_time = pygame.time.get_ticks()
        
        while True:
            if not self.game_started:
                self.draw_start_screen()
                pygame.display.update()
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                        if event.type == pygame.KEYDOWN:
                            waiting = False
                            self.game_started = True
                continue
                
            if self.game_over:
                self.draw_game_over()
                pygame.display.update()
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                            self.__init__()
                            waiting = False
                continue
                
            if self.paused:
                self.draw_pause_screen()
                pygame.display.update()
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                            self.paused = False
                            waiting = False
                continue
                
            self.screen.fill(BLACK)
            
            current_time = pygame.time.get_ticks()
            delta_time = (current_time - last_time) / 1000
            last_time = current_time
            fall_time += delta_time
            
            # 根据等级调整下落速度
            adjusted_fall_speed = max(0.05, fall_speed - (self.level - 1) * 0.05)
            
            # 自动下落
            if fall_time >= adjusted_fall_speed:
                fall_time = 0
                if self.valid_move(self.current_piece, 0, 1):
                    self.current_piece['y'] += 1
                    if self.move_sound:
                        self.move_sound.play()
                else:
                    self.lock_piece()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # 暂停游戏
                        self.paused = not self.paused
                    elif self.paused:
                        continue
                        
                    if event.key == pygame.K_LEFT and self.valid_move(self.current_piece, -1, 0):
                        self.current_piece['x'] -= 1
                        if self.move_sound:
                            self.move_sound.play()
                    elif event.key == pygame.K_RIGHT and self.valid_move(self.current_piece, 1, 0):
                        self.current_piece['x'] += 1
                        if self.move_sound:
                            self.move_sound.play()
                    elif event.key == pygame.K_DOWN and self.valid_move(self.current_piece, 0, 1):
                        self.current_piece['y'] += 1
                        if self.move_sound:
                            self.move_sound.play()
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
                        if self.rotate_sound:
                            self.rotate_sound.play()
                    elif event.key == pygame.K_SPACE:  # 硬降落
                        while self.valid_move(self.current_piece, 0, 1):
                            self.current_piece['y'] += 1
                        self.lock_piece()
                        
            # 每清除10行升一级
            if self.lines_cleared >= self.level * 10:
                self.level += 1
                
            self.draw_grid()
            self.draw_matrix()
            self.draw_piece(self.current_piece)
            self.draw_score()
            
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Tetris()
    game.run()
    pygame.quit()
