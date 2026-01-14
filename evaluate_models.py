import os
import sys
import numpy as np

# Set environment variables to reduce TensorFlow logging and ensure legacy Keras compatibility.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["TF_USE_LEGACY_KERAS"] = "1"

import tf_keras as keras
from tf_keras.models import load_model
from tf_keras.preprocessing import image
from tf_keras.layers import DepthwiseConv2D

# Compatibility shim: remove unexpected 'groups' kwarg if present when loading older TM models.
class CustomDepthwiseConv2D(DepthwiseConv2D):
    def __init__(self, **kwargs):
        if 'groups' in kwargs:
            del kwargs['groups']
        super().__init__(**kwargs)

# Configuration: paths, model folder list and class mappings used across the script.
TEST_DIR = 'test'
TRAINING_DIR = os.path.join('training', 'models')
MODEL_FOLDERS = ['model01', 'model02', 'model03', 'model04', 'model05']

CLASS_MAP = {'soup': 0, 'main': 1, 'salad': 2, 'dessert': 3, 'nofood': 4}
NUMBER_MAP = {'01': 'soup', '02': 'main', '03': 'salad', '04': 'dessert', '05': 'nofood'}
INT_TO_CLASS = {v: k for k, v in CLASS_MAP.items()}


# Determine the true label index for a test filename.
# Supports either a textual prefix (e.g. 'salad_xxx') or a numeric prefix mapping (e.g. '03_xxx').
def get_true_label(filename):
    parts = filename.split('_')
    prefix = parts[0]
    if prefix in NUMBER_MAP:
        return CLASS_MAP[NUMBER_MAP[prefix]]
    if prefix in CLASS_MAP:
        return CLASS_MAP[prefix]
    return None


# Load and preprocess an image to the model's expected input shape and normalization.
# Returns a numpy array shaped (1,224,224,3) with values in [-1, 1] (Teachable Machine standard).
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    normalized_image_array = (img_array.astype(np.float32) / 127.5) - 1
    return normalized_image_array


# Evaluate a single model folder: load model, run predictions on all test images,
# collect per-class metrics and print a concise summary with per-category accuracy.
def evaluate_model(model_path, model_name):
    print(f"\n{'='*60}")
    print(f"Evaluando modelo: {model_name}")
    print(f"{'='*60}")

    try:
        model = load_model(model_path, custom_objects={'DepthwiseConv2D': CustomDepthwiseConv2D}, compile=False)
    except Exception as e:
        print(f"Error cargando el modelo {model_path}: {e}")
        return

    total_images = 0
    total_correct = 0
    class_metrics = {k: {'total': 0, 'correct': 0, 'false_positives': 0, 'false_negatives': 0} for k in CLASS_MAP.keys()}

    test_files = [f for f in os.listdir(TEST_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not test_files:
        print("No se encontraron imágenes en la carpeta test.")
        return

    print(f"Procesando {len(test_files)} imágenes de prueba...\n")

    for filename in test_files:
        true_label_idx = get_true_label(filename)
        if true_label_idx is None:
            print(f"Advertencia: No se pudo determinar la clase para el archivo {filename}. Saltando.")
            continue

        img_path = os.path.join(TEST_DIR, filename)
        try:
            processed_img = preprocess_image(img_path)
            prediction = model.predict(processed_img, verbose=0)
            predicted_label_idx = np.argmax(prediction)

            true_class_name = INT_TO_CLASS[true_label_idx]
            predicted_class_name = INT_TO_CLASS[predicted_label_idx]

            total_images += 1
            class_metrics[true_class_name]['total'] += 1

            if predicted_label_idx == true_label_idx:
                total_correct += 1
                class_metrics[true_class_name]['correct'] += 1
            else:
                class_metrics[true_class_name]['false_negatives'] += 1
                class_metrics[predicted_class_name]['false_positives'] += 1
                print(f"[FALLO] {filename}: Real: {true_class_name} -> Predicho: {predicted_class_name}")

        except Exception as e:
            print(f"Error procesando imagen {filename}: {e}")

    accuracy = (total_correct / total_images) * 100 if total_images > 0 else 0
    print(f"\n--- Resultados para {model_name} ---")
    print(f"Precisión Global (Accuracy): {accuracy:.2f}% ({total_correct}/{total_images})")

    print("\nDetalle por Categoría:")
    print(f"{'Categoría':<15} | {'Total':<6} | {'Aciertos':<8} | {'Fallos (FN)':<12} | {'Precisión':<10}")
    print("-" * 65)
    for class_name, metrics in class_metrics.items():
        total = metrics['total']
        correct = metrics['correct']
        fn = metrics['false_negatives']
        acc = (correct / total * 100) if total > 0 else 0
        print(f"{class_name:<15} | {total:<6} | {correct:<8} | {fn:<12} | {acc:.2f}%")


# Iterate the configured model folders and evaluate each model found.
def main():
    for folder in MODEL_FOLDERS:
        model_path = os.path.join(TRAINING_DIR, folder, 'keras_model.h5')
        if os.path.exists(model_path):
            evaluate_model(model_path, folder)
        else:
            print(f"Modelo no encontrado en: {model_path}")


if __name__ == "__main__":
    main()
