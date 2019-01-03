__author__ = 'Ajaya Neupane'
import os
from collections import defaultdict
import logging
import csv

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def _reverse(classtype):
	if str(classtype) == 'one':
		return '1'
	if str(classtype) == 'two':
		return '2'
	if str(classtype) == 'three':
		return '3'
	if str(classtype) == 'four':
		return '4'
	if str(classtype) == 'five':
		return '5'
	if str(classtype) == 'six':
		return '6'
	if str(classtype) == 'seven':
		return '7'
	if str(classtype) == 'eight':
		return '8'
	if str(classtype) == 'nine':
		return '9'
	if str(classtype) == 'zero':
		return '0'
	else:
		#print(classtype)
		return str(classtype)

def charName(classtype):
	#print(classtype)
	if str(classtype) == '1':
		return 'one'
	if str(classtype) == '2':
		return 'two'
	if str(classtype) == '3':
		return 'three'
	if str(classtype) == '4':
		return 'four'
	if str(classtype) == '5':
		return 'five'
	if str(classtype) == '6':
		return 'six'
	if str(classtype) == '7':
		return 'seven'
	if str(classtype) == '8':
		return 'eight'
	if str(classtype) == '9':
		return 'nine'
	if str(classtype) == '0':
		return 'zero'
	else:
		#print(classtype)
		return str(classtype)