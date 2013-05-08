#!/usr/bin/env python3.3

import argparse, pprint
from joystickreader import JoystickReader, BadInputError

def main():
    # initialise the serial port
    print('Initialising the serial port...')
    jr = JoystickReader()
    
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
                
                if args.v:
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
    argp.add_argument('-v', action='store_true', default=False, help='verbose mode')
    args = argp.parse_args()
    main()