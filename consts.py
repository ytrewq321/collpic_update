''' глобальные константы '''

def update_consts(SIZE_FIELD):
	global SIZE_SCREEN
	global LENGTH_BORDER
	SIZE_SCREEN   = SIZE_CHIP * SIZE_FIELD + (SIZE_FIELD - 1) * GAP_CHIP + 2 * (MARGIN_FIELD + WIDTH_BORDER) # ширина и высота окна
	LENGTH_BORDER = SIZE_SCREEN - 2 * MARGIN_FIELD # длина границы игрового поля


SIZE_CHIP     = 100 # ширина и высота квадратной фишки (в пикселах)
GAP_CHIP      = 1   # зазор между соседними фишками (в пикселах)
WIDTH_BORDER  = 8   # ширина рамки игрового поля
MARGIN_FIELD  = 15  # отступ игрового поля от краёв окна
SIZE_SCREEN   = 0
LENGTH_BORDER = 0
QUALITYMIX    = 500

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
COLOR = (213, 251, 80)
