from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import onnxruntime as ort

allClasses = ['Bird', 'Flower', 'Hand', 'House', 'Pencil', 'Mug', 'Spoon', 'Sun', 'Tree', 'Umbrella']

ort_session = ort.InferenceSession('model.onnx')

def process(path):
    print('WORKING')
    
    image = Image.fromarray(plt.imread(path)[:, :, 3])
    image=image.resize((384,384))
    
  
    image = (np.array(image) > 0.1).astype(np.float32)[None, :, :]
    image = (image - 0.1307)/0.38

    return image[None]

def test(path):
    
    image = process(path)
    output = ort_session.run(None, {'data': image})[0].argmax()

    print(allClasses[output], output)

    return allClasses[output]