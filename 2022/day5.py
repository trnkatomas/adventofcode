
stacks = {1:['G', 'F', 'V', 'H', 'P', 'S'],
          2:['G', 'J', 'F', 'B', 'B', 'D', 'Z', 'M'],
          3:['G', 'M', 'L', 'J', 'N'],
          4:['N', 'G', 'Z', 'V', 'D', 'W', 'P'],
          5:['V', 'R', 'C', 'B'],
          6:['V', 'R', 'S', 'M', 'P', 'W', 'L', 'Z'],
          7:['T', 'H', 'P'],
          8:['Q', 'R', 'S', 'N', 'C', 'H', 'Z', 'V'],
          9:['F', 'F', 'G', 'P', 'V', 'Q', 'J']}

stacks_small = {1:['Z', 'N'],
          2:['M', 'C', 'D'],
          3:['P']}

# move 1 from 2 to 1

DEBUG = 0

from copy import deepcopy

def read_moves(fname):
    moves = []
    with open(fname) as infile:
        for line in infile:
            if line.startswith("move "):
                where_to = line[5:].split('from')
                how_many = int(where_to[0])
                stack_from = int(where_to[1].split('to')[0])
                stack_to = int(where_to[1].split('to')[1])
                if DEBUG:
                    print(how_many, stack_from, stack_to)
                moves.append([how_many, stack_from, stack_to])
    return moves

def move_boxes(moves, curent_stacks):
    for move in moves:
        for _ in range(move[0]):
            elem_to_move = curent_stacks[move[1]].pop()
            curent_stacks[move[2]].append(elem_to_move)
            if DEBUG:
                print(f"moving {elem_to_move} from {move[1]} to {move[2]}")
    if DEBUG:
        print(curent_stacks)
    stack_tops = [stack[-1] for stack in curent_stacks.values()]
    if DEBUG:
        print(stack_tops)
    return stack_tops

def move_boxes_9001(moves, current_stacks):
    print(current_stacks)
    for move in moves:
        elems_to_move = []
        for _ in range(move[0]):
            elem_to_move = current_stacks[move[1]].pop()
            elems_to_move.append(elem_to_move)
        current_stacks[move[2]].extend(elems_to_move[::-1])
        if DEBUG:
            print(f"moving {elems_to_move} from {move[1]} to {move[2]}")
    if DEBUG:
        print(current_stacks)
    stack_tops = [stack[-1] for stack in current_stacks.values()]
    if DEBUG:
        print(stack_tops)
    return stack_tops

if __name__ == "__main__":
    current_moves = read_moves("day5.small")
    moves_boxes = move_boxes(current_moves, deepcopy(stacks_small))
    moves_boxes_9001 = move_boxes_9001(current_moves, deepcopy(stacks_small))
    print("".join(moves_boxes))
    print("".join(moves_boxes_9001))

    current_moves = read_moves("day5.input")
    moves_boxes = move_boxes(current_moves, deepcopy(stacks))
    moves_boxes_9001 = move_boxes_9001(current_moves, deepcopy(stacks))
    print("".join(moves_boxes))
    print("".join(moves_boxes_9001))