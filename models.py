import random

import numpy as np

from without_masking import number_of_players


class Card:
    def __init__(self, number):
        self.number = number
        if number == 55:
            self.value = 7
        elif number % 11 == 0:
            self.value = 5
        elif number % 10 == 0:
            self.value = 3
        elif number % 5 == 0:
            self.value = 2
        else:
            self.value = 1

    def __repr__(self):
        return f"<Card Number: {self.number} , Value: {self.value}>"

    def compare(self, card):
        if self.number > card.number:
            return 1
        else:
            return -1

    def array(self):
        return np.array([self.number, self.value])


class Table:
    def __init__(self, slots):
        self.slots = slots
        self.table_slots = []
        self.played_cards = []
        self.played_this_round = []
        for _ in range(slots):
            self.table_slots.append([])

    def array(self):
        table_piles_array = np.zeros((4, 5, 2))
        for i in range(len(self.table_slots)):
            for y in range(5):
                if y < len(self.table_slots[i]):
                    table_piles_array[i][y][0] = self.table_slots[i][y].number
                    table_piles_array[i][y][1] = self.table_slots[i][y].value
        played_cards_array = np.zeros((4 + (10 * number_of_players), 2))
        for i in range(len(self.played_cards)):
            played_cards_array[i][0] = self.played_cards[i].number
            played_cards_array[i][1] = self.played_cards[i].value
        # played_this_round = np.zeros((number_of_players, 2))
        # for i in range(len(self.played_this_round)):
        #     played_this_round[i][0] = self.played_this_round[i].number
        #     played_this_round[i][1] = self.played_this_round[i].value
        # return table_piles_array, played_cards_array, played_this_round
        return table_piles_array, played_cards_array

    def print_table(self):
        for idx, table_slot in enumerate(self.table_slots):
            print(f"Table {idx}({len(table_slot)}): {table_slot}")

    def reset_table(self, cards):
        for table_slot in self.table_slots:
            table_slot.clear()
            popped_card = cards.pop()
            self.played_cards.append(popped_card)
            table_slot.append(popped_card)

    def play_card_onto_table(self, card):
        self.played_cards.append(card)
        tableslot_to_play_on = -1
        distance = 105
        for idx, table_slot in enumerate(self.table_slots):
            if card.number > table_slot[-1].number and distance > (card.number - table_slot[-1].number):
                tableslot_to_play_on = idx
                distance = card.number - table_slot[-1].number
        from without_masking import debug_print
        if debug_print:
            print(f"Playing Card: {card} on Table: {tableslot_to_play_on} with distance {distance}")
        if tableslot_to_play_on == -1:
            table_to_replace = -1
            lowest_value = 99
            for idx, table_slot in enumerate(self.table_slots):
                value_sum = 0
                for table_card in table_slot:
                    value_sum = value_sum + table_card.value
                if value_sum < lowest_value:
                    table_to_replace = idx
                    lowest_value = value_sum
            if debug_print:
                print(
                    f"Replacing Table {table_to_replace}: {self.table_slots[table_to_replace]} and receiving penalty of: {lowest_value}")
            self.table_slots[table_to_replace].clear()
            self.table_slots[table_to_replace].append(card)
            return lowest_value, table_to_replace, True
        else:
            if len(self.table_slots[tableslot_to_play_on]) == 5:
                value_sum = 0
                for table_card in self.table_slots[tableslot_to_play_on]:
                    value_sum = value_sum + table_card.value
                if debug_print:
                    print(
                        f"Replacing Table {tableslot_to_play_on}: {self.table_slots[tableslot_to_play_on]} and receiving penalty of: {value_sum}")
                self.table_slots[tableslot_to_play_on].clear()
                self.table_slots[tableslot_to_play_on].append(card)
                return value_sum, tableslot_to_play_on, True
            else:
                self.table_slots[tableslot_to_play_on].append(card)
                return 0, tableslot_to_play_on, False


class Player:
    def __init__(self, id):
        self.id = id
        self.hand_cards = []
        self.played_card_index = 0
        self.played = None
        self.penalty_cards = []
        self.penalty_sum = 0

    def array(self):
        array = np.zeros((10, 2))
        for i in range(len(self.hand_cards)):
            array[i][0] = self.hand_cards[i].number
            array[i][1] = self.hand_cards[i].value
        # return array, self.played_card_index
        return array

    def select_playing_card(self, played_card_index=None):
        if played_card_index is None:
            self.played_card_index = 0
            self.played = self.hand_cards.pop(random.randrange(len(self.hand_cards)))
            return True
        self.played_card_index = played_card_index
        if played_card_index >= len(self.hand_cards):
            # print(f"Selected out of bounce Card: {played_card_index} // {self.hand_cards}")
            self.played = self.hand_cards.pop(random.randrange(len(self.hand_cards)))
            return False
        self.played = self.hand_cards.pop(played_card_index)
        return True

    def __repr__(self):
        return f"<Player {self.id} Penalty_sum: {self.penalty_sum} Playing Card: {self.played}>"
