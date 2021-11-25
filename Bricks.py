import pygame as pg
import random as rnd
import time
import math
from dataclasses import dataclass
pg.init()
width, columns, rows = 400, 15, 30
distance = width // columns # 400/15 = 26
height = distance * rows
grid = [0] * columns * rows
#print(grid)
speed, score, level, temp = 1000, 0, 1, 0
# load hình 
picture = [] # 
for n in range(8):
  picture.append(pg.transform.scale(pg.image.load(f'T_{n}.gif'), (distance, distance)))
screen = pg.display.set_mode([width, height])
pg.display.set_caption('Tetris Game')
# tạo các sự kiện
tetroromino_down = pg.USEREVENT+1
#speedup = pg.USEREVENT+2
pg.time.set_timer(tetroromino_down, speed)
#pg.time.set_timer(speedup, 30_000) # tốc độ rơi xuống
pg.key.set_repeat(1, 100)
# tetroromino cho các chữ cái O, I, J, L, S, Z, T
tetrorominos = [[0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], #O
               [0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0], #I
               [0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0], #J
               [0, 0, 4, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0], #L
               [0, 5, 5, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #S
               [6, 6, 0, 0, 0, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0], #Z
               [0, 0, 0, 0, 7, 7, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0]] #T

#tạo lớp và định nghĩa các hàm
@dataclass
class tetroromino():
  tetro: list
  row: int = 0 # vị trí xuất hiện đầu tiên
  column: int = 5

  def show(self):
    for n, color in enumerate(self.tetro): # enumerate tạo list dạng liệt kê
      if color > 0:
        x = (self.column + n % 4) * distance
        y = (self.row + n // 4) * distance
        screen.blit(picture[color], (x, y))

  def check(self, r, c):
    for n, color in enumerate(self.tetro):
      if color > 0:
        rs = r + n // 4
        cs = c + n % 4
        if rs >= rows or cs < 0 or cs >= columns or grid[rs * columns + cs] > 0:
          return False
    return True

  def update(self, r, c):
    if self.check(self.row + r, self.column + c):
      self.row += r
      self.column += c
      return True
    return False

  def rotate(self):
    savetetro = self.tetro.copy()
    #print('self.tetro=',self.tetro)
    for n, color in enumerate(savetetro):
      self.tetro[(2-(n % 4))*4+(n // 4)] = color
    if not self.check(self.row, self.column):
      self.tetro = savetetro.copy()

def ObjectOnGridline():
  for n, color in enumerate(character.tetro):
    if color > 0:
      grid[(character.row + n // 4)*columns+(character.column + n % 4)] = color

def DeleteFullRows():
  fullrows = 0
  for row in range(rows):
    for column in range(columns):
      if grid[row*columns+column] == 0: # in ra một cột có 30 số 0 ???#kiểm tra nếu dòng nào có ô rỗng thì bỏ qua
        break
    else:
      del grid[row*columns:row*columns+columns] # [2, 1, 1, 1, 1, 7, 7, 7, 2, 2, 2, 2, 7, 7, 7]
      grid[0:0] = [0]*columns  # trả về []
      fullrows += 1
  return fullrows**2*100 # xóa càng nhiều dòng cùng lúc điểm càng lũy thừa cao lên nhiều lần

character = tetroromino(rnd.choice(tetrorominos))

status = True
#clock = pg.time.Clock()
while status:
  #clock.tick(80)
  pg.time.delay(100)
  for event in pg.event.get():
    if event.type == pg.QUIT:
      status = False
    if event.type == tetroromino_down:
      if not character.update(1, 0): # kiểm tra khi mỗi chữ cái được đặt xong tại một vị trí
        ObjectOnGridline()
        score += DeleteFullRows()
        if score > 0 and score//500 >= level and temp != score:
          speed = int(speed * 0.8)
          pg.time.set_timer(tetroromino_down, speed)
          level = score // 500 + 1
          temp = score 
        character = tetroromino(rnd.choice(tetrorominos))
    if event.type == pg.KEYDOWN:
      if event.key == pg.K_LEFT:
        character.update(0, -1) #dòng không đổi, cột giảm 1
      if event.key == pg.K_RIGHT:
        character.update(0, 1)
      if event.key == pg.K_DOWN:
        character.update(1, 0)
      if event.key == pg.K_SPACE:
        character.rotate()

  screen.fill((128, 128, 128))
  character.show()

  textsurface = pg.font.SysFont('consolas', 40).render(f'{score:,}', False, (255, 255, 255))
  screen.blit(textsurface, (width // 2 - textsurface.get_width() // 2, 5))
  textsurface = pg.font.SysFont('consolas', 20).render(f'Level: {level}', False, (255, 255, 255))
  screen.blit(textsurface, (width // 2 - textsurface.get_width() // 2, 55))

  for n, color in enumerate(grid):
    if color > 0:
      x = n % columns * distance
      y = n // columns * distance
      screen.blit(picture[color], (x, y))
  
  pg.display.flip()

pg.quit()