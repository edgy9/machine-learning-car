import pygame
import time
import math
from utils import scale_image, blit_rotate_center
import neat
import sys

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)

CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.55)

WIDTH, HEIGHT = GRASS.get_width(), GRASS.get_height()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Driving Sim")
FPS = 60

generation = 0


class Obstacle:
    def __init__(self):
        self.obsticals = {1:[300,200,500,300],2:[800,500,1200,800],3:[100,400,700,1000],4:[0,0,1500,1500]}
        self.obsticals_rect = {1:[300,200,200,100],2:[800,500,400,300],3:[100,400,600,600],4:[0,0,1300,1300]}
        self.obsticals = {}
        self.obsticals_rect = {}
        self.goal = [800,200,850,250]
        self.goal_rect = [800,200,50,50]

    def draw(self,WINDOW):
        pygame.draw.rect(WINDOW,(0,0,255),(self.obsticals_rect[1]))
        pygame.draw.rect(WINDOW,(0,0,255),(self.obsticals_rect[2]))
        pygame.draw.rect(WINDOW,(0,0,255),(self.obsticals_rect[3]))
        pygame.draw.rect(WINDOW,(0,0,255),(self.obsticals_rect[4]),3)
        pygame.draw.rect(WINDOW,(252, 186, 3),(self.goal_rect))
        
class Car:
    def __init__(self):
        
        self.speed = 2
        self.angle = 270
        self.img = CAR
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
    
    def draw(self, WINDOW):
        blit_rotate_center(WINDOW, self.img, (self.x, self.y), self.angle,self,obstacle)
        #pygame.draw.circle(WINDOW,(0,0,255),(self.center_x,self.center_y),5)
        self.draw_rays()
        
        


    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.speed
        horizontal = math.sin(radians) * self.speed
        #print("moving")
        self.y -= vertical
        self.x -= horizontal
        self.angle = self.angle
        self.draw(WINDOW)
        self.draw_rays()
    
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
        
    def find_goal_angle(self):
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
            for obsticals in obstacle.obsticals:
                x_range = range(obsticals[0],obsticals[2])
                y_range = range(obsticals[1],obsticals[3])
                if points[0] in x_range and points[1] in y_range: 
                    print("collided")
                    self.is_alive = False
                    break
            x_range = range(obstacle.goal[0],obstacle.goal[2])
            y_range = range(obstacle.goal[1],obstacle.goal[3])
            if points[0] in x_range and points[1] in y_range: 
                print("goal reached")
                self.is_alive = False
                self.goal_reached = True
                break
            """
            #print(WINDOW.get_at(((int(points[0]),int(points[1])))))
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
        values[5] = self.dist_goal
        #print(values)
        return values
    
    def check_alive(self):
        return self.is_alive
    
    def get_reward(self):
        pos_x, pos_y = self.center_x,self.center_y
        goal_pos_x, goal_pos_y = (obstacle.goal_rect[0] + (obstacle.goal_rect[2]/2)),(obstacle.goal_rect[1] + (obstacle.goal_rect[3]/2))
        distance_from_goal = abs(pos_x-goal_pos_x)+abs(pos_y-goal_pos_y)
        if self.goal_reached: return 10000

        if self.pre_cord == (self.center_x,self.center_y): return -10
        self.pre_cord = (self.center_x,self.center_y)

        return self.dist_goal
    
    def update(self):
        self.draw_rays()
        self.check_collision()
        
    
        
    







#playercar = Car()
obstacle = Obstacle()


def draw(WINDOW):
    WINDOW.blit(GRASS,(0,0))
    obstacle.draw(WINDOW)
    

def run_car(genomes, config):

    nets = []
    cars = []

    for id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        cars.append(Car())

    pygame.init()
    clock = pygame.time.Clock()

    global generation
    generation += 1

    while True:
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

        
        
        
        

        # Input data and get result from the network
        for index, car in enumerate(cars):
            output = nets[index].activate(car.get_data())
            
            i = output.index(max(output))
            
            if i == 0:
                car.move()
                #print("why dont you move")
                pass
            if i == 1:
                if car.angle == 0: car.angle = 360
                car.angle -= 2

            else:
                if car.angle == 360: car.angle = 0
                car.angle += 2
            
               
        # Update car and fitness
        remain_cars = 0
        for i, car in enumerate(cars):
            if car.check_alive():
                remain_cars += 1
                car.update()
                genomes[i][1].fitness += car.get_reward()
        
        if remain_cars == 0:
            break

        draw(WINDOW)
        for car in cars:
            if car.check_alive():
                car.draw(WINDOW)

        pygame.display.flip()    
        clock.tick(FPS)
        
        

if __name__ == "__main__":
    # Set configuration file
    config_path = "./config.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Create core evolution algorithm class
    p = neat.Population(config)
    #p.run(eval_genomes, 50)
    # Add reporter for fancy statistical result
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run NEAT
    p.run(run_car, 1000)
    