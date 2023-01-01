import logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

def load_data():
    with open("input/day_10.txt") as f:
        data = f.read().split('\n')
        return data

def should_draw(pixel, x):
    return abs(x-pixel%40)<=1

if __name__ == '__main__':
    data = load_data()

    signal_strengths = [0]
    x = 1
    cycle_number = 1
    x_values = [x]

    for instruction in data:
        if instruction.startswith('addx'):
            signal_strengths.append(x * cycle_number)
            logger.info(f'{cycle_number:3} - {x:3} - ({cycle_number*x:4})  --  ')
            cycle_number += 1
            delta_x = int(instruction.split(' ')[1])
        elif instruction.startswith('noop'):
            delta_x = 0
            
        signal_strengths.append(x * cycle_number)
        logger.info(f'{cycle_number:3} - {x:3} - ({cycle_number*x:4})  --  {instruction}')
        x += delta_x
        cycle_number += 1
    
    interesting = [signal_strengths[i] for i in range(20, len(signal_strengths), 40)]
    print(f'part 1 sum of interesting numbers: {sum(interesting)}\n')

    # Part 2:

    x_values = [int(signal_strength/i) if i != 0 else 1 for i, signal_strength in enumerate(signal_strengths)][1:]
    line_breaks = [c for c in range(39, len(x_values), 40)]

    for pixel, x in enumerate(x_values):
        cycle = pixel + 1
        
        if should_draw(pixel, x):
            print('#', end='')
        else:
            print('.', end='')
        
        if pixel in line_breaks:
            print('\n', end='')

    print('')
    print('I see PAPJCBHP above --^')
        

