import unittest
import sys
sys.path.append('../src')
from src.autocomplete_engine import autocomplete_engine
from src.trie import Trie
from src.trie import Node
from unittest.mock import patch
import io
import sys

class TestAutoCompleteMethods(unittest.TestCase):

	@patch("sys.stdin", io.StringIO("complete, ba, 2\ncomplete, be, 0\n\n"))
	def test_read_input_queries(self):
		engine =  autocomplete_engine('corpus1.txt')
		engine.read_input_queries()
		self.assertEqual(engine.queries, [('ba',2), ('be', 0)])
	
	@patch("sys.stdin", io.StringIO("complete, ba\n\n"))
	def test_read_input_query_failure_1(self):
		engine =  autocomplete_engine('corpus1.txt')
		capturedOutput = io.StringIO()
		sys.stdout = capturedOutput 
		engine.read_input_queries()
		assertString = 'Invalid input : Please use the following format to input a command : "complete, prefix, max_count"\n'
		self.assertEqual(capturedOutput.getvalue(), assertString)

	@patch("sys.stdin", io.StringIO("complete, ba, 1.5\n\n"))
	def test_read_input_query_failure_2(self):
		engine =  autocomplete_engine('corpus1.txt')
		capturedOutput = io.StringIO()
		sys.stdout = capturedOutput 
		engine.read_input_queries()
		assertString = 'Invalid input for "max_count", should only be an integer greater than or equal to 0\n'
		self.assertEqual(capturedOutput.getvalue(), assertString)

	def test_autocomplete_queries(self):
		engine =  autocomplete_engine('corpus1.txt')
		engine.queries = [('ba',1)]
		engine.autocomplete_queries()
		self.assertEqual(engine.results, ['bat'])


	def test_display_results(self):
		engine =  autocomplete_engine('corpus1.txt')
		engine.results = ['bat, bar', 'bark, bat']
		capturedOutput = io.StringIO()
		sys.stdout = capturedOutput         
		engine.display_results()
		sys.stdout = sys.__stdout__    
		self.assertEqual(capturedOutput.getvalue() , 'bat, bar\nbark, bat\n')     


	def test_file_exception(self):
		engine =  autocomplete_engine('corpus1.txt')
		engine.corpus_filename = 'file_does_not_exist.txt'
		with self.assertRaises(FileNotFoundError):
			engine.build_trie()

	

class TestTrieMethods(unittest.TestCase):
	def test_trie_node(self):
		trie_node = Node(15)
		self.assertEqual(trie_node.char, 'p')
		self.assertEqual(trie_node.val, 0)
		self.assertEqual(trie_node.children, [None] * 27)
		
	def test_traverse_prefix(self):
		my_trie = Trie()
		my_trie.insert('bark')
		my_trie.insert('bar')
		trie_node = my_trie.traverse_prefix('bar')
		self.assertEqual(trie_node.char, 'r')
		self.assertEqual(trie_node.val, 1)
		arr = [None] * 27
		arr[10] = Node(10)
		self.assertEqual(trie_node.children[10].char, arr[10].char)
		self.assertEqual(trie_node.children[10].val, 1)

	def test__trie_auto_complete_query(self):
		my_trie = Trie()
		my_trie.insert('bark')
		my_trie.insert('bar')
		my_trie.insert('bark')
		results  = my_trie.auto_complete_query('ba', 2)
		self.assertEqual(results, [(1,'bar'), (2, 'bark')])

if __name__ == '__main__':
	unittest.main()