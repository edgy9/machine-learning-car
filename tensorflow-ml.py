import random
from self_drive3 import *
import numpy as np

def basic_policy(obs):
    return random.randint(-1,1)

totals = []
for episode in range(10):
    episode_rewards = 0
    env_start()
    obs = env_observe()
    for step in range(2000):
        action = basic_policy(obs)
        obs, reward, done, info = env_step(action)
        episode_rewards += reward
        if done:
            break
        
    totals.append(episode_rewards)
print(np.mean(totals), np.std(totals),np.min(totals),np.max(totals))