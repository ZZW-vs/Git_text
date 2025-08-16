import pygame
import random

# 初始化
pygame.init()

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # I
    (0, 0, 255),    # J
    (255, 165, 0),  # L
    (255, 255, 0),  # O
    (0, 255, 0),    # S
    (128, 0, 128),  # T
    (255, 0, 0)     # Z
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
        self.score = 0
        self.font = pygame.font.SysFont('Arial', 25)
        
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
        # 绘制游戏区域背景
        pygame.draw.rect(self.screen, BLACK, 
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
                    pygame.draw.rect(self.screen, piece['color'], 
                                    (GAME_AREA_LEFT + (piece['x'] + x) * CELL_SIZE, 
                                     (piece['y'] + y) * CELL_SIZE, 
                                     CELL_SIZE, CELL_SIZE))
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
        self.screen.blit(score_text, (GAME_AREA_LEFT + GRID_WIDTH * CELL_SIZE + 20, 30))
        
    def draw_game_over(self):
        if self.game_over:
            text = self.font.render('游戏结束! 按R键重新开始', True, WHITE)
            self.screen.blit(text, (GAME_AREA_LEFT + 30, SCREEN_HEIGHT // 2 - 30))
            
    def run(self):
        fall_time = 0
        fall_speed = 0.5  # 秒
        last_time = pygame.time.get_ticks()
        
        while not self.game_over:
            self.screen.fill(BLACK)
            
            current_time = pygame.time.get_ticks()
            delta_time = (current_time - last_time) / 1000
            last_time = current_time
            fall_time += delta_time
            
            # 自动下落
            if fall_time >= fall_speed:
                fall_time = 0
                if self.valid_move(self.current_piece, 0, 1):
                    self.current_piece['y'] += 1
                else:
                    self.lock_piece()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    return
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.valid_move(self.current_piece, -1, 0):
                        self.current_piece['x'] -= 1
                    elif event.key == pygame.K_RIGHT and self.valid_move(self.current_piece, 1, 0):
                        self.current_piece['x'] += 1
                    elif event.key == pygame.K_DOWN and self.valid_move(self.current_piece, 0, 1):
                        self.current_piece['y'] += 1
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
                    elif event.key == pygame.K_SPACE:  # 硬降落
                        while self.valid_move(self.current_piece, 0, 1):
                            self.current_piece['y'] += 1
                        self.lock_piece()
                    elif event.key == pygame.K_r and self.game_over:
                        self.__init__()  # 重置游戏
                        
            self.draw_grid()
            self.draw_matrix()
            self.draw_piece(self.current_piece)
            self.draw_score()
            self.draw_game_over()
            
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Tetris()
    game.run()
    pygame.quit()
