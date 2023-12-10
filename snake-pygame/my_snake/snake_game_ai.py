import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
from snake_game_player import SnakeGame


pygame.init()
font = pygame.font.Font('arial.ttf', 25)

# reset
# reward
# play(action) -> direction
# game_iteration
# is_collision


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

GAME_SCREEN_WIDTH = 640
BLOCK_SIZE = 20
p_snake = SnakeGame()

mine_image = pygame.image.load("mine.png")
mine_image = pygame.transform.scale(mine_image, (BLOCK_SIZE, BLOCK_SIZE))

class SnakeGameAI:
    
    def __init__(self, w = GAME_SCREEN_WIDTH*2 + BLOCK_SIZE * 2, h = 480):
        self.w = w
        self.h = h
        self.speed = 200
        self.game_width = GAME_SCREEN_WIDTH
        self.mine_interval = 0
        self.round_vs_player = {50,60,70,80,90,100,110,120,130,140,150} # 11 rounds
        self.is_round_start = True
        self.countdown = 0
        self.winrate = 0
        self.ai_win = 0
        self.player_win = 0
        self.draw = 0
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake AI vs Human')
        self.clock = pygame.time.Clock()
        self.reset()
        p_snake = SnakeGame()
        p_snake.reset()
        

    def reset(self):
        # init game state
        self.direction = Direction.RIGHT
        self.head = Point(self.game_width/2, self.h/2)
        self.snake = [self.head, 
                    Point(self.head.x-BLOCK_SIZE, self.head.y), 
                    Point(self.head.x-BLOCK_SIZE*2, self.head.y)]
        self.score = 0
        self.food = None
        self.mine = []
        self._place_food()
        self.frame_iteration = 0

    def reset_p_snake(self):
        p_snake.reset()

    # helper function
    def _place_food(self):
        x = random.randint(0, (self.game_width - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if(self.food in self.snake or self.food in self.mine):
            self._place_food()

    def _place_mine(self):
        x = random.randint(0, (self.game_width - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        new_mine = Point(x,y)
        if(new_mine in self.mine or new_mine in self.snake or new_mine == self.food):
            self._place_mine()
        else:
            self.mine.append(new_mine)
            self.mine_interval = 0
            

    
    def play_step(self, action):
        self.frame_iteration += 1
        self.mine_interval += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if p_snake.direction != 1:
                        p_snake.direction = 2
                elif event.key == pygame.K_RIGHT:
                    if p_snake.direction != 2:
                        p_snake.direction = 1
                elif event.key == pygame.K_UP:
                    if p_snake.direction != 4:
                        p_snake.direction = 3
                elif event.key == pygame.K_DOWN:
                    if p_snake.direction != 3:
                        p_snake.direction = 4
                # break -> one key input per play_step
                break
            
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        # 3. check if game over
        reward = 0
        game_over1 = False
        game_over2 = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over1 = True
            reward = -10
            return reward, game_over1, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            # recursive -> helper function
            self._place_food()
            # no pop is done -> list size not reduced -> looks like increasing its size in the game
        else:
            # remove last element of snake
            self.snake.pop()

        if self.mine_interval >= self.speed/5:
            self._place_mine()

        # 5. return game over and score
        game_over1  = False
        return reward, game_over1, self.score

    def player_play_step(self):            
        # 2. move

        p_snake.move(p_snake.direction)
        # 3. check if game over
        p_snake.game_over = False
        if p_snake.is_collision():
            p_snake.game_over = True
            p_snake.best_score = p_snake.score if p_snake.score > p_snake.best_score else p_snake.best_score
            return p_snake.game_over, p_snake.score, p_snake.best_score
        # 4. place new food or just move

        p_snake.place_or_move()
        # 6. return game over and score
        p_snake.game_over  = False
        p_snake.best_score = p_snake.score if p_snake.score > p_snake.best_score else p_snake.best_score
        return p_snake.game_over, p_snake.score, p_snake.best_score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.game_width - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        # self.snake[0] -> head
        if pt in self.snake[1:]:
            return True
        if pt in self.mine:
            return True
        return False

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1,0,0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0,1,0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0,0,1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

    def update_ui(self, n_games=0):
        self.n_games = n_games
        
        if self.n_games in self.round_vs_player:
            if self.is_round_start:
                self.countdown = 5
                self.speed = 20
                self.last_count = pygame.time.get_ticks()
                self.is_round_start = False
            if self.is_round_start == False:
                if self.countdown > 0:
                    self.clock.tick(self.speed)
                    self.display.fill(BLACK)
                    timer_text = font.render(str(self.countdown), True, WHITE)
                    self.display.blit(timer_text, [self.w/2, self.h/2])
                    pygame.display.flip()
                    if pygame.time.get_ticks() - self.last_count > 1000:
                        self.countdown -= 1
                        self.last_count = pygame.time.get_ticks()
        else:
            self.speed = 200
            self.is_round_start = True
        
        
        
        if self.countdown == 0:
            self.clock.tick(self.speed) # decide frame update
            self.display.fill(BLACK)

            for pt in self.snake:
                pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))
            pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
            for block in range(0, int(self.h/ BLOCK_SIZE)):
                pygame.draw.rect(self.display, WHITE, pygame.Rect(self.game_width, block*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(self.display, WHITE, pygame.Rect(self.game_width + BLOCK_SIZE, block*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            
            for pt in p_snake.snake:
                pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))
            for fd in p_snake.food:
                pygame.draw.rect(self.display, RED, pygame.Rect(fd.x, fd.y, BLOCK_SIZE, BLOCK_SIZE))

            for mine in self.mine:
                self.display.blit(mine_image, (mine.x, mine.y))

            score_text = font.render("Score: " + str(self.score), True, WHITE)
            score_text_p = font.render("Score: " + str(p_snake.score), True, WHITE)
            best_score_text_p = font.render("Best Score: " + str(p_snake.best_score), True, WHITE)

            train_num_text = font.render("#Train: " + str(n_games), True, WHITE)
            self.display.blit(score_text, [0,0])
            self.display.blit(train_num_text, [500,0])
            self.display.blit(score_text_p, [680,0])
            self.display.blit(best_score_text_p, [680,50])

            # update display surface to the screen
            pygame.display.flip()

    def show_results(self, ai_score, player_best):
        self.display.fill(BLACK)
        if player_best > ai_score:
            self.vs_result = "Win"
            self.player_win += 1
        elif player_best < ai_score:
            self.vs_result = "Lose"
            self.ai_win += 1
        else:
            self.vs_result = "Draw"
            self.draw += 1
        
        vs_text = font.render("AI (#" + str(self.n_games) + "): " + str(ai_score) + " Player: " + str(player_best) + " " + self.vs_result, True, WHITE)
        self.display.blit(vs_text, [self.w/2 - 150, self.h/2])
        pygame.display.flip()
        pygame.time.delay(3000)
        if self.n_games == 150:
            self.display.fill(BLACK)
            vs_text = font.render("You've beaten AI " + str(self.player_win) + " times with the win rate of " + str(self.player_win/(self.player_win+self.ai_win +self.draw)*100), True, WHITE)
            self.display.blit(vs_text, [self.w/2 - 300, self.h/2])
            pygame.display.flip()
            pygame.time.delay(5000)
            pygame.quit()
            quit()




'''
# leave it for the agent
if __name__ == '__main__':
    game = SnakeGameAI()

    # game loop
    while True:
        game_over1, score = game.play_step()

        # break if game over
        if game_over1 == True:
            break

    print('Final Score', score)
    
    pygame.quit()
'''