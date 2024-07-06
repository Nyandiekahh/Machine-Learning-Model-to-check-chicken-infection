# -*- coding: utf-8 -*-
"""Copy_of_Generate.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12BGlB79Fm8RKewPvz7_HI7jyRngVP4Mu
"""

from google.colab import drive

try:
  drive.mount('/content/drive')
except ValueError as e:
  if 'must not already contain files' in str(e):
    print("Mountpoint directory is not empty. Clearing it...")
    !rm -rf /content/drive/*
    drive.mount('/content/drive')
  else:
    raise e  # Re-raise other errors

import os
import matplotlib.pyplot as plt

# Path to the folders containing healthy and unhealthy images
healthy_dir = '/content/drive/MyDrive/FP_data/original/healthy'
unhealthy_dir = '/content/drive/MyDrive/FP_data/original/infected'

# Count the number of images in each folder
num_healthy_images = len(os.listdir(healthy_dir))
num_unhealthy_images = len(os.listdir(unhealthy_dir))

# Print the number of images in each original set
print(f"Number of healthy images in the 'original' set: {num_healthy_images}")
print(f"Number of infected images in the 'original' set: {num_unhealthy_images}")

# Create labels and corresponding counts
labels = ['Healthy', 'Unhealthy']
counts = [num_healthy_images, num_unhealthy_images]

# Create bar chart
plt.bar(labels, counts, color=['green', 'blue'])
plt.xlabel('Category')
plt.ylabel('Number of Images')
plt.title('Distribution of Healthy and Unhealthy Images')
plt.show()

import os
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from PIL import Image

# Function to resize image
def resize_image(input_image_path, target_size):
    try:
        image = Image.open(input_image_path)
        if image.size[0] == 0 or image.size[1] == 0:
            return None
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        resized_image = image.resize(target_size)
        return resized_image
    except Exception as e:
        print(f"Error processing image '{input_image_path}': {e}")
        return None

# Set the paths to the folders containing your original images
infected_original_images_path = "/content/drive/MyDrive/FP_data/original/infected"
healthy_original_images_path = "/content/drive/MyDrive/FP_data/original/healthy"

# Set the paths to the folders where you want to save the augmented images
augmented_infected_images_path = "/content/drive/MyDrive/FP_data/Aug/Aug infected"
augmented_healthy_images_path = "/content/drive/MyDrive/FP_data/Aug/Aug healthy"

# Create an instance of the ImageDataGenerator class
datagen = ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest",
    # Rescale images to the range [0, 1]
    rescale=1.0/255.0
)

# Process infected images
for filename in os.listdir(infected_original_images_path):

    input_image_path = os.path.join(infected_original_images_path, filename)
    resized_image = resize_image(input_image_path, (125, 125))

    # Skip if image couldn't be resized
    if resized_image is None:
        print(f"Skipping image '{filename}' due to error during resizing.")
        continue

    # Convert resized image to array and reshape
    img = image.img_to_array(resized_image)
    img = img.reshape((1,) + img.shape)


    if not os.path.exists(augmented_infected_images_path):
        os.makedirs(augmented_infected_images_path)

    # Generate augmented images and save them to the augmented folder
    try:
        i = 0
        for batch in datagen.flow(img, batch_size=1, save_to_dir=augmented_infected_images_path, save_prefix=filename.split(".")[0] + "_aug", save_format="jpg"):
            i += 1
            if i >= 8:  # Generate 8 augmented images for each original image
                break
    except Exception as e:
        print(f"Error generating augmented images for '{filename}': {e}")

# Process healthy images
for filename in os.listdir(healthy_original_images_path):
    # Resize
    input_image_path = os.path.join(healthy_original_images_path, filename)
    resized_image = resize_image(input_image_path, (125, 125))

    # Skip  couldn't be resized
    if resized_image is None:
        print(f"Skipping image '{filename}' due to error during resizing.")
        continue

    # Convert resized image to array and reshape
    img = image.img_to_array(resized_image)
    img = img.reshape((1,) + img.shape)  # Reshape to fit flow method

    # Create a directory for the augmented images if it doesn't exist
    if not os.path.exists(augmented_healthy_images_path):
        os.makedirs(augmented_healthy_images_path)

    # Generate augmented images and save them to the augmented folder
    try:
        i = 0
        for batch in datagen.flow(img, batch_size=1, save_to_dir=augmented_healthy_images_path, save_prefix=filename.split(".")[0] + "_aug", save_format="jpg"):
            i += 1
            if i >= 8:  # Generate 8 augmented images for each original image
                break
    except Exception as e:
        print(f"Error generating augmented images for '{filename}': {e}")

import os

# Define folder paths (adjust as needed)
healthy_original_path = "/content/drive/MyDrive/FP_data/original/healthy"
healthy_augmented_path = "/content/drive/MyDrive/FP_data/Aug/Aug healthy"
infected_original_path = "/content/drive/MyDrive/FP_data/original/infected"
infected_augmented_path = "/content/drive/MyDrive/FP_data/Aug/Aug infected"
test_folder_path = "/content/drive/MyDrive/FP_data/Test folder"

# Define all folders to consider
folders = [
    healthy_original_path,
    healthy_augmented_path,
    infected_original_path,
    infected_augmented_path
]

# Create the test folder if it doesn't exist
os.makedirs(test_folder_path, exist_ok=True)

# Loop through each folder
for folder in folders:
    # Get all image filenames from the current folder
    filenames = [
        f for f in os.listdir(folder) if f.endswith((".jpg", ".png"))
    ]

    # Randomly select 20% of the filenames
    num_to_select = int(0.2 * len(filenames))
    selected_filenames = random.sample(filenames, num_to_select)

    # Move the selected images to the test folder
    for filename in selected_filenames:
        source_filepath = os.path.join(folder, filename)
        dest_filepath = os.path.join(test_folder_path, filename)
        os.rename(source_filepath, dest_filepath)

    print(f"Moved {len(selected_filenames)} images from {folder} to test folder.")

import os
import matplotlib.pyplot as plt

# Define paths to folders
folder_paths = [
    '/content/drive/MyDrive/FP_data/Train/T_healthy',
    '/content/drive/MyDrive/FP_data/Train/T_infected',
    '/content/drive/MyDrive/FP_data/Train/not_recognized',
    '/content/drive/MyDrive/FP_data/original/healthy',
     '/content/drive/MyDrive/FP_data/original/infected',
    '/content/drive/MyDrive/FP_data/Aug/Aug infected',
    '/content/drive/MyDrive/FP_data/Aug/Aug healthy',
    '/content/drive/MyDrive/FP_data/Test folder'
]

# Count the number of images in each folder
num_images = [len(os.listdir(folder)) for folder in folder_paths]

# Labels for each folder
labels = [
    'T_healthy', 'T_infected','not_recognized',
    'Original Healthy',
    'Original Infected','Augmented Infected', 'Augmented Healthy',
    'Test Folder'
]

# Print the number of images in each folder
for label, num in zip(labels, num_images):
    print(f"Number of images in {label}: {num}")

# Create bar chart
plt.figure(figsize=(10, 6))
plt.bar(labels, num_images, color=['red', 'red', 'red', 'green', 'green', 'blue', 'blue','black'])
plt.xlabel('Folder')
plt.ylabel('Number of Images')
plt.title('Distribution of Images Across Folders')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def sample_visualization():
    # Paths for Train data
    train_healthy_path = "/content/drive/MyDrive/FP_data/Train/T_healthy"
    train_infected_path = "/content/drive/MyDrive/FP_data/Train/T_infected"
    train_not_recognized_path = "/content/drive/MyDrive/FP_data/Train/not_recognized"

    # Paths for Original data
    original_healthy_path = "/content/drive/MyDrive/FP_data/original/healthy"
    original_infected_path = "/content/drive/MyDrive/FP_data/original/infected"

    train_healthy_sample_path = os.path.join(train_healthy_path, os.listdir(train_healthy_path)[0])
    train_healthy_sample_img = mpimg.imread(train_healthy_sample_path)

    train_infected_sample_path = os.path.join(train_infected_path, os.listdir(train_infected_path)[0])
    train_infected_sample_img = mpimg.imread(train_infected_sample_path)

    train_not_recognized_sample_path = os.path.join(train_not_recognized_path, os.listdir(train_not_recognized_path)[0])
    train_not_recognized_sample_img = mpimg.imread(train_not_recognized_sample_path)

    original_healthy_sample_path = os.path.join(original_healthy_path, os.listdir(original_healthy_path)[0])
    original_healthy_sample_img = mpimg.imread(original_healthy_sample_path)

    original_infected_sample_path = os.path.join(original_infected_path, os.listdir(original_infected_path)[0])
    original_infected_sample_img = mpimg.imread(original_infected_sample_path)

    # Plot side by side
    plt.figure(figsize=(16, 8))

    # Plotting Train data samples
    plt.subplot(2, 3, 1)
    plt.imshow(train_healthy_sample_img)
    plt.title('Train Healthy Sample')
    plt.axis('off')

    plt.subplot(2, 3, 2)
    plt.imshow(train_infected_sample_img)
    plt.title('Train Infected Sample')
    plt.axis('off')

    plt.subplot(2, 3, 3)
    plt.imshow(train_not_recognized_sample_img)
    plt.title('Train Not Recognized Sample')
    plt.axis('off')

    # Plotting Original data samples
    plt.subplot(2, 3, 4)
    plt.imshow(original_healthy_sample_img)
    plt.title('Original Healthy Sample')
    plt.axis('off')

    plt.subplot(2, 3, 5)
    plt.imshow(original_infected_sample_img)
    plt.title('Original Infected Sample')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

sample_visualization()



import os
from PIL import Image, ImageFilter, UnidentifiedImageError
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import secrets
from tensorflow.keras import optimizers

# Directory paths
parent_directory = r"/content/drive/MyDrive/FP_data/Train"
model_path = os.path.join(r"/content/drive/MyDrive/FP_data/model",'chicken_predictor.h5')
test_data = r"/content/drive/MyDrive/FP_data/Test folder"



# Image Processing
def filter_img(scaled_img):
    boxblurred_img_5 = scaled_img.filter(ImageFilter.BoxBlur(5))
    boxblurred_img_20 = scaled_img.filter(ImageFilter.BoxBlur(20))
    gaussianblurred_img = scaled_img.filter(ImageFilter.GaussianBlur(20))
    return boxblurred_img_5, boxblurred_img_20, gaussianblurred_img

def scale_img(raw_img_path):
    with Image.open(raw_img_path) as img:
        transposed_img = img.rotate(180, expand=True)
        img_list = [transposed_img.rotate(angle, expand=True) for angle in [0, 45, 90, 135, 180, 225]]
        filtered_img_list = [filter_img(image) for image in img_list]
    return filtered_img_list

import matplotlib.pyplot as plt
from tensorflow.keras.regularizers import l1, l2

def create_and_train_cnn(data_directory=parent_directory, target_size=(128, 128), epochs=25,dropout_rate=0.5, l1_reg=0.01, l2_reg=0.01):
    # Data augmentation and preprocessing
    train_data_gen = ImageDataGenerator(
        rescale=1./255,
        brightness_range=[0.5, 1.5],

        validation_split=0.2
    )

    train_data = train_data_gen.flow_from_directory(
        data_directory,
        target_size=target_size,
        batch_size=32,
        class_mode='categorical',
        subset="training"
    )

    validation_data = train_data_gen.flow_from_directory(
        data_directory,
        target_size=target_size,
        batch_size=32,
        class_mode='categorical',
        subset="validation"
    )

    # Model architecture
    model = Sequential([
         layers.Conv2D(64, (3, 3), activation='relu', input_shape=(target_size[0], target_size[1], 3), kernel_regularizer=l2(l2_reg)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu', kernel_regularizer=l2(l2_reg)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(256, (3, 3), activation='relu', kernel_regularizer=l2(l2_reg)),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(256, activation='relu', kernel_regularizer=l2(l2_reg)),
        layers.Dropout(dropout_rate),
        layers.Dense(128, activation='relu', kernel_regularizer=l2(l2_reg)),
        layers.Dropout(dropout_rate),
        layers.Dense(3, activation='softmax')
    ])

    # Model compilation
    model.compile(optimizer=optimizers.Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

    # Learning rate reduction callback
    lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-7)

    # Early stopping callback
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)


    # Model training
    history = model.fit(
        train_data,
        epochs=epochs,
        validation_data=validation_data,
        steps_per_epoch=len(train_data),
        validation_steps=len(validation_data),
        callbacks=[lr_scheduler]
    )

    # Save the trained model
    model.save(model_path)

    # Visualize training
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training and Validation Loss')
    plt.legend()

    plt.show()

    return model



# Prediction function
def predict_image_state(image_path, model):
    try:
        if os.path.exists(image_path):
            img = Image.open(image_path)
            img = img.resize((128, 128))
            img = np.array(img) / 255.0
            img = np.expand_dims(img, axis=0)

            prediction = model.predict(img)

            class_index = np.argmax(prediction)
            if class_index == 0:
                return "Healthy"
            elif class_index == 1:
                return "Infected"
            else:
                return "Not Chicken"
    except (UnidentifiedImageError, OSError):
        os.remove(image_path)

def train_predict():
    if input('Train Data? [y/n] ').lower() == 'y':
        trained_model = create_and_train_cnn()
    else:
        trained_model = load_model(model_path)

    # Renaming test images
    for item in os.listdir(test_data):
        image_path = os.path.join(test_data, item)
        os.rename(image_path, os.path.join(test_data, f'{secrets.token_urlsafe(16)}.jpg'))

    # Predicting and renaming images
    for index, image in enumerate(os.listdir(test_data)):
        image_path1 = os.path.join(test_data, image)
        image_code = predict_image_state(image_path1, trained_model)
        if os.path.exists(image_path1):
            print(f'{image} status: {image_code}')
            new_path = os.path.join(test_data, f'{image_code}[{index}].jpg')
            os.rename(image_path1, new_path)

train_predict()

import os
import tensorflow as tf

# Define paths
model_path_h5 = os.path.join("/content/drive/MyDrive/FP_data/model", 'chicken_predictor.h5')
model_path_tflite = os.path.join("/content/drive/MyDrive/FP_data/new_model", 'new_model.tflite')

# Load the model
model = tf.keras.models.load_model(model_path_h5)

# Convert the model to TFLite format
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the TFLite model
with open(model_path_tflite, 'wb') as f:
    f.write(tflite_model)