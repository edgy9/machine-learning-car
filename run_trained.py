
import os
import pickle

import neat
from self_drive3 import *

steps = 2000
# load the winner
with open('winner-feedforward.pkl', 'rb') as f:
    c = pickle.load(f)

print('Loaded genome:')
print(c)

# Load the config file, which is assumed to live in
# the same directory as this script.
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config-feedforward')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)

net = neat.nn.FeedForwardNetwork.create(c, config)

env_start()

obs = env_observe()
for step in range(steps):
    inputs = obs
    action = net.activate(inputs)
    action = action.index(max(action))

    obs, reward, done, info = env_step(action)

    if done:
        break