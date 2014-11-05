#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
keywords=['auto','int','double','long','char','float','short','signed','unsigned','struct','union','enum','static',
'switch','case','default','break','register','const','volatile','typedef','extern','return','void','continue',
'do','while','if','else','for','goto','sizeof']
seperatelist=['{', '}', '[', ']', '(', ')', '~', ',', ';', '.', '#', '?', ':']
oplist=['<<', '>>', '<', '<=', '>', '>=', '=', '==', '|', '||', '|=', '^', '^=', '&', '&&', '&=', '%', '%=', '+', '++', '+=', '-', '--', '-=', '/', '/=', '*', '*=', '!', '!=']
oct_list= ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e']
ES_list = ['\\', 't', 'a', 'b', 'f', 'n', 'r', 't', 'v', '\'', '\"', '0']
dict_id = {'|=': '56', '>=': '51', '>>': '47', '*=': '73', 'int': '5', '++': '65', '<<': '46', 'float': '4', ',': '40', 'char': '1', '&=': '61', 'static': '28', '/': '70', 'sizeof': '30', '!=': '75', 'id': '=', 'if': '18', '!': '74', '\'': '75', '\"': '76','typedef': '31', 'const': '29', 'struct': '9', 'for': '13', '&': '59', 'union': '10', '(': '37', '+': '64', '*': '72', '-': '67', 'unsigned': '11', 'long': '6', '.': '42', 'switch': '21', 'volatile': '32', '//': '100', '^=': '58', ';': '41', ':': '45', '=': '52', '<': '48', '?': '44', '>': '50', 'do': '14', '<=': '49', 'return': '24', 'goto': '20', '==': '53', 'auto': '25', 'void': '12', 'enum': '3', '#': '43', 'else': '19', 'break': '16', '/=': '71', '*/': '102', '&&': '60', 'extern': '26', '%': '62', '[': '35', ']': '36', '^': '57', 'case': '22', '%=': '63', '||': '55', 'short': '7', '/*': '101', 'default': '23', 'double': '2', '--': '68', 'register': '27', 'signed': '8', ')': '38', 'while': '15', 'continue': '17', '-=': '69', '{': '33', '}': '34', '|': '54', '+=': '66', '~': '39', 'number': '91', 'const': '92', 'id':'90'}
opdict = {'==': 'EQ_OP', '*=': 'MUL_ASSIGN', '<=': 'LE_OP', '^=': 'XOR_ASSIGN', '>>': 'RIGHT_OP', '++': 'INC_OP', '<<': 'LEFT_OP', '|=': 'OR_ASSIGN', '&=': 'AND_ASSIGN', '%=': 'MOD_ASSIGN', '--': 'DEC_OP', '/=': 'DIV_ASSIGN', '&&': 'AND_OP', '-=': 'SUB_ASSIGN', '->': 'PTR_OP', '!=': 'NE_OP', '||': 'OR_OP', '+=': 'ADD_ASSIGN', '>=': 'GE_OP'}
result=[]
idmaps = {}
line = 1
col = 0
idnum = 0


'''标准输出格式的函数
'''
def get_std_output(lines):
	global dict_id
	global keywords
	global seperatelist
	global oplist
	global oct_list
	global oct_list
	global ES_list
	global dict_id
	global opdict
	global result
	global idmaps
	global line
	global col
	global idnum
	outputstr = '< '
	if lines[0] in dict_id:
		outputstr += (lines[0]+', '+dict_id[lines[0]]+', '+lines[1])
	elif lines[1] in dict_id:
		outputstr += (lines[0]+', '+dict_id[lines[1]]+', '+lines[1])
	else:
		outputstr += (lines[0]+', '+'?????'+', '+lines[1])
	if (lines[0] == 'IDENTIFIER'):
		outputstr += str(', ' + str(idmaps[lines[1]][0]))
	outputstr += ' >'
	return outputstr

'''文件输出函数
'''

#def fileoutput(filename):
#	fileout=open(filename,'w')
#	error_fileout = open('error'+filename, 'w')
#	id_fileout = open('id'+filename, 'w')
#	number_fileout = open('number'+filename, 'w')
#	sep_fileout = open('sep'+filename, 'w')

#	for key in idmaps.keys():
#		id_fileout.write(key+  ', '+ str(idmaps[key][0]) + ' ' + str(idmaps[key][1]) + '\n')
#	for lines in result:
#		if isinstance(lines, tuple):
#			outputstr = get_std_output(lines)
#			fileout.write(outputstr + '\n')
#		else:
#			fileout.write(lines + '\n')
#		if isinstance(lines, tuple):
#			key = lines[0]
#			#if key == 'id':
#			#	id_fileout.write(lines[0]+  ','+ lines[1]+' ')
			#	id_fileout.write(str(idmaps[lines[1]][0]) + ' ' + str(idmaps[lines[1]][1]) + '\n')
#			if key in seperatelist:
#				sep_fileout.write(lines[0]+  ' , '+ lines[1]+'\n')
#			if key == 'CONSTANT':
#				number_fileout.write(lines[0]+  ' , '+ lines[1]+'\n')
#		else:
#			error_fileout.write(lines+'\n')
#	error_fileout.close()
#	id_fileout.close()
#	number_fileout.close()
#	fileout.close()

'''屏幕输出函数
'''
def stdoutput():
	global dict_id
	global keywords
	global seperatelist
	global oplist
	global oct_list
	global oct_list
	global ES_list
	global dict_id
	global opdict
	global result
	global idmaps
	global line
	global col
	global idnum
	for lines in result:
		if isinstance(lines, tuple):
			outputstr = get_std_output(lines)
			print(outputstr)
		else:
			print(lines)

'''获取标识符以及关键字的函数
'''
def detector(content):
	global dict_id
	global keywords
	global seperatelist
	global oplist
	global oct_list
	global oct_list
	global ES_list
	global dict_id
	global opdict
	global result
	global idmaps
	global line
	global col
	global idnum
	if not content:
		return
	if content in keywords:
		result.append((content,content,(col,line)))
	else:
		if content not in idmaps.keys():
			idmaps[content] = (idnum, line) #记录标识符时也同时记录了标识符对应的行号
			idnum += 1
		result.append(('IDENTIFIER',content,(col,line)))

'''判断变量命名是否符合规范
'''
def isidentify(ch):
	if ch=='_' or str.isalpha(ch):
		return True
	return False


'''注释自动机，识别//以及/*两种注释方式
'''
def is_comment(filein):
	global dict_id
	global keywords
	global seperatelist
	global oplist
	global oct_list
	global oct_list
	global ES_list
	global dict_id
	global opdict
	global result
	global idmaps
	global line
	global col
	global idnum
	tmpline = line
	tmpcol = col
	nextc = filein.read(1)
	tmpcol += 1
	if nextc == '/':
		while 1:
			nextc = filein.read(1)
			tmpcol+= 1
			if nextc == '\n':
				col=0
				line=tmpline+1
				break
		return True
	elif nextc == '*':
		commentlen = 0
		state = 0
		while 1:
			nextc=filein.read(1)
			if not nextc:
				outputstr=str(line)+':'+str(col)+"  "+'unterminated /* comment'
				result.append(outputstr)
				filein.seek(-(commentlen+state),1)
				tmpcol-=(commentlen+state)
				break
			tmpcol+=1
			if nextc == '*':
				state=1
				commentlen+=1
			elif nextc == '/' and state == 1:
				line=tmpline
				col=tmpcol
				break
			else:
				if nextc == '\n':
					tmpcol=0
					tmpline+=1
					commentlen+=1
		return True
	else:
		return False	


'''获取操作符的自动机
'''
def get_operation(c,filein):
	global dict_id
	global keywords
	global seperatelist
	global oplist
	global oct_list
	global oct_list
	global ES_list
	global dict_id
	global opdict
	global result
	global idmaps
	global line
	global col
	global idnum
	nextc=filein.read(1)
	col+=1
	if nextc in oplist:
		opstr=c+nextc
		#if opdict.has_key(opstr):
		#	result.append((opdict[opstr],opstr,(col,line)))
		if opstr in oplist:
			result.append((opstr,opstr,(col,line)))
		else:
			result.append((c,c,(col,line)))
			filein.seek(-1, 1)
			return
	else:
		result.append((c,c,(col,line)))
		filein.seek(-1,1)
		col-=1
	return

'''字符验证的自动机，能识别未闭合的字符，以及字符数超过1的字符
'''
def char_DFA(filein):
	global dict_id
	global keywords
	global seperatelist
	global oplist
	global oct_list
	global oct_list
	global ES_list
	global dict_id
	global opdict
	global result
	global idmaps
	global line
	global col
	global idnum
	nextchar=filein.read(1)
	col+=1
	nextc=filein.read(1)
	col+=1
	if (nextc=='\''):
		#result.append((nextc,nextc,(col,line)))
		result.append(('CONST_CHAR',nextchar,(col,line)))
		#result.append((nextc,nextc,(col,line)))
	else:
		outputstr=str(line)+':'+str(col)+"  "+'error: unknown character'
		result.append(outputstr)
		filein.seek(-2,1)
		col-=2
	return


'''字符串验证的自动机，能识别未闭合的字符串
'''

def string_DFA(filein):
	global dict_id
	global keywords
	global seperatelist
	global oplist
	global oct_list
	global oct_list
	global ES_list
	global dict_id
	global opdict
	global result
	global idmaps
	global line
	global col
	global idnum
	tmpcol = col
	tmpline = line
	string = ''
	flag = 0
	while 1:
		nextc=filein.read(1)
		if not nextc:
			break
		col += 1
		if nextc=='\"':
			#result.append((nextc,nextc,(col,line)))
			result.append(('CONST_STRING',string,(col,line)))
			#result.append((nextc,nextc,(col,line)))
			flag = 1
			col = tmpcol
			line = tmpline
			break
		else:
			if (nextc == '\n'):
				tmpcol = 0
				tmpline += 1
			string += nextc
	if not flag == 1:
		outputstr=str(line)+':'+str(col)+"  "+'error: missing terminating \'\"\' character'
		result.append(outputstr)
		filein.seek(-len(string),1)
	return

'''识别科学计数法的自动机
'''
def scientific_num_DFA(num, filein):
	global dict_id
	global keywords
	global seperatelist
	global oplist
	global oct_list
	global oct_list
	global ES_list
	global dict_id
	global opdict
	global result
	global idmaps
	global line
	global col
	global idnum
	state = 0
	while True:
		nextc = filein.read(1)
		col += 1
		if nextc in ['-', '+'] and state == 0:
			state = 1
			num += nextc
		elif str.isdigit(nextc):
			num += nextc
		else:
			result.append(('CONST_INT', num,(col,line)))
			filein.seek(-1, 1)
			col -= 1
			return
'''识别10进制整数以及小数的自动机
'''
def number_DFA(c, filein):
	global dict_id
	global keywords
	global seperatelist
	global oplist
	global oct_list
	global oct_list
	global ES_list
	global dict_id
	global opdict
	global result
	global idmaps
	global line
	global col
	global idnum
	num = str(c)
	mode = 0
	while True:
		nextc = filein.read(1)
		col += 1
		if (str.isdigit(nextc)):
			num += nextc
		elif (nextc == '.' and mode == 0):
			mode = 1
			num += nextc
		elif (nextc == 'f' and mode == 1):
			num +=nextc
			result.append(('CONST_INT', num,(col,line)))
			return
		elif (nextc == 'e'):
			num += nextc
			scientific_num_DFA(num, filein)
			return

		else:
			col -= 1
			result.append(('CONST_INT', num,(col,line)))
			filein.seek(-1,1)
			return


'''识别16进制整数的自动机
'''
def hex_DFA(filein):
	global dict_id
	global keywords
	global seperatelist
	global oplist
	global oct_list
	global oct_list
	global ES_list
	global dict_id
	global opdict
	global result
	global idmaps
	global line
	global col
	global idnum
	num = '0x'
	errorflag = 0
	while True:
		nextc = filein.read(1)
		col += 1
		if str.isdigit(nextc) or (nextc in oct_list):
			num += nextc
		elif nextc in seperatelist or nextc in oplist:
			col -= 1
			if (errorflag == 0):
				result.append(('CONST_INT', num,(col,line)))
			else:
				outputstr = str(line)+':'+str(col)+"  "+'illegal hex number'
				result.append(outputstr)
				filein.seek(-1, 1)
			return
		else:
			errorflag = 1
			num += nextc

'''识别8进制整数的自动机
'''
def oct_DFA(c, filein):
	global dict_id
	global keywords
	global seperatelist
	global oplist
	global oct_list
	global oct_list
	global ES_list
	global dict_id
	global opdict
	global result
	global idmaps
	global line
	global col
	global idnum
	errorflag = 0
	num = '0' + c
	while True:
		nextc = filein.read(1)
		col += 1
		if (str.isdigit(nextc) and nextc not in ['8', '9']):
			num += nextc
		elif nextc in seperatelist or nextc in oplist:
			col -= 1
			if (errorflag == 0):
				result.append(('CONST_INT', num,(col,line)))
			else:
				outputstr = str(line)+':'+str(col)+"  "+'illegal oct number'
				result.append(outputstr)
				filein.seek(-1, 1)
			return
		else:
			errorflag = 1
			num += nextc




def doToken(filename):
	global dict_id
	global keywords
	global seperatelist
	global oplist
	global oct_list
	global oct_list
	global ES_list
	global dict_id
	global opdict
	global result
	global idmaps
	global line
	global col
	global idnum
	filein=open(filename,'r')
	tmpstr=''
	while 1:
		c=filein.read(1) #每次读取一个字符
		if not c:
			break
		col+=1
		if c=='\n':
			detector(tmpstr) #换行时清理未处理的变量，以及更新行号以及列号
			tmpstr=''
			col=0
			line+=1
			continue
		elif str.isspace(c):
			detector(tmpstr) #遇到空格时更新标识符
			tmpstr = ''
			continue
		elif c in seperatelist:
			detector(tmpstr)
			tmpstr = ''
			result.append((c,c,(col,line))) #遇到分隔符时更新标识符
			continue
		elif c == '/':
			if (is_comment(filein)): #遇到/跳转到注释自动机
				continue
		elif c == '-': #遇到-，分别处理负数以及减号两种情况
			#print("##############")
			nextc = filein.read(1)
			if (str.isdigit(nextc)):
				filein.seek(-1, 1)
				number_DFA(c, filein)
				continue
			else:
				filein.seek(-1, 1)
		if c in oplist: #跳转到操作符自动机
			detector(tmpstr)
			tmpstr = ''
			get_operation(c,filein)
			continue
		elif c == '\'': #跳转到字符自动机
			char_DFA(filein)
			continue
		elif c == '\"': #跳转到字符串自动机
			string_DFA(filein)
			continue
		elif str.isdigit(c): #跳转到数字自动机
			if not tmpstr:
				nextc = filein.read(1)
				col += 1
				if c == '0' and (nextc in ['x', 'X']):
					hex_DFA(filein)
				elif c == '0' and str.isdigit(nextc):
					oct_DFA(nextc, filein)
				else:
					col -= 1
					filein.seek(-1, 1)
					number_DFA(c, filein)
			else:
				tmpstr+=c
			continue
		elif isidentify(c): 
			tmpstr+=c
			continue
		outputstr = str(line)+':'+str(col)+"  "+'error: illegal character'
		result.append(outputstr)
		#处理非法字符

	return result


	

def main():
	filename=sys.argv[1]
	doToken(filename)
	try:
		if sys.argv[2]:		#第二个参数作为输出文件
			fileoutput(sys.argv[2])
	except IndexError:
		pass
	stdoutput()


if __name__=='__main__':
	main()