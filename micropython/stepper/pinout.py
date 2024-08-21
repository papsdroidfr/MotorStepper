from machine import Pin

class Pinout():
    """ pinout LN298 <--> microcontroller
        Args: pin1 (int), pin2 (int), pin3 (int), pin4 (int): GPIO pin of microcontroller
    """

    def __init__(self, pin1:int, pin2:int, pin3:int, pin4:int)->None :
        """ Set pinout of microcontrolleur GPIO -> IN LN298 driver """
               
        print(f"Pinout  initialization to control L298N driver:")
        print(f"... GPIO_{pin1} ---> in1 L298N (B+) ")
        print(f"... GPIO_{pin2} ---> in2 L298N (A+) ")
        print(f"... GPIO_{pin3} ---> in3 L298N (B-) ")
        print(f"... GPIO_{pin4} ---> in4 L298N (A-) ")

        self._pin_in1 = Pin(pin1, Pin.OUT)
        self._pin_in2 = Pin(pin2, Pin.OUT)
        self._pin_in3 = Pin(pin3, Pin.OUT)
        self._pin_in4 = Pin(pin4, Pin.OUT)
    
    @property
    def pin1(self)->Pin : 
        return self._pin_in1
    
    @property
    def pin2(self)->Pin : 
        return self._pin_in2
    
    @property
    def pin3(self)->Pin : 
        return self._pin_in3
    
    @property
    def pin4(self)->Pin : 
        return self._pin_in4
