import cv2
from matplotlib import pyplot as plt

img_path = './day_world/control_imgs/123.png'
img = cv2.imread(img_path)
if img is None:
    print("Error: Could not read image.")
else:
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()