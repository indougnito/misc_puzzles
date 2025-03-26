#!/usr/bin/env python3

'''
  Permutation lookup service. Accepts an input string, and returns all known permutations of that string
  from an internal word list file.

  At startup, loads a word list file into a dictionary (hash table) as follows:
  - each key is a character-sorted string.
  - each value is the list of permutations of that string from the word list file.

  Subsequently, this dictionary supports O(1) lookup of known permutations of an input string.
'''

import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

'''
  This is the data map for the permutation lookup service.
  Each key is a character-sorted string.
  Each value is a list of permutations of that key string as loaded from the word list file.
'''
lookup_data = {} # init empty; to be populated at application startup

'''
  Sorts the characters of an input string, and returns the sorted string.
'''
def sort_string_alphabetically(input_string):
    char_list = list(input_string)
    sorted_chars = sorted(char_list)
    sorted_string = ''.join(sorted_chars)
    return sorted_string

'''
  Loads the provided word list file into memory. Space complexity is O(N), where N=line count.
'''
def load_word_list(file):
  with open(file, 'r') as file:
    for line in file:
      key = sort_string_alphabetically(line)
      key = key.strip() # remove any leading or trailing whitespace
      value = line.strip()
      if key in lookup_data:
        lookup_data[key].append(value)
      else:
        lookup_data[key] = [value]

'''
  Given a word, returns all permutations of that word from the data map. Lookup time complexity is O(1).
'''
def get_permutations(word):
  key = sort_string_alphabetically(word)
  permutations = lookup_data.get(key, [])
  return permutations

'''
  HTTP Request Handler for the permutation lookup service.
'''
class PermutationLookupHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    parsed_url = urlparse(self.path)
    path = parsed_url.path
    params = parse_qs(parsed_url.query)
    if path == '/permutations':
      if not 'word' in params:
        self.bad_request('Missing required query parameter: word')
      else:
        word = params['word'][0]
        permutations = get_permutations(word)
        message = str(permutations)
        self.success(message)
    else:
      self.not_found(f'Endpoint not found: {path}')

  def success(self, message):
    self.respond(200, message)
  
  def not_found(self, message):
    self.respond(404, message)

  def bad_request(self, message):
    self.respond(400, message)

  def respond(self, response_code, message):
    self.send_response(response_code)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    self.wfile.write(message.encode())

'''
  Main function. Takes command line arguments and launches the web server.
'''
def main(args):
  print(f'Hello, {args.file}!')
  load_word_list(args.file)
  print(f'Lookup data is {lookup_data}')
  port = 8000
  httpd = HTTPServer(('localhost', port), PermutationLookupHandler)
  print(f"Serving on port: {port}")
  httpd.serve_forever()

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Runs a web service on port 8000 that provides permutation lookup.')
  parser.add_argument("-f", "--file", required=True, help="word list file")
  args = parser.parse_args()
  main(args)
