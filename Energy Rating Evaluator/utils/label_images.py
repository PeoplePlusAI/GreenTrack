import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.models import Model
from sklearn.cluster import KMeans
import numpy as np
import os
import glob
from tqdm import tqdm
import pandas as pd
import yaml

# Function to load and preprocess images
def load_and_preprocess_image(img_path, target_size=(224, 224)):
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=target_size)
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

# Function to extract features for each image
def extract_features(df):
    # Load pre-trained VGG16 model + higher level layers
    base_model = VGG16(weights='imagenet')
    model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)
    
    features = []
    for img_path in df['Image Path']:
        img = load_and_preprocess_image(img_path)
        feature = model.predict(img)
        features.append(feature[0])
    return features

# Function to generate labels
def generate_labels(features, index_to_label_mapping):
    labels = np.full(len(features), np.nan)
    for index, label in index_to_label_mapping.items():
        feature_to_match = features[index]
        for i, feature in enumerate(features):
            if np.array_equal(feature, feature_to_match):
                labels[i] = label
    return labels

# Function to implement the complete process
def process_images_and_generate_labels(csv_path, config_path):
    # Read the config.yml file
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    # Get the mapping from the config
    index_to_label_mapping = config['index_to_label_mapping']

    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Extract features
    features = extract_features(df)

    # Generate labels
    labels = generate_labels(features, index_to_label_mapping)

    # Add labels to dataframe
    df['Star Rating'] = labels

    return df

# Example usage
if __name__ == "__main__":
    csv_path = '../resources/test_csvs/Ceiling Fan - Star Rating List_combined_output.csv'
    config_path = 'config.yml'

    # Process the images and generate labels
    df_with_labels = process_images_and_generate_labels(csv_path, config_path)
    display(df_with_labels.head())
