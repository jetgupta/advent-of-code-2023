from collections import defaultdict
from math import pow


class Card:
    def __init__(self, definition_string) -> None:
        self.winning_numbers, self.card_numbers = None, None
        self.__create_card(definition_string)

    def __create_card(self, definition_string):
        index_numbers_list = definition_string.split(":")
        numbers_string = index_numbers_list[1]

        winning_numbers_string, card_numbers_string = numbers_string.split("|")
        self.winning_numbers = set(
            [int(number) for number in winning_numbers_string.split()]
        )
        self.card_numbers = set([int(number) for number in card_numbers_string.split()])

    def __str__(self):
        return f"Card object - winnning numbers: {self.winning_numbers}, card numbers: {self.card_numbers}"


class CardPointCalculator:
    def __init__(self, raw_lines) -> None:
        self.cards = [Card(line) for line in raw_lines.split("\n")[:-1]]
        self.card_counts = {index: 1 for index in range(len(self.cards))}

    def calculate_deck_total(self) -> int:
        total = 0

        for index in range(len(self.cards)):
            total += self.__calculate_card_points(index)

        return total

    def calculate_total_cards_won(self):
        total = len(self.cards)
        for index in range(len(self.cards)):
            matching_numbers = self.__calculate_matching_numbers(index)

            for number in range(1, matching_numbers + 1):
                won_card = index + number
                self.card_counts[won_card] += self.card_counts[index]
                total += self.card_counts[index]

        return total

    def __calculate_matching_numbers(self, card_index) -> int:
        card = self.cards[card_index]

        matching_numbers = 0
        for card_number in card.card_numbers:
            if card_number in card.winning_numbers:
                matching_numbers += 1

        return matching_numbers

    def __calculate_card_points(self, card_index) -> int:
        raw_points = self.__calculate_matching_numbers(card_index)

        if raw_points > 0:
            return int(pow(2, raw_points - 1))
        else:
            return 0


def test_card_aggregation():
    test_case = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
    calculator = CardPointCalculator(test_case)
    cards_won = calculator.calculate_total_cards_won()
    assert cards_won == 30
    print(f"tests passed, {cards_won} cards won")


def main():
    filename = "day4/input_day_4.txt"
    with open(filename, "r") as file:
        raw_lines = file.read()

    calculator = CardPointCalculator(raw_lines)
    # print(calculator.calculate_deck_total())
    print(calculator.calculate_total_cards_won())


if __name__ == "__main__":
    # test_card_aggregation()
    main()
