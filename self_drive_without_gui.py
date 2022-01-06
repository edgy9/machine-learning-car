

import time
import math
from utils_without_gui import  blit_rotate_center
import neat
import sys
import os
import random






def draw(WINDOW, images, car):
    for img, pos in images:
        WINDOW.blit(img, pos)
    
    car.draw(WINDOW)
    obstacle.draw(WINDOW)
    car.draw_rays()
    #print(car.get_reward())
   

class Obstacle:
    def __init__(self):
        self.obsticals = {1:[800,500,1200,800],2:[100,400,700,1000],3:[300,200,500,300]}
        self.obsticals_rect = {1:[300,200,200,100],2:[800,500,400,300],3:[100,400,600,600],4:[0,0,1300,1300]}
        self.border = [0,0,1500,1500]
        self.goal = [800,200,850,250]
        self.goal_rect = [800,200,50,50]

    def draw(self,WINDOW):
        
        pass
class Car:
    def __init__(self):
        
        self.speed = 2
        self.angle = 270
        
        self.START_POS = (180, 200)
        self.x, self.y = self.START_POS
        self.is_alive = True
        self.center_x = 0
        self.center_y = 0
        self.turn_angle = 2
        self.test_ray_len = 1000
        self.intersection = (0,0)
        self.four_points = []
        self.ray_len = 100
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
    
    def draw(self, WINDOW):
        self.draw_rays()
        blit_rotate_center(WINDOW, self.img, (self.x, self.y), self.angle,self,obstacle)
        
        
        
        
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
        self.y -= vertical
        self.x -= horizontal
        
        
    
    def check_if_ray_is_infront_of_car(self,point_x,point_y):
        angle_of_car = self.angle
        angle_of_car_line = angle_of_car + 270
        radians_of_car_line = math.radians(angle_of_car_line)
        vertical = math.cos(radians_of_car_line)*self.test_ray_len
        horizontal = math.sin(radians_of_car_line)*self.test_ray_len
        if vertical == 0 or horizontal == 0: return
        Ax,Ay = ((self.center_x - horizontal),(self.center_y - vertical))
        Bx,By = ((self.center_x + horizontal),(self.center_y + vertical))
        position = math.copysign(1,((Bx - Ax) * (point_y - Ay) - (By - Ay) * (point_x - Ax)))
        if position == 1.0: return True
        return 
        
    def find_ray(self,horizontal,vertical,id):
        if horizontal == 0: return
        if vertical == 0: return
        self.rays[id]["ob_x"] = 0
        self.rays[id]["ob_y"] = 0
        self.rays[id]["goal_x"] = 0
        self.rays[id]["goal_y"] = 0
        slope = (vertical/horizontal)
       
        c = self.center_y - slope * self.center_x   
        closest_line = 1000
        for index in obstacle.obsticals:
            cords = obstacle.obsticals[index]
            #print(cords)
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
                            
                if y1==y2:
                    x = (y1-c) / slope
                    if x > x1 and x < x2:
                        if self.check_if_ray_is_infront_of_car(x,y1):
                            length = math.sqrt(((x - self.center_x)**2)+((y1 - self.center_y)**2))
                            if length < closest_line:
                                closest_line = length
                                self.rays[id]["ob_x"] = x
                                self.rays[id]["ob_y"] = y1
        
    def draw_rays(self):
        
        self.rays[1]["angle"] = self.angle+120
        self.rays[1]["radians"] = math.radians(self.rays[1]["angle"])
        self.rays[1]["vertical"] = math.cos(self.rays[1]["radians"]) * self.test_ray_len
        self.rays[1]["horizontal"] = math.sin(self.rays[1]["radians"]) * self.test_ray_len
        self.find_ray((self.rays[1]["horizontal"]),(self.rays[1]["vertical"]),1)
        self.rays[1]["vertical"] = math.cos(self.rays[1]["radians"]) * self.ray_len
        self.rays[1]["horizontal"] = math.sin(self.rays[1]["radians"]) * self.ray_len
        
        
        self.rays[2]["angle"] = self.angle+160
        self.rays[2]["radians"] = math.radians(self.rays[2]["angle"])
        self.rays[2]["vertical"] = math.cos(self.rays[2]["radians"]) * self.ray_len
        self.rays[2]["horizontal"] = math.sin(self.rays[2]["radians"]) * self.ray_len
        self.find_ray((self.rays[2]["horizontal"]),(self.rays[2]["vertical"]),2)
        self.rays[2]["vertical"] = math.cos(self.rays[2]["radians"]) * self.ray_len
        self.rays[2]["horizontal"] = math.sin(self.rays[2]["radians"]) * self.ray_len

        self.rays[3]["angle"] = self.angle+200
        self.rays[3]["radians"] = math.radians(self.rays[3]["angle"])
        self.rays[3]["vertical"] = math.cos(self.rays[3]["radians"]) * self.ray_len
        self.rays[3]["horizontal"] = math.sin(self.rays[3]["radians"]) * self.ray_len
        self.find_ray((self.rays[3]["horizontal"]),(self.rays[3]["vertical"]),3)
        self.rays[3]["vertical"] = math.cos(self.rays[3]["radians"]) * self.ray_len
        self.rays[3]["horizontal"] = math.sin(self.rays[3]["radians"]) * self.ray_len

        self.rays[4]["angle"] = self.angle+240
        self.rays[4]["radians"] = math.radians(self.rays[4]["angle"])
        self.rays[4]["vertical"] = math.cos(self.rays[4]["radians"]) * self.ray_len
        self.rays[4]["horizontal"] = math.sin(self.rays[4]["radians"]) * self.ray_len
        self.find_ray((self.rays[4]["horizontal"]),(self.rays[4]["vertical"]),4)
        self.rays[4]["vertical"] = math.cos(self.rays[4]["radians"]) * self.ray_len
        self.rays[4]["horizontal"] = math.sin(self.rays[4]["radians"]) * self.ray_len
        
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
            
            for i in obstacle.obsticals:
                obsticals = obstacle.obsticals[i]
                
                x_range = range(obsticals[0],obsticals[2])
                y_range = range(obsticals[1],obsticals[3])
                if int(points[0]) in x_range and int(points[1]) in y_range: 
                    print("collided")
                    self.is_alive = False
                    break
            x_range = range(obstacle.goal[0],obstacle.goal[2])
            y_range = range(obstacle.goal[1],obstacle.goal[3])
            if int(points[0]) in x_range and int(points[1]) in y_range: 
                print("goal reached")
                self.is_alive = False
                self.goal_reached = True
                break
            x_range = range(obstacle.border[0],obstacle.border[2])
            y_range = range(obstacle.border[1],obstacle.border[3])
            if int(points[0]) not in x_range and int(points[1]) not in y_range:
                print("outside border")
                self.is_alive = False
                break
        #print(self.center_x,self.center_y)
                
        

        """
        for points in self.four_points:
            if (WINDOW.get_at(((int(points[0]),int(points[1]))))) == (0, 0, 255, 255):
                print("died")
                #self.is_alive = False
                break
            if (WINDOW.get_at(((int(points[0]),int(points[1]))))) == (252, 186, 3, 255):
                print("Goal reached!")
                self.goal_reached = True
                break
        """
        

    def get_data(self):
        values = [0, 0, 0, 0, 0, 0]
        for i in range(1,4):
            values[i] = int(self.rays[i]["length"]/30)
        values[4] = self.goal_angle
        
        #print(values)
        return values
    
    def check_alive(self):
        return self.is_alive
    
    def get_reward(self):
        self.reward = 0
        if self.goal_reached: self.is_alive = False; return 10000 #if goal reached big reward
        self.reward -= 1 # penalty for every step to reduce time
        if self.pre_goal_dist > self.dist_goal: #if closer big reward
            self.reward += 5
        if self.pre_goal_dist <= self.dist_goal:   #if further negitive reward
            self.reward -= 5
        if (self.center_x,self.center_y) in self.pre_pos: 
            self.reward -= 0.05
        self.pre_goal_dist = self.dist_goal
        self.pre_pos.append((self.center_x,self.center_y))
        return self.reward
    
    def update(self):
        #print(self.center_x,self.center_y)
        #self.move()
        pass
    
        
    







def env_start():
    global car,obstacle,clock,images
    

    
    car = Car()
    obstacle = Obstacle()
    #while True:
        #step(random.randint(-1,1))

def env_observe():
    return car.get_data()

def env_step(action):
    if action == 0:
        car.rotate(right=True)
    if action == 1:
        car.rotate(left=True)
    car.move()

    car.check_collision()
    car.find_goal_angle_and_distance()
    if car.is_alive:
        reward = car.get_reward()
    else:
        reward = 0
    info = {}
    #print(reward)
    done = False
    if not car.is_alive:
        done = True
    return_data = (car.get_data(), reward, done,info)
    return return_data

#env_start()