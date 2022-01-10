

import time
import math

from utils_without_gui import blit_rotate_center
import neat
import sys
import os
import random


WIDTH = 1500
HEIGHT = 1000




def draw(car):
    car.draw_rays()
    car.draw()

class Obstacle:
    def __init__(self):
        w, h = WIDTH, HEIGHT
        #self.obsticals = {1:[800,500,1200,800],2:[100,400,700,1000],3:[300,200,500,300]}
        #self.obsticals_rect = {1:[300,200,200,100],2:[800,500,400,300],3:[100,400,600,600]}
        self.obsticals = {}
        self.obsticals_rect = {}
        self.border = [1,1,w-1,h-1]
        self.border_rect = [1,1,w-2,h-2]
        self.goal = [800,200,850,250]
        self.goal_rect = [800,200,50,50]

        
class Car:
    def __init__(self):
        
        self.speed = 2
        self.angle = 270
        self.START_POS = self.get_start_pos()
        #self.START_POS = 100,200
        #print(self.START_POS)
        self.center_x, self.center_y = self.START_POS
        self.is_alive = True
        self.turn_angle = 1
        self.test_ray_len = 1000
        self.intersection = (0,0)
        self.four_points = []
        self.ray_len = 1000
        self.rays = {
            1:{"angle":0,"radians":0,"slope":0,"length":0,"horizontal":0,"vertical":0,"ob_x":0,"ob_y":0,"goal_x":0,"goal_y":0},
            2:{"angle":0,"radians":0,"slope":0,"length":0,"horizontal":0,"vertical":0,"ob_x":0,"ob_y":0,"goal_x":0,"goal_y":0},
            3:{"angle":0,"radians":0,"slope":0,"length":0,"horizontal":0,"vertical":0,"ob_x":0,"ob_y":0,"goal_x":0,"goal_y":0},
            4:{"angle":0,"radians":0,"slope":0,"length":0,"horizontal":0,"vertical":0,"ob_x":0,"ob_y":0,"goal_x":0,"goal_y":0}
            }
        self.dist_goal = 0
        self.goal_angle = 0
        self.rays_show = True
        self.pre_cord = self.START_POS
        self.goal_reached = False
        self.pre_goal_dist = 0 
        self.reward = 0
        self.pre_pos = []
    
    def draw(self):
        self.draw_rays()
        blit_rotate_center(self)


    def get_start_pos(self):
        w, h = WIDTH, HEIGHT
        while True:
            points = [random.randint(50,w-50),random.randint(50,h-50)]
            alive = True                
            for i, obsticals in obstacle.obsticals.items():
                x_range = range(obsticals[0]-50,obsticals[2]+50)
                y_range = range(obsticals[1]-50,obsticals[3]+50)
                if int(points[0]) in x_range and int(points[1]) in y_range:   
                    alive = False
            if alive:
                return (int(points[0]),int(points[1]))

        
        
        
        
    def rotate(self, left=False, right=False):
        if left:
            if self.angle == 360: self.angle = 0
            self.angle += self.turn_angle
        elif right:
            if self.angle == 0: self.angle = 360
            self.angle -= self.turn_angle
        
       
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.speed
        horizontal = math.sin(radians) * self.speed
        #print("moving")
        self.center_y -= vertical
        self.center_x -= horizontal
        
        
    
    def check_if_ray_is_infront_of_car(self,point_x,point_y):
        angle_of_car = self.angle
        angle_of_car_line = angle_of_car + 270
        radians_of_car_line = math.radians(angle_of_car_line)
        vertical = math.cos(radians_of_car_line)*self.test_ray_len
        horizontal = math.sin(radians_of_car_line)*self.test_ray_len
        if vertical == 0 or horizontal == 0: vertical, horizontal = 0.0001,0.0001
        Ax,Ay = ((self.center_x - horizontal),(self.center_y - vertical))
        Bx,By = ((self.center_x + horizontal),(self.center_y + vertical))
        position = math.copysign(1,((Bx - Ax) * (point_y - Ay) - (By - Ay) * (point_x - Ax)))
        if position == 1.0: return True
        return 
        
    def find_ray_nearest_obstacle(self,horizontal,vertical,id):
        if horizontal == 0: return
        if vertical == 0: return
        #sets nearest obstacle and goal to cords 0,0
        self.rays[id]["ob_x"] = 0
        self.rays[id]["ob_y"] = 0
        self.rays[id]["goal_x"] = 0
        self.rays[id]["goal_y"] = 0
        #find slope of current ray
        slope = (vertical/horizontal)
        #finds y intercept
        c = self.center_y - slope * self.center_x   

        #set the closest line to ray length
        #this will stop any lines longer from being found
        closest_line = self.ray_len
        #iterates through the list of obstacles
        for index in obstacle.obsticals:
            cords = obstacle.obsticals[index]
            #print(cords)

            #finds the four sides of the current obstacle
            lines = []
            line1 = [cords[0],cords[1],cords[2],cords[1]]
            line2 = [cords[2],cords[1],cords[2],cords[3]]
            line3 = [cords[0],cords[3],cords[2],cords[3]]
            line4 = [cords[0],cords[1],cords[0],cords[3]]
            lines.append(line1)
            lines.append(line2)
            lines.append(line3)
            lines.append(line4)
            
            #iterates through sides of obstacle
            for line in lines:
                x1, y1, x2, y2 = line
                 
                if x1 == x2:        #if line vertical
                    y = slope*x1+c  #find y cord where ray intercepts side of obstacle
                    if y > y1 and y < y2:   #if y is between the two furthest points of side
                        if self.check_if_ray_is_infront_of_car(x1,y):
                            length = math.sqrt(((x1-self.center_x)**2)+((y-self.center_y)**2))
                            if length < closest_line:   #if is the closest line
                                closest_line = length
                                self.rays[id]["ob_x"] = x1
                                self.rays[id]["ob_y"] = y
                                self.rays[id]["length"] = closest_line

                if y1==y2:
                    x = (y1-c) / slope
                    if x > x1 and x < x2:
                        if self.check_if_ray_is_infront_of_car(x,y1):
                            length = math.sqrt(((x - self.center_x)**2)+((y1 - self.center_y)**2))
                            if length < closest_line:
                                closest_line = length
                                self.rays[id]["ob_x"] = x
                                self.rays[id]["ob_y"] = y1
                                self.rays[id]["length"] = closest_line
        
        cords = obstacle.border
        #print(cords)       [0,0,1500,1500]
        lines = []
        line1 = [cords[0],cords[1],cords[2],cords[1]]
        line2 = [cords[2],cords[1],cords[2],cords[3]]
        line3 = [cords[0],cords[3],cords[2],cords[3]]
        line4 = [cords[0],cords[1],cords[0],cords[3]]
        lines.append(line1)
        lines.append(line2)
        lines.append(line3)
        lines.append(line4)
        
        
        for line in lines:
            x1, y1, x2, y2 = line
            if x1 == x2:
                y = slope*x1+c
                if y > y1 and y < y2:
                    if self.check_if_ray_is_infront_of_car(x1,y):
                        length = math.sqrt(((x1-self.center_x)**2)+((y-self.center_y)**2))
                        if length < closest_line:
                                closest_line = length
                                self.rays[id]["ob_x"] = x1
                                self.rays[id]["ob_y"] = y
                                self.rays[id]["length"] = closest_line
                        
            if y1==y2:
                x = (y1-c) / slope
                if x > x1 and x < x2:
                    if self.check_if_ray_is_infront_of_car(x,y1):
                        length = math.sqrt(((x - self.center_x)**2)+((y1 - self.center_y)**2))
                        if length < closest_line:
                                closest_line = length
                                self.rays[id]["ob_x"] = x
                                self.rays[id]["ob_y"] = y1
                                self.rays[id]["length"] = closest_line
    def draw_rays(self):
        
        self.rays[1]["angle"] = self.angle+120
        self.rays[1]["radians"] = math.radians(self.rays[1]["angle"])
        self.rays[1]["vertical"] = math.cos(self.rays[1]["radians"]) * self.ray_len
        self.rays[1]["horizontal"] = math.sin(self.rays[1]["radians"]) * self.ray_len
        self.find_ray_nearest_obstacle((self.rays[1]["horizontal"]),(self.rays[1]["vertical"]),1)
        
        
        self.rays[2]["angle"] = self.angle+160
        self.rays[2]["radians"] = math.radians(self.rays[2]["angle"])
        self.rays[2]["vertical"] = math.cos(self.rays[2]["radians"]) * self.ray_len
        self.rays[2]["horizontal"] = math.sin(self.rays[2]["radians"]) * self.ray_len
        self.find_ray_nearest_obstacle((self.rays[2]["horizontal"]),(self.rays[2]["vertical"]),2)

        self.rays[3]["angle"] = self.angle+200
        self.rays[3]["radians"] = math.radians(self.rays[3]["angle"])
        self.rays[3]["vertical"] = math.cos(self.rays[3]["radians"]) * self.ray_len
        self.rays[3]["horizontal"] = math.sin(self.rays[3]["radians"]) * self.ray_len
        self.find_ray_nearest_obstacle((self.rays[3]["horizontal"]),(self.rays[3]["vertical"]),3)

        self.rays[4]["angle"] = self.angle+240
        self.rays[4]["radians"] = math.radians(self.rays[4]["angle"])
        self.rays[4]["vertical"] = math.cos(self.rays[4]["radians"]) * self.ray_len
        self.rays[4]["horizontal"] = math.sin(self.rays[4]["radians"]) * self.ray_len
        self.find_ray_nearest_obstacle((self.rays[4]["horizontal"]),(self.rays[4]["vertical"]),4)

    def find_goal_angle_and_distance(self):
        goal_rect = obstacle.goal_rect
        car = [self.center_x, self.center_y]
        
        #find center of goal
        goal = [goal_rect[0] + (goal_rect[2]/2), goal_rect[1] + (goal_rect[3]/2)]

        #find distance between goal and car
        x1, y1 = car
        x2, y2 = goal
        length = math.sqrt(((x2-x1)**2)+((y2-y1)**2))

        a = (y1-y2)
        b = (x1-x2)
        if a == 0 or b == 0: return
        angle = math.degrees(math.atan(a/b))


        ver_angle = 90 + angle
        angle_to_car = ver_angle + self.angle
        if x1 > x2: angle_to_car += 180
        if angle_to_car > 359: angle_to_car -= 360
        angle_to_car = abs(angle_to_car)
        
        self.dist_goal = length
        self.goal_angle = angle_to_car
        #print(angle_to_car,length)


    def check_collision(self):
        self.is_alive = True
        for points in self.four_points:
            
            for i, obsticals in obstacle.obsticals.items():
                x_range = range(obsticals[0],obsticals[2])
                y_range = range(obsticals[1],obsticals[3])
                if int(points[0]) in x_range and int(points[1]) in y_range: 
                    #print("collided")
                    self.is_alive = False
                    break
            x_range = range(obstacle.goal[0],obstacle.goal[2])
            y_range = range(obstacle.goal[1],obstacle.goal[3])
            if int(points[0]) in x_range and int(points[1]) in y_range: 
                #print("goal reached")
                self.is_alive = False
                self.goal_reached = True
                break
            x_range = range(obstacle.border[0],obstacle.border[2])
            y_range = range(obstacle.border[1],obstacle.border[3])
            if int(points[0]) not in x_range or int(points[1]) not in y_range:
                #print("outside border")
                self.is_alive = False
                break
       
        

    def get_data(self):
        values = [0, 0, 0, 0, 0]
        for i in range(0,4):
            values[i] = int(self.rays[i+1]["length"])
        values[4] = round(self.goal_angle)
        #values[5] = self.angle
        #values[5] = round(self.dist_goal)
        #print(values)
        return values
    
    def check_alive(self):
        return self.is_alive
    
    def get_reward(self):
        self.reward = 1
        if self.goal_reached: self.is_alive = False; return 1000000 #if goal reached big reward
        if self.is_alive == False: return 0

        self.reward -= 0.1 # penalty for every step to reduce time
        if self.pre_goal_dist > self.dist_goal: #if closer big reward
            self.reward += 1
        if self.pre_goal_dist <= self.dist_goal:   #if further negitive reward
            self.reward -= 1
        if (self.center_x,self.center_y) in self.pre_pos: 
            self.reward -= 5
        self.pre_goal_dist = self.dist_goal
        self.pre_pos.append((self.center_x,self.center_y))
        if self.angle == int(self.goal_angle):
            self.reward += 2
        
        return self.reward
    
    def update(self):
        #print(self.center_x,self.center_y)
        #self.move()
        pass
    
        
    







def env_start():
    global car,obstacle

    obstacle = Obstacle()
    car = Car()
    #while True:
        #step(random.randint(-1,1))

def env_observe():
    return car.get_data()

def env_step(action):
        
    draw(car)

    if action == 0:
        car.rotate(left=True)
    if action == 1:
        car.rotate(right=True)
    if action == 2:
        car.move()

    car.check_collision()
    car.find_goal_angle_and_distance()
    
    info = {}
    #print(reward)
    done = False
    if car.is_alive == False:
        done = True
    return_data = (car.get_data(), car.get_reward(), done,info)
    return return_data

class Car_Sim_with_GUI:
    def start():
        env_start
    def step(action):
        env_step(action)
    def observe():
        env_observe()
#env_start()