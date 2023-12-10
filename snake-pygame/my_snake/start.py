from agent import Agent
from snake_game_ai import SnakeGameAI
from helper import plot



def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        game.update_ui(agent.n_games)
        if game.countdown == 0:
            # get old state
            state_old = agent.get_state(game)

            # get move
            final_move = agent.get_action(state_old)

            # perform move and get new state

            reward, done, score = game.play_step(final_move)
            game_over, p_score, p_best = game.player_play_step()

            state_new = agent.get_state(game)

            # train short memory
            agent.train_short_memory(state_old, final_move, reward, state_new, done)

            # remember
            agent.remember(state_old, final_move, reward, state_new, done)

            if done:
                if agent.n_games in game.round_vs_player:
                    game.show_results(score, p_best)
                # train long memory, plot result
                game.reset()
                agent.n_games += 1
                agent.train_long_memory()

                if score > record:
                    record = score
                    # agent.model.save()

                print('Game', agent.n_games, 'Score', score, 'Record:', record)

                plot_scores.append(score)
                total_score += score
                mean_score = total_score / agent.n_games
                plot_mean_scores.append(mean_score)
                #plot(plot_scores, plot_mean_scores)
            if agent.n_games in game.round_vs_player:    
                if game_over:
                    game.reset_p_snake()
            elif agent.n_games in [add + 1 for add in game.round_vs_player]:
                if game_over:
                    game.reset_p_snake()


            

if __name__ == '__main__':
    agent = Agent()
    train()