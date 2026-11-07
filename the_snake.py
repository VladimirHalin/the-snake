from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игровых объектов.

    Хранит общие атрибуты игровых объектов:

    position — координаты объекта на игровом поле (кортеж из двух чисел);
    body_color — цвет объекта в формате RGB.

    Дочерние классы переопределяют метод draw() и рисуют объект
    на экране своим способом.
    """

    def __init__(self):
        """Инициализирует позицию и цвет игрового объекта.

        Позиция по умолчанию — центр игрового поля,
        цвет по умолчанию — белый.
        """
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = (255, 255, 255)

    def draw(self):
        """Отрисовывает объект на игровом поле.

        Реализуется в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс яблока.

    Яблоко занимает одну клетку игрового поля и хранит:

    position — координаты яблока, кратные GRID_SIZE;
    body_color — цвет яблока.

    После того как змейка съедает яблоко, оно появляется
    в новой случайной точке поля.
    """

    def __init__(self):
        """Инициализирует яблоко красным цветом и случайной позицией."""
        super().__init__()
        self.body_color = (255, 0, 0)
        self.randomize_position()

    def randomize_position(self):
        """Выбирает случайную клетку игрового поля,
        сохраняет её в position.
        """
        x_position = randint(0, GRID_WIDTH - 1)
        y_position = randint(0, GRID_HEIGHT - 1)
        self.position = (x_position * GRID_SIZE, y_position * GRID_SIZE)

    def draw(self):
        """Отрисовывает яблоко квадратом в одну клетку с бирюзовой рамкой."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки.

    Отвечает за хранение змейки, её движение,
    изменение направления, рост после съеденного яблока,
    сброс после столкновения с собой и отрисовку на экране.

    Хранит атрибуты:

    body_color — цвет змейки;
    length — текущая длина змейки;
    positions — список координат, первый элемент — голова;
    direction — текущее направление движения (dx, dy);
    next_direction — направление, выбранное пользователем;
    last — координаты последнего сегмента перед удалением,
    нужны для очистки клетки на экране.
    """

    def __init__(self):
        """Инициализирует змейку одним сегментом в центре поля.

        Начальное направление движения — вправо.
        """
        super().__init__()
        self.body_color = (0, 255, 0)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает координаты головы змейки — первый элемент positions."""
        return self.positions[0]

    def move(self):
        """Перемещает змейку на одну клетку в текущем направлении.

        Вычисляет новую позицию головы по вектору direction и шагу
        GRID_SIZE. Остаток от деления на размеры экрана обеспечивает
        проход сквозь границы поля. Новая голова добавляется в начало
        списка positions. Если длина списка превышает length, последний
        сегмент удаляется, а его координаты сохраняются в last.
        """
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

    def reset(self):
        """Возвращает змейку в начальное состояние.

        Длина становится равна 1, список positions содержит только
        начальную позицию в центре поля, направление движения
        выбирается случайным образом. Экран очищается цветом
        игрового поля перед новой игрой.
        """
        self.positions = [self.position]
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)

    def draw(self):
        """Отрисовывает все сегменты змейки на экране.

        Тело и голова рисуются квадратами в одну клетку с рамкой.
        Клетка удалённого сегмента (last) затирается цветом игрового
        поля, чтобы за змейкой не оставалось следов.
        """
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Обновляет текущее направление движения змейки.

        Переносит next_direction в direction, если пользователь
        выбрал новое направление, и сбрасывает next_direction.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(game_object):
    """Обрабатывает события клавиатуры и закрытия окна.

    При нажатии стрелок сохраняет выбранное направление
    в next_direction игрового объекта. Противоположное текущему
    направление игнорируется, чтобы змейка не могла мгновенно
    развернуться. При закрытии окна завершает программу.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Запускает игру и собирает основной игровой цикл.

    Создаёт игровые объекты, затем в цикле обрабатывает ввод,
    обновляет направление и позицию змейки, проверяет съеденное
    яблоко и столкновения, отрисовывает объекты и обновляет экран.
    """
    pygame.init()
    screen.fill(BOARD_BACKGROUND_COLOR)
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
