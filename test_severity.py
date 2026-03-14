from PIL import Image
from agents.diagnosis_agent import DiagnosisAgent

agent = DiagnosisAgent()

images = ["A.jpg","B.jpg","C.jpg","D.jpg"]

results = []

for img in images:

    image = Image.open(img)

    pneumonia, confidence = agent.analyze_xray(image)

    results.append((img,confidence,pneumonia))

print("\nResults\n")

for r in results:
    print(r)

print("\nSorted by severity (confidence):\n")

print(sorted(results,key=lambda x:x[1]))