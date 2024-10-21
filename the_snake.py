from random import randint

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
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.

class GameObject:
    """
    Doc string1
    Doc string2
    """

    def __init__(self, body_color, position):
        """
        Doc string1
        Doc string2
        """
        self.position = position
        self.body_color = body_color

    def draw(self):
        """
        Doc string1
        Doc string2
        """
        pass


class Apple(GameObject):
    """
    Doc string1
    Doc string2
    """

    def __init__(self):
        """
        Doc string1
        Doc string2
        """
        super().__init__(APPLE_COLOR, self.randomize_position())

    @classmethod
    def randomize_position(cls):
        """
        Doc string1
        Doc string2
        """
        return randint(0, 64) * 10, randint(0, 38) * 10

    def draw(self):
        """
        Doc string1
        Doc string2
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Doc string1
    Doc string2
    """

    def __init__(self):
        """
        Doc string1
        Doc string2
        """
        super().__init__(SNAKE_COLOR, (320, 240))
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """
        Doc string1
        Doc string2
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple_not_eaten=True):
        """
        Doc string1
        Doc string2
        """
        dirc1 = self.direction[0]
        dirc2 = self.direction[1]
        next_position1 = (dirc1 * 10 + self.get_head_position()[0]) % 640
        next_position2 = (dirc2 * 10 + self.get_head_position()[1]) % 480
        self.positions.insert(0, (next_position1, next_position2))
        self.last = self.positions[-1]
        self.length += 1
        if apple_not_eaten:
            self.length -= 1
            self.positions = self.positions[0: -1]

    def get_head_position(self):
        """
        Doc string1
        Doc string2
        """
        return self.positions[0]

    def draw(self):
        """
        Doc string1
        Doc string2
        """
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """
        Doc string1
        Doc string2
        """
        if self.length > 1:
            for pos in self.positions[1:]:
                x_apple = pos[0] == self.get_head_position()[0]
                y_apple = pos[1] == self.get_head_position()[1]
                if x_apple and y_apple:
                    self.__init__()
                    self.draw()
                    break


def handle_keys(game_object):
    """
    Doc string1
    Doc string2
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
    """
    Doc string1
    Doc string2
    """
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()
    snake.draw()
    apple.draw()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        x_apple = apple.position[0] - snake.get_head_position()[0]
        y_apple = apple.position[1] - snake.get_head_position()[1]
        print(x_apple, y_apple)
        if abs(x_apple) + abs(y_apple) < 15:
            print("EATEN++++++++++++")
            snake.move(False)
            apple.body_color = (0, 0, 0)
            apple.draw()
            apple = Apple()
            apple.draw()
        else:
            snake.move()
        snake.reset()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
