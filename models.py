import random


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


class Table:

    def __init__(self, slots):
        self.table_slots = []
        for _ in range(slots):
            self.table_slots.append([])

    def print_table(self):
        for idx, table_slot in enumerate(self.table_slots):
            print(f"Table {idx}({len(table_slot)}): {table_slot}")

    def reset_table(self, cards):
        for table_slot in self.table_slots:
            table_slot.clear()
            table_slot.append(cards.pop())

    def play_card_onto_table(self, card):
        tableslot_to_play_on = -1
        distance = 105
        for idx, table_slot in enumerate(self.table_slots):
            if card.number > table_slot[-1].number and distance > (card.number - table_slot[-1].number):
                tableslot_to_play_on = idx
                distance = card.number - table_slot[-1].number
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
            print(
                f"Replacing Table {table_to_replace}: {self.table_slots[table_to_replace]} and receiving penalty of: {lowest_value}")
            self.table_slots[table_to_replace].clear()
            self.table_slots[table_to_replace].append(card)
            return lowest_value
        else:
            if len(self.table_slots[tableslot_to_play_on]) == 5:
                value_sum = 0
                for table_card in self.table_slots[tableslot_to_play_on]:
                    value_sum = value_sum + table_card.value
                print(
                    f"Replacing Table {tableslot_to_play_on}: {self.table_slots[tableslot_to_play_on]} and receiving penalty of: {value_sum}")
                self.table_slots[tableslot_to_play_on].clear()
                self.table_slots[tableslot_to_play_on].append(card)
                return value_sum
            else:
                self.table_slots[tableslot_to_play_on].append(card)
                return 0


class Player:
    def __init__(self, id):
        self.id = id
        self.hand_cards = []
        self.played = None
        self.penalty_cards = []
        self.penalty_sum = 0

    def select_playing_card(self):
        self.played = self.hand_cards.pop(random.randrange(len(self.hand_cards)))

    def __repr__(self):
        return f"<Player {self.id} Penalty_sum: {self.penalty_sum} Playing Card: {self.played}>"
