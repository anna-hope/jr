#!/usr/bin/env python3.3

# (c) Anton Osten for the PyBot Project

import serial

# a custom exception for when we are given bad data
class BadInputError(Exception):
    def __str__(self):
        return 'Bad input data'

class JoystickReader(object):
    def __init__(self, port='/dev/tty.usbmodemfd121'):
        self.ser = serial.Serial(port)
        
    # let's have a few fancy decorators to help us interpret the input

    # this one is to convert input data to a tuple of integer values
    def convert_values(fn):
        def wrapped(*args):
            values = fn(*args)
            return (int(values[0].decode('ascii').strip()),
                    int(values[1].decode('ascii').strip()),
                    int(values[2].decode('ascii').strip()),
                    int(values[3].decode('ascii').strip()))
        return wrapped

    # this one is to apply the sort_input function
    def sort_values(fn):
        def wrapped(*args):
            '''The format of input data is (0, button_value, y_value, x_value).
            Note that it can be shifted.'''
            values = fn(*args)
            # get the index of the begginning 0
            start_index = values.index(0)
            # we need to get other indeces accounting for the shift
            # the formula goes like this: abs(normal_index - start_index)
            button_index = abs(1 - start_index)
            y_index = abs(2 - start_index)
            x_index = abs(3 - start_index)
            # now that we have the indeces, let's get the values
            button_value = values[button_index]
            y_value = values[y_index]
            x_value = values[x_index]
            return (button_value, y_value, x_value)
        return wrapped

    @sort_values   
    @convert_values
    def read_values(self):
        return (self.ser.readline(), self.ser.readline(),
             self.ser.readline(), self.ser.readline())

    def interpret_values(self, sorted_values=None):
        '''Interprets the pre-sorted joystick data.
        Raises BadInputError when there is something wrong with the data.'''
        if sorted_values is None:
            sorted_values = self.read_values()
        button_value = sorted_values[0]
        # let's check that we are given correctly sorted values with the right data 
        # (3 items, button value, which is at index 0, has to be 1 or 2)
        if len(sorted_values) > 3 or button_value not in {1, 2}:
            raise BadInputError
        # okay, if the data are right, then let's interpret them
        # the button is pressed when its value is 1 (and not pressed when it's 2)
        button_pressed = True if button_value is 1 else False
        # now let's work on x and y
        # the range for x and y is 1-250
        # from experience we know that zero for y is at 126
        y = sorted_values[1] - 126
        if y > 0:
            y_direction = 'up'
        elif y < 0:
            y_direction = 'down'
        else:
            y_direction = None
        # and zero for x is between 132 and 134
        x = sorted_values[2] - 133
        # we need to account for x sometimes being at 1 even when it's not pressed
        if x > 1:
            x_direction = 'left'
        elif x < 0:
            x_direction = 'right'
        else:
            x_direction = None
        # now let's split each direction into 'steps'
        # i.e. how far is the joystick moved in a particular direction
        y_steps = round(abs(y) / 10)
        x_steps = round(abs(x) / 10)
    
        return {'button_pressed': button_pressed,
        'y_value': y, 'y_direction': y_direction, 'y_steps': y_steps,
        'x_value': x, 'x_direction': x_direction, 'x_steps': x_steps}