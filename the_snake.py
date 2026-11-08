from random import choice, randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

KEY_TURNS = {
    (pygame.K_UP, LEFT): UP,
    (pygame.K_UP, RIGHT): UP,
    (pygame.K_DOWN, LEFT): DOWN,
    (pygame.K_DOWN, RIGHT): DOWN,
    (pygame.K_LEFT, UP): LEFT,
    (pygame.K_LEFT, DOWN): LEFT,
    (pygame.K_RIGHT, UP): RIGHT,
    (pygame.K_RIGHT, DOWN): RIGHT,
}

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """Хранит общие атрибуты игровых объектов:

    position — координаты объекта на игровом поле (кортеж из двух чисел);
    body_color — цвет объекта в формате RGB.
    """

    def __init__(self):
        """Инициализирует позицию и цвет игрового объекта."""
        self.position = CENTER_POSITION
        self.body_color = (255, 255, 255)

    def draw_cell(self, position, color, border_color=BORDER_COLOR):
        """Отрисовывает одну ячейку игрового поля."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        if border_color:
            pygame.draw.rect(screen, border_color, rect, 1)

    def draw(self):
        """Отрисовывает объект на игровом поле."""


class Apple(GameObject):
    """Яблоко занимает одну клетку игрового поля.
    После того как змейка съедает яблоко, оно появляется
    в новой случайной точке поля.

    Хранит атрибуты:

    position — координаты яблока, кратные GRID_SIZE;
    body_color — цвет яблока.
    """

    def __init__(self):
        """Инициализирует яблоко красным цветом и случайной позицией."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self, occupied_cells=None):
        """Выбирает случайную клетку игрового поля."""
        if occupied_cells is None:
            occupied_cells = (CENTER_POSITION,)
        while True:
            x_position = randint(0, GRID_WIDTH - 1)
            y_position = randint(0, GRID_HEIGHT - 1)
            position = (x_position * GRID_SIZE, y_position * GRID_SIZE)
            if position not in occupied_cells:
                self.position = position
                break

    def draw(self):
        """Отрисовывает яблоко."""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Отвечает за хранение змейки, её движение,
    изменение направления, рост после съеденного яблока,
    сброс после столкновения с собой и отрисовку на экране.

    Хранит атрибуты:

    body_color — цвет змейки;
    length — текущая длина змейки;
    positions — список координат, первый элемент — голова;
    direction — текущее направление движения (dx, dy);
    last — координаты последнего сегмента перед удалением,
    нужны для очистки клетки на экране.
    """

    def __init__(self):
        """Инициализирует змейку одним сегментом в центре поля."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.reset(RIGHT)

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Перемещает змейку на одну клетку в текущем направлении."""
        head_x_position, head_y_position = self.get_head_position()
        dx, dy = self.direction
        new_head_x_position = head_x_position + dx * GRID_SIZE
        new_head_y_position = head_y_position + dy * GRID_SIZE
        new_head = (
            new_head_x_position % SCREEN_WIDTH,
            new_head_y_position % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self, direction=None):
        """Возвращает змейку в начальное состояние."""
        self.position = CENTER_POSITION
        self.positions = [self.position]
        self.length = 1
        self.direction = (
            direction if direction is not None
            else choice([UP, DOWN, LEFT, RIGHT])
        )
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)

    def draw(self):
        """Отрисовывает все сегменты змейки на экране."""
        for position in self.positions[1:]:
            self.draw_cell(position, self.body_color)

        self.draw_cell(self.get_head_position(), self.body_color)

        if self.last:
            self.draw_cell(
                self.last,
                BOARD_BACKGROUND_COLOR,
                border_color=None
            )

    def update_direction(self, direction):
        """Обновляет текущее направление движения змейки."""
        if direction:
            self.direction = direction


def handle_keys(game_object):
    """Обрабатывает события клавиатуры и закрытия окна."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            new_direction = KEY_TURNS.get((event.key, game_object.direction))
            if new_direction:
                game_object.update_direction(new_direction)


def main():
    """Запускает игру и собирает основной игровой цикл."""
    pygame.init()
    screen.fill(BOARD_BACKGROUND_COLOR)
    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        head_position = snake.get_head_position()
        if head_position == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if head_position in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
