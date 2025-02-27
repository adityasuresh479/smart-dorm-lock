import RPi.GPIO as GPIO
import time

servo_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # 50Hz PWM
pwm.start(0)

def unlock_door():
    """Rotate servo to unlock position"""
    pwm.ChangeDutyCycle(7)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)
    print("Door Unlocked!")

def lock_door():
    """Rotate servo to lock position"""
    pwm.ChangeDutyCycle(2)  # Adjust as per servo position
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)
    print("Door Locked!")
