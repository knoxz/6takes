# Settings
import random
from pathlib import Path

import numpy as np
from sb3_contrib import MaskablePPO
from sb3_contrib.common.maskable.policies import MaskableMultiInputActorCriticPolicy
from sb3_contrib.common.wrappers import ActionMasker
from sb3_contrib.common.maskable.evaluation import evaluate_policy
from sb3_contrib.common.envs import InvalidActionEnvDiscrete

import gym
from gym import spaces

import models

debug_print = False
info_print = False

# 6 Nimmt Config
number_of_players = 10
table_piles = 4

# Agent Config
total_timesteps = 150000
n_epochs = 20


def mask_fn(envo: gym.Env) -> np.ndarray:
    return envo.get_action_masks()


class SixthTakes(InvalidActionEnvDiscrete):
    """Custom Environment that follows gym interface"""

    def __init__(self):
        super(SixthTakes, self).__init__()
        # Define action and observation space
        # self.number_of_players = number_of_players
        self.cards = []
        self.players = []
        self.table = models.Table(table_piles)
        self.create_player(number_of_players)
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
                "played_cards": spaces.Box(0, 104, shape=(4 + (number_of_players * 10), 2), dtype=int),
            }
        )

    def get_obs(self):
        pile_array, played_cards_array = self.table.array()
        hand_cards = self.players[0].array()
        return {"hand_cards": hand_cards,
                "piles": pile_array,
                "played_cards": played_cards_array
                }

    def get_action_masks(self):
        # return np.arange(0, len(self.players[0].hand_cards))
        number_of_hand_cards = len(self.players[0].hand_cards)
        possible_actions = []
        for i in range(10):
            if i < number_of_hand_cards:
                possible_actions.append(True)
            else:
                possible_actions.append(False)
        return possible_actions

    def step(self, action):
        round_reward = 0
        round_done = False
        # self.invalid_actions = np.arange(9 - self.round, len(self.players[0].hand_cards))
        valid_card_selected = self.players[0].select_playing_card(action)
        # if valid_card_selected:
        #     self.play_round()
        # else:
        #     self.selected_wrong_card += 1
        #     round_done = True
        #     round_reward = -1000
        if not valid_card_selected:
            print("SHOULD NOT HAPPEN!")
        self.play_round()
        round_reward -= self.players[0].penalty_sum
        # reward -= self.selected_wrong_card * 100
        self.round += 1

        if self.round == 10:
            round_done = True
            if info_print:
                print(f"Round:{self.round} Reward: {round_reward}")

        round_info = {}
        return self.get_obs(), round_reward, round_done, round_info

    def reset(self):
        self.done = False
        self.reward = 0
        self.selected_wrong_card = 0
        self.cards = []
        self.players = []
        self.table = models.Table(table_piles)
        self.create_player(number_of_players)
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
            self.players.append(models.Player(i))

    def reset_playing_cards(self):
        self.cards.clear()
        for i in range(104):
            self.cards.append(models.Card(i + 1))
        if debug_print:
            print(f"Playing Cards: {self.cards}")
        random.shuffle(self.cards)

    def play_round(self):
        if debug_print:
            print(f"Round {self.round}")
        self.table.played_this_round.clear()
        for player in self.players:
            # This is random for now.
            if not player.played:
                player.select_playing_card()
            self.table.played_this_round.append(player.played)
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


if __name__ == "__main__":
    env = SixthTakes()
    env = ActionMasker(env, mask_fn)  # Wrap to enable masking

    # episodes = 1000
    # reward_list = []
    # for episode in range(1, episodes + 1):
    #     state = env.reset()
    #     done = False
    #     score = 0
    #     while not done:
    #         action = env.action_space.sample()
    #         n_state, reward, done, info = env.step(None)
    #         print(f"Episode:{episode} Score:{reward}")
    #     print(f"Episode:{episode} Score:{reward}")
    #     reward_list.append(reward)
    # print(f"Mean reward with {episodes} game is {sum(reward_list) / episodes}")

    from stable_baselines3 import DQN, A2C, PPO

    states = env.observation_space.shape
    env.reset()
    observation = env.get_obs()
    actions = env.action_space.n

    log_path = Path("Training", "Logs")
    log_path.mkdir(parents=True, exist_ok=True)

    # model = DQN("MultiInputPolicy", env, verbose=1, tensorboard_log=log_path)
    model = MaskablePPO(MaskableMultiInputActorCriticPolicy, env, verbose=1, tensorboard_log=log_path,
                        n_epochs=n_epochs)
    model.learn(total_timesteps=total_timesteps, log_interval=4)

    dqn_path = Path("Training", "Models", "Maskable_PPO")

    model.save(dqn_path)

    print("Training done starting eval")

    eval = evaluate_policy(model, env, n_eval_episodes=1000, render=False)
    print(eval)
