#Normal data acquisition function, separates into lines and strips off line characters
def get_data(file):
  data=[]
  with open(file, 'r') as f:
     for line in f:
       data.append(line.rstrip())
  return data

def partone(file):

  #set the number of game tokens we have
  game_tokens = {'blue':14, 'red':12, 'green':13}
  #set the sum of possible games
  game_sum = 0

  for line in file:
    #split off the game index from the instructions for the games
    game_number, game_info = line.split(': ')
    game_number = game_number.split(" ")[1]
    #split the instructions into individual pulls
    instructions = game_info.split(';')

    for inst in instructions:
      #iterated through instructions taking individual tile pulls
      new_inst = inst.split(",")

      for inst1 in new_inst:
        #separate the quantity of tiles from the amount, compare to the number of possible tiles. If the number exceeds possibility, this game is
        #impossible so we excliude it by setting its number to 0.
        inst1 = inst1.strip()
        inst2 = inst1.split(" ")
        inst2[0] = int(inst2[0])

        if inst2[0] > game_tokens[inst2[1]]:
          game_number = 0
    #for valid games, adds it on to the total. For invalid games, just adds 0
    game_sum += int(game_number)

  return game_sum

#print the part one answer
print("Part One Answer: ",partone(get_data("AoC_Day02.input.txt")))

def parttwo(file):

  game_sum = 0

  for line in file:
    #split data like before
    game_number, game_info = line.split(': ')
    game_number = game_number.split(" ")[1]
    instructions = game_info.split(';')
    #now we want to track how many tokens we need.
    game_tokens = {'blue':0, 'red':0, 'green':0}

    for inst in instructions:
      #iterate through pulls like before
      new_inst = inst.split(",")
      
      for inst1 in new_inst:

        inst1 = inst1.strip()
        inst2 = inst1.split(" ")
        inst2[0] = int(inst2[0])
        #check to see if we need additional tiles, if we do, update the number of tiles we need.
        if inst2[0] > game_tokens[inst2[1]]:
          game_tokens[inst2[1]] = inst2[0]

      #once we've processed all pulls, calculate the power given the number of tiles required.
      game_power = game_tokens["blue"]*game_tokens["red"]*game_tokens['green']
    #add to the game sum the power of the game.
    game_sum += game_power

  return game_sum

#print the part two answer
print("Part Two Answer: ", parttwo(get_data("AoC_Day02.input.txt")))