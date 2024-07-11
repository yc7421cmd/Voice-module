import time
import sys
from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize
from unitree_sdk2py.idl.default import unitree_go_msg_dds__SportModeState_
from unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_
from unitree_sdk2py.go2.sport.sport_client import (
    SportClient,
    PathPoint,
    SPORT_PATH_POINT_SIZE,
)
from extract import *
from open import *

# Robot state
robot_state = unitree_go_msg_dds__SportModeState_()
def HighStateHandler(msg: SportModeState_):
    global robot_state
    robot_state = msg

if len(sys.argv)>1:
    ChannelFactoryInitialize(0, sys.argv[1])
else:
    ChannelFactoryInitialize(0)
    
sub = ChannelSubscriber("rt/sportmodestate", SportModeState_)
sub.Init(HighStateHandler, 10)
time.sleep(1)
client = SportClient()  # Create a sport client
client.SetTimeout(10.0)
client.Init()

def act(text):
    # command = extract_keywords(text) # 单纯分词器，但所很高级
    command = llm(text) # llama3
    print(command)
    speed = command[0]
    flag = command[1]
    tim = command[2]
    if(flag == 0):
        return False
    elif(flag <= 6 ):
        t0 = time.time()
        if(flag == 1):
            print("Move forward!")
            while(time.time() - t0 <= tim):
                client.Move(speed, 0, 0)


        elif(flag == 2):
            print("Move backward!")
            while(time.time() - t0 <= tim):
                client.Move(-speed, 0, 0)

        elif(flag == 3):
            print("Move leftward!")
            while(time.time() - t0 <= tim):
                client.Move(0, speed, 0)

        elif(flag == 4):
            print("Move rightward!")
            while(time.time() - t0 <= tim):
                client.Move(0,-speed, 0)

        elif(flag == 5):
            print("Turn left!")
            while(time.time() - t0 <= tim):
                client.Move(0, 0, speed)

        elif(flag == 6):
            print("Turn right!")
            while(time.time() - t0 <= tim):
                client.Move(0, 0, -speed)


    elif(flag ==7 ):
        print("Dance1!")
        client.Dance1()
    elif(flag == 8):
        print("Sit!")
        client.Sit()
    elif(flag == 9):
        print("Stand!")
        client.RiseSit()
    elif(flag == 10):
        print("Show Heart!")
        client.Heart()
    elif(flag == 11):
        print("Stand down!")
        client.StandDown()
    elif(flag == 12):
        print("Stand up!")
        client.StandUp()
    time.sleep(2)
    return True
