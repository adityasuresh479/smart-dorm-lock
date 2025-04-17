import lgpio
import time

CHIP = 0  # Default gpiochip0
GPIO = 23  # GPIO23 (physical pin 16)
PWM_FREQ = 50  # 50 Hz for servo

h = lgpio.gpiochip_open(CHIP)

# Claim the pin for output
lgpio.gpio_claim_output(h, GPIO, 0)

# Send neutral pulse (servo center position)
lgpio.tx_pwm(h, GPIO, PWM_FREQ, 7.5)
time.sleep(1)

# Move to 0 degrees
lgpio.tx_pwm(h, GPIO, PWM_FREQ, 2.5)
time.sleep(1)

# Move to 180 degrees
lgpio.tx_pwm(h, GPIO, PWM_FREQ, 12.5)
time.sleep(1)

# Stop PWM
lgpio.tx_pwm(h, GPIO, 0, 0)

lgpio.gpiochip_close(h)
