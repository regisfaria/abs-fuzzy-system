'''
ABS FUZZYLOGIC SYSTEM

github: https://github.com/regisfaria
'''

import numpy as np
import skfuzzy as fuzz
import random
import time
from skfuzzy import control as ctrl

# Antecedents
obstacle = ctrl.Antecedent(np.arange(-36, 137, 1), 'obstacle')
brake_force = ctrl.Antecedent(np.arange(-36, 128, 1), 'brake_force')
slip = ctrl.Antecedent(np.arange(0, 101, 1), 'slip')

# Auto-membership functions
obstacle_proximity = ['very near', 'near', 'no obstacle']
obstacle.automf(names=obstacle_proximity)

brake_intensity = ['low', 'high']
brake_force.automf(names=brake_intensity)

slip_level = ['safe', 'critical', 'unsafe']
slip.automf(names=slip_level)

# Consequent
abs_brake = ctrl.Consequent(np.arange(0, 101, 1), 'abs_brake')
abs_brake['no brake'] = fuzz.trimf(abs_brake.universe, [0, 16.7, 33.4])
abs_brake['medium brake'] = fuzz.trimf(abs_brake.universe, [33.5, 49.5, 66.7])
abs_brake['high brake'] = fuzz.trimf(abs_brake.universe, [66.8, 83, 100])

# Ploting obstacle
obstacle.view()
time.sleep(3)

# Ploting brake force
brake_force.view()
time.sleep(3)

# Ploting slip
slip.view()
time.sleep(3)

# Now it's time to define the rules of this system
# I'm going to create a rules array, so all the rules will be stored here
rules = []

# Rules for no brake
rule1 = ctrl.Rule(obstacle['very near'] & brake_force['high'] & slip['unsafe'], abs_brake['no brake'])
rules.append(rule1)
rule2 = ctrl.Rule(obstacle['near'] & brake_force['high'] & slip['unsafe'], abs_brake['no brake'])
rules.append(rule2)
rule3 = ctrl.Rule(obstacle['no obstacle'] & brake_force['high'] & slip['unsafe'], abs_brake['no brake'])
rules.append(rule3)
rule4 = ctrl.Rule(obstacle['no obstacle'] & brake_force['low'] & slip['unsafe'], abs_brake['no brake'])
rules.append(rule4)

# Rules for medium brake
rule5 = ctrl.Rule(obstacle['very near'] & brake_force['high'] & slip['critical'], abs_brake['medium brake'])
rules.append(rule5)
rule6 = ctrl.Rule(obstacle['near'] & brake_force['high'] & slip['critical'], abs_brake['medium brake'])
rules.append(rule6)
rule7 = ctrl.Rule(obstacle['near'] & brake_force['low'] & slip['critical'], abs_brake['medium brake'])
rules.append(rule7)
rule8 = ctrl.Rule(obstacle['no obstacle'] & brake_force['high'] & slip['critical'], abs_brake['medium brake'])
rules.append(rule8)
rule9 = ctrl.Rule(obstacle['no obstacle'] & brake_force['low'] & slip['critical'], abs_brake['medium brake'])
rules.append(rule9)

# Rules for high brake
rule10 = ctrl.Rule(obstacle['very near'] & brake_force['high'] & slip['safe'], abs_brake['high brake'])
rules.append(rule10)
rule11 = ctrl.Rule(obstacle['near'] & brake_force['high'] & slip['safe'], abs_brake['high brake'])
rules.append(rule11)
rule12 = ctrl.Rule(obstacle['near'] & brake_force['low'] & slip['safe'], abs_brake['high brake'])
rules.append(rule12)
rule13 = ctrl.Rule(obstacle['no obstacle'] & brake_force['low'] & slip['safe'], abs_brake['high brake'])
rules.append(rule13)

# Now I'll create the rule system
abs_brake_ctrl = ctrl.ControlSystem(rules)

# Creating a simulation
abs_brake_intensity = ctrl.ControlSystemSimulation(abs_brake_ctrl)

# Here I'll pick up the inputs from the user
print('We will test the intensity of the ABS brake of a car based on 3 variables\n\n')
obstacle_user =  str(raw_input('In a scale of 0 to 100, how close is the obstacle?(press "r" for random)\n'))
if obstacle_user == 'r':
    obstacle_user = float(random.triangular(-36, 137))
    print('The random value is:', obstacle_user)
else:
    obstacle_user = float(obstacle_user) + float(random.triangular(-36, 37))

brake_force_user = str(raw_input("How long you've been pressing the brake in a scale of 0 to 100?(press 'r' for random)\n"))
if brake_force_user == 'r':
    brake_force_user = float(random.triangular(-36, 128))
    print('The random value is:', brake_force_user)
else:
    brake_force_user = float(brake_force_user) + float(random.triangular(-36, 28))

# Calculating slip
slip_user = raw_input('Now we will need to calculate the slip rate, press "r" for a random value or "enter" otherwise')
if slip_user == 'r':
    slip_user = float(random.triangular(0, 100))
    print('The random value is:', slip_user)
else:
    car_speed = float(raw_input('How fast is the car going?\n'))
    wheel_speed = float(raw_input('How fast is the wheel?\n'))
    slip_user = 100*((car_speed-wheel_speed)/car_speed)

# Here we will use the user inputs to calculate the abs intensity
abs_brake_intensity.input['obstacle'] = obstacle_user
abs_brake_intensity.input['brake_force'] = brake_force_user
abs_brake_intensity.input['slip'] = slip_user

abs_brake_intensity.compute()

print('The abs intensity:', abs_brake_intensity.output['abs_brake'])
abs_brake.view(sim=abs_brake_intensity)

# Code to end the program
raw_input('Press enter to end the program')
