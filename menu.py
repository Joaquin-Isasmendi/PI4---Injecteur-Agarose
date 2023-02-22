import lcd_driver
import rotaryEncoder

def navigate(encoder, lcd_object, text, unit):
        button = 0 
        print('The value is now:')
        lcd_object.disp(text)
        while not button:
                value = encoder.update()
                print(f'\tValue:{value}')
                lcd_object.disp(f'{value} {unit}', line=2, pos=15-len(str(value)) -len(unit)) 
                button = input('Press 1')#*encoder.get_switch()
        lcd_object.lcd_clear()
        return value


# Setting I/O values for peripherals
lcd_address = 0x27
encoder_pins=[22,27,18]

# Initializing user interface controls
controller = rotaryEncoder.encoder(*encoder_pins)
lcd_screen = lcd_driver.lcd(address=lcd_address)

#
#  VOLUME SELECT
#
print('User selecting volume...')
volume_start =1500
volume_increment =50 
volume_clamp = [500, 3000] # in uL

controller.set_value(volume_start, volume_increment, volume_clamp)

user_volume = navigate(controller, lcd_screen, 'Volume', 'uL')

print(f'\tUser selected volume = {user_volume} uL.')

#
#  FLOW RATE SELECT
#
print('User selecting flow rate...')
flow_start = 0.2
flow_increment = 0.05
flow_clamp = [0.1, 0.3455] # in uL/s    

controller.set_value(flow_start, flow_increment, flow_clamp)

user_flow = navigate(controller, lcd_screen, 'Flow rate', 'mL/s')

print(f'\tUser selected flow rate = {user_flow} mL/s.')

#
#  TEMPERATURE SELECT
#
print('User selecting temperature...')
temp_start = 40
temp_increment = 1
temp_clamp = [35, 45] # in *C    

controller.set_value(temp_start, temp_increment, temp_clamp)

user_temp = navigate(controller, lcd_screen, 'Temperature', '*C')

print(f'\tUser selected temp = {user_temp} uL.')

#
# START PROCEDURE
#

