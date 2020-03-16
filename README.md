# Autocomplete engine

Please use the index.html file in docs/src for a complete documentation.

This particular code returns autocomplete results for queries input by user.
It returns these results based upon the frequency of the phrases appearing in a corpus of text input to the engine.

To run `autocomplete_engine.py` please use the following command from the base directory.

	python3 src/autocomplete_engine.py <corpus_file_path>
To run the unit tests please run the following command :

	python3 -m unittest tests.unittest_autocomplete

This engine has three primary classes. 

1. The driver class `autocomplete_engine` which is used to take corpus file, user input and display the output to the user.
2. The data structure class `Trie` which is used to store the corpus data in the form of a tree.
3. The `Node` class that is used to represent a node in the `Trie`.




### Trie

The choice of data structure used for this was a prefix tree known as Trie. This tree is built from the corpus text file.

1. **Node** : 
 Each node of the trie is represented using the `Node` class which contains a `char` field that stores the character associated at the node. A `val` field that is used to store the number of times a word ends at this node in the corpus and finally a list of 27 elements each potentially representing children nodes (for 26 letters a-z and a space).	Having a list representing each letter speeds up traversals as lookup for a letter becomes constant.


The `Trie` class initializes the tree using the phrases in the corpus and inserts these phrases into the tree. 

To autocomplete a phrase there are two steps which are taken.

1. Traverse the tree till the phrase and return the current node.
2. Perform Depth First Traversal on the subtree from the current node and find all the phrases and their counts.

After finding the phrases we can return the most frequently occuring phrases as per `max_count`. However, this sorting may be time intensive. To make this process faster we maintain a min heap of size `max_count`. At every stage we find a phrase if the phrase has a frequency higher than the top of the min heap we pop the heap and push this phrase onto. This way we will not need to sort the final results and at all stages we will have the top `max_count` occuring phrases in the heap. A disadvantage of using Trie is the amount of space it uses to store data, however the lookup and autocomplete is extremely time efficient.

If the data size increases signficantly this would be time efficient but not space efficient. If space is of concern something like a ternary search tree can be used.

Another form of optimization which can be performed is separating the training and prediction. That is once we have built the Trie we can persist with something like `pickle` and use that to load it later and do auto completion predictions with the saved Trie.


There is another `unittest_autocomplete` module that contains unit testing classes for the `autocomplete_engine` and the `trie`. There are basic test cases checking functionality of user input, stdout, file exception, node initialization, traversing a prefix and auto completing a query.