
import cv2
from . import img_pro
new_hand_num = None
last_hand_num = None
two_last_hand_num = 0
count = 0
hand_num = None
get_hand_num = False

get_hand = False
last_hand = 0
hand_count = 0
reset = False
debug = True

stream = "http://127.0.0.1:8080/?action=stream?dummy=param.mjpg"
orgFrame = None
stop = False
rz = 60
ori_width = int(rz * 4)
ori_height = int(rz * 3)


def Camera_isOpened():
    global stream, cap
    cap = cv2.VideoCapture(stream)


try:
    Camera_isOpened()
    # cap = cv2.VideoCapture(stream)
except Exception as e:
    print('Unable to detect camera! \n')
    # check_camera.CheckCamera()
#
get_image_ok = False


def CvHandNumber(frame):
    global get_hand_num, hand_num
    global two_last_hand_num
    global new_hand_num, last_hand_num
    binary = img_pro.image_process(frame)
    # cv2.imshow('bin', binary)
    # 获取手指个数
    hand_num = img_pro.get_hand_number(binary, frame)
    return hand_num


def get_finger_num():
    global cap
    cap = cv2.VideoCapture(stream)
    if cap.isOpened():
        ret, orgFrame = cap.read()
        i = 0
        while i < 30:
            if ret:
                org = cv2.resize(orgFrame, (ori_width, ori_height), interpolation=cv2.INTER_CUBIC)
                orgframe = cv2.flip(org, 0)
                dd = CvHandNumber(orgframe)
                if dd:
                    cv2.destroyAllWindows()
                    # kill_process("find_finger.py")
                    return dd
            cv2.waitKey(1)
            i += 1
    cv2.destroyAllWindows()

# print(get_finger_num())



