import pygame
import math

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def blit_rotate_center(window, image, top_left, angle, self, obstacle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    self.center_x, self.center_y = new_rect.center
    window.blit(rotated_image, new_rect.topleft)
    self.center = [int(self.center_x),int(self.center_y)]
    len = 25
    right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 120))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 120))) * len]
    left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 240))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 240))) * len]
    right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 300))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 300))) * len]
    left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 60))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 60))) * len]
    self.four_points = [left_top, right_top, left_bottom, right_bottom]
    #pygame.draw.lines(window,(0,0,255),True,self.four_points,3)
    if self.rays_show:
        pygame.draw.line(window,(0,255,255),(self.center_x,self.center_y),((self.center_x + self.rays[1]["horizontal"]),(self.center_y + self.rays[1]["vertical"])),3)
        pygame.draw.line(window,(0,255,255),(self.center_x,self.center_y),((self.center_x + self.rays[2]["horizontal"]),(self.center_y + self.rays[2]["vertical"])),3)
        pygame.draw.line(window,(0,255,255),(self.center_x,self.center_y),((self.center_x + self.rays[3]["horizontal"]),(self.center_y + self.rays[3]["vertical"])),3)
        pygame.draw.line(window,(0,255,255),(self.center_x,self.center_y),((self.center_x + self.rays[4]["horizontal"]),(self.center_y + self.rays[4]["vertical"])),3)

        pygame.draw.line(window,(255,0,255),(self.center_x,self.center_y),((obstacle.goal_rect[0]+(obstacle.goal_rect[2]/2)),(obstacle.goal_rect[1]+(obstacle.goal_rect[3]/2))),3)

        if (self.rays[1]["ob_x"]) != 0:
            pygame.draw.circle(window,(255,0,0),((self.rays[1]["ob_x"]),(self.rays[1]["ob_y"])),5)
            pygame.draw.line(window,(255,0,0),(self.center_x,self.center_y),((self.rays[1]["ob_x"]),(self.rays[1]["ob_y"])),3)
        if (self.rays[2]["ob_x"]) != 0:
            pygame.draw.circle(window,(255,0,0),((self.rays[2]["ob_x"]),(self.rays[2]["ob_y"])),5)
            pygame.draw.line(window,(255,0,0),(self.center_x,self.center_y),((self.rays[2]["ob_x"]),(self.rays[2]["ob_y"])),3)  
        if (self.rays[3]["ob_x"]) != 0:
            pygame.draw.circle(window,(255,0,0),((self.rays[3]["ob_x"]),(self.rays[3]["ob_y"])),5)
            pygame.draw.line(window,(255,0,0),(self.center_x,self.center_y),((self.rays[3]["ob_x"]),(self.rays[3]["ob_y"])),3)
        if (self.rays[4]["ob_x"]) != 0:
            pygame.draw.circle(window,(255,0,0),((self.rays[4]["ob_x"]),(self.rays[4]["ob_y"])),5)
            pygame.draw.line(window,(255,0,0),(self.center_x,self.center_y),((self.rays[4]["ob_x"]),(self.rays[4]["ob_y"])),3)

       