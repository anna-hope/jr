#!/usr/bin/env python3.3

import argparse, pprint, sys
from joystickreader import JoystickReader, BadInputError, BadPortError

def calibrate():
    x_zero = int(input('Zero for x\n> '))
    y_zero = int(input('Zero for y\n> '))
    return x_zero, y_zero

def main():
    # initialise the serial port
    print('Initialising the serial port...')
    x_zero = 127
    y_zero = 127
    if args.calibrate:
        x_zero, y_zero = calibrate()
    if args.port:
        jr = JoystickReader(port=args.port, x_zero=x_zero, y_zero=y_zero)
    else:
        try:
            jr = JoystickReader()
        except BadPortError:
            connected = False
            while not connected:
                port = input('port: ')
                try:
                    jr = JoystickReader(port=port, x_zero=x_zero, y_zero=y_zero)
                except BadPortError as e:
                    print(e)
                    continue
                else:
                    connected = True
    
    
    pp = pprint.PrettyPrinter()
    
    print('Waiting for input.')
    
    last_values = {'x_steps': None, 'y_steps': None}
    
    while True:
        try:
            values = jr.interpret_values()
        # sometimes there is a random ValueError, whose origin I'm still not sure of
        except ValueError:
            continue
        # and sometimes the input data is also bad, and I also don't know why
        except BadInputError as e:
            print(e)
            print('Relaunch me because something went wrong.')
            break
        else:
            if last_values['x_steps'] != values['x_steps'] or last_values['y_steps'] != values['y_steps']:
                last_values = values
                
                if args.r:
                    pp.pprint(values)
                else:
                    button_pressed = values['button_pressed']
                
                    y_direction = values['y_direction']
                    y_steps = values['y_steps']
            
                    x_direction = values['x_direction']
                    x_steps = values['x_steps']
                
                
                    if button_pressed:
                        print('You pressed the button.')
                    if y_steps > 0:
                        print('Y is {} steps {}'.format(values['y_steps'],
                            values['y_direction']))
                    if x_steps > 0:
                        print('X is {} steps {}'.format(values['x_steps'],
                            values['x_direction']))
                    if not button_pressed and y_steps is 0 and x_steps is 0:    
                        print('All at rest')
            else:
                continue
            
    

if __name__ == '__main__':
    argp = argparse.ArgumentParser()
    argp.add_argument('-p', '--port', type=str, default='/dev/tty.usbmodemfa131',
                     help='serial port to connect on')
    argp.add_argument('-r', action='store_true', default=False, help='raw mode')
    argp.add_argument('-c', '--calibrate', action='store_true',
                         help='calibration mode')
    args = argp.parse_args()
    main()