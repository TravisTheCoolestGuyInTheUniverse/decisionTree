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
