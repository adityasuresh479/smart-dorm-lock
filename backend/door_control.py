import lgpio
import time

# GPIO setup
CHIP = 0
SERVO_GPIO = 23
PWM_FREQ = 50

# Global handle
h = None

def init_gpio():
    global h
    if h is None:
        h = lgpio.gpiochip_open(CHIP)
        try:
            lgpio.gpio_claim_output(h, SERVO_GPIO, 0)
        except lgpio.error as e:
            if 'GPIO busy' not in str(e):
                raise e

def unlock_door():
    print("Unlocking door...")
    init_gpio()
    lgpio.tx_pwm(h, SERVO_GPIO, PWM_FREQ, 2.5)  # 0 degrees
    time.sleep(1)
    lgpio.tx_pwm(h, SERVO_GPIO, PWM_FREQ, 0)

def lock_door():
    print("Locking door...")
    init_gpio()
    lgpio.tx_pwm(h, SERVO_GPIO, PWM_FREQ, 12.5)  # 180 degrees
    time.sleep(1)
    lgpio.tx_pwm(h, SERVO_GPIO, PWM_FREQ, 0) 

def cleanup():
    global h
    print("Cleaning up...")
    try:
        if h is not None:
            lgpio.tx_pwm(h, SERVO_GPIO, 0, 0)
            lgpio.gpiochip_close(h)
            h = None
    except Exception as e:
        print(f"Cleanup error: {e}")


