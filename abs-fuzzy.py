'''
ABS FUZZYLOGIC SYSTEM

github: https://github.com/regisfaria
'''

'''
NOTES

 In this code I'm taking consideration three parameters
 1. Obstacle 
 2. Brakeforce  
 3. Slip
'''
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Antecedents
obstacle = ctrl.Antecedent(np.arange(0, 101, 1), 'obstacle')
#np.arange(-36, 137, 1)
brake_force = ctrl.Antecedent(np.arange(0, 101, 1), 'brake_force')
#np.arange(-36, 128, 1)
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
abs_brake['minimum'] = fuzz.trimf(abs_brake.universe, [0, 16.7, 33.4])
abs_brake['medium'] = fuzz.trimf(abs_brake.universe, [33.4, 49.5, 66.7])
abs_brake['maximum'] = fuzz.trimf(abs_brake.universe, [66.7, 83, 100])#101 maybe

# Ploting obstacle
obstacle.view()

# Ploting brake force
brake_force.view()

# Ploting slip
slip.view()

# Now it's time to define the rules of this system
# I'm going to create a rules array, so all the rules will be stored here
rules = []

rule1 = ctrl.Rule(obstacle['very near'] & brake_force['high'] & slip['unsafe'], abs_brake['minimum'])
rules.append(rule1)
rule2 = ctrl.Rule(obstacle['very near'] & brake_force['high'] & slip['critical'], abs_brake['medium'])
rules.append(rule2)
rule3 = ctrl.Rule(obstacle['very near'] & brake_force['high'] & slip['safe'], abs_brake['maximum'])
rules.append(rule3)
rule4 = ctrl.Rule(obstacle['near'] & brake_force['high'] & slip['unsafe'], abs_brake['minimum'])
rules.append(rule4)
rule5 = ctrl.Rule(obstacle['near'] & brake_force['high'] & slip['critical'], abs_brake['medium'])
rules.append(rule5)
rule6 = ctrl.Rule(obstacle['near'] & brake_force['high'] & slip['safe'], abs_brake['maximum'])
rules.append(rule6)
rule7 = ctrl.Rule(obstacle['near'] & brake_force['low'] & slip['safe'], abs_brake['maximum'])
rules.append(rule7)
rule8 = ctrl.Rule(obstacle['near'] & brake_force['low'] & slip['critical'], abs_brake['medium'])
rules.append(rule8)
rule9 = ctrl.Rule(obstacle['no obstacle'] & brake_force['low'] & slip['safe'], abs_brake['maximum'])
rules.append(rule9)
rule10 = ctrl.Rule(obstacle['no obstacle'] & brake_force['high'] & slip['critical'], abs_brake['medium'])
rules.append(rule10)
rule11 = ctrl.Rule(obstacle['no obstacle'] & brake_force['high'] & slip['unsafe'], abs_brake['minimum'])
rules.append(rule11)
rule12 = ctrl.Rule(obstacle['no obstacle'] & brake_force['low'] & slip['unsafe'], abs_brake['minimum'])
rules.append(rule12)
rule13 = ctrl.Rule(obstacle['no obstacle'] & brake_force['low'] & slip['critical'], abs_brake['medium'])
rules.append(rule13)

# Now I'll create the rule system
abs_brake_ctrl = ctrl.ControlSystem(rules)

# Creating a simulation
abs_brake_intensity = ctrl.ControlSystemSimulation(abs_brake_ctrl)

# Here I'll pick up the inputs from the user
print('We will test the intensity of the ABS brake of a car based on 3 variables\n\n')
obstacle_user =  float(input('In a scale of 0 to 100, how close is the obstacle?\n'))
brake_force_user = float(input('How abrupt you press the brake in a scale of 0 to 100?\n'))

# Calculating slip
car_speed = float(input('How fast is the car going?\n'))
wheel_speed = float(input('How fast is the wheel?\n'))
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
