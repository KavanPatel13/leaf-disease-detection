# Leaf Disease Detection using KNN

Machine learning project that detects diseases in apple leaves.

## Supported classes
- `Black_rot`
- `Cedar_rust`
- `Scab`
- `Healthy` 
- `Not_Apple_Leaf` after you add healthy apple leaf images and retrain the model

## Technologies
- Python
- Flask
- OpenCV
- Scikit-Learn
- Bootstrap

## Run the project
```bash
pip install -r requirements.txt
python train_model.py
python app.py
```

## Add a real healthy class
To make "No disease" accurate, add healthy apple leaf images here:

```text
dataset/Healthy/
```

Then retrain:

```bash
python train_model.py
```

The training script now loads every dataset subfolder automatically, so any valid `Healthy` folder will be included in the new model.
