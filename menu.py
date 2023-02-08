import lcd_driver
import rotaryEncoder

def navigate(encoder):
        button = False
        print('The value is now:')
        while not button:
                encoder.update()
                print(f'\t{encoder.get_value}')
                
                button = encoder.get_switch()
        return encoder.get_value


# Setting I/O values for peripherals
lcd_address = 0x27
encoder_pins=[1,2,3]

# Initializing user interface controls
controller = rotaryEncoder.encoder(*encoder_pins)
lcd_screen = lcd_driver.lcd(address=lcd_address)

#
#  VOLUME SELECT
#
print('User selecting volume...')
volume_start = 3000
volume_increment = 10
volume_clamp = [200, 3000] # in uL

controller.set_value(volume_start, volume_increment, volume_clamp)

user_volume = controller.navigate()

print(f'\tUser selected volume = {user_volume} uL.')

#
#  FLOW RATE SELECT
#
print('User selecting flow rate...')
flow_start = 0.1
flow_increment = 0.01
flow_clamp = [0.1, 5] # in uL/s    

controller.set_value(flow_start, flow_increment, flow_clamp)

user_flow = controller.navigate()

print(f'\tUser selected flow rate = {user_flow} uL.')

#
#  TEMPERATURE SELECT
#
print('User selecting temperature...')
temp_start = 40
temp_increment = 1
temp_clamp = [35, 45] # in uL/s    

controller.set_value(temp_start, temp_increment, temp_clamp)

user_temp = controller.navigate()

print(f'\tUser selected temp = {user_temp} uL.')

#
# START PROCEDURE
#

