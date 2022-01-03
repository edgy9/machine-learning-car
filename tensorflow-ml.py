import random
from self_drive3 import *
import numpy as np
import pygame

def basic_policy(obs):
    keys = pygame.key.get_pressed()
    action = 2
    if keys[pygame.K_a]:
        action = 0
        
    if keys[pygame.K_d]:
        action = 1
        
    if keys[pygame.K_w]:
        action = 2
    
    return action

totals = []
for episode in range(10):
    episode_rewards = 0
    env_start()
    obs = env_observe()
    for step in range(2000):
        action = basic_policy(obs)
        
        obs, reward, done, info = env_step(action)
        print(reward)
        episode_rewards += reward
        if done:
            break
        
    totals.append(episode_rewards)
print(np.mean(totals), np.std(totals),np.min(totals),np.max(totals))