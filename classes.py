import pygame, sys, os, random, pygame.gfxdraw

# вынес сюда все константы из consts.py чтоб не импортировать их
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
COLOR = (213, 251, 80)
SIZE_CHIP     = 100 # ширина и высота квадратной фишки (в пикселах)
GAP_CHIP      = 1   # зазор между соседними фишками (в пикселах)
WIDTH_BORDER  = 8   # ширина рамки игрового поля
MARGIN_FIELD  = 15  # отступ игрового поля от краёв окна
QUALITYMIX    = 500
class Field():



  def __init__(self, SIZE_FIELD): # добавил в конструктор SIZE_FIELD
    self.matrix = [] # список для хранения структуры игрового поля
    self.SIZE_FIELD = SIZE_FIELD;
    self.SIZE_SCREEN   = SIZE_CHIP * SIZE_FIELD + (SIZE_FIELD - 1) * GAP_CHIP + 2 * (MARGIN_FIELD + WIDTH_BORDER) # ширина и высота окна
    self.LENGTH_BORDER = self.SIZE_SCREEN - 2 * MARGIN_FIELD # длина границы игрового поля
    '''
    Теперь SIZE_SCREEN, SIZE FIELD и LENGTH_BORDER являются полями класса Field, и соответственно перед любым обращением к этим полям внутри класа стоит
    префикс self.
    '''


    ''' Инициализация главной структуры данных '''
    for i in range(0, SIZE_FIELD):
      self.matrix.append([])
      for j in range(0, SIZE_FIELD):
        self.matrix[i].append(j+SIZE_FIELD*i)
    self.matrix[-1][-1] = None
    
    self.initmatrix = self.matrix                      # копия начальной структуры игрового поля
    self.pics       = []                               # хранилище картинок
    self.indexNone  = (SIZE_FIELD - 1, SIZE_FIELD - 1) # индекс пустой клетки
    self.level      = []
	
    ''' заполнение хранилища картинок '''
    random.shuffle(self.level)
    if (self.SIZE_FIELD == 3): self.address = os.path.join("pics", "300x300", "2")
    if (self.SIZE_FIELD == 4): self.address = os.path.join("pics", "400x400", "2")
    if (self.SIZE_FIELD == 5): self.address = os.path.join("pics", "500x500", "2")
	
	
    for i in range(0, SIZE_FIELD**2):
      self.pics.append(pygame.image.load(os.path.join(self.address, str(i) + ".jpg"))) # Заполнение полей в поле
    
  def fromGlobalToLocal(self, gx, gy): # Перевод из глобальной в локальную
    lx = int((gx - MARGIN_FIELD - WIDTH_BORDER)/(SIZE_CHIP + GAP_CHIP))
    ly = int((gy - MARGIN_FIELD - WIDTH_BORDER)/(SIZE_CHIP + GAP_CHIP))
    return (lx, ly)
    
  def fromLocalToGlobal(self, lx, ly): # Перевод из локальной в глобальную
    gx = MARGIN_FIELD + WIDTH_BORDER + (SIZE_CHIP + GAP_CHIP) * lx
    gy = MARGIN_FIELD + WIDTH_BORDER + (SIZE_CHIP + GAP_CHIP) * ly
    return (gx, gy)

  def drawField(self, screen): # Нарисовать поле
    pygame.gfxdraw.box(screen, (MARGIN_FIELD, MARGIN_FIELD, self.LENGTH_BORDER, self.LENGTH_BORDER), BLACK)
    pygame.gfxdraw.box(screen, (MARGIN_FIELD + WIDTH_BORDER, MARGIN_FIELD + WIDTH_BORDER, self.LENGTH_BORDER - 2 * WIDTH_BORDER, self.LENGTH_BORDER - 2 * WIDTH_BORDER), WHITE)
    for i in range(1, self.SIZE_FIELD):
      x = y = MARGIN_FIELD + WIDTH_BORDER + i * SIZE_CHIP + (i - 1) * GAP_CHIP
      pygame.gfxdraw.box(screen, (x, MARGIN_FIELD + WIDTH_BORDER, GAP_CHIP, self.LENGTH_BORDER - 2 * WIDTH_BORDER), BLACK)
      pygame.gfxdraw.box(screen, (MARGIN_FIELD + WIDTH_BORDER, y, self.LENGTH_BORDER - 2 * WIDTH_BORDER, GAP_CHIP), BLACK)
      
  def assignment(self, screen): # Заполнение поля фишками
    for ly in range(0, self.SIZE_FIELD):
      for lx in range(0, self.SIZE_FIELD):
        (gx, gy) = self.fromLocalToGlobal(lx, ly)
        if self.matrix[ly][lx] != None:
          screen.blit(self.pics[self.matrix[ly][lx]], (gx, gy, SIZE_CHIP, SIZE_CHIP))

  def makeMove(self, gx, gy): # Сделать один ход
    lx, ly = self.fromGlobalToLocal(gx, gy)
    for j in range(0, self.SIZE_FIELD):
      for i in range(0, self.SIZE_FIELD):
        if self.matrix[j][i] == None: index = (i, j)
    if ((lx == index[0] - 1 or lx == index[0] + 1) and ly == index[1]) or ((ly == index[1] - 1 or ly == index[1] + 1) and lx == index[0]):
      tmp = self.matrix[ly][lx]
      self.matrix[ly][lx] = None
      self.matrix[index[1]][index[0]] = tmp
      self.indexNone = (lx, ly)
      
  def findRandNeighbor(self): # Найти случайного соседа с пустой клеткой
    indexNone = self.indexNone
    neighbors = [] # список соседей
    if indexNone[0] - 1 >= 0: neighbors.append((indexNone[0] - 1, indexNone[1]))
    if indexNone[0] + 1 <= self.SIZE_FIELD - 1: neighbors.append((indexNone[0] + 1, indexNone[1]))
    if indexNone[1] - 1 >= 0: neighbors.append((indexNone[0], indexNone[1] - 1))
    if indexNone[1] + 1 <= self.SIZE_FIELD - 1: neighbors.append((indexNone[0], indexNone[1] + 1))
    random.shuffle(neighbors)
    return neighbors[0]

  def randomMix(self): # Случайное перемешивание фишек в поле
    for i in range(0, QUALITYMIX):
      neighbor = self.findRandNeighbor()
      
      tmp = self.matrix[neighbor[1]][neighbor[0]]
      self.matrix[neighbor[1]][neighbor[0]] = None
      self.matrix[self.indexNone[1]][self.indexNone[0]] = tmp
      self.indexNone = neighbor

  def isFinish(self): # Проверить, закончилась ли игра
    if self.matrix == self.initmatrix:
      return True
    else:
      return False

# реализовал класс кнопки в меню выбора уровня
class LevelButton:

  def __init__(self, x, y, size, n):
    self.x = x; self.y = y;
    self.size = size;
    self.n = n;
    self.text = pygame.font.SysFont('Comic Sans MS', 30).render(str(self.n), False, (25, 25, 25))

  def draw(self, screen):
    pygame.draw.rect(screen, (25, 25, 25),
                      (self.x, self.y, self.size, self.size), 4);
    screen.blit(self.text, (self.x + self.size // 2 - 15, self.y + self.size // 2 - 15));

  def collides(self, event):
    return event.pos[0] > self.x and event.pos[0] < self.x + self.size and event.pos[1] > self.y and event.pos[1] < self.y + self.size

