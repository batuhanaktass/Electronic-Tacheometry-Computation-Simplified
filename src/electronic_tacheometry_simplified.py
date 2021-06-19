import math; import sys
# --- Title Section --- 
title = '     Program for Electrometric Tacheometry Computation     '  # Program Title
proportion = len(title)  # Value For Organizing
print('\n' + title + '\n' + ('-' * proportion))  # Title Format

# --- Variable Section ---
stationary_pID = input(f'{"Enter the stationary traverse ID":<{proportion - 2}} {": "}')  # Stationary PID Value
referenced_pID = input(f'{"Enter the referenced traverse ID":<{proportion - 2}} {": "}')  # Referenced PID Value
# PID List
pID_list = [stationary_pID, referenced_pID]  # Take Variables
# Same Point ID Exception
def Same_except(error_message):
    if error_message.lower() == 'y' or error_message.lower() == 'yes':
        print('Resuming...')
        pass
    else:
        sys.exit()
if len(pID_list) != len(set(pID_list)):
    print('\n'+'You Should Not Have Same Point ID' + '\n' + 'That Can Cause Conflict')
    error_message = input('Do You Want To Continue? (Not Recommended) (y/n): ')
    Same_except(error_message)
else:
    pass  

referenced_Y = float(input(f'Enter the Y coordinates of {pID_list[1]:<{proportion - 32}} (m): '))  # Referenced Y Coordinates
referenced_X = float(input(f'Enter the X coordinates of {pID_list[1]:<{proportion - 32}} (m): '))  # Referenced X Coordinates
referenced_height = float(input(f'Enter the height of {pID_list[1]:<{proportion - 25}} (m): '))  # Referenced Height
stationary_Y = float(input(f'Enter the Y coordinates of {pID_list[0]:<{proportion - 32}} (m): '))  # Stationary Y Coordinates
stationary_X = float(input(f'Enter the X coordinates of {pID_list[0]:<{proportion - 32}} (m): '))  # Stationary X Coordinates
stationary_height = float(input(f'Enter the height of {pID_list[0]:<{proportion - 25}} (m): '))  # Stationary Height
detail_pID = input(f'{"Enter the point ID of detail point":<{proportion - 2}} {": "}')  # Detail Point PID
pID_list.append(detail_pID)

if len(pID_list) != len(set(pID_list)):
    print('\n'+'You Should Not Have Same Point ID' + '\n' + 'That Can Cause Conflict')
    error_message = input('Do You Want To Continue? (Not Recommended) (y/n): ')
    Same_except(error_message)
else:
    pass 

detail_horizontal = float(input(f'Enter the horizontal direction of point {pID_list[2]:<{proportion - 48}} (grad): '))  # Detail Point Horizontal Angle
detail_verticle = float(input(f'Enter the verticle angle of point {pID_list[2]:<{proportion - 42}} (grad): '))  # Detail Point Vertical Angle
slope_distance = float(input(f'Enter the slope distance between {pID_list[0]} and {pID_list[2]:<{proportion - (len(pID_list[0]) + 43)}} (m): '))  # Slope Distance Between Stationary and Detail Point
instrument_height = float(input(f'{"Enter the height of instrument":<{proportion - 5}} {"(m): "}'))  # Instrument Height
reflector_height = float(input(f'{"Enter the height of reflector":<{proportion - 6}}  {"(m): "}'))  # Reflector Height

# --- Calculation Section --- 
# Height Difference
delta_H = (slope_distance * math.cos(detail_verticle * math.pi / 200)) + instrument_height - reflector_height
# Elevation
elevation = stationary_height + delta_H
# Horizontal Distance
horizontal_distance = slope_distance * math.sin(detail_verticle * math.pi / 200)
# Azimuth Calculation Between Stationary and Referenced
delta_Y = stationary_Y - referenced_Y
delta_X = stationary_X - referenced_X
# Ignore Zero Division Error
global azimuth
try:
    azimuth = math.atan((abs(delta_Y)) / (abs(delta_X))) * 200 / math.pi
    # Azimuth Conditions
    if delta_Y > 0 and delta_X > 0:
        azimuth = azimuth
    elif delta_Y > 0 and delta_X < 0:
        azimuth = 200 - azimuth
    elif delta_Y < 0 and delta_X < 0:
        azimuth = 200 + azimuth
    elif delta_Y < 0 and delta_X > 0:
        azimuth = 400 - azimuth
    elif delta_Y == 0 and delta_X >= 0:
        azimuth = 0
    elif delta_Y == 0 and delta_X < 0:
        azimuth = 200 
except ZeroDivisionError:  # If Delta X = 0, azimuth takes unique value
    if delta_Y < 0:
        azimuth = 300
    elif delta_Y > 0:
        azimuth = 100
    else:
        azimuth = 0
# Next Azimuth Calculations
k = azimuth + detail_horizontal
if k < 200:
    k += 200
elif 200 < k < 600:
    k -= 200
elif k > 600:
    k -= 600
# Coordinate Calculation
coordinate_Y = stationary_Y + (horizontal_distance * math.sin(k * math.pi / 200))
coordinate_X = stationary_X + (horizontal_distance * math.cos(k * math.pi / 200))

# --- Output Section --- 
# It is recommended that you use a minimum 90X25 tab for the proper notation.
calc_title = f'{"Point ID":<12} {"Point ID":<12} {"Hor. Dist.":<12} {"Delta H":<12} {"Elevation":<12} {"Coord. (Y)":<12} {"Coord. (X)":<12}'  # Output Title
calc_values = f'{stationary_pID:<12} {detail_pID:<12} {format(horizontal_distance, ".3f"):<12} {format(delta_H, ".3f"):<12} {format(elevation, ".3f"):<12} {format(coordinate_Y, ".3f"):<12} {format(coordinate_X, ".3f"):<12}'  # Output Values
print('\n' + calc_title + '\n' + ('-' * len(calc_title)) + '\n' + calc_values + '\n' + ('-' * len(calc_title)))  # Output