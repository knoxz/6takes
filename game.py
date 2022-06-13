# Settings
from pathlib import Path

from gym.wrappers import FilterObservation, FlattenObservation
from keras import Sequential
from keras.layers import Flatten, Dense, Activation
from stable_baselines3.common.evaluation import evaluate_policy

from game_functions import *

import gym
import numpy as np
from gym import spaces

debug_print = False
info_print = True


class SixthTakes(gym.Env):
    """Custom Environment that follows gym interface"""

    def __init__(self, number_of_players):
        super(SixthTakes, self).__init__()
        # Define action and observation space
        self.number_of_players = number_of_players
        self.cards = []
        self.players = []
        self.table = Table(4)
        self.create_player(self.number_of_players)
        self.round = 0
        self.reward = 0
        self.selected_wrong_card = 0
        self.done = False
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(10)
        # # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Dict(
            {
                "hand_cards": spaces.Box(0, 104, shape=(10, 2), dtype=int),
                "piles": spaces.Box(0, 104, shape=(4, 5, 2), dtype=int),
                "played_cards": spaces.Box(0, 104, shape=(110, 2), dtype=int),
            }
        )

        # self.observation_space = spaces.Tuple((spaces.Box(0, 104, shape=(10, 2), dtype=int),
        #                                        spaces.Box(0, 104, shape=(4, 5, 2), dtype=int),
        #                                        spaces.Box(0, 104, shape=(110, 2), dtype=int),
        #                                        ))
        # self.observation_space = spaces.Box(low=0, high=255,
        #                                     shape=(N_CHANNELS, HEIGHT, WIDTH), dtype=np.uint8)
        # print(self.observation_space.sample())

    def get_obs(self):
        pile_array, played_cards_array = self.table.array()
        return {"hand_cards": self.players[0].array(),
                "piles": pile_array,
                "played_cards": played_cards_array}

    def step(self, action):
        reward = 0
        if not self.players[0].select_playing_card(action):
            reward -= 100
            self.selected_wrong_card += 1
        self.play_round()
        reward -= self.players[0].penalty_sum
        self.round += 1
        if self.round == 10:
            done = True
            if info_print:
                print(f"Final Reward: {reward} // {self.selected_wrong_card}")
        else:
            done = False
        info = {}
        return self.get_obs(), reward, done, info

    def reset(self):
        self.done = False
        self.reward = 0
        self.selected_wrong_card = 0
        self.cards = []
        self.players = []
        self.table = Table(4)
        self.create_player(self.number_of_players)
        self.round = 0
        self.reset_playing_cards()
        for player in self.players:
            for _ in range(10):
                player.hand_cards.append(self.cards.pop())
        self.table.reset_table(self.cards)
        if debug_print:
            print(self.get_obs())
        return self.get_obs()  # reward, done, info can't be included

    def render(self, mode='human'):
        pass

    def close(self):
        pass

    def create_player(self, player_number):
        for i in range(player_number):
            self.players.append(Player(i))

    def reset_playing_cards(self):
        self.cards.clear()
        for i in range(104):
            self.cards.append(Card(i + 1))
        if debug_print:
            print(f"Playing Cards: {self.cards}")
        random.shuffle(self.cards)

    def play_round(self):
        if debug_print:
            print(f"Round {self.round}")
        for player in self.players:
            # This is random for now.
            if not player.played:
                player.select_playing_card()
        sorted_player_list = sorted(self.players, key=lambda player_sort: player_sort.played.number, reverse=True)
        if debug_print:
            print(f"Sorted Player List: {sorted_player_list}")
        if debug_print:
            self.table.print_table()
        for _ in range(len(self.players)):
            playing_player = sorted_player_list.pop()
            if debug_print:
                print(f"Player {playing_player.id} will play Card {playing_player.played} will be played!")
            penalty = self.table.play_card_onto_table(playing_player.played)
            for player in self.players:
                if player.id == playing_player.id:
                    player.played = None
                    player.penalty_sum = player.penalty_sum + penalty
            if debug_print:
                self.table.print_table()


env = SixthTakes(4)
# env = FlattenObservation(env)
# episodes = 10
# for episode in range(1, episodes + 1):
#     state = env.reset()
#     done = False
#     score = 0
#
#     while not done:
#         action = env.action_space.sample()
#         n_state, reward, done, info = env.step(action)
#         score += reward
#     print(f"Episode:{episode} Score:{score}")

# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Flatten
# from tensorflow.keras.optimizers import Adam

from stable_baselines3 import DQN, A2C, PPO

states = env.observation_space.shape
actions = env.action_space.n

log_path = Path("Training", "Logs")
log_path.mkdir(parents=True, exist_ok=True)

# model = DQN("MultiInputPolicy", env, verbose=1, tensorboard_log=log_path)
model = PPO("MultiInputPolicy", env, verbose=1, tensorboard_log=log_path)
model.learn(total_timesteps=150000, log_interval=4)

dqn_path = Path("Training", "Models", "A2C_Takes6")

model.save(dqn_path)

eval = evaluate_policy(model, env, n_eval_episodes=10, render=False)
print(eval)
