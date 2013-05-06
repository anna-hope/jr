#!/usr/bin/env python2.7

# let's make it as much like python3 as we can
from __future__ import division, print_function, unicode_literals
import sys
# vpython
from visual import *
# joystick
from joystickreader import JoystickReader, BadInputError

def main():
    square = box(pos=vector(1, 1), size=(0.1, 0.1), color=color.blue)
    
    deltat = 0.005
    
    jr = JoystickReader()
    
    while True:
        try:
            values = jr.interpret_values()
        except ValueError:
            continue
        except BadInputError as e:
            print(e)
            print('Remove and reconnect the joystick and restart me')
            break
        
        rate(100)
        
        if values['button_pressed'] is True:
            square.color = color.red
        elif values['button_pressed'] is False:
            square.color = color.blue
            
        
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
        
        square.velocity = vector(x, y)
        
        square.pos = square.pos + square.velocity*deltat

if __name__ == '__main__':
    main()