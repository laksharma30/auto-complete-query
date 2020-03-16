import sys
sys.path.append('../src')
from trie import Trie
import argparse

class autocomplete_engine():

	def __init__(self, corpus_filename):
		"""The autocomplete engine class. 
		Args:
			corpus_filename (String) : The corpus filename for the basis of the autocomplete engine.

			trie (`Trie`) : The trie data structure used to store the phrases in the corpus.

			queries (List) : List of queries to autocomplete.

			results (List) : List of results for each query.
		"""
		self.corpus_filename = corpus_filename
		self.trie = Trie()
		try:
			self.build_trie()
		except FileNotFoundError:
			raise
		self.queries = []
		self.results = []

	def build_trie(self):
		"""
		Build the trie for the phrases in the corpus.

		Returns:
			No Value
		"""
		try:
			with open(self.corpus_filename, 'r+') as f:
				phrases = f.read().splitlines()
		except FileNotFoundError:
			raise
		for phrase in phrases:
			self.trie.insert(phrase)

	def read_input_queries(self):
		"""Read the input queries from the user per line.

		Returns:
			No Value
		"""
		for line in iter(input, ''):
			if len(line.split(',')) != 3:
				print('Invalid input : Please use the following format to input a command : "complete, prefix, max_count"' )
				continue
			command = line.split(',')[0].strip()
			if command != 'complete':
				print('Invalid input : Please use the following format to input a command : "complete, prefix, max_count"' )
				continue
			prefix = line.split(',')[1].lstrip()
			if len(prefix) == 0:
				prefix = ' '
			try:
				max_count = int(line.split(',')[2].strip())
				if max_count < 0:
					raise ValueError
				self.queries.append((prefix, max_count))
			except ValueError:
				print('Invalid input for "max_count", should only be an integer greater than or equal to 0')
		
			

	def autocomplete_queries(self):
		"""
		Get autocomplete results for each query the user has input.

		Returns:
			No Value
		"""
		for query in self.queries:
			result = self.trie.auto_complete_query(query[0], query[1])
			output = [x[1] for x in result]
			output = ', '.join(output)
			self.results.append(output)
			


	def display_results(self):
		"""
		Display autocomplete results for each query the user has input.

		Returns:
			No Value
		"""
		for result in self.results:
			print(result)



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Auto complete query')
	parser.add_argument('corpus_file_name', nargs=1,
					help='The corpus file name for the auto complete engine')
	args = parser.parse_args()
	filename = args.corpus_file_name[0]

	try:
		engine = autocomplete_engine(filename)
	except FileNotFoundError as e:
		print('The corpus file "', filename,'" does not exist.')
		sys.exit(1)

	engine.read_input_queries()
	engine.autocomplete_queries()
	engine.display_results()

