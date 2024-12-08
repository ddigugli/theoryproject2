# drew diguglielmo
# proj 3 - ntm behavior


# import libraries
import csv
from collections import deque

# simulate the behavior ntm
def ntm(machinefile, inputstr, stepmax=float('inf')):
    # read machine config from inputted file
    with open(machinefile, 'r') as file:
        reader = csv.reader(file)
        lines = [line for line in reader]

    # extract relevant info from the leading lines
    name = lines[0][0]
    start = lines[4][0]
    acc = lines[5][0]
    rej = lines[6][0]
    transitions = lines[7:]

    # set up initial config of NTM
    initconfig = {
        'state': start,
        'tape': list(inputstr),
        'head_position': 0
    }

    # initialize a queue for bfs
    queue = deque([(initconfig, 0)])  # queue of config, depth
    stepcnt = 0  # variable keep track number of steps

    # open output file, write input str
    outfile = open(f"{name}.txt", 'a')
    outfile.write(f"\nMachine name: {name}\n")
    outfile.write(f"Initial String: {inputstr}\n")

    # main loop
    while queue:
        currconfig, depth = queue.popleft()  # get the config and depth
        stepcnt += 1  # increment the count (number steps)

        # check if machine has reached an accept
        if currconfig['state'] == acc:
            outfile.write(f"{''.join(currconfig['tape'])}{acc}")
            outfile.write(f"\nDepth: {depth}\nString accepted in {stepcnt} steps (execution time)\n")
            return 

        # check if at max steps
        if stepcnt > stepmax:
            depth = depth - 1
            outfile.write(f"\nExecution stopped after reaching the {stepmax} step limit\n")
            return

        # get next poss config based on current state and symbol
        nextconfigs = getnextconfig(currconfig, transitions, outfile)
        
        # add next config to queue, explore further
        for nextconfig in nextconfigs:
            queue.append((nextconfig, depth + 1))

    # if no accept state within limit, print reject info
    outfile.write(f"{''.join(currconfig['tape'])}{rej}")
    outfile.write(f"\nDepth: {depth}\nString rejected in {stepcnt} steps (execution time)\n")

# func to get next possible configs based on curr state and symbol
def getnextconfig(currconfig, transitions, outfile):
    # list to st next poss configs
    nextconfigs = []  

    # for each transition rule
    for transition in transitions:
        state, tapechar, nextstate, writec, movedir = transition

        # check if transition rule apploes to curr config
        if (
            state == currconfig['state'] and
            currconfig['head_position'] < len(currconfig['tape']) and
            tapechar == currconfig['tape'][currconfig['head_position']]
        ):
            # create new config based on transition rule
            newconfig = {
                'state': nextstate,
                'tape': currconfig['tape'][:],
                'head_position': currconfig['head_position']
            }

            # update tape, (according to rule)
            newconfig['tape'][currconfig['head_position']] = writec

            # move head based on rule
            if movedir == 'L':
                newconfig['head_position'] -= 1
            elif movedir == 'R':
                newconfig['head_position'] += 1
            elif movedir == '_': # if move direction is '_', head remains
                pass

            # add new config to list
            nextconfigs.append(newconfig)
            
            # print tape config path for visual
            printconfig(currconfig, outfile)

    return nextconfigs

# func to print tape config path to visualize
def printconfig(currconfig, outfile):
    print_tape = currconfig['tape'][:]
    print_tape[currconfig['head_position']] = f"[{currconfig['state']}]"
    print_tape = ''.join(print_tape)
    outfile.write(print_tape + "\n")
    #print(print_tape)

# main func, gets input file and starts tracing process
def main():
    continue_flag = True
    machinefile = input("Enter input file name: ")
    inputstr = input("Enter the input string: ")
    stepmax = 1000
    while(continue_flag):
        ntm(machinefile, inputstr, stepmax)
        continue_input = input("Continue? (y/n): ")
        if (continue_input == 'y'):
            inputstr = input("Enter the input string: ")
        else:
            continue_flag = False

if __name__ == "__main__":
    main()
