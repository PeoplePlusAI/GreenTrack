# 1. Collect and Preprocess Data
# Gather all your icon images (jpeg files) into a single directory.
# Load and preprocess these images: 
# resize them to a consistent size 
# (e.g., 64x64 or 128x128). 
# You may also need to normalize pixel values 
# (scale them between 0 and 1).

# 2. Create a Model
#    You can use a variety of machine learning or deep learning techniques. 
#    For this example, let’s consider using a Convolutional Neural Network (CNN)

import os
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical

# Load icons
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = load_img(os.path.join(folder, filename), target_size=(64, 64))  # Resize to (64, 64)
        img_array = img_to_array(img)
        images.append(img_array)
    return np.array(images)

icons = load_images_from_folder('path_to_icons_folder')
icons = icons.astype('float32') / 255.0  # Normalize
labels = np.ones(len(icons))  # Icons are of the same class

# For negative samples, you would also need a dataset of non-icon images and load them similarly
# non_icons = load_images_from_folder('path_to_non_icons_folder')
# non_icons = non_icons.astype('float32') / 255.0
# non_labels = np.zeros(len(non_icons))  # Non-icons are a different class

# Combine datasets
# X = np.concatenate((icons, non_icons))
# y = np.concatenate((labels, non_labels))

# Split into train and test sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


# 3. Build the CNN model

model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(1, activation='sigmoid'))  # Binary classification

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 4. Train the model

model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# 5. Classify new images 
def classify_image(input_image_path):
    img = load_img(input_image_path, target_size=(64, 64))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize
    prediction = model.predict(img_array)
    return prediction[0][0]  # Returns a probability

result = classify_image('path_to_input_image')
if result > 0.5:
    print("The image is similar to the icons.")
else:
    print("The image is not similar to the icons.")

# 6. Suggestions for Improvements
# Data Augmentation: You might want to enhance your dataset with image augmentations 
# (rotations, flips, brightness adjustments) to improve model robustness.
# Transfer Learning: Consider using a pre-trained model (like VGG16 or ResNet) to 
# leverage existing feature extraction capabilities.
# Evaluation: Ensure to evaluate your model with a proper validation set and metrics 
# beyond accuracy, such as F1-score or confusion matrix, especially for imbalanced datasets.
# This approach should help you build a basic classifier that recognizes whether an 
# input image is similar to your set of icons.