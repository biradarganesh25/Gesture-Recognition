import random

# Creating a good dataset from all the files avaliable.
# Ensuring that an equal mix of all the ten gestures in random order
# are used in the training set to avoid overtraining the classifier
# on any one gesture.

def take_equal_examples():
    print "Enter the numbers for training, separated with commas:"
    labels = raw_input('>')
    labels = labels.split(',')
    training_file = open('training_selected.txt', 'w')
    testing_file = open('testing_selected.txt', 'w')
    for label in labels:
        label_file = open(label + '.txt', 'r')
        data_label = label_file.read().split("\n")
        total_length = len(data_label)
        training_length = .7 * total_length # Using 70 percent as the training examples.
        for i in range(0, total_length - 1):
            if i < training_length:
                training_file.write(data_label[i] + "\n")
            else:
                testing_file.write(data_label[i] + "\n")
        label_file.close()

    training_file.close()
    testing_file.close()

def randomize(source_file, target_file): # Randomizing the test data so that the model is without bias.
    with open(source_file, 'r') as source:
        data = [(random.random(), line) for line in source]
    source.close()
    data.sort()

    with open(target_file, 'w') as target:
        for _, line in data:
            target.write(line)
    target.close()


take_equal_examples()
randomize('training_selected.txt', 'training_selected_random.txt')
randomize('testing_selected.txt', 'testing_selected_random.txt')