from src.util.DataSetUtil import read_classes, read_train_sets
from src.util.ModelsUtil import createCnnModel, createBigCnnModel, VGG_16, VGG_19
from src.util.VisualisationUtil import createPlot
from src.train.train import start
import os
import configparser
import datetime
import json
from keras.utils import plot_model
from keras.callbacks import CSVLogger


def buildPathToSave():
    now = datetime.datetime.now()
    dir_name = '{}_{}_{}__{}_{}'.format(now.day, now.month, now.year, now.hour, now.minute)
    return '{}/{}'.format(save_dir, dir_name)


# Open properties file
config = configparser.RawConfigParser()
config.read('./resources/application.properties')

# Neural network properties
batch_size = int(config.get('NeuralNetwork', 'batchSize'))
epochs = int(config.get('NeuralNetwork', 'epochs'))
train_path = config.get('NeuralNetwork', 'trainPath')
save_dir = config.get('NeuralNetwork', 'saveDir')
validation_size = float(config.get('NeuralNetwork', 'validationSize'))
img_size = int(config.get('NeuralNetwork', 'imageSize'))
num_channels = int(config.get('NeuralNetwork', 'channels'))

# Loading all classes
classes = read_classes(train_path)
num_classes = len(classes)

# Creating directory to save all data
path_to_save = buildPathToSave()
if not os.path.isdir(path_to_save):
    os.makedirs(path_to_save)

# Saving base information
with open('{}/meta.json'.format(path_to_save), 'w') as f:
    json.dump({'classes': classes, 'img_size': img_size, 'num_channels': num_channels}, f)

# Loading data set
data = read_train_sets(train_path, img_size, classes, validation_size=validation_size)

print("Complete reading input data. Will Now print a snippet of it")
print("Number of files in Training-set:\t\t{}".format(len(data.train.labels)))
print("Number of files in Validation-set:\t{}".format(len(data.valid.labels)))

# open('{}/log.csv'.format(path_to_save),'w').close()
csv_logger = CSVLogger('{}/log.csv'.format(path_to_save), append=True, separator=';')

# Train neural network
input_shape = (img_size, img_size, num_channels)
model, history, score = start(model=createBigCnnModel(input_shape, num_classes),
                              data=data,
                              batch_size=batch_size,
                              epochs=epochs,
                              callbacks=[csv_logger])

# Save model
plot_model(model, to_file='{}/model.png'.format(path_to_save), show_shapes=True, show_layer_names=True)
open('{}/model.json'.format(path_to_save), 'w').write(model.to_json())

# Save model and weights
model_path = os.path.join(path_to_save, 'trained_model.h5')
model.save(model_path)
print('Saved trained model at %s ' % model_path)

# Save plot with training results
createPlot('model accuracy', 'accuracy', path_to_save, history.history['val_acc'], history.history['acc'])
createPlot('model loss', 'loss', path_to_save, history.history['val_acc'], history.history['loss'])
print('Saved plots')


