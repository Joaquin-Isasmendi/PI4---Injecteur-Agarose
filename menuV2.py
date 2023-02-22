import lcd_driver
import rotaryEncoder
from time import sleep
#import menu


def navigate_menu(encoder, lcd_object, disp_dict):
        text = disp_dict['text']
        var_text = disp_dict['var_text']
        lines = disp_dict['line']
        position = disp_dict['position']
        button = False

        while not button:
                for i in range(len(text["str"])):
                    lcd_object.disp(text["str"][i], text["line"][i], text["pos"][i])
                x = int(input('Value:'))
                lcd_object.disp(var_text, lines[x], position[x])
                end = input(f'Choose value = {x}? (y/n)')
                if end.lower() == 'y': button = True

        print(f'Chosen value:{x}')
        return x


def navigate_parameter(encoder, lcd_object, disp_dict):
        text = disp_dict['text']
        var_text = disp_dict['var_text']
        lines = disp_dict['line']
        position = disp_dict['position']
        button = False

        x = 0
        while not button:
                for i in range(len(text["str"])):
                    lcd_object.disp(text["str"][i], text["line"][i], text["pos"][i])
                x = int(input('Value:'))
                lcd_object.disp(str(x), line=2, pos = text["pos"][-1]-len(str(x)))
                end = input(f'Choose value = {x}? (y/n)')
                if end.lower() == 'y': button = True

        print(f'Chosen value:{x}')
        return x

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
    controller = rotaryEncoder.encoder(*controller_pins) # clk, dt, sw
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
            "text":{
                "str":[' Volume:',' uL'],
                "line":[1,2], 
                "pos":[0,12]
            },
            "var_text":'*',
            "unit": "",
            "line":[1,1,2],
            "position": [1,9,1]
        },
        "flow_rate":{
            "text":{
                "str":[' Flow rate:',' mL/s'],
                "line":[1,2], 
                "pos":[0,11]
            },
            "var_text":'*',
            "unit": "",
            "line":[1,1,2],
            "position": [1,9,1]
        },
        "menu":{
            "text":{
                "str":['  volume  start ','  flow rate'],
                "line":[1,2], 
                "pos":[0,0]
            },
            "var_text":'*',
            "unit": "",
            "line":[1,1,2],
            "position": [1,9,1]
        }
    }

    menu_values = [volume, flow_rate, start]
    selected_item =0 
    lcd_screen.disp(, line=1)
    lcd_screen.disp(, line=2)
    while selected_item != start:
        controller.set_value(0, 1, [0,2])
        while not button:
            selected_item = navigate_menu(controller, lcd_screen, display_dictionnaries['menu'])

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