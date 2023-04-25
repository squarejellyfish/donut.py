from math import floor, cos, sin, pi
import os
import numpy as np

theta_spacing = 0.07
phi_spacing = 0.02
screen_width = os.get_terminal_size()[0]
screen_height = os.get_terminal_size()[1]
R1 = 1
R2 = 2
K2 = 5
# calculate the K1 based on the terminal width
K1 = screen_width*R1 / 20*(R1+R2)
# Precompute a blank screen
OUTPUT = np.empty((screen_height, screen_width), dtype=str)
for i in range(screen_height):
    for j in range(screen_width):
        OUTPUT[i][j] = ' '
ZBUFFER = np.zeros((screen_height, screen_width))

light_source = np.array([0, -1, -1])

# Original: chars = '.,-~:;!=*#$@'
chars = '_.,-:;!=+?$W#@'


def render(A: float, B: float):

    # Refresh the screen.
    output = OUTPUT.copy()
    zbuffer = ZBUFFER.copy()

    cosA = cos(A)  # A, B is for spinning the torus
    sinA = sin(A)
    cosB = cos(B)
    sinB = sin(B)

    for theta in np.arange(0, 2*pi, theta_spacing):

        costheta = cos(theta)
        sintheta = sin(theta)
        for phi in np.arange(0, 2*pi, phi_spacing):

            cosphi = cos(phi)
            sinphi = sin(phi)

            circlex = R2 + R1 * costheta
            circley = R1 * sintheta

            # Some part is multiplied out for performance purposes.
            circleVec = [circlex*(cosB*cosphi + sinA*sinB*sinphi) - circley*cosA*sinB,
                         circlex*(sinB*cosphi - sinA*cosB*sinphi) +
                         circley*cosA*cosB,
                         circlex*cosA*sinphi + circley*sinA + K2]
            if circleVec[2] != 0:
                ooz = 1 / circleVec[2]
            else:
                ooz = 0  # 'one over z'

            # Calculate the x', y' (projection point on screen)
            xp = floor(screen_width/2 + K1*ooz*circleVec[0])
            yp = floor(screen_height/2 + K1*ooz*circleVec[1])

            # N = surface normal = (Nx, Ny, Nz)
            # Nx: costheta*(cosB*cosphi + sinA*sinB*sinphi) - sintheta*cosA*sinB
            # Ny: costheta*(sinB*cosphi - sinA*cosB*sinphi) + sintheta*cosA*cosB
            # Nz: costheta*cosA*sinphi + sintheta*sinA + K2
            surfaceNorm = [costheta*(cosB*cosphi + sinA*sinB*sinphi) - sintheta*cosA*sinB,
                           costheta*(sinB*cosphi - sinA*cosB *
                                     sinphi) + sintheta*cosA*cosB,
                           costheta*cosA*sinphi + sintheta*sinA]
            # This part is just: L = surfaceNorm @ light_source (both need to be numpy.array),
            # but I multiplied it out for performance.
            # -sqrt2 < L < sqrt2
            L = 0*surfaceNorm[0] - surfaceNorm[1] - surfaceNorm[2]

            # Check if luminance value is not negative and the point is not outside the screen.
            if L >= 0 and xp >= 0 and xp < screen_width and yp >= 0 and yp < screen_height:

                if ooz > zbuffer[yp][xp]:  # check if already render a point infront

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
        try:
            render(A, B)
            A -= 0.05
            B -= 0.05
        except KeyboardInterrupt:
            break
