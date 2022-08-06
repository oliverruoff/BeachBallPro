from lcd import LCD_0inch96
from machine import Pin, ADC, I2C
from time import sleep

from imu import MPU6050

#color is BGR
RED = 0x00F8
GREEN = 0xE007
BLUE = 0x1F00
WHITE = 0xFFFF
BLACK = 0x0000

# Initializing acceleration sensor
i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000)
imu = MPU6050(i2c)

# Initializing sound sensor
sensor_a = ADC(0)
sensor_d = Pin(22, Pin.IN)

# Initializing display

lcd = LCD_0inch96()   
lcd.fill(BLACK) 

GYRO_THRESHOLD = 10
DISPLAY_DIGITS = 4

ball_hits = 0
highscore = 0

# trying to get highscore
try:
    print('Trying to read highscore file')
    with open("highscore.txt") as file_in:
     highscore = int(file_in.read())
     print('Highscore detected: ', highscore)
except:
    highscore = 0
    print('No highscore file detected')
        
  
def display_new_numbers(current_ball_hits):
    global highscore
    if current_ball_hits > highscore:
        highscore = current_ball_hits
        print('New highscore:', highscore)
        with open('highscore.txt', 'w') as out_file:
            out_file.write(str(highscore))
    lcd.fill(BLACK) 
    lcd.text("Beach Ball Pro",0,0,GREEN)
    lcd.text("Fred. Moreau Edition",0,24,GREEN)    
    lcd.text("Highscore: " + str(highscore),0,48,GREEN)
    lcd.text("Aktuell: " + str(current_ball_hits),0,72,GREEN)
    lcd.display()
  
display_new_numbers(ball_hits)
    
while True:
    gy=imu.gyro.y
    sound_detected = sensor_d.value()
    if sound_detected:
        gy_rounded = round(gy)
        print('Sound detected! Gy: ', gy_rounded)
        if abs(gy_rounded) > GYRO_THRESHOLD:
            print('Hit counts! ', ball_hits)
            ball_hits += 2
        display_new_numbers(ball_hits)
        lcd.display()
        # so that it is not executed multiple times if the sound and accel. was long enough
        sleep(0.5)
