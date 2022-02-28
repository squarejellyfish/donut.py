from math import floor, cos, sin, pi
import os
import numpy as np
import time

h_spacing = 0.06
w_spacing = 0.06
screen_width = os.get_terminal_size()[0]
screen_height = os.get_terminal_size()[1]
WIDTH = 2
K2 = 5
# calculate the K1 based on the terminal width
K1 = screen_width*WIDTH / 12*(WIDTH)
# Precompute a blank screen
OUTPUT = np.empty((screen_height, screen_width), dtype=str)
for i in range(screen_height):
    for j in range(screen_width):
        OUTPUT[i][j] = ' '
ZBUFFER = np.zeros((screen_height, screen_width))

light_source = np.array([0, -1, -1])

# Original: chars = '.,-~:;!=*#$@'
chars = '_.,-:;!=+?$W#@'

def render(A=0, B=0):

    # Refresh the screen.
    output = OUTPUT.copy()
    zbuffer = ZBUFFER.copy()

    cosA = cos(A)  # A, B is for spinning the torus
    sinA = sin(A)
    cosB = cos(B)
    sinB = sin(B)

    for h in np.arange(-1, 1, w_spacing):

        for w in np.arange(-1, 1, h_spacing):

            for face in range(6):
                # compute every faces
                if face == 0:
                    # xy 1
                    x = w
                    y = h
                    z = -1
                    surfaceNorm = [0, 0, -1]
                elif face == 1:
                    # yz 1
                    x = 1
                    y = w
                    z = h
                    surfaceNorm = [1, 0, 0]
                elif face == 2:
                    # xz 1
                    x = w
                    y = -1
                    z = h
                    surfaceNorm = [0, -1, 0]
                elif face == 3:
                    # yz 2
                    x = -1
                    y = w
                    z = h
                    surfaceNorm = [-1, 0, 0]
                elif face == 4:
                    # xz 2
                    x = w
                    y = 1
                    z = h
                    surfaceNorm = [0, 1, 0]
                elif face == 5:
                    # xy 1
                    x = w
                    y = h
                    z = 1
                    surfaceNorm = [0, 0, 1]

                cubeVec = [x*cosB - y*sinB*cosA + z*sinA*sinB, 
                            x*sinB + y*cosA*cosB - z*sinA*cosB, 
                            y*sinA + z*cosA + K2]
                if cubeVec[2] != 0:
                    ooz = 1 / cubeVec[2]
                else: ooz = 0 # 'one over z'
                
                # Calculate the x', y' (projection point on screen)
                xp = floor(screen_width/2 + K1*ooz*cubeVec[0])
                yp = floor(screen_height/2 + K1*ooz*cubeVec[1])

                surfaceNorm = [surfaceNorm[0]*cosB - surfaceNorm[1]*sinB*cosA + surfaceNorm[2]*sinA*sinB, 
                                surfaceNorm[0]*sinB + surfaceNorm[1]*cosA*cosB - surfaceNorm[2]*sinA*cosB, 
                                surfaceNorm[1]*sinA + surfaceNorm[2]*cosA]
                # This part is just: L = surfaceNorm @ light_source (both need to be numpy.array),
                # but I multiplied it out for performance.
                # -sqrt2 < L < sqrt2
                L = 0*surfaceNorm[0] - 2*surfaceNorm[1] - 0*surfaceNorm[2]

                # Check if luminance value is not negative and the point is not outside the screen.
                if L >= 0 and xp >= 0 and xp < screen_width and yp >= 0 and yp < screen_height: 

                    if ooz > zbuffer[yp][xp]: # check if already render a point infront
                        
                        # lindex = luminance index
                        # This part would be more flexible if we use np.interp(), 
                        # but the graphics would be horrible.
                        # Original: lindex = floor(L * 8)
                        lindex = 13 if floor(L * 10) >= 14 else floor(L * 10)
                        zbuffer[yp][xp] = ooz
                        output[yp][xp] = chars[lindex]
                # This part is for the point that is facing away from the light source, 
                # I simply set it to the darkest luminance.
                elif L < 0 and xp >= 0 and xp < screen_width and yp >= 0 and yp < screen_height:

                    if ooz > zbuffer[yp][xp]:

                        lindex = 0
                        zbuffer[yp][xp] = ooz
                        output[yp][xp] = chars[lindex]

    print('\x1b[H')
    # os.system('clear') is also ok.
    for row in output:
        for col in row:
            print(col, end='')
        print('')

if __name__ == '__main__':

    A = 0
    B = 0
    while 1:
        render(A, B)
        A -= 0.07
        B -= 0.03
        time.sleep(0.016)

