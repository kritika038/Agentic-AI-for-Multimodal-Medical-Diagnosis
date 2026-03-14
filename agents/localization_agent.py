# import numpy as np

# class LocalizationAgent:

#     def locate_infection(self,image):

#         img = np.array(image.convert("L"))

#         h,w = img.shape

#         left = img[:, :w//2]
#         right = img[:, w//2:]

#         if left.mean() < right.mean():
#             return "Left Lung"
#         else:
#             return "Right Lung"
import numpy as np
import cv2

class LocalizationAgent:

    def locate_infection(self,image):

        img = np.array(image.convert("L"))
        img = cv2.resize(img, (256, 256))
        inverted = 255 - img
        blurred = cv2.GaussianBlur(inverted, (15, 15), 0)

        h, w = blurred.shape
        quadrants = {
            "Upper Left Lung": blurred[: h // 2, : w // 2].mean(),
            "Upper Right Lung": blurred[: h // 2, w // 2 :].mean(),
            "Lower Left Lung": blurred[h // 2 :, : w // 2].mean(),
            "Lower Right Lung": blurred[h // 2 :, w // 2 :].mean(),
        }

        return max(quadrants, key=quadrants.get)
