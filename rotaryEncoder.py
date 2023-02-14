<<<<<<< Updated upstream
from RPi import GPIO
from time import sleep

# Clamp variable value to designated range
def clamp(n, lim=[0,10]):
    if n < lim[0]: n = lim[0]
    elif n > lim[1]: n = lim[1]
    else: return n

class encoder():
        def __init__(self, clk, dt, sw, start_value=0):
                self.pins = {'clk':clk, 'dt':dt, 'sw':sw}       

                GPIO.setmode(GPIO.BCM)
                GPIO.setup(self.pins['clk'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                GPIO.setup(self.pins['dt'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                GPIO.setup(self.pins['sw'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                
                self.last_state = GPIO.input(self.pins['clk'])
                self.value= start_value
        
        # Define control domain
        def set_value(self, new_value, increment, limits):
                self.value = new_value
                self.increment = increment
                self.limits = limits # [min, max]

        # Read switch ON/OFF
        def get_switch(self):
                self.button_press = bool(GPIO.input(self.pins['sw']))
                return self.button_press
        
        # Read clk and dt and return modified value
        def update(self):
                self.clk_state = GPIO.input(self.pins['clk'])
                self.dt_state = GPIO.input(self.pins['dt'])
                if self.clk_state != self.last_state:
                        if self.dt_state != self.clk_state:
                                self.value += self.increment
                        else:
                                self.value -= self.increment

                        # print(self.counter)
                # elif self.clk_state == self.last_state:
                #         self.counter = 0
                
                else: EnvironmentError()
                self.last_state = self.clk_state
                sleep(0.01)

                return clamp(self.value, )
        


# Test library functionalities
def __main__():
        clk = 17
        dt = 18
        sw = 19
        value = 5

        controller = encoder(clk,dt,sw, start_value=value)
        
        controller.update()

if __name__=='__main__':
        __main__()
=======
from RPi import GPIO
from time import sleep

# Clamp variable value to designated range
def clamp(n, lim=[0,10]):
    if n <= lim[0]: n = lim[0]
    elif n >= lim[1]: n = lim[1]
    return n

class encoder():
        def __init__(self, clk, dt, sw, start_value=0):
                self.pins = {'clk':clk, 'dt':dt, 'sw':sw}       

                GPIO.setmode(GPIO.BCM)
                GPIO.setup(self.pins['clk'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                GPIO.setup(self.pins['dt'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                GPIO.setup(self.pins['sw'], GPIO.IN)#, pull_up_down=GPIO.PUD_UP)
                
                self.last_state = GPIO.input(self.pins['clk'])
                self.value= start_value
        
        # Define control domain
        def set_value(self, new_value, increment, limits):
                self.value = new_value
                self.increment = increment
                self.limits = limits # [min, max]

        # Read switch ON/OFF
        def get_switch(self):
                return GPIO.input(self.pins['sw'])
                
        
        # Read clk and dt and return modified value
        def update(self):
                self.clk_state = GPIO.input(self.pins['clk'])
                self.dt_state = GPIO.input(self.pins['dt'])
                #print(f'CLK:{self.clk_state} DT = {self.dt_state}')
                if self.clk_state != self.last_state:
                        if self.dt_state != self.clk_state:
                                self.value += self.increment
                        else:
                                self.value -= self.increment

                        # print(self.counter)
                # elif self.clk_state == self.last_state:
                #         self.counter = 0
                
                else: EnvironmentError()
                self.last_state = self.clk_state
                sleep(0.01)

                return clamp(self.value)
        


# Test library functionalities
def __main__():
        from time import sleep
        clk=22
        dt=27
        sw=17
        value = 5
        button=False
        controller = encoder(clk,dt,sw, start_value=value)
        controller.set_value(value, 1, [0,10])
        while button != True:
            value= controller.update()
            print(f'Value:{value}')
            button=controller.get_switch()
            print(f'\tBOUTON ={button}')
            #sleep(0.01)

if __name__=='__main__':
        __main__()
>>>>>>> Stashed changes
