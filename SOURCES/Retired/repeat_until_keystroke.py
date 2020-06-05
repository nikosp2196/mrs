import keyboard

while True:
      if keyboard.is_pressed('y') or keyboard.is_pressed('Y'):
            break
      else:
            print('\tDKEEP READING MOVIE RATINGS ... until you press \'Y\' or \'y')

print('\n Got you!!! You just pressed \'Y\' or \'y\' :) ')
