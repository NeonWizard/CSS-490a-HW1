from tflite_runtime.interpreter import Interpreter
from PIL import Image
import numpy as np
import time
import os
import pickle
from tqdm import tqdm

data_folder = "./data/"
image_folder = "./images/"

model_path = data_folder + "mobilenet_v1_1.0_224_quant.tflite"
label_path = data_folder + "labels_mobilenet_quant_v1_224.txt"

# Read the labels from the text file as a Python list.
def load_labels(path):
  with open(path, 'r') as f:
    return [line.strip() for i, line in enumerate(f.readlines())]

def set_input_tensor(interpreter, image):
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image

def classify_image(interpreter, image, top_k=1):
  set_input_tensor(interpreter, image)

  interpreter.invoke()
  output_details = interpreter.get_output_details()[0]
  output = np.squeeze(interpreter.get_tensor(output_details['index']))

  scale, zero_point = output_details['quantization']
  output = scale * (output - zero_point)

  ordered = np.argpartition(-output, top_k)
  return [(i, output[i]) for i in ordered[:top_k]][0]


def main():
  interpreter = Interpreter(model_path)
  print("Model Loaded Successfully.")

  interpreter.allocate_tensors()
  _, height, width, _ = interpreter.get_input_details()[0]['shape']
  print("Image Shape (", width, ",", height, ")")

  # Iterate over each class folder and the images inside
  bench_data = {}
  class_count = 0
  imagenet_folder = image_folder + "imagenet_images"
  with tqdm(total=1000, ncols=64) as pbar:
    for classname in os.listdir(imagenet_folder):
      image_count = 0
      class_folder = imagenet_folder + "/" + classname
      bench_data[classname] = []
      for filename in os.listdir(class_folder):
        image = Image.open(class_folder + "/" + filename).convert('RGB').resize((width, height))
        bench = {}

        # Classify the image.
        time1 = time.time()
        label_id, prob = classify_image(interpreter, image)
        time2 = time.time()
        classification_time = np.round(time2-time1, 5)
        bench["time"] = classification_time
        # print("Classification Time =", classification_time, "seconds.")

        # Read class labels.
        labels = load_labels(label_path)

        # Return the classification label of the image.
        classification_label = labels[label_id]
        accuracy = np.round(prob*100, 2)
        bench["accuracy"] = accuracy
        # print("Image Label is :", classification_label, ", with Accuracy :", accuracy, "%.")

        bench_data[classname].append(bench)
        image_count += 1

        # print(f"{class_count * 10 + image_count}/1000")
        pbar.update(1)

        if image_count == 10:
          break

      class_count += 1
      if class_count == 100:
        break

  with open("benchmark.p", 'wb') as f:
    pickle.dump(bench_data, f)
    print("Wrote benchmark data as pickled file.")

if __name__ == "__main__":
  main()
