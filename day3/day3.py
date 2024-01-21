

def parse_line(line, adjacent_rows):
    line_total = 0
    index = 0
    while index < len(line):
        curr_num = line[index]
        
        if curr_num.isnumeric():
            #build full number
            num_length = 1
            while line[index + num_length].isnumeric() and 0 <= index + num_length < len(line) :
                curr_num += line[index + num_length]
                num_length += 1
                
            #search four sides for symbol
            added = False
            
            adjacent_rows.append(line)
            for row in adjacent_rows:
                for col in range(index - 1, index + num_length + 1):

                    #if char is a symbol
                    if 0 <= col < len(row) and not(row[col].isnumeric() or row[col] == '.' or row[col] == '\n'):
                        line_total += int(curr_num)
                        added = True
                        break
                if added:
                    break

            index += num_length
                     
        else:
            index += 1

    return line_total

if __name__ == "__main__":
    file_path = "./input_day_3.txt"
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

        total = 0

        num_lines  = len(lines)
        
        for index in range(num_lines):
            adjacent_rows = []
            middle_row = 0 < index < num_lines - 1

            if index == 0 or middle_row:
                adjacent_rows.append(lines[index + 1])

            if index == num_lines - 1 or middle_row:
                adjacent_rows.append(lines[index - 1])
            total += parse_line(lines[index], adjacent_rows)
        
    print(total)
    

