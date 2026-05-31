import cv2
import numpy as np
import matplotlib.pyplot as plt

clean_img = cv2.imread("D:/stegoproject/flower.jpg", 0)
stego_img = cv2.imread("D:/stegoproject/stego_flower.png", 0)

srm_filter = np.array([[-1,  2, -1],
                       [ 2, -4,  2],
                       [-1,  2, -1]])

clean_noise = cv2.filter2D(clean_img, -1, srm_filter)
stego_noise = cv2.filter2D(stego_img, -1, srm_filter)

clean_noise = np.absolute(clean_noise)
clean_noise = np.absolute(stego_noise)

clean_noise = cv2.normalize(clean_noise, None, 0, 255, cv2.NORM_MINMAX)
stego_noise = cv2.normalize(stego_noise, None, 0, 255, cv2.NORM_MINMAX)

plt.subplot(1,2,1)
plt.title("clean Noise (Enhanced)")
plt.imshow(stego_noise, cmap='gray')

plt.subplot(1,2,2)
plt.title("Stego Noise (Enhanced)")
plt.imshow(stego_noise, cmap='gray')

plt.show()
