import utime
from stepper.pinout import Pinout
from machine import Pin

class BipolarStepper():
    """ Control a Bipolar stepper motor through L298N driver
        
        Default pinout for a Raspberry PICO:
            In1 - GPIO_17 (B+)
            In2 - GPIO_16 (A+)
            In3 - GPIO_15 (B-)
            In4 - GPIO_14 (A-)
        
        Args:
            pin1 to pin4 (int): pinout to use with the microcontroller (default raspberry PICO)
            speed (str): 'high' (default), 'medium', 'low', or 'test'
            direction (str): 'forward' (default) , 'backward'
            steps360 (int): nb of steps to make a full 360° rotation (default 200)
        
        Methods:
            set_direction(direction) : set direction 'forward'|'backward'
            set_speed(speed)         : set motor speed 'high'|'medium'|'low'|'test'
            next_step(nbsteps)       : move motor *nsteps
            next_angle(angle)        : move motor in degrees (360 = full rotation)
            sleep()                  : release the motor, stop consumming power.
            split_steps(nsplits)     : split step360 into nsplit
        
        Usage:
            bp = BipolarStepper(speed='medium')
            bp.next_step(100) # move 100 steps forward speed medium
            bp.set_direction('backward')
            bp.set_speed('high')
            bp.next_step(50) # move 50 steps backward highest speed
        
    """
    # constructor
    def __init__(self, pin1:int=17, pin2:int=16, pin3:int=15, pin4:int=14,
                 speed='high', direction='forward', steps360=200)->None :
        """ constructor
            Args:
                pin1 to pin4: pinout (default Raspberry PICO) to use
                speed = 'high' (default), 'medium', 'low', 'test'
                direction = 'forward' (default), 'backward'
                steps360 (200 default): nb of steps to rotate 360°
        """
        #pinout initialization
        self._pinout = Pinout(pin1,pin2,pin3,pin4)
        
        #speed motor: delays between 2 steps
        self._speed = {'high': 0.005,   # 5ms delay between 2 steps
                      'medium': 0.008,  # 8ms delay between 2 steps
                      'low': 0.016,     # 16ms delay between 2 steps
                      'test':0.5,       # 0.5s delay between 2 steps, for testing activity
                      }
        self.set_speed(speed)
        
        #direction forward or backward
        self._dic_direction = { 'forward':1, 'backward':-1 }
        self.set_direction(direction)
        
        self._steps360 = steps360
 
        # sequences to run in circle for A+, B+, A-, B-
        self._full_step_seq = [ 
            [1,1,0,0],  
            [0,1,1,0],  
            [0,0,1,1], 
            [1,0,0,1],
        ] 
        self._seq = 0   # current sequence: 0,1,2,3
        
        #init motor with first position seq 0
        print('init motor')
        self._move_motor()
        utime.sleep(0.5)

    # Private methods
    # -------------------------------------------------
    
    def _move_motor(self)->None :
        """ Move motor to curent step and wait """
        #run current sequence
        (self.pin2).value(self._full_step_seq[self._seq][0]) # A+
        (self.pin1).value(self._full_step_seq[self._seq][1]) # B+
        (self.pin4).value(self._full_step_seq[self._seq][2]) # A-
        (self.pin3).value(self._full_step_seq[self._seq][3]) # B-
        utime.sleep(self._delay)
    

    # Public methods
    # ---------------------------------------------------------------
    @property
    def steps360(self)->int :
        return self._steps360

    @property
    def pin1(self)->Pin :
        return self._pinout.pin1
    
    @property
    def pin2(self)->Pin :
        return self._pinout.pin2
    
    @property
    def pin3(self)->Pin :
        return self._pinout.pin3
    
    @property
    def pin4(self)->Pin:
        return self._pinout.pin4
    

    def set_speed(self, speed)->None :
        """ Set motor speed: 'high' (default), 'medium', 'low' or 'test' """
        try:
            self._delay = self._speed[speed]
        except:
            self._delay = self._speed['high']
    
    
    def set_direction(self, direction)->None :
        """ Set direction: 'forward' (default) or 'backward' """
        try:
            self._direction = self._dic_direction[direction]
        except:
            self._direction = self._dic_direction['forward']          
    
    
    def next_steps(self, nsteps=1)->None :
        """ Move motor nsteps. """
        for _ in range(nsteps):
            self._seq = (self._seq + self._direction)%4
            self._move_motor()          


    def next_angle(self, angle=90)->None :
        """ Move motor for an angle in degree (360=full rotation). """
        self.next_steps(self.steps360*angle//360)
    
    
    def sleep(self)->None :
        """ Release motor, stop consuming power """
        (self.pin1).value(0)
        (self.pin2).value(0)
        (self.pin3).value(0)
        (self.pin4).value(0)
        
        
    def split_steps(self, nsplits=1)->list :
        """ split steps360 into a list of nsplits equivalent steps"""
        l = nsplits*[self.steps360//nsplits] # list of nsplits equal steps
        r = self.steps360%nsplits   # add this value, so that sum of steps = steps360
        for i in range(r):
            l[-1-i]+= 1 #r value added from the end of the list
        return l

