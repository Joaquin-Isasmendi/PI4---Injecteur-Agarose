import lcd_driver
import rotaryEncoder
from time import sleep
#import menu

# def navigate(encoder, lcd_object, text, unit):
#         button = False
#         print('The value is now:')
#         while not button:
#                 encoder.update()
                
#                 button = encoder.get_switch()
        
#         print(f'Chosen value:{encoder.get_value}')
#         return encoder.get_value

def navigate(encoder, lcd_object, disp_dict):
        text = disp_dict['text']
        # unit = disp_dict['unit']
        line = disp_dict['line']
        position = disp_dict['position']
        button = False

        while not button:
                x = input('Value:')
                lcd_object.disp(text, line = line, position = position)
                end = input(f'Choose value = {x}? (y/n)')
                if end.lower() == 'y': button = True

        print(f'Chosen value:{x}')
        return x[:-1]

def pumpProtocol(values):
    import pumpCtrl
    
    temp_threshold = values["max_temp"]
    pump_volume = values["volume"]
    pump_flowrate = values["flow_rate"]

    port = pumpCtrl.setup_serial("COM7", 19200, 1)
    
    print('Connected.')

    print(f'Port accesible:{port.writable()}')

    a = pumpCtrl.cmdsp('RUN')
    print(f'RUN command in bytes: {a}')

    port.open()
    print(f"Port open: {port.isOpen()}")

    port.write(a)
    sleep(1)
    port.write(pumpCtrl.cmdsp('STP'))

    print('Fini.')
    port.close()

    print(f'Port accesible:{port.writable()}')

def __main__():
    # Defining 
    max_temp = 40

    controller_pins = [22,27,17]
    controller = rotaryEncoder(*controller_pins) # clk, dt, sw
    button = False

    lcd_address = 0x27
    lcd_screen = lcd_driver.lcd(address=lcd_address)

    ## Menu

    volume = {
        "start" : 3000,
        "increment" : 10,
        "clamp" : [200, 3000],
        "text": "Volume",
        "units": "uL",
        "selected_value": 3000
    }

    flow_rate = {
        "start" : 3000,
        "increment" : 10,
        "clamp" : [200, 3000],
        "text": "Flow rate",
        "units": "mL/s",
        "selected_value": 3000
    }

    start = 2

    display_dictionnaries = {
        "volume":{
            "text":"Volume",
            "unit": "uL",
            "line":2,
            "position":0
        },
        "flow_rate":{
            "text":"Volume",
            "unit": "uL",
            "line":2,
            "position":0
        },
        "menu":{
            "text":"",
            "var_text":"\u22c5",
            "unit": "",
            "line":[1,1,2],
            "position": [2,10,2]
        }
    }

    menu_values = [volume, flow_rate, start]
    lcd_screen.disp('  volume  start ', line=1)
    lcd_screen.disp('  flow rate', line=2)
    while selected_item != start:
        controller.set_value(0, 1, [0,2])
        while not button:
            selected_item = controller.update()
            button = controller.get_switch()

        if selected_item != start:
            parameter = menu_values[selected_item]
            parameter["selected_value"] = navigate(menu_values[selected_item])

    #-----------------------|
    #   START PROCEDURE     |
    #-----------------------|

    protocol_values = {
        "volume": volume["selected_value"],
        "flow_rate":flow_rate["selected_value"],
        "temperature":max_temp,
    }

    pumpProtocol(protocol_values)

    print(f'Finished pumping.')

if __name__=='__main__': __main__()