"""
Name: Travis Stop
Class: Artificial Intelligence (CSC 3250)
Professor: Dr. Jason Pittman

Description: given a training set of examples, this program will build a decision
tree for whether or not one should wait to eat at a resturaunt or not. Or at least
that's what it's supposed to do but right now it builds a bad tree that is
inaccurate. The user can then traverse the tree by inputing values for attributes
and see what decision the tree comes to.

the tree learning algorithm used is described in chapter 18.3 of
Artificial Intelligence: A Modern Approach.

This program takes the name of a csv file as input. The csv file should be formatted
such that each row is an example and each column represents values for attributes.
The attributes are: alternate location, bar, friday, hungry, patrons, price, rain,
reservation, type, estimated wait time, and finally the decision whether or not to
wait. The format of each row in the csv file is below:

[alt] [bar] [fri] [hun] [pat] [price] [rain] [res] [type] [est] [willWait]
"""


import csv
import math

#global classification values
POSITIVE = "Yes"
NEGATIVE = "No"

"""
example class that keeps track of data associated with an example.
"""
class example:
    def __init__(self, alt, bar, fri, hun, pat, price, rain, res, type, est, willWait):
        self.attributes = {"alt":alt, "bar":bar, "fri":fri, "hun":hun, "pat":pat,\
        "price":price, "rain":rain, "res":res, "type":type, "est":est, "willWait":willWait}

"""
Tree class: keeps track of a node and connections to other nodes. Implements
functionality to add connections to the tree, print the connections of the tree,
and build a tree from examples.
"""
class tree:
    def __init__(self, node):
        #node will be attribute unless it is leaf, in which case it will be yes or no
        self.node = node
        #connections are values of attribute along with a connection to another node
        self.connections = []
        self.parent = None
        self.valueToParent = None

    """
    adds a connection to another tree or "branch" with a label of value.
    """
    def addConnection(self, branch, value):
        self.connections.append((branch, value))
        branch.parent = self.node
        branch.valueToParent = value

    """
    recursively prints each node in the tree along with their parent and the label
    between them. Useful for drawing the tree that the tree learning algorithm
    generates for trouble shooting.
    """
    def printTree(self):
        print(f'{self.node} Parent: {self.parent} value: {self.valueToParent}')
        for connection in self.connections:
            connection[0].printTree()

    """
    The tree learning algorithm. takes a list of examples and attributes and uses
    them to construct a decision tree. parentExamples can be an empty list.
    Greedy divide and conquer algorithm.
    """
    def treeLearningAlgorithm(self, examples, attributes, parentExamples):
        if examples == []:
            return self.pluralityValue(parentExamples)
        elif self.allSameClassification(examples):
            #print(examples[0].attributes["willWait"])
            #print(f'Classification: {examples[0].attributes["willWait"]}')
            return tree(examples[0].attributes["willWait"])
        elif attributes == []:
            return self.pluralityValue(examples)
        else:
            A = self.importance(attributes, examples)
            tre = tree(A)
            #print(examples[0].attributes)
            values = self.getAttributeValues(examples, A)
            exs = []
            for value in values:
                #print(f'VALUE: {value} ATTRIBUTE: {A}')
                for example in examples:
                    if example.attributes[A] == value:
                        exs.append(example)
                if A in attributes:
                    attributes.remove(A)
                subtree = self.treeLearningAlgorithm(exs, attributes, examples)
                tre.addConnection(subtree, value)
            return tre



    """
    returns a tree of whatever classification is most prevalent among the examples.
    """
    def pluralityValue(self, examples):
        p = n = 0
        for example in examples:
            if example.attributes["willWait"] == POSITIVE:
                p += 1
            elif example.attributes["willWait"] == NEGATIVE:
                n += 1

        if p >= n:
            return tree(POSITIVE)
        else:
            return tree(NEGATIVE)
    """
    determines whether or not all examples in the set of examples
    have the same classification
    """
    def allSameClassification(self, examples):
        classification = examples[0].attributes["willWait"]

        for example in examples:
            if example.attributes["willWait"] != classification:
                #print("RETURNING FALSE")
                return False
        #print("RETURNING TRUE")
        """print()
        for example in examples:
            print(example.attributes)"""

        return True

    """
    determines which attribute yields the most gain and returns it.
    The "greedy" part of the greedy algorithm.
    """
    def importance(self, attributes, examples):
        posAndNeg = self.numPosNeg(examples)
        p = posAndNeg[0]
        n = posAndNeg[1]

        """print(f'p: {p}, n: {n}')
        for example in examples:
            print(example.attributes)
        print()"""

        bestGain = currentGain = -1.0
        bestAttribute = attributes[0]
        for attribute in attributes:
            currentGain = self.gain(attribute, examples, p, n)
            #print(f'attribute: {attribute}, gain: {currentGain}, bestGain: {bestGain}')
            if currentGain >= bestGain:
                bestGain = currentGain
                bestAttribute = attribute
        #print(f'bestAttribute: {bestAttribute}')
        #print()
        return bestAttribute



    """
    given an attribute, a list of examples, and the number of positive and negative
    classifications in the set of examples, calculate the information gain
    of the attribute.
    """
    def gain(self, attribute, examples, p, n):
        return self.entropy(p/(p+n)) - self.remainder(attribute, examples, p, n)

    """
    given a number between 0 and 1 inclusive, calculate entropy (uncertainty of
    value of willWait attribute) and return it.
    """
    def entropy(self, input):
        #print(input)
        #if input is 0 or 1, there is no entropy. but when 0 or 1 is input, throws error.
        if input <= 0 or input >= 1:
            return 0
        else:
            return -(input*math.log(input, 2) + (1-input) * math.log(1 - input, 2))

    """
    given an attribute, set of examples, and the number of positive and negative
    classifications in the set of examples, return the remaining entropy
    after testing the attribute.
    """
    def remainder(self, attribute, examples, p, n):
        valueCount = self.posNegExampleCount(examples, attribute)
        remainder = 0.0
        for value in valueCount:
            pk = valueCount[value][0]
            nk = valueCount[value][1]
            #print(f'value: {value}')
            #print(f'pk: {pk}, nk: {nk}')
            #print(pk / (pk + nk))
            entropy = self.entropy(pk/(pk+nk))
            remainder += ((pk + nk)/(p + n)) * entropy
        return remainder


    """
    finds the number of positive and negative examples
    in set of examples. returns p, n as a tuple
    """
    def numPosNeg(self, examples):
        p = n = 0
        for example in examples:
            if example.attributes["willWait"] == POSITIVE:
                p += 1
            elif example.attributes["willWait"] == NEGATIVE:
                n += 1
        return (p, n)

    """
    given a set of examples and an attribute, count the number of
    positive and negative classifications for each value of an
    attribute. return this as a dictionary where the key is the value of the
    attribute and the value is a list of two numbers: count of positive and
    negative classifications of examples respectively.
    """
    def posNegExampleCount(self, examples, attribute):
        valueCount = {}
        for example in examples:
            value = example.attributes[attribute]
            if valueCount.get(value, False):
                if example.attributes["willWait"] == POSITIVE:
                    valueCount[value][0] += 1
                else:
                    valueCount[value][1] += 1
            elif example.attributes["willWait"] == POSITIVE:
                valueCount[value] = [1, 0]
            else:
                valueCount[value] = [0, 1]
        return valueCount

    """
    given a set of examples and an attribute, return a list of all unique values
    that appear in the set of examples for the given attribute.
    """
    def getAttributeValues(self, examples, attribute):
        values = []
        for example in examples:
            if not (example.attributes[attribute] in values):
                values.append(example.attributes[attribute])
        """print(f'Attribute: {attribute}')
        for value in list(values):
            print(value)"""
        return values

    """
    recursively traverse throgh the tree starting at the root using user input.
    User inputs value of current node(attribute) until a decision is reached.
    """
    def askUser(self, examples):
        if self.node != POSITIVE and self.node != NEGATIVE:
            print(f"Type a value for {self.node}")
            values = self.getAttributeValues(examples, self.node)
            print(f"possible values: [{values}]")
            value = input()
            for connection in self.connections:
                if connection[1] == value:
                    connection[0].askUser(examples)
        else:
            print(f'DECISION: {self.node}!!!')





"""
takes the name of a csv file and an empty list variable as parameters. Reads in
examples and puts them in the list of examples. See top for format of csv file.
"""
def readData(csvName, examples):
    with open(csvName, newline = '') as f:
        reader = csv.reader(f, delimiter = ",")
        for row in reader:
            ex = example(row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip(),\
            row[4].strip(), row[5].strip(), row[6].strip(), row[7].strip(), row[8].strip(),\
            row[9].strip(), row[10].strip())
            examples.append(ex)


if __name__ == "__main__":
    examples = []
    attributes = ["alt", "bar", "fri", "hun", "pat",\
    "price", "rain", "res", "type", "est"]
    csvName = "restaurant.csv"
    #if you want to use your own training sets:
    #print("training data set file name: ", end = "")
    #csvName = input()
    readData(csvName, examples)
    t = tree("").treeLearningAlgorithm(examples, attributes, [])
    t.askUser(examples)
