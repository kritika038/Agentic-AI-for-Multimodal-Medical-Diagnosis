import numpy as np
import cv2

class SeverityAgent:

    def severity_score(self, image):

        img = np.array(image.convert("L"))

        img = cv2.resize(img,(256,256))

        # pneumonia increases opacity
        score = img.mean()

        return score

    def assess(self, image, pneumonia_confidence):
        opacity_score = 255.0 - self.severity_score(image)
        severity_score = max(0.0, min(100.0, (opacity_score * 0.5) + (pneumonia_confidence * 0.5)))

        if severity_score >= 75:
            severity_level = "High"
        elif severity_score >= 45:
            severity_level = "Moderate"
        else:
            severity_level = "Low"

        return round(severity_score, 2), severity_level


    def rank_images(self, images):

        results = []

        for name,image in images.items():

            score, _ = self.assess(image, 50.0)

            results.append((name,score))

        results.sort(key=lambda x:x[1])

        return results
