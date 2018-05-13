#!/usr/bin/env python3
#
# How to run: python3 bonus2.py <desired_epoch> <generate_random_weights> <w0> <w1> <w2>
# generate_random_weights: 1 if true, 0 if false
# e.g.: python3 bonus2.py 1000 1
# e.g.: python3 bonus2.py 1000 0 1.2 -0.6 0.3

import sys
import random

# x1, x2, output
training_data = [
[1.0,1.0,1],
[9.4,6.4,-1],
[2.5,2.1,1],
[8.0,7.7,-1],
[0.5,2.2,1],
[7.9,8.4,-1],
[7.0,7.0,-1],
[2.8,0.8,1],
[1.2,3.0,1],
[7.8,6.1,-1],
]

def net(weight_vector, row):
    net = 0
    for i in range(2):
        net = net + (weight_vector[i+1] * row[i]) # w1 * x1 + w2 * x2
    net = net + (1*weight_vector[0]) # net = Σwixi= w1*x1+w2*x2+w0*1
    return(net)

def f(net):
    return (1 if net >= -0.6 else -1)

def update_weights(weights, t, a, row):
    # w = w + learning_rate * (expected - predicted) * x
    l = 0.1
    delta = l * (t-a)
    w = list()
    for i in range(2):
        delta_w = delta * row[i]
        w.append(weights[i] + delta_w)
    w.append(weights[2]*1)
    return(w)

if __name__ == "__main__":
    termination = int(sys.argv[1]) # termination condition

    if sys.argv[2] == '1':
        w0 = random.uniform(-1,1)
        w1 = random.uniform(-1,1)
        w2 = random.uniform(-1,1)
    else:
        w0 = float(sys.argv[3])
        w1 = float(sys.argv[4])
        w2 = float(sys.argv[5])
    initial_weights = [w0, w1, w2]

    weights = initial_weights

    epoch = 0

    counter = 0 # to determine that we converged
    for i in range(termination):
        for i in range(10):
            row = training_data[i]
            # print("row:", i+1)
            # print("weights:", weights, "row_values:", row)
            net_value = net(weights, row)
            a = f(net_value)
            t = row[2]
            # print("net:", net_value, "a:", a, "t:", t)
            # print("error:", sum_error)
            if t != a:
                weights = update_weights(weights, t, a, row)
                # print("Updated weights:", weights)
                counter = 0
            else:
                counter = counter + 1
            # print()
        epoch = epoch + 1
        if counter == 10:
            break
        counter = 0
    print("Resulting weights:", weights)
    print("Counter:", counter)
    print("Epoch:", epoch)
