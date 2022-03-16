from time import sleep
from approxeng.input.selectbinder import ControllerResource
import RPi.GPIO as GPIO

left_en = 33
left_forward = 13
left_backward = 15

right_en = 32
right_forward = 16
right_backward = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(left_en, GPIO.OUT)
GPIO.setup(left_forward, GPIO.OUT)
GPIO.setup(left_backward, GPIO.OUT)

GPIO.output(left_forward, 0)
GPIO.output(left_backward, 0)
left_pwm = GPIO.PWM(left_en, 100)

GPIO.setup(right_en, GPIO.OUT)
GPIO.setup(right_forward, GPIO.OUT)
GPIO.setup(right_backward, GPIO.OUT)
right_pwm = GPIO.PWM(right_en, 100)

GPIO.output(right_forward, 0)
GPIO.output(right_backward, 0)
left_pwm.start(0)
right_pwm.start(0)

def left_motor_forward():
   GPIO.output(left_forward, 1)
   GPIO.output(left_backward, 0)

def right_motor_forward():
   GPIO.output(right_forward, 1)
   GPIO.output(right_backward, 0)

def left_motor_backward():
   GPIO.output(left_forward, 0)
   GPIO.output(left_backward, 1)

def right_motor_backward():
   GPIO.output(right_forward, 0)
   GPIO.output(right_backward, 1)

def motor_stop():
   GPIO.output(left_forward, 0)
   GPIO.output(left_backward, 0)
   GPIO.output(right_forward, 0)
   GPIO.output(right_backward, 0)

while True:
    try:
        with ControllerResource() as joystick:
            while joystick.connected:

                left_trigger_value = joystick.lt
                right_trigger_value = joystick.rt
                #print("Left: " + str(left_trigger_value) + " Right: " + str(right_trigger_value))

                x_axis_joystick_value = joystick.lx
                #print("X axis: " + str(x_axis_joystick_value))

                x_button_pressed = joystick.square
                left_trigger_pressed = joystick.l2
                right_trigger_pressed = joystick.r2

                if left_trigger_pressed is not None:
                        left_motor_backward()
                        right_motor_backward()

                        normal_pwm = left_trigger_value * 100
                        turn_pwm = normal_pwm - (normal_pwm * abs(x_axis_joystick_value))
                        #print("Normal: " + str(normal_pwm) + " Turn: " + str(turn_pwm))

                        if x_axis_joystick_value > 0:
                            left_pwm.ChangeDutyCycle(normal_pwm)
                            right_pwm.ChangeDutyCycle(turn_pwm)
                        elif x_axis_joystick_value < 0:
                            left_pwm.ChangeDutyCycle(turn_pwm)
                            right_pwm.ChangeDutyCycle(normal_pwm)
                        else:
                            left_pwm.ChangeDutyCycle(normal_pwm)
                            right_pwm.ChangeDutyCycle(normal_pwm)

                elif right_trigger_pressed is not None:
                        left_motor_forward()
                        right_motor_forward()

                        normal_pwm = right_trigger_value * 100
                        turn_pwm = normal_pwm - (normal_pwm * abs(x_axis_joystick_value))
                        #print("Normal: " + str(normal_pwm) + " Turn: " + str(turn_pwm))

                        if x_axis_joystick_value > 0:
                            left_pwm.ChangeDutyCycle(normal_pwm)
                            right_pwm.ChangeDutyCycle(turn_pwm)
                        elif x_axis_joystick_value < 0:
                            left_pwm.ChangeDutyCycle(turn_pwm)
                            right_pwm.ChangeDutyCycle(normal_pwm)
                        else:
                            left_pwm.ChangeDutyCycle(normal_pwm)
                            right_pwm.ChangeDutyCycle(normal_pwm)

                elif x_button_pressed is not None:
                     normal_pwm = abs(x_axis_joystick_value) * 100
                     left_pwm.ChangeDutyCycle(normal_pwm)
                     right_pwm.ChangeDutyCycle(normal_pwm)

                     if x_axis_joystick_value > 0:
                         left_motor_forward()
                         right_motor_backward()
                     elif x_axis_joystick_value < 0:
                         left_motor_backward()
                         right_motor_forward()
                     else:
                         motor_stop()

                else:
                        motor_stop()

                sleep(0.1)


    except IOError:
        motor_stop()
        sleep(1.0)
