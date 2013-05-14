#!/usr/bin/env python2.7

# (c) Anton Osten for the PyBot Project

# let's make it as much like python3 as we can
from __future__ import division, print_function, unicode_literals
import sys, time, math
# vpython
from visual import *
# joystick
from joystickreader import JoystickReader, BadInputError

class MagicBox(box):
    '''Custom box class to define useful properties'''
    
    @property
    def volume(self):
        return self.size.x * self.size.y * self.size.z
    
    @property
    def density(self):
        return 2.75
    
    @property
    def mass(self):
        return self.density * self.volume
    
    @property
    def half_size(self):
        half_size = vector(self.size.x / 2, self.size.y / 2)
        return half_size
        
class MagicSphere(sphere):
   
   @property
   def volume(self):
       return (4 * math.pi * self.radius**3) / 3
   
   @property
   def density(self):
       return 2.75
   
   @property
   def mass(self):
       return self.density * self.volume
       
       
def actor_velocity(values):
    if values['x_direction'] == 'right':
        x = values['x_steps']
    elif values['x_direction'] == 'left':
        x = -(values['x_steps'])
    else:
        x = 0
    
    if values['y_direction'] == 'up':
        y = values['y_steps']
    elif values['y_direction'] == 'down':
        y = -(values['y_steps'])
    else:
        y = 0
    
    return vector(x, y)
        
def move(pos, velocity, bounds=vector(5, 5)):
    new_pos = pos + velocity
    
    if new_pos.x <= bounds.x and new_pos.y <= bounds.y:
        return new_pos
    else:
        return pos
    

def touch(square, circle):
    """Let's define touch as the edge of the box touching the surface of the sphere 
    (and we won't care if the box is inside the sphere, or vice versa).
    
    The positions of our objects are calculated from their centres.
    Therefore, to see if two objects touch, we need to get the distance between their centres,
    along the X and Y planes.
    If we compare those distances to the sum of the half size of the box plus the radius of the sphere 
    (since its position is calculated from its centre)
    and find that they are equal, we know that they could be touching along that plane.
    
    To account for the other plane (i.e. to see if our objects aren't 'touching' on X,
     but are miles away on Y),
    we just need to check that the distance along that other plane
    is not greater than the sum of the box size and the radius.
    
    Ask me to look at this in a couple of months, and I might not get it either."""
    
    # distance between the two centres along X
    dist_x = abs(square.pos.x - circle.pos.x)
    # and along Y
    dist_y = abs(square.pos.y - circle.pos.y)
    
    # let's compare those distances
    if (round(dist_x, 1) <= square.half_size.x + circle.radius
        and dist_y <= square.half_size.x + circle.radius):
        print('touch')
        return True
    elif (round(dist_y, 1) <= square.half_size.y + circle.radius
        and dist_x <= square.half_size.y + circle.radius):
        print('touch')
        return True
    else:
        print('no touch')
        return False


def main():
    # canvas = box(pos=vector(0, 0), size=(10,10), color=color.white)
    square = MagicBox(pos=vector(0, 0), size=(2, 2, 2), color=color.blue)
    ball = MagicSphere(pos=vector(2, 2), radius=0.5, color=color.green)
    
    deltat = 0.005
    
    jr = JoystickReader()
    # scene.autoscale = False
    
    while True:
        try:
            values = jr.interpret_values()
        except ValueError:
            continue
        except BadInputError as e:
            print(e)
            print('Remove and reconnect the joystick')
            time.sleep(3)
            main()
        
        rate(50)
        
        if values['button_pressed'] is True:
            square.color = color.red
        elif values['button_pressed'] is False:
            square.color = color.blue
        
        square.velocity = actor_velocity(values)
    
        if touch(square, ball):
            ball.color = color.orange
            impact = square.mass/ball.mass
            ball.velocity = vector(square.velocity.x/impact, square.velocity.y/impact)
            t = 0
            while t < 3:
                new_pos = ball.pos + ball.velocity*deltat
                if new_pos < vector(5, 5):
                    ball.pos = new_pos
                t += deltat
        else:
            ball.color = color.green
            square.pos = move(square.pos, square.velocity*deltat)

if __name__ == '__main__':
    main()