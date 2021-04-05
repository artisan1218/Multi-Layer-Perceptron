# Multiple-Layer-Perceptron
Python implementation of a simple MLP without using external packages

### Training data and labels
The MLP uses data of a make-up example matrix:
```
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
```
For each list in the matrix, if there are odd number of occurences of 1, then the label should be 1. If there are even number of occurences of 1, then it should be -1.
For example ```[-1, -1, -1, -1, -1]``` should be predicted as -1 because the number of occurences of 1 is 0, which is an even number.

### Training process
For each epoch, first do forward-feeding with the softsign activation func of this form: ![image](https://user-images.githubusercontent.com/25105806/113526095-72819180-956d-11eb-9617-470d327335d4.png), then perform back-propagation, calculate the error and do the weight update. Training will not stop until the error is smaller than 0.05.

### Result: 

![image](https://user-images.githubusercontent.com/25105806/113525719-6563a300-956b-11eb-8905-62176d90b76a.png)
