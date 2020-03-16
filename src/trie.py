import heapq
import math

class Node():
	"""The trie node class. 
		Attributes:
			char (char) : The character of the node

			val (int) : The value of the node in the tree. That is how many times this word is seen in the corpus.

			children (List->`Node`) : List of nodes representing children for this node.

	"""
	def __init__(self, idx):
		if idx == 26:
			self.char = ' '
		else:
			self.char = chr(idx + ord('a'))
		self.val = 0
		self.children = [None] * 27



class Trie():
	"""The trie node class. 
		Attributes:
			root (`Node`) : The root node of the tree.

			heap (List->str) : A min heap data structure to store the most frequenty occuring phrases.

			heapsize (int) : Integer variable to store the heap size.

	"""
	def __init__(self):
		self.root = Node(-1)
		self.heap = []
		self.heapsize = 0

	def insert(self, word):
		"""Insert a word into the trie.

		Args:
			word (str) : The word to insert into the Trie.

		Returns:
			No value

		"""
		curr_node = self.root
		for ch in word.lower():
			if ch == ' ':
				ch_index =  26
			else:
				ch_index = ord(ch) - ord('a')
			if curr_node.children[ch_index] is None:
				curr_node.children[ch_index] = Node(ch_index)
			curr_node = curr_node.children[ch_index]
		curr_node.val += 1

	def print_trie(self,root):
		"""Utility function to print the trie.

		Args:
			root (`Node`) : The root node of the tree.

		Returns:
			No value

		"""
		if root is None:
			return
		for idx,child in enumerate(root.children):
			if child is not None:
				print(child.char, child.val)
				self.print_trie(child)

	def traverse_prefix(self, prefix):
		"""Utility function traverse the trie till the prefix.

		Args:
			prefix (str) : The prefix to traverse in the tree.

		Returns:
			curr_node (`Node`) : The node in the tree at the end of the prefix.

		"""
		curr_node = self.root

		for ch in prefix:
			if ch == ' ':
				ch_index =  26
			else:
				ch_index = ord(ch) - ord('a')
			if curr_node.children[ch_index] is None:
				return None
			curr_node = curr_node.children[ch_index]
		return curr_node

	def auto_complete_query(self, prefix, max_count):
		"""Function to return the k most frequenty occuring results given a prefix.

		Args:
			prefix (str) : The prefix to autocomplete.

			max_count (int) : The k most frequenty occuring phrases in the corpus. 
			If 0, it returns all the results for that prefix.

		Returns:
			heap (List->str) : List of the `max_count` frequently occuring phrases in the corpus given the `prefix`.

		"""
		self.heap = []
		if max_count == 0:
			self.heapsize = -math.inf
		else:
			self.heapsize = 0

		curr_node = self.traverse_prefix(prefix)

		if curr_node is None:
			return []

		self.traverse_subtrees(curr_node, max_count, prefix)

		return self.heap

	def traverse_subtrees(self, root, max_count, string_so_far):
		"""Utility function to perform recursive DFS over the tree.

		This function takes a node and performs DFS to find all the valid phrases
		in the subtree of the root node. It maintains a min heap of the size `max_count`
		to maintain the total number of results.

		Args:
			root (`Node`) : Current node while doing DFS.

			max_count (int) : The k most frequenty occuring phrases in the corpus. 
			If 0, it returns all the results for that prefix.
			
			string_so_far (str) : Keeping track of string has been built in the Trie
			to insert into the heap if this string was seen before.


		Returns:
			No value.

		"""
		if root is None:
			return 

		if root.val > 0:
			if self.heapsize < max_count:
				heapq.heappush(self.heap, (root.val,string_so_far))
				self.heapsize += 1
			else:
				heapq.heappushpop(self.heap, (root.val,string_so_far ))

		for idx,child in enumerate(root.children):
			if child is not None:
				self.traverse_subtrees(child, max_count, string_so_far + child.char)

