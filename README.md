# Clasificación de Imágenes de Comida (Transfer Learning)

Este proyecto utiliza modelos de Deep Learning (entrenados con Teachable Machine) para clasificar diferentes tipos de comida u objetos relacionados.

## Estructura del Proyecto

- `training/images/`: Imágenes originales organizadas por categoría (estas son las imágenes que se usaron para entrenar los modelos).
  - `training/images/01_soup`
  - `training/images/02_main`
  - `training/images/03_salad`
  - `training/images/04_dessert`
  - `training/images/05_nofood`
- `training/models/`: Contiene las carpetas con los modelos exportados desde Teachable Machine. Cada subcarpeta incluye `keras_model.h5` y `labels.txt`.
  - Los modelos están organizados en carpetas `model01`, `model02`, `model03`, `model04`, `model05`.
  - Cada carpeta contiene `keras_model.h5` y `labels.txt`.
- `test/`: Imágenes para evaluación (nombres usados para inferir la etiqueta verdadera).
- `evaluate_models.py`: Script para evaluar modelos frente a las imágenes en `test/`.
- `check_tf.py`: Script de utilidad para verificar la instalación de TensorFlow/Keras.

## Cómo reproducir el entrenamiento (Teachable Machine)

1.  Accede a https://teachablemachine.withgoogle.com/ y crea un "Image Project".
2.  Crea las clases y nómbralas: `soup`, `main`, `salad`, `dessert`, `nofood`.
3.  Sube las imágenes desde `training/images/<carpeta_de_clase>` a la clase correspondiente.
    - Por ejemplo, para `soup` sube las imágenes de `training/images/01_soup`.
4.  Entrena el modelo en Teachable Machine.
5.  Exporta el modelo (TensorFlow -> Keras) y coloca el contenido descomprimido en una carpeta dentro de `training/models/`.
    - Ejemplo: `training/models/mi_modelo/keras_model.h5` y `training/models/mi_modelo/labels.txt`.

## Ejecución de la Evaluación

1.  Instala dependencias si es necesario:
```bash
pip install tensorflow pillow numpy
```
2.  Coloca las imágenes de prueba en `test/`.
3.  Nombres de archivo aceptados (para que el script determine la etiqueta verdadera):
   - Prefijo por nombre: `salad_01.jpg`, `main_02.png`, etc.
  - Prefijo numérico: `01_...` -> `soup`, `02_...` -> `main`, `03_...` -> `salad`, `04_...` -> `dessert`, `05_...` -> `nofood`.
     - Ejemplo: `03_mi_ensalada.jpg` será interpretado como `salad`.
4.  Ejecuta la evaluación:
```bash
python evaluate_models.py
```
5.  `evaluate_models.py` leerá las carpetas listadas en la variable `MODEL_FOLDERS` dentro de `training/models/` (por ejemplo `model01`, `model02`, ...) y generará métricas por modelo.

## Requisitos
- Python 3.x
- tensorflow / tf-keras
- pillow
- numpy

## Notas
- Asegúrate de que cada carpeta de modelo en `training/models/` contenga `keras_model.h5`.
- Las imágenes de entrenamiento originales se guardan en `training/images/` para referencia y reproducibilidad.
 - Las imágenes fueron seleccionadas manualmente de Internet y redimensionadas a 224x224px.

## Evalúa uno o varios modelos propios

Si quieres evaluar modelos propios, hazlo desde una única sección: puedes evaluar uno o varios modelos siguiendo estos pasos.

- Opción 1 — Reemplazar el contenido de las carpetas existentes (recomendado):
  - Sustituye los archivos dentro de `training/models/model01`, `model02`, `model03`, `model04`, `model05` por los de tus modelos. Cada carpeta debe contener:
    - `keras_model.h5`
    - `labels.txt` (lista de etiquetas, una por línea, en el orden de salida del modelo)

- Opción 2 — Añadir una carpeta nueva y apuntar solo a ella:
  - Crea `training/models/mi_model/` y coloca `keras_model.h5` y `labels.txt` dentro.

Después, indica qué carpetas evaluar editando la lista `MODEL_FOLDERS` en `evaluate_models.py`. Ejemplos:

```python
# Evaluar solo el modelo en model01
MODEL_FOLDERS = ['model01']

# Evaluar varios modelos (model02 y model05)
MODEL_FOLDERS = ['model02', 'model05']

# Evaluar una carpeta nueva llamada mi_model
MODEL_FOLDERS = ['mi_model']
```

Finalmente ejecuta:

```bash
python evaluate_models.py
```

Con esto puedes evaluar uno o varios modelos desde la misma sección sin duplicar instrucciones.

---
---

English

# Food Image Classification (Transfer Learning)

This project uses Deep Learning models (exported from Teachable Machine) to classify food and related objects.

## Project Structure 

- `training/images/`: Original images organized by category (these were used to train the models).
  - `training/images/01_soup`
  - `training/images/02_main`
  - `training/images/03_salad`
  - `training/images/04_dessert`
  - `training/images/05_nofood`
- `training/models/`: Contains folders with models exported from Teachable Machine. Each subfolder includes `keras_model.h5` and `labels.txt`.
  - Models are organized in folders `model01`, `model02`, `model03`, `model04`, `model05`.
  - Each folder contains `keras_model.h5` and `labels.txt`.
- `test/`: Images used for evaluation (file names are used to infer the ground-truth label).
- `evaluate_models.py`: Script to evaluate models against the images in `test/`.
- `check_tf.py`: Utility script to verify TensorFlow/Keras installation.

## How to Reproduce Training (Teachable Machine)

1. Go to https://teachablemachine.withgoogle.com/ and create an Image Project.
2. Create classes and name them: `soup`, `main`, `salad`, `dessert`, `nofood`.
3. Upload images from `training/images/<class_folder>` to the corresponding class.
   - For example, upload images from `training/images/01_soup` to the `soup` class.
4. Train the model in Teachable Machine.
5. Export the model (TensorFlow -> Keras) and place the extracted content into a folder inside `training/models/`.
   - Example: `training/models/my_model/keras_model.h5` and `training/models/my_model/labels.txt`.

## Running Evaluation

1. Install dependencies if needed:
```bash
pip install tensorflow pillow numpy
```
2. Put your test images into `test/`.
3. Accepted filename formats (used by the script to determine the true label):
   - Name prefix by class: `salad_01.jpg`, `main_02.png`, etc.
   - Numeric prefix: `01_...` -> `soup`, `02_...` -> `main`, `03_...` -> `salad`, `04_...` -> `dessert`, `05_...` -> `nofood`.
     - Example: `03_my_salad.jpg` will be interpreted as `salad`.
4. Run evaluation:
```bash
python evaluate_models.py
```
5. `evaluate_models.py` will read the folders listed in the `MODEL_FOLDERS` variable inside `training/models/` (for example `model01`, `model02`, ...) and will print metrics per model.

## Requirements
- Python 3.x
- tensorflow / tf-keras
- pillow
- numpy

## Notes
- Make sure each model folder in `training/models/` contains a `keras_model.h5` file.
- The original training images are kept in `training/images/` for reference and reproducibility.
 - Images were manually selected from the internet and resized to 224x224px.

## Evaluate one or several custom models

You can evaluate one or multiple custom models from a single unified section. Two simple approaches are supported:

- Option 1 — Replace the contents of existing folders (recommended):
  - Replace the files inside `training/models/model01`, `model02`, `model03`, `model04`, `model05` with your model files. Each folder must contain:
    - `keras_model.h5`
    - `labels.txt` (one label per line, in the order of the model output)

- Option 2 — Add a new folder and point to it:
  - Create `training/models/my_model/` and place `keras_model.h5` and `labels.txt` inside.

Then specify which folders to evaluate by editing the `MODEL_FOLDERS` list in `evaluate_models.py`. Examples:

```python
# Evaluate only the model in model01
MODEL_FOLDERS = ['model01']

# Evaluate multiple models (model02 and model05)
MODEL_FOLDERS = ['model02', 'model05']

# Evaluate a newly added folder called my_model
MODEL_FOLDERS = ['my_model']
```

Finally run:

```bash
python evaluate_models.py
```

This allows you to evaluate one or several models from the same instructions without duplication.

## Additional notes
- If you use a helper script like `run_models.py` or invoke evaluation directly, you may not need to edit `evaluate_models.py`.
- Ensure `labels.txt` matches the model output order (index 0 = first label in `labels.txt`).


