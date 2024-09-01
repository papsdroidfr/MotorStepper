import utime
from stepper.bipolar import BipolarStepper

print('test module stepper')
bp = BipolarStepper(speed='medium')   

print('move 200 steps forward, speed medium') 
bp.next_steps(200)
bp.sleep()
utime.sleep(0.5)

print('move 100 steps backward highest speed')
bp.set_direction('backward')            
bp.set_speed('high')            
bp.next_steps(100)
bp.sleep()
utime.sleep(0.5)
    
print('move 4 times to 90°')
for _ in range(4):
    bp.next_angle(90)
    bp.sleep()
    utime.sleep(0.5)

print(f"split {bp.steps360} steps in 7: {bp.split_steps(7)}")

bp.sleep()
print('bye')
