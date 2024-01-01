import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import matplotlib.pyplot as plt
import os

# Load the MNIST dataset
(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()

# Preprocess the data
train_images = train_images.reshape((60000, 28, 28, 1))
test_images = test_images.reshape((10000, 28, 28, 1))

# Normalize the pixel values
train_images, test_images = train_images / 255.0, test_images / 255.0

# Split training data into training and validation sets
validation_images, train_images = train_images[:5000], train_images[5000:]
validation_labels, train_labels = train_labels[:5000], train_labels[5000:]

# Build the CNN model
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')  # 10 classes for MNIST
])

# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
history = model.fit(train_images, train_labels, epochs=5,
                    validation_data=(validation_images, validation_labels))

# Evaluate the model
test_loss, test_acc = model.evaluate(test_images, test_labels)
print(f'Test accuracy: {test_acc}')

# Save the model
model.save('mnist_cnn_model.h5')

# Load the model
loaded_model = tf.keras.models.load_model('mnist_cnn_model.h5')

# Testing the model with an example
def test_model(image_index, model):
    plt.imshow(test_images[image_index].reshape(28, 28), cmap='gray')
    plt.show()
    pred = model.predict(test_images[image_index].reshape(1, 28, 28, 1))
    print(f'Predicted label: {np.argmax(pred)}')
    print(f'Actual label: {test_labels[image_index]}')

test_model(123, loaded_model)  # Test the model with the image at index 123

# Plotting training results
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label='val_accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='loss')
plt.plot(history.history['val_loss'], label='val_loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
# save plot to file
plt.savefig('training_results.png')
plt.show()

# Save training results to a file
if not os.path.exists('training_results'):
    os.makedirs('training_results')

with open('training_results/results.txt', 'w') as f:
    f.write('Training and Validation Results\n')
    f.write('Epochs: 5\n')
    f.write(f'Training Accuracy: {history.history["accuracy"]}\n')
    f.write(f'Validation Accuracy: {history.history["val_accuracy"]}\n')
    f.write(f'Training Loss: {history.history["loss"]}\n')
    f.write(f'Validation Loss: {history.history["val_loss"]}\n')
    f.write(f'Test Accuracy: {test_acc}\n')
