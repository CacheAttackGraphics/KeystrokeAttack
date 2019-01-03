import sys
from encoder import _reverse

file_out = open('results.csv','a')
def generateWords(keys, l, d, i, cur, cur_val):
  global found
  global count
  if found == 1:
    return cur

  if i == l:
    count = count+1
    if word_given == cur:
      print("we found it",str(count))
      found = 1
    return cur
  
  for j in range(len(keys[i])):
    generateWords(keys, l, d, i + 1, cur + _reverse(keys[i][j]), cur_val + j);

def dict_search(keys,word_given):
  d = [];
  l = len(keys);
  generateWords(keys, l, d, 0, "", 0);
  count = 0

  for a_tuple in d:
    if word_given in a_tuple:
      print("we found it",str(count))
      file_out.write(word_given+","+str(count)+"\n")
      break
    count+=1  


