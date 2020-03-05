import csv
import math


POSITIVE = "Yes"
NEGATIVE = "No"


class example:
    def __init__(self, alt, bar, fri, hun, pat, price, rain, res, type, est, willWait):
        self.attributes = {"alt":alt, "bar":bar, "fri":fri, "hun":hun, "pat":pat,\
        "price":price, "rain":rain, "res":res, "type":type, "est":est, "willWait":willWait}

class tree:
    def __init__(self, node):
        #node will be attribute unless it is leaf, in which case it will be yes or no
        self.node = node
        #connections are values of attribute along with a connection to another node
        self.connections = []
        self.parent = None
        self.valueToParent = None

    def addConnection(self, branch, value):
        self.connections.append((branch, value))
        branch.parent = self.node
        branch.valueToParent = value

    def printTree(self):
        print(f'{self.node} Parent: {self.parent} value: {self.valueToParent}')
        for connection in self.connections:
            connection[0].printTree()


    def treeLearningAlgorithm(self, examples, attributes, parentExamples):
        if examples == []:
            return self.pluralityValue(parentExamples)
        elif self.allSameClassification(examples):
            return tree(examples[0].attributes["willWait"])
        elif attributes == set():
            return self.pluralityValue(examples)
        else:
            A = self.importance(attributes, examples)
            tre = tree(A)
            #print(examples[0].attributes)
            values = self.getAttributeValues(examples, A)
            exs = []
            for value in values:
                for example in examples:
                    if example.attributes[A] == value:
                        exs.append(example)
                if A in attributes:
                    attributes.remove(A)
                subtree = self.treeLearningAlgorithm(exs, attributes, examples)
                tre.addConnection(subtree, value)
            return tre




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

    def allSameClassification(self, examples):
        classification = examples[0].attributes["willWait"]
        for example in examples:
            if example.attributes["willWait"] != classification:
                return False
        return True

    def importance(self, attributes, examples):
        posAndNeg = self.numPosNeg(examples)
        p = posAndNeg[0]
        n = posAndNeg[1]
        bestGain = currentGain = 0.0
        bestAttribute = attributes.pop()
        attributes.add(bestAttribute)
        for attribute in attributes:
            currentGain = self.gain(attribute, examples, p, n)
            if currentGain > bestGain:
                bestGain = currentGain
                bestAttribute = attribute
        return bestAttribute




    def gain(self, attribute, examples, p, n):
        return self.entropy(p/(p+n)) - self.remainder(attribute, examples, p, n)

    def entropy(self, input):
        #print(input)
        #if input is 0 or 1, there is no entropy. but when 0 or 1 is input, throws error.
        if input <= 0 or input >= 1:
            return 0
        else:
            return -(input*math.log(input, 2) + (1-input) * math.log(1 - input, 2))

    def remainder(self, attribute, examples, p, n):
        valueCount = self.posNegExampleCount(examples, attribute)
        remainder = 0.0
        for value in valueCount:
            pk = valueCount[value][0]
            nk = valueCount[value][1]
            #print(f'pk: {pk}, nk: {nk}')
            #print(pk / (pk + nk))
            entropy = self.entropy(pk / (pk + nk))
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

    def getAttributeValues(self, examples, attribute):
        values = set()
        for example in examples:
            values.add(example.attributes[attribute])
        return values



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
    readData("restaurant.csv", examples)
    '''for ex in examples:
        print(f'{ex.attributes}')'''

    #print(tree("yeet").pluralityValue(examples).node)
    #print(tree("yeet").allSameClassification(examples))

    #x = tree("yeet").entropy(.99)
    #print(x)
    #print(f'p: {x[0]}, n: {x[1]}')

    """x = tree("yeet").numPosNegForAttributeValue(examples, "pat")
    for key in x:
        print(f'{key}: positive: {x[key][0]}')
        print(f'{key}: negative: {x[key][1]}')"""

    #x = tree("yeet").gain("type", examples, 6, 6)
    #x = tree("yeet").entropy(0.0)
    #print(x)
    attributes = {"alt", "bar", "fri", "hun", "pat",\
    "price", "rain", "res", "type", "est"}
    """x = tree("yeet").importance(attributes, examples)
    print(x)"""

    """x = tree("yeet").getAttributeValues(examples, "willWait")
    for value in x:
        print(value)"""

    x = tree("root").treeLearningAlgorithm(examples, attributes, examples)
    x.printTree()




"""    t = tree("taste")
    t.addConnection("willEat", "sweet")
    t.addConnection("isCoffee", "bitter")
    t.connections[1][0].addConnection("willEat", "Yes")
    t.connections[1][0].addConnection("willNotEat", "No")

    print(t.node) #node
    print(t.connections[0][0].node) #value of first connected node
    print(t.connections[0][1]) #first branch value
    print(t.connections[1][0].node)
    print(t.connections[1][1])
    print(t.connections[1][0].connections[0][0].node)
    print(t.connections[1][0].connections[0][1])
    print(t.connections[1][0].connections[1][0].node)
    print(t.connections[1][0].connections[1][1])"""
