# import keras packages
# NOTE: To import the keras package you must install tensorflow - which can be found here: https://www.tensorflow.org/install/
import keras as kr

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
with gzip.open('t10k-images-idx3-ubyte.gz', 'rb') as f:
    image_content = f.read()
    
# This opens the label file which is located in our local directory and assigns the read in value to a variable
with gzip.open('t10k-labels-idx1-ubyte.gz', 'rb') as f:
    label_content = f.read()
    
# This opens the training images file which is located in our local directory and assigns the read in value to a variable
with gzip.open('train-images-idx3-ubyte.gz', 'rb') as f:
    train_img = f.read()

# This opens the training label file which is located in our local directory and assigns the read in value to a variable
with gzip.open('train-labels-idx1-ubyte.gz', 'rb') as f:
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

def test_rand():
    from random import randint
    for i in range(10):
        print("Test Number : ", i+1,"\n")
        #Generate a random number between 0-9999 to get a random index
        x = randint(0, 9999)
        print("The random index: ", x, "\n")
        print("The result array: ")
        test = model.predict(test_inputs[x:x+1])
        # Print the result array
        print(test, "\n")
        # Get the maximum value from the machine predictions
        pred_result = test.argmax(axis=1)

        print("The networks prediction: =>> ",  pred_result)
        print("The actual number: =>> ", label_test[x:x+1])
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

menu_options = input("Please Select a menu option: 1 - Test 10 random images from the test set")
if menu_options == '1':
    test_rand()
else:
    exit()