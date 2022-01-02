
import math


def blit_rotate_center(self):
    len = 25
    right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 120))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 120))) * len]
    left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 240))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 240))) * len]
    right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 300))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 300))) * len]
    left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 60))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 60))) * len]
    self.four_points = [left_top, right_top, left_bottom, right_bottom]
   
    