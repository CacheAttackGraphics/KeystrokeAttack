import sys
from encoder import _reverse

#length of the password: n
#possible guesses in each position: k (calculated based on the probability distribution obtained from the classifier)
#fix the positions with the highest probability first (this can be the improvement on the number of guesses)--to be implement afterwards
#pick the possible words from the dictionary
#match the perfect guess, return the number of guesses -- This is for the ground truth. 
#worst case will be the number of combinations of characters
#brute force is 26^8

import pandas as pd
from collections import defaultdict
from dict_search_rnd import dict_search
from random import randint,shuffle
from encoder import charName

names=['inst#','actual','pred','error','0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
filename = "passwd_10k.txt"
symbols = ['?','#','*','.','&','-','+','_','!','\\']
file_out = open('results_random.csv','w')
#This function returns the list of passwords I want to break
def generateRandomWords():
  words = []
  with open(filename, 'r') as fp:
    rows = fp.readlines()
    for a_row in rows:
      flag = True
      for a_char in a_row:
        if a_char in symbols:
          flag = False 
      if flag == True:
        words.append(a_row.strip())
  #print(words)
  return words

print(names[4:])
words = generateRandomWords()

word_given = ""
for p_word in words:
  p_word = p_word.lower()
  print(p_word)
  keys = []
  x = names[4:]
  shuffle(x)
  for a_char in p_word:
    keys.append(x)  

  #print(keys)
  x = [ keys[i].index(p_word[i]) for i in range(len(p_word))]
  print(x)
  ret = 0

  for i in range(len(p_word)):
    z = 1
    for j in range(i+1,len(p_word)):
      z = z * len(keys[j])
    ret += x[i] * z
    print(z,x[i],ret)
    
  file_out.write(p_word.lower()+","+str(ret)+"\n")