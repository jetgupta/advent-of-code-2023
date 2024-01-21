from collections import defaultdict
from collections import deque


class GearRatioFinder:
    def __init__(self, schematic_lines):
        self.schematic_lines = schematic_lines
        self.processed_numbers = defaultdict(set)

    def __find_full_number(self, asterisk_location, row, col):
        full_number = deque([self.schematic_lines[row][col]])
        self.processed_numbers[asterisk_location].add((row, col))

        ptr = col - 1
        while (
            self.__isValidCol(row, ptr) and self.schematic_lines[row][ptr].isnumeric()
        ):
            full_number.appendleft(self.schematic_lines[row][ptr])
            self.processed_numbers[asterisk_location].add((row, ptr))
            ptr -= 1

        ptr = col + 1
        while (
            self.__isValidCol(row, ptr) and self.schematic_lines[row][ptr].isnumeric()
        ):
            full_number.append(self.schematic_lines[row][ptr])
            self.processed_numbers[asterisk_location].add((row, ptr))
            ptr += 1

        return int("".join(full_number))

    def __isValidCol(self, row, col):
        return 0 <= col < len(self.schematic_lines[row])

    def __isValidRow(self, row):
        return 0 <= row < len(self.schematic_lines)

    def __find_gear_ratio(self, curr_line, char_index):
        part_number_count = 0
        part_number_product = 1
        asterisk_location = (curr_line, char_index)

        for adjacent_row in range(curr_line - 1, curr_line + 2):
            for adjacent_col in range(char_index - 1, char_index + 2):
                if self.__isValidRow(adjacent_row) and self.__isValidCol(
                    adjacent_row, adjacent_col
                ):
                    adjacent_char = self.schematic_lines[adjacent_row][adjacent_col]

                    if (
                        adjacent_char.isnumeric()
                        and (adjacent_row, adjacent_col)
                        not in self.processed_numbers[asterisk_location]
                    ):
                        part_number = self.__find_full_number(
                            asterisk_location, adjacent_row, adjacent_col
                        )
                        part_number_count += 1

                        if part_number_count > 2:
                            del self.processed_numbers[asterisk_location]
                            return False, -1

                        part_number_product *= part_number

        del self.processed_numbers[asterisk_location]
        if part_number_count == 2:
            return True, part_number_product
        else:
            return False, -2

    def __find_line_total(self, curr_line, adjacent_rows):
        line_total = 0
        for char_index, char in enumerate(self.schematic_lines[curr_line]):
            if char == "*":
                isGear, gear_ratio = self.__find_gear_ratio(curr_line, char_index)
                if isGear:
                    line_total += gear_ratio

        return line_total

    def find_gear_ratio_total(self):
        total = 0
        num_lines = len(self.schematic_lines)

        for index in range(num_lines):
            adjacent_rows = []
            middle_row = 0 < index < num_lines - 1

            if index == 0 or middle_row:
                adjacent_rows.append(index + 1)

            if index == num_lines - 1 or middle_row:
                adjacent_rows.append(index - 1)
            total += self.__find_line_total(index, adjacent_rows)

        return total


def test_sum_of_gear_ratios():
    engine_schematic = """...100...7*8.\n.*..*......6.\n..4..7......."""
    engine_schematic = engine_schematic.split("\n")
    ratio_finder = GearRatioFinder(engine_schematic)
    gear_ratio_sum = ratio_finder.find_gear_ratio_total()
    assert gear_ratio_sum == 700, f"sum of gear ratios is {gear_ratio_sum}"
    print("All tests passed successfully!")


def main():
    input_filename = "/input_day_3.txt"
    with open(input_filename, "r") as file:
        schematic = file.read()
        schematic_lines = schematic.split("\n")[:-1]

    ratio_finder = GearRatioFinder(schematic_lines)
    gear_ratio = ratio_finder.find_gear_ratio_total()
    print(f"Gear Ratio is: {gear_ratio}")


if __name__ == "__main__":
    main()
