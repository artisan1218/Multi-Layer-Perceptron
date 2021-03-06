import numpy as np
import random

# Create a network
# One layer if composed of a neuron and the weights from previous layer that are connected to this neuron.
def initialize_network(num_inputs, num_hidden, num_outputs):
  network = [] # the neuron network is a list that contains all layers
  hiddenLayer = [] # hiddenLayer list, contains all neurons with weights
  outputLayer = [] # same as above

  for i in range(num_hidden): # loop through all neurons in hidden layer
    # initialize all weights that are connected to the neuron in hidden layer, plus 1 means the bias
    # each neuron is a dict, k is 'weights' and v is the weights values
    # the key 'weights' is actually the weights of neuron i, the value of it is the weights that are connected to it
    hiddenLayerNeuron = {'weights':[random.uniform(-1.0,1.0) for i in range(num_inputs+1)]} 
    hiddenLayer.append(hiddenLayerNeuron) # append neuron to hidden layer list

  for i in range(num_outputs):
    outputLayerNeuron = {'weights':[random.uniform(-1.0,1.0) for i in range(num_hidden+1)]}
    outputLayer.append(outputLayerNeuron)
 
  # connect hidden layer and output layer to form a network
  network.append(hiddenLayer)
  network.append(outputLayer)
  return network

# Feed forward
# neuron activation function
def activate(weights, inputs):
  activationVal = weights[-1] # assume the last weight is bias, since bias is always one, so we can simply use the weight of it to calculate
  for i in range(len(weights)-1): # does not include the last one, which is bias
    activationVal += weights[i] * inputs[i] # weighted sum plus bias
  return activationVal #weighted sum

# def of activation function, we use tanh
def activation_func(activationVal):
  #return np.tanh(activationVal)
  #return 1.0/(1.0 + np.exp(-activationVal))  # sigmoid
  return activationVal / (1+ abs(activationVal))  # softsign function

# feed forward algorithm
# data is a set of input such like [1,1,1,1,1]
def feed_forward(network, data):
  inputs = data
  for layer in network:
    newInputs = [] # the value calculated from activation function
    for neuron in layer:
      # neuron['weights'] gives the value of all weights of that neuron, inputs gives the data value, both are lists
      activationVal = activate(neuron['weights'], inputs) # activationVal is actually weighted sum, inputs are raw data for the first hidden layer and activation value for the rest layers
      neuron['output'] = activation_func(activationVal) # put the weighted sum into activation function and append output to the neuron list, so we can use later
      neuron['weightedSum'] = activationVal
      newInputs.append(neuron['output']) # have a list to store the activation value for next use
    inputs = newInputs # the value coming out of act func is the inputs for the next hidden layer
  
  return inputs

# What we've done above is predicting output, we now need to compute error at output
def activation_func_derivative(output):
  #return 1/(np.cosh(output))**2 # the derivative of tanh function
  #return output * (1 - output)
  return 1/(1+abs(output))**2

def backpropagate(network, expected):  # expected value is only a number, not array. So it only works for the network that generate only 1 output
  for i in reversed(range(len(network))):   # iterate through all the layers in the network, going backwards
    layer = network[i] # get a layer
    errors = [] # error list
    '''
    code below (in the if branch) is to calculate the error at output
    '''
    if i == len(network)-1: # i is the output layer, which is diff from hidden layer
      errorSum = 0
      for j in range(len(layer)):
        neuron = layer[j] # the output neuron, in this case, the only one neuron in the output layer
        errorSum += (expected[j] - neuron['output'])
        #errorSum += 0.5 * pow((expected[j] - neuron['output']),2)
      errors.append(errorSum) # the error, which is the diff bet expected value and the neuron's output, which is the activation value
    else: # i is at hidden layer
      for j in range(len(layer)):  # j is the index of the neuron at that layer
        errorSum = 0 # we want the accumulated errors
        for neuron in network[i+1]: # for the neuron in next layer, which has weights connected to current layer (because you're going backwards)
          errorSum += neuron['weights'][j] * neuron['delta'] # j is the index of the weights in next neuron, which denotes 'each weight in next layer'
        errors.append(errorSum)
    for j in range(len(layer)):
      neuron = layer[j] # jth neuron at ith layer
      neuron['delta'] = errors[j] * activation_func_derivative(neuron['output'])   #pg.14, but learning rate is not included here

# weights update
def weight_update(network, data, learning_rate, momentum):
  for i in range(len(network)):
    inputs = data # get the data
    deltaWeight = [] # list to hold the deltaweight value used for momentum
    if i != 0: # for the hidden layer
      '''
      The inputs for the neurons in hidden layer are output of the neurons in previous layer. 
      So we replace the inputs with the output of neurons from previous layer, which denoted by network[i-1]
      '''
      inputs = [neuron['output'] for neuron in network[i - 1]] 
    for neuron in network[i]: 
      for j in range(len(inputs)): # weight update for neurons
        deltaWeight.append(learning_rate * neuron['delta'] * inputs[j]) 
        '''
        upper one is the weight update with momentum added
        lower one is the weight update without momentum added
        '''
        #neuron['weights'][j] += deltaWeight[j] * momentum + learning_rate * neuron['delta'] * inputs[j] # weight update formula for input layer, pg.14
        neuron['weights'][j] += learning_rate * neuron['delta'] * inputs[j]
      '''
      weight update for bias, always has a fixed value of 1. Assume it's the last one.
      upper one is the weight update with momentum added
      lower one is weight update without momentum added
      '''
      #neuron['weights'][-1] += deltaWeight[j] * momentum+learning_rate * neuron['delta'] 
      neuron['weights'][-1] += learning_rate * neuron['delta']

# train the network
def train(network, training_data, expected, learning_rate, momentum):
  epochNum = 1
  isWellTrained = train_one_epoch(network, training_data, expected, learning_rate, epochNum, momentum)
  while isWellTrained is False:
    isWellTrained = train_one_epoch(network, training_data, expected, learning_rate, epochNum, momentum)
    epochNum+=1
  print('The neural network converges at epoch number: ', epochNum, '. Training complete.')


def train_one_epoch(network, epoch, expected, learning_rate, epoch_index, momentum):
  wellTrained = True
  avgError = 0
  for index in range(len(epoch)):
    data = epoch[index]
    outputs = feed_forward(network, data)
    error = abs(expected[index][0] - outputs[0])
    avgError+=error
    if error > 0.05:
      wellTrained = False
    backpropagate(network, expected[index])
    weight_update(network, data, learning_rate, momentum)
  avgError = avgError/32
  if epoch_index % 100 ==0:
    print('This is epoch: ', epoch_index, ', The average error is: ', avgError)
  return wellTrained

# train

training_data = [[-1, -1, -1, -1, -1],
                 [-1, -1, -1, -1,  1],
                 [-1, -1, -1,  1, -1],
                 [-1, -1, -1,  1,  1],
                 [-1, -1,  1, -1, -1],
                 [-1, -1,  1, -1,  1],
                 [-1, -1,  1,  1, -1],
                 [-1, -1,  1,  1,  1],
                 [-1,  1, -1, -1, -1],
                 [-1,  1, -1, -1,  1],
                 [-1,  1, -1,  1, -1],
                 [-1,  1, -1,  1,  1],
                 [-1,  1,  1, -1, -1],
                 [-1,  1,  1, -1,  1],
                 [-1,  1,  1,  1, -1],
                 [-1,  1,  1,  1,  1],
                 [ 1, -1, -1, -1, -1],
                 [ 1, -1, -1, -1,  1],
                 [ 1, -1, -1,  1, -1],
                 [ 1, -1, -1,  1,  1],
                 [ 1, -1,  1, -1, -1],
                 [ 1, -1,  1, -1,  1],
                 [ 1, -1,  1,  1, -1],
                 [ 1, -1,  1,  1,  1],
                 [ 1,  1, -1, -1, -1],
                 [ 1,  1, -1, -1,  1],
                 [ 1,  1, -1,  1, -1],
                 [ 1,  1, -1,  1,  1],
                 [ 1,  1,  1, -1, -1],
                 [ 1,  1,  1, -1,  1],
                 [ 1,  1,  1,  1, -1],
                 [ 1,  1,  1,  1,  1]]

expected = []
for data in training_data:
  oneCount = 0
  for num in data:
    if(num==1):
      oneCount+=1
  if oneCount%2 !=0:
    expected.append([1])
  else:
    expected.append([-1])

momentum = 0.8 
network = initialize_network(num_inputs=5, num_hidden=10, num_outputs=1)
learning_rate = 0.05
train(network, training_data, expected, learning_rate, momentum)

index = -1
for onePiece in training_data:
  test = feed_forward(network, onePiece) 
  index += 1
  print('test: ', test[0], ', expected: ', expected[index][0], ', accuracy: ', (1 - abs(expected[index][0]-test[0]))*100, '%')
