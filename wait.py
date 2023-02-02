from datetime import datetime, time
from time import sleep

def act(x):
    return x+10

def wait_start(runTime, action):
    startTime = time(*(map(int, runTime.split(':'))))
    while startTime > datetime.today().time(): # you can add here any additional variable to break loop if necessary
        sleep(1)# you can change 1 sec interval to any other
    return action

wait_start('20:13', lambda: act(100))