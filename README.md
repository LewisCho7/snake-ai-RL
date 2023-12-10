# snake-ai-RL
# Snake AI RL vs Human
스네이크: 인공지능 대 인간

## Project Objective
1. To study and develop artificial intelligence, especially Reinforcement Learning.
2. I have never used pygame before as a game engine and therefore wanted to learn about pygame
3. To get used to Python language. To practice pythonic code.
4. To start on mixing games and reinforcement learning for future projects
5. To try using pytorch for implementing deep learning (neural network)

## Briefly about Reinforcement Learning and Deep Q-Learning model
Explanation about what I understood
### Reinforcement Learning
- **agent** -> **action**
- agent is in a certain **environment**
- agent gets a **reward** for the action
### Deep neural network
- When given state(input)
- go through layers of perceptrons (input/hidden/output)
- computes the output and error with loss function
### Deep Q-Learning
- Q value is the Quality of action
  0. Initialize Q value(= init model)
  1. Choose action (predict by model *or* random move) -> trade-off relationship
  2. Perform action
  3. Measure Reward
  4. Update Q-Value(and train model)
- repeate 1~4
- Bellman Equation is used -> Optimality
- Activation Function = ReLU

## Requirements for executing file
- Python 3.7
- pytorch
- pygame
- IPython
- matplotlib(not used but included)

## How to execute file
- Run start.py in my_snake folder

## Project Explanation
- Snake game AI is trained using deep learning
- After 50 times of training, competition between AI and human player begins
- Every after 10 trainings, player is able to control the snake on the right side
- Result will be shown when the AI snake collides with the wall or one of the mines or its body
- After 150 training, the final results and win rate is displayed on the screen

## Important features(creative)
- Because AI is so much better at this game, I added many handicaps to AI version game :joy:
1. I added mines that is placed frequently when the play_step loop is ongoing -> makes AI harder to get high-score
```
    def _place_mine(self):
        x = random.randint(0, (self.game_width - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        new_mine = Point(x,y)
        if(new_mine in self.mine or new_mine in self.snake or new_mine == self.food):
            self._place_mine()
        else:
            self.mine.append(new_mine)
            self.mine_interval = 0
```
2. When playing versus human, the score for AI is only for that training (epoch), but player's score is counted as a highscore.
`vs_text = font.render("AI (#" + str(self.n_games) + "): " + str(ai_score) + " Player: " + str(player_best) + " " + self.vs_result, True, WHITE)`
3. When playing versus human, the player can have many chances to get high score, but AI has only one chance -> has a high rate of getting low score due to randomness
4. When the player is playing, the size of food is quadrupled(2x2) :stuck_out_tongue:
```
 def place_food(self):
        x = random.randint(0, (self.w - 2*BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE + self.w + BLOCK_SIZE*2
        y = random.randint(0, (self.h - 2*BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        self.food = [Point(x, y), Point(x+BLOCK_SIZE, y), Point(x, y+BLOCK_SIZE), Point(x+BLOCK_SIZE, y+ BLOCK_SIZE)]
        for fd in self.food:
            if(fd in self.snake):
                self.place_food()
                break
```
5. But still, AI can be better(or almost is better) when training num increases
6. Very interesting because you can see the process of reinforcement learning by speeding up the timer(pygame)

## Youtube Video
[Snake RL AI vs Human](https://youtu.be/ZEw18XKcVQQ)
got 100% win rate by luck!

## Referenced open-source
[Snake_Game](https://github.com/patrickloeber/python-fun/tree/master/snake-pygame)
[Snake_Pytorch](https://github.com/patrickloeber/snake-ai-pytorch)

## Notifiable changes that I made
- Combined SnakeGameAI and SnakeGame class and made into a one pygame (was very hard to adjust to pythonic OOP)
- Separated start.py and SnakeGameAI class
- Understanding and adding UI features such as images and texts
- Took a lot of time spending on *Game Loop* and *Timer* (even though I practiced with Unity for 2 years!!)
- Made a complete playable game with ending
- Added one more danger feature(mines)

## Limitations
- Some minor bugs (player snake)
- Studied a lot on deep q-learning but did not make use of it well in the code
- Had an idea of adding new food that gives less reward(but did not have time.. maybe later)
- Wanted to use the matplotlib library as well but the graph appeared in front of the game and made problem when tried to move
- Could have researched more on why the ai snake was stuck and rotating on its own

## Overall
I learned a lot on this project and I hope I will keep on studying computer games and artificial intelligence!

