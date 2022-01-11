import random
from self_drive3 import *
import numpy as np
import pygame

pygame.init() 

def basic_policy(obs):
    keys = pygame.key.get_pressed()
    action = 3
    if keys[pygame.K_w]:
        action = 2
    if keys[pygame.K_a]:
        action = 0
        
    if keys[pygame.K_d]:
        action = 1
    
    
    
    
    return action

totals = []
for episode in range(1):
    episode_rewards = 0
    env_start()
    obs = env_observe()
    for step in range(2000):
        action = basic_policy(obs)
        
        obs, reward, done, info = env_step(action)
        print(reward)
        #episode_rewards += reward
        if done:
            break
        
    totals.append(reward)
print(np.mean(totals), np.std(totals),np.min(totals),np.max(totals),max(totals))