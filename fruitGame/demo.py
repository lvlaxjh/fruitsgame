"""Just for a test"""
# created by Huang Lu
# 27/08/2016 17:05:45 
# Department of EE, Tsinghua Univ.

import cv2
import numpy as np
import pygame
from img_percess import percess

pygame.init()
screen = pygame.display.set_mode((600,400))
cap = cv2.VideoCapture(0)
#cv2.namedWindow('capture', cv2.WINDOW_NORMAL)
while 1:
    # get a frame
    ret, frame = cap.read()
    #frame = cv2.flip(frame, 1)
    try:
        # show a frame
        position = percess(frame)
        #print(position)
        cv2.circle(frame, position, 60, (0, 0, 255), 0)
    except e:
        print('rua')
    finally:
        #cv2.imshow("capture", frame)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        screen.blit(frame, (0, 0))
        pygame.display.update()
cap.release()
cv2.destroyAllWindows()
