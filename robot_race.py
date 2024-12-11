import robot_race_functions as rr
from collections import deque, Counter, namedtuple
from time import time, sleep

maze_file_name = 'maze_data_1.csv'
seconds_between_turns = 0.3
max_turns = 35

# Initialize the robot race
maze_data = rr.read_maze(maze_file_name)
rr.print_maze(maze_data)
walls, goal, bots = rr.process_maze_init(maze_data)

# Populate a deque of all robot commands for the provided maze
robot_moves = deque()
num_of_turns = 0

# Iterate through every bot that has not finished the race
while not rr.is_race_over(bots) and num_of_turns < max_turns:
    for bot in bots:
        if not bot.has_finished:
            # Calculate the robot's next move using compute_robot_logic
            robot_name, action, has_collided = rr.compute_robot_logic(walls, goal, bot)
            # Append the robot's decision to robot_moves
            robot_moves.append((robot_name, action, has_collided))
    num_of_turns += 1

# Count the number of moves based on the robot names
move_counts = Counter(move[0] for move in robot_moves)

# Count the number of collisions by robot name
collision_counts = Counter(move[0] for move in robot_moves if move[2])

# Create a namedtuple to keep track of our robots' points
BotScoreData = namedtuple('BotScoreData', ['name', 'num_moves', 'num_collisions', 'score'])

# Calculate the scores (moves + collisions) for each robot and append it to bot_scores 
bot_scores = []
for bot in bots:
    num_moves = move_counts[bot.name]
    num_collisions = collision_counts[bot.name]
    score = num_moves + num_collisions
    bot_scores.append(BotScoreData(bot.name, num_moves, num_collisions, score))

# Populate a dict to keep track of the robot movements
bot_data = {bot.name: bot for bot in bots}

# Move the robots and update the map based on the moves deque
while len(robot_moves) > 0:
    robot_name, action, _ = robot_moves.popleft()
    bot = bot_data[robot_name]
    bot.process_move(action)

    # Update the maze characters based on the robot positions and print it to the console
    rr.update_maze_characters(maze_data, bots)
    rr.print_maze(maze_data)
    sleep(seconds_between_turns - time() % seconds_between_turns)

# Print out the results!
rr.print_results(bot_scores)
