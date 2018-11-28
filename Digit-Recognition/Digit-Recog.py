# import keras, Matplotlib and tkinter packages
# NOTE: To import the keras package you must install tensorflow - which can be found here: https://www.tensorflow.org/install/
import keras as kr
from keras.preprocessing import image
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

# Create the sequential model
model = kr.models.Sequential()

# Add layers to the model
model.add(kr.layers.Dense(units=1000, activation='linear', input_dim=784))
#model.add(kr.layers.Dense(units=400, activation='relu'))
model.add(kr.layers.Dense(units=10, activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

# Import the gzip and numpy packages
import gzip
import numpy as np

# This opens the images file which is located in our local directory and assigns the read in value to a variable
with gzip.open('data/t10k-images-idx3-ubyte.gz', 'rb') as f:
    image_content = f.read()
    
# This opens the label file which is located in our local directory and assigns the read in value to a variable
with gzip.open('data/t10k-labels-idx1-ubyte.gz', 'rb') as f:
    label_content = f.read()
    
# This opens the training images file which is located in our local directory and assigns the read in value to a variable
with gzip.open('data/train-images-idx3-ubyte.gz', 'rb') as f:
    train_img = f.read()

# This opens the training label file which is located in our local directory and assigns the read in value to a variable
with gzip.open('data/train-labels-idx1-ubyte.gz', 'rb') as f:
    train_lbl = f.read()
    
# Assign the training data set to a numpy array holding all the values in a 28x28 array
train_img = ~np.array(list(train_img[16:])).reshape(60000, 28, 28).astype(np.uint8) / 255.0
# Assign the training label data set to a numpy array
train_lbl =  np.array(list(train_lbl[8:])).astype(np.uint8)

# Assign the data set to a numpy array holding all the values in a 28x28 array
image_test = ~np.array(list(image_content[16:])).reshape(10000, 28, 28).astype(np.uint8) / 255.0

# Assign the label data set to a numpy array
label_test =  np.array(list(label_content[8:])).astype(np.uint8)

# Reshape the 3D array into a 1D array
inputs = train_img.reshape(60000, 784)
test_inputs = image_test.reshape(10000, 784)

# For encoding categorical variables.
import sklearn.preprocessing as pre

# set up the binary encoder
encoder = pre.LabelBinarizer()
# fit the labels into the binary format
encoder.fit(train_lbl)
# Transform the labels to the binary format
outputs = encoder.transform(train_lbl)

# Train the model and assign it to a variable so we can use it to plot our data
model.fit(inputs, outputs, epochs=20, batch_size=100, verbose=1)

def train_nn():
    model.fit(inputs, outputs, epochs=20, batch_size=100, verbose=1)
    
def train_nn_param(eps, batch):
    model.fit(inputs, outputs, epochs=eps, batch_size=batch, verbose=1)

def test_rand():
    from random import randint
    for i in range(10):
        print("Test Number : ", i+1)
        # Generate a random number between 0-9999 to get a random index
        x = randint(0, 9999)
        print("Index in dataset (Randomly generated): ", x)
        test = model.predict(test_inputs[x:x+1])
        # Get the neural networks prediction
        prediction = test.argmax(axis=1)
        print("The networks prediction: ====> ",  prediction)
        print("The actual number: ====> ", label_test[x:x+1])
        if(prediction == label_test[x:x+1]):
            print("Correct!")
        else:
            print("Incorrect")
        print("--------------------------------------------\n")
        
def test_rand_param(loopSize):
    from random import randint
    for i in range(loopSize):
        print("Test Number : ", i+1)
        # Generate a random number between 0-9999 to get a random index
        x = randint(0, 9999)
        print("Index in dataset (Randomly generated): ", x)
        test = model.predict(test_inputs[x:x+1])
        # Get the neural networks prediction
        prediction = test.argmax(axis=1)
        print("The networks prediction: ====> ",  prediction)
        print("The actual number: ====> ", label_test[x:x+1])
        if(prediction == label_test[x:x+1]):
            print("Correct!")
        else:
            print("Incorrect")
        print("--------------------------------------------\n")
        
# input file adapted from https://stackoverflow.com/questions/9319317/quick-and-easy-file-dialog-in-python
def upload_image():
    root = tk.Tk()
    root.withdraw()
    # Open the GUI for the user to select an image
    file_path = filedialog.askopenfilename()
    # Convert image to prefered size
    uploaded_image = image.load_img(path=file_path,color_mode = "grayscale",target_size=(28,28,1))
    # Convert image into numpy array
    img_data = np.array(list(image.img_to_array(uploaded_image))).reshape(1, 784).astype(np.uint8) / 255.0
    # Predict the number on the image
    img_predict = model.predict(img_data)
    # Print prediction
    print("Nerual networks prediction: ", img_predict.argmax(axis=1))

menu_options = input("Please Select a menu option: \n1 - Test 10 random images from the test set. \n2 - Test a given number of random images from the test set. \n3 - Retrain the neural network. \n4 - Retrain the neural network with your own epoch and batch_size values. \n5 - Upload an image to be recognised. \n-1 to exit")
while menu_options != '-1':    
    if menu_options == '1':
        test_rand()
    elif menu_options == '2':
        loopSize = input("Enter the amount of numbers you wish to test:")
        test_rand_param(int(loopSize))
    elif menu_options == '3':
        train_nn()
    elif menu_options == '4':
        eps = input("Enter the number of iterations: ")
        batch = input("Enter a Batch Size: ")
        train_nn_param(int(eps), int(batch))
    elif menu_options == '5':
        upload_image()
        
    menu_options = input("\nPlease Select a menu option: \n1 - Test 10 random images from the test set. \n2 - Test a given number of random images from the test set. \n3 - Retrain the neural network. \n4 - Retrain the neural network with your own epoch and batch_size values. \n5 - Upload an image to be recognised. \n-1 to exit")

exit()