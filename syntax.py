#! /usr/bin/python
# -*- coding:UTF-8 -*-
import lexer
import sys
import re
import copy
first_dict = {} 
#存储first集的结果
symbol_list = []
#所有终结符以及非终结符的集合
follow_dict = {}
#存储follow集的结果
token_list = []
#存储文法集合
new_grammer_token_list = []
#存储带动作的文法

selected = {}
#存放select集的字典

item_num = 0
#四元式数目

label_num = 0
#标记数目

quaternary_list = []
#四元式列表

labele_dict = {}
#标记字典

#selected_dict = {}
generation_dict = {}
#存储分析表
getin_stack = []
#句法分析的存储栈
result_generation_list = []
#句法分析过程中所有的产生式

value_stack = []
#存储变量的值

#错误信息列表
error_list = []
#terminal_list = ['IDENTIFIER', 'CONSTANT', 'STRING_LITERAL', 'SIZEOF', 'PTR_OP', 'INC_OP', 'DEC_OP', 'LEFT_OP', 'RIGHT_OP', 'LE_OP', 'GE_OP', 'EQ_OP', 'NE_OP', 'AND_OP', 'OR_OP', 'MUL_ASSIGN', 'DIV_ASSIGN', 'MOD_ASSIGN', 'ADD_ASSIGN', 'SUB_ASSIGN', 'LEFT_ASSIGN', 'RIGHT_ASSIGN', 'AND_ASSIGN', 'XOR_ASSIGN', 'OR_ASSIGN', 'TYPE_NAME', 'TYPEDEF', 'EXTERN', 'STATIC', 'AUTO', 'REGISTER', 'CHAR', 'SHORT', 'INT', 'LONG', 'SIGNED', 'UNSIGNED', 'FLOAT', 'DOUBLE', 'CONST', 'VOLATILE', 'VOID', 'STRUCT', 'UNION', 'ENUM', 'ELLIPSIS', 'CASE', 'DEFAULT', 'IF', 'ELSE', 'SWITCH', 'WHILE', 'DO', 'FOR', 'GOTO', 'CONTINUE', 'BREAK', 'RETURN']
terminal_list = ['CONST_INT', 'CONST_FLOAT', 'CONST_CHAR', 'CONST_STRING', 'IDENTIFIER', 'number']
#所有终结符的列表

keyword_list=['auto','int','double','long','char','float','short','signed','unsigned','struct','union','enum','static',
'switch','case','default','break','register','const','volatile','typedef','extern','return','void','continue',
'do','while','if','else','for','goto','sizeof']
#关键字列表

seperatelist=['{', '}', '[', ']', '(', ')', '~', ',', ';', '.', '#', '?', ':']
oplist=['<<', '>>', '<', '<=', '>', '>=', '=', '==', '|', '||', '|=', '^', '^=', '&', '&&', '&=', '%', '%=', '+', '++', '+=', '-', '--', '-=', '/', '/=', '*', '*=', '!', '!=']
#分隔符列表，以及操作符列表



class Token(object):
	"""Token类
		五个属性：
		标志位，鉴别是词法错误还是正确识别的词法Token
		类别，鉴别是关键字，分隔符，常量等
		内容，token中的具体内容
		行号和列号
	"""
	def __init__(self, key=None, content=None, col=None, line=None, flag=None, key_2=None):
		super(Token, self).__init__()
		self.key = key
		self.content = content
		self.col = col
		self.line = line
		self.typeflag = flag
		self.key_2 = key_2

class Element(object):
	def __init__(self):
		super(Element, self).__init__()
		self.width = 0
		self.type = ''
		self.addr = ''
		self.true = ''
		self.false = ''
		self.next = ''
class QuaterItem(object):
	def __init__(self):
		super(Element, self).__init__()
		self.op = ''
		self.arg1 = ''
		self.arg2 = ''
		self.result = ''

					

#初始化first字典
def add_first_dict(key):
	global first_dict
	if not first_dict.has_key(key):
		first_dict[key] = set()

#输出select集中的内容
def check_select():
	global generation_dict
	for key in generation_dict.keys():
		print(key+'->'+str(generation_dict[key]))


#判断字符是否为终结符
def is_terminal_symbol(s):
	global terminal_list
	global keyword_list
	global seperatelist
	global oplist
	#global terminal_symbol_list
	if s in keyword_list:
		return True
	if s in terminal_list:
		return True
	if s in seperatelist:
		return True
	if s in oplist:
		return True
#	try:
#		if s[0]=='\'' and s[-1]=='\'':
#			return True
#	except IndexError:
#		print s
	#print '###'+s
	if s[0]=='\'' and s[-1]=='\'':
		return True
	return False


'''def get_real_content(s):
	pattern = re.compile(r'(?<=<).+?(?=>)')
	result = pattern.findall(s)
	if result == []:
		return '@'
	else:
		return result[0]
'''

#初始化文法，从文件中读文法
#生成对应的文法列表

def getin_grammer(filename):
	global token_list
	global symbol_list
	global new_grammer_token_list
	filein = open(filename, 'r')
	#first_dict['@'] = set()
	unterminal_set = set()
	while True:
		line = filein.readline()
		if not line:
			break
		line = line[:-1]
		#tmplist = []
		#item = tmplist.split('->')
		tmplist = line.split(' ')
		if len(tmplist) == 1:
			continue
		#key = get_real_content(item[0])
		#tmplist.append(key)
		#for item_list in item[1].split(' '):
		#	tmplist.append(get_real_content(item))
		for item in tmplist:
			if not is_terminal_symbol(item):
				unterminal_set.add(item)
				add_first_dict(item)
		token_list.append(tmplist)
	symbol_list = list(unterminal_set)
	#print(token_list)
	filein = open('my_production_action.txt', 'r')
	while True:
		line = filein.readline()
		if not line:
			break
		line = line[:-1]
		tmplist = line.split(' ')
		if len(tmplist) == 1:
			continue
		new_grammer_token_list.append(tmplist)
	filein.close()

#计算first集合
#
def get_first():
	global token_list
	global first_dict
	flag = True
	for item in token_list:
		key = item[0]
		#generation_str_list = item.split('->')[1].split(' ')
		tmp_len = len(first_dict[key])
		i = 1
		while len(item) > i:
			tmp_content = item[i]
			#print(tmp_content)
			#右部第一个终结符，更新first集合
			if is_terminal_symbol(tmp_content):
				first_dict[key].add(tmp_content)
				#first_dict[key].append(tmp_content)
				#first_dict[key] = set(first_dict[key])
				break
			#直接退出空产生式，更新first集合
			elif tmp_content == '@':
				first_dict[key].add('@')
				break
			#根据右部字串更新first集合
			else:
				if '@' in first_dict[tmp_content]:
					first_dict[key].update(first_dict[tmp_content].difference('@'))
					i = i + 1
				else:
					first_dict[key].update(first_dict[tmp_content])
					break
		if i == len(item):
			first_dict[key].add('@')
		if tmp_len != len(first_dict[key]):
			flag = False
	return flag

#初始化follow集合
def init_follow():
	global symbol_list
	for item in symbol_list:
		follow_dict[item] = set()

#计算follow集合

def get_follow():
	global token_list
	global follow_dict
	global first_dict
	#print(first_dict['program'])
	#print('sfdsf')
	init_follow()
	#follow_dict['start'].add('$')	
	follow_dict['program'].add('$')
	flag = True
	while flag == True:
		flag = False
		for item in token_list:
			key = item[0]
			#generation_str_list = item.split('->')[1].split(' ')
			i = 1
			while i<len(item):
				if item[i] == '@':
					#右部为空的产生式无法更新follow集
					break
				tmp_content = item[i]
				#过滤掉终结符
				if is_terminal_symbol(tmp_content):
					i = i + 1
					continue
				originlen = len(follow_dict[tmp_content])
				if (i == len(item)-1):
					follow_dict[tmp_content].update(follow_dict[key])
					if originlen != len(follow_dict[tmp_content]):
						flag = True
					break
				next_tmp_content = item[i+1]
				#非终结符后直接跟着一个终结符，添加到follow集
				if is_terminal_symbol(next_tmp_content):
					#follow_dict[tmp_content].add(next_tmp_content[1:-1])
					follow_dict[tmp_content].add(next_tmp_content)
				#根据后面的字串更新follow集
				else:
					j = i + 1
					while j<len(item):
						if is_terminal_symbol(item[j]):
							follow_dict[tmp_content].add(item[j])
							break
						if '@' not in first_dict[next_tmp_content]:
							follow_dict[tmp_content].update(first_dict[item[j]])
							break
						else:
							follow_dict[tmp_content].update(first_dict[item[j]].difference('@'))
							j = j + 1
					if j == len(item):
						follow_dict[tmp_content].update(follow_dict[key])
				i = i + 1
				#判断follow集是否有更新
				if originlen != len(follow_dict[tmp_content]):
					flag = True

#添加文法项到转换表中
def add_to_gendict(key, value, item):
	global generation_dict
	try:
		if generation_dict[key].has_key(value):
			#print(key)
			#if item != generation_dict[key][value]:
			#	print(key+'#'+value+'#'+str(generation_dict[key][value]))
			#	print(key+'#'+value+'#'+str(item))
			#	print('select error')
			pass
		else:
			generation_dict[key][value] = item
		#print('select error!')
		#exit()
	except KeyError:
		generation_dict[key] = {}
		generation_dict[key][value] = item

def creat_table():
	global selected
	global new_grammer_token_list
	i = 0
	for item in new_grammer_token_list:
		key = item[0]
		#tmp_list = selected[key]
		for value in selected[i]:
			add_to_gendict(key,value,item[1:])
		i = i + 1
#计算select集合，生成转换表		
def get_selected():
	global token_list
	global follow_dict
	global terminal_list
	global first_dict
	global selected
	#global new_grammer_token_list
	#print(first_dict['start'])
	#fout1 = open('fuck_1.txt', 'w')
	#fout2 = open('fuck_2.txt', 'w')
	#for a in first_dict.keys():
	#	fout1.write(a+'->'+str(first_dict[a])+'\n')
	#for a in follow_dict:
	#	fout2.write(a+'->'+str(follow_dict[a])+'\n')
	i = 0
	for item in token_list:
		key = item[0]
		#if not selected.has_key(key):
		#	selected[key] = []
		selected[i] = []
		#generation_str_list = item.split('->')[1].split(' ')
		#flag = False
		j = 1
		mark = item[j]
		#对于空产生式，将左部的follow集加入到select集合中	
		if mark == '@':
			for sym in follow_dict[key]:
				selected[i].append(sym)

		#若右部第一个字符是终结符，那么把终结符加入转换表中	
		elif is_terminal_symbol(mark):
			selected[i].append(mark)

		#对于右部是非终结符，将first集合中内容加入select中，如果first集合中有@那么看下一个字符
		else:
			flag = True
			while j < len(item) and flag == True:
				mark = item[j]
				j = j + 1
				flag = False
				for sym in first_dict[mark]:
					if sym != '@':
						selected[i].append(sym)
						#add_to_gendict(key,sym,item[1:])
					else:
						flag = True
		if j == len(item) and flag == True:
			for sym in follow_dict[key]:
#				if sym == '$':
#					continue
				selected[i].append(sym)
				#add_to_gendict(key,sym,item[1:])
		i = i + 1

#向转换表中添加synch，进行错误恢复
def add_synch():
	global generation_dict
	#print(generation_dict['start'])
	for key in generation_dict.keys():
		for item in follow_dict[key]:
			if not generation_dict[key].has_key(item):
				generation_dict[key][item] = 'synch'

#初始化文法，生成first集合，follow集合以及转换表
def init_grammer():
	filename = 'my_production.txt'
	#filename = './LL1/out_grammer.txt'
	getin_grammer(filename)
	flag = False
	while not flag:
		flag = get_first()
	get_follow()
	get_selected()
	creat_table()
	add_synch()

#将词法分析结果转化成token类
def get_symbol(sym_str):
	#print(type(sym_str))
	if isinstance(sym_str, tuple):
		key_2 = None
		#print('dsad')
		if sym_str[0] in terminal_list and sym_str[0] != 'IDENTIFIER':
			key = 'number'
			key_2 = sym_str[0]
		else:
			key = sym_str[0]
		content = sym_str[1]
		col = sym_str[2][0]
		line = sym_str[2][1]
		return Token(key=key, content=content, col=col, line=line, flag=1, key_2=key_2)

	else:
		return Token(content=sym_str, flag = 0)
def is_action(s):
	if s[:4] == 'act_':
		return True
	return False

def generate_quater(op_1, arg1, arg2, result):
	global quaternary_list
	global item_num
	outstr = ''
	if op_1 == '=':
		outstr = result + op_1 + arg1 + arg2
	else:
		outstr = result + '=' + arg1 + op_1 + arg2
	#print outstr
	quaternary_list.append(outstr)
	item_num = item_num + 1
	#print item_num

def generate_quater_jump(relop2, arg2, relop1=None, arg1=None):
	global quaternary_list
	global item_num
	if relop1 == None:
		outstr = relop2 +' '+arg2
		quaternary_list.append(outstr)
		print outstr
	else:
		outstr = relop1 + ' ' + arg1 + ' ' + relop2 + ' ' + arg2
		quaternary_list.append(outstr)
		print outstr
	item_num = item_num + 1


def newlabel():
	global labele_dict
	global label_num
	#global item_num
	key = 'fuck' + str(label_num)
	labele_dict[key] = 0
	label_num = label_num + 1
	return key

def labeled(s):
	global labele_dict
	global item_num
	labele_dict[s] = item_num

def lookup(id):
	global id_symbol_dict
	if id_symbol_dict.has_key(id.addr):
		return True
	return False
def is_type(s):
	s_list = ['int', 'char', 'float', 'double']
	if s in s_list:
		return True
	return False

#进行句法分析
def do_syntax(filename):
	global generation_dict
	global getin_stack
	global result_generation_list
	global value_stack
	global id_symbol_dict
	global item_num
	begin = ''
	offset = 0
	id_symbol_dict = {}
	tmp_op = ''
	fout1 = open('processing.txt', 'w')
	fout3 = open('error.txt', 'w')
	#init_grammer()
	lexer_list = lexer.doToken(filename)
	length = len(lexer_list)
	#print(length)
	fout4 = open('hehe.txt', 'w')
	for i in lexer_list:
		fout4.write(str(i)+'\n')
	fout4.close()
	#exit()
	#print(generation_dict['type_specifier']['int'])
	getin_stack.append('program')
	i = 0
	#noerror_flag = True
	while i < length and getin_stack != []:
		#print(lexer_list[i])
		terminal_symbol = get_symbol(lexer_list[i])
		#print(terminal_symbol.content)
		if terminal_symbol.typeflag == 0:
			#print(terminal_symbol.content)
			error_list.append(terminal_symbol.content)
			fout3.write(terminal_symbol.content)
			i = i + 1
			continue
		while getin_stack!=[]:
			stack_top_symbol = getin_stack.pop()
			if stack_top_symbol == '$':
				exit()
			if is_action(stack_top_symbol):
				if stack_top_symbol == 'act_1':
					#print('######')
					tmp_id = value_stack.pop()
					tmp_name = tmp_id.addr
					#print "######"+stack_top_symbol 
					tmp_width = value_stack[-1].width
					tmp_type = value_stack[-1].type
					out_str = tmp_type + '#' + str(tmp_width) 
					if id_symbol_dict.has_key(tmp_name):
						error_list.append(stack_top_symbol+'--'+terminal_symbol.key+' : '+str(terminal_symbol.line)+' '+str(terminal_symbol.col)+'redefinition !!Error!!')
						print stack_top_symbol+'--'+terminal_symbol.key+' : '+str(terminal_symbol.line)+' '+str(terminal_symbol.col)+'redefinition !!Error!!'
					else :
						id_symbol_dict[tmp_name] = out_str
				if stack_top_symbol == 'act_2':
					if not lookup(value_stack[-2]):
						error_list.append(stack_top_symbol+'--'+terminal_symbol.key+' : '+str(terminal_symbol.line)+' '+str(terminal_symbol.col)+'undefined identifer Error')
						print stack_top_symbol+'--'+terminal_symbol.key+' : '+str(terminal_symbol.line)+' '+str(terminal_symbol.col)+'undefined identifer Error'
					else:
						if value_stack[-2].type != value_stack[-1].type:
							error_list.append(stack_top_symbol+'--'+terminal_symbol.key+' : '+str(terminal_symbol.line)+' '+str(terminal_symbol.col)+'Type Mismatch !!Error!!')
							print stack_top_symbol+'--'+terminal_symbol.key+' : '+str(terminal_symbol.line)+' '+str(terminal_symbol.col)+'Type Mismatch !!Error!!'
						else:
							#print '###'+value_stack[-2].addr
							generate_quater('=',value_stack[-1].addr,' ',value_stack[-2].addr)
					value_stack.pop()
					value_stack.pop()
					value_stack.pop()
				if stack_top_symbol == 'act_3':
					generate_quater(tmp_op, value_stack[-3].addr,value_stack[-1].addr,value_stack[-4].addr)
					#value_stack[-3].type = value_stack[-1].type
					#value_stack[-3].addr = value_stack[-2].addr + '+' + value_stack[-1].addr
					if value_stack[-1].type != value_stack[-3].type:
						error_list.append(stack_top_symbol+'--'+terminal_symbol.key+' : '+str(terminal_symbol.line)+' '+str(terminal_symbol.col)+'Type Mismatch !!Error!!')
						print(stack_top_symbol+'--'+terminal_symbol.key+' : '+str(terminal_symbol.line)+' '+str(terminal_symbol.col)+'Type Mismatch !!Error!!')
					value_stack[-4].type = value_stack[-1].type
					value_stack.pop()
					value_stack.pop()
					value_stack.pop()
				if stack_top_symbol == 'act_4':
					value_stack.pop()
					tmp_id = value_stack.pop()
					if tmp_id.width != 0:
						if not id_symbol_dict.has_key(tmp_name):
							error_list.append(stack_top_symbol+'--'+terminal_symbol.key+' : '+str(terminal_symbol.line)+' '+str(terminal_symbol.col)+'undefined !!Error!!')
							print stack_top_symbol+'--'+terminal_symbol.key+' : '+str(terminal_symbol.line)+' '+str(terminal_symbol.col)+'undefined !!Error!!'
						else:
							value_stack[-1].type = tmp_id.type
							value_stack[-1].addr = tmp_id.addr
					else:
						tmp_num = tmp_id
						value_stack[-1].type = tmp_num.type
						value_stack[-1].addr = tmp_num.addr
						#print '####'+tmp_num.addr
				#if stack_top_symbol == 'act_4':
				#	generate_quater('*',value_stack[-2].addr,value_stack[-1].addr,value_stack[-3].addr)
				#	value_stack.pop()
				#	value_stack.pop()
				if stack_top_symbol == 'act_5':
					generate_quater('-',' ',value_stack[-1].addr,value_stack[-2].addr)
					value_stack[-2].addr = -value_stack[-1].addr
					value_stack.pop()
				if stack_top_symbol == 'act_6':
					value_stack[-2].addr = value_stack[-1].addr
					value_stack.pop()
				if stack_top_symbol == 'act_7':
					value_stack[-2].type = value_stack[-1].type
					value_stack[-2].addr = value_stack[-1].addr
					value_stack.pop()
				if stack_top_symbol == 'act_relop_1':
					value_stack[-4].addr = value_stack[-3].addr + value_stack[-2].addr + value_stack[-1].addr
					#print('#####'+value_stack[-3].addr)
					value_stack.pop()
					value_stack.pop()
					value_stack.pop()
				if stack_top_symbol == 'act_relop_2':
					value_stack[-1].addr = tmp_op
				if stack_top_symbol == 'act_if_1':
					value_stack[-1].true = newlabel()
					value_stack[-1].false = newlabel()
					value_stack[-1].next = newlabel()
					#print "####"+value_stack[-1].true + ' '+ value_stack[-1].false + ' ' + value_stack[-1].next
					generate_quater_jump('goto',value_stack[-1].true,'if',value_stack[-1].addr)
					generate_quater_jump('goto',value_stack[-1].false)
					#value_stack[-1].true = newlabel()
					#value_stack[-1].false = newlabel()
					#value_stack.pop()
				if stack_top_symbol == 'act_jump_next':
					#value_stack.pop()
					print '###' + value_stack[-1].addr
					print '###' + value_stack[-2].addr
					print '###' + value_stack[-2].next
					generate_quater_jump('goto', value_stack[-1].next)
				if stack_top_symbol == 'act_catch_next':
					#value_stack.pop()
					labeled(value_stack[-1].next)
					value_stack.pop()
					value_stack.pop()
					value_stack.pop()
				if stack_top_symbol == 'act_catch_label_t':
					labeled(value_stack[-1].true)
				if stack_top_symbol == 'act_catch_label_f':
					labeled(value_stack[-1].false)
				if stack_top_symbol == 'act_catch_label_f_n':
					#value_stack.pop()
					labeled(value_stack[-1].false)
					value_stack.pop()
					value_stack.pop()
				if stack_top_symbol == 'act_while_2':
					value_stack[-1].true = newlabel()
					value_stack[-1].false = value_stack[-2].false
					generate_quater_jump('goto', value_stack[-1].true, 'if', value_stack[-1].addr)
					generate_quater_jump('goto',value_stack[-1].false)
				if stack_top_symbol == 'act_while_1':
					begin = newlabel()
					labeled(begin)
					value_stack[-1].false = newlabel()
				if stack_top_symbol == 'act_while_3':
					#labeled(value_stack[-2].true)
					#value_stack[-1].next = begin
					generate_quater_jump('goto',begin)
				if stack_top_symbol == 'act_pop':
					value_stack.pop()
				if stack_top_symbol == 'act_pop_2':
					value_stack.pop()
					value_stack.pop()
				if stack_top_symbol == 'act_clean':
					value_stack = []
				continue
			if is_terminal_symbol(stack_top_symbol):
				if stack_top_symbol in oplist:
					tmp_op = stack_top_symbol
				if stack_top_symbol == 'number':
					if terminal_symbol.key in terminal_list:
						tmp_element = Element()
						tmp_index = terminal_symbol.key_2.find('_')
						tmp_key = str.lower(terminal_symbol.key_2[tmp_index+1:])
						tmp_element.type = tmp_key
						tmp_element.addr =  terminal_symbol.content
						#print(tmp_element)
						value_stack.append(tmp_element)
						output_str = 'top of the stack is '+stack_top_symbol+' -> '
						output_str = output_str + 'input_str is '+terminal_symbol.key
						output_str = output_str + ' ->operation is COMBINE'
						print(output_str)
						fout1.write(output_str+'\n')
						i += 1
						break
					else:
						output_str = str(terminal_symbol.line)+' '+str(terminal_symbol.col)+': '
						output_str = output_str + stack_top_symbol+'--'+terminal_symbol.key+' : ' + 'not match top of stack!'
						error_list.append(output_str)
						fout3.write(output_str+'\n')
					continue
				if stack_top_symbol == terminal_symbol.key:
					if stack_top_symbol == 'IDENTIFIER':
						id_num = terminal_symbol.content
						tmpid = Element()
						tmpid.addr = id_num
						if id_symbol_dict.has_key(id_num):
							#print('####'+id_symbol_dict[id_num])
							tmpid.type = id_symbol_dict[id_num].split('#')[0]
							tmpid.width = id_symbol_dict[id_num].split('#')[1]
						value_stack.append(tmpid)
					if is_type(stack_top_symbol):
						if stack_top_symbol == 'char':
							value_stack[-1].type = 'char'
							value_stack[-1].width = 1
						if stack_top_symbol == 'int':
							value_stack[-1].type = 'int'
							value_stack[-1].width = 4
						if stack_top_symbol == 'float':
							value_stack[-1].type = 'float'
							value_stack[-1].width = 4
						if stack_top_symbol == 'double':
							value_stack[-1].type ='double'
							value_stack[-1].width = 8
					output_str = 'top of the stack is '+stack_top_symbol+' -> '
					output_str = output_str + 'input_str is '+terminal_symbol.key
					output_str = output_str + ' ->operation is COMBINE'
					print(output_str)
					fout1.write(output_str+'\n')
					i += 1
					break
				else:
					output_str = str(terminal_symbol.line)+' '+str(terminal_symbol.col)+': '
					output_str = output_str + stack_top_symbol+'--'+terminal_symbol.key+' : ' + 'not match top of stack!'
					error_list.append(output_str)
					fout3.write(output_str+'\n')
				continue
			try:
				t_ele = Element()
				t_ele.addr = 't'+ str(item_num)
				value_stack.append(t_ele)
				#print(stack_top_symbol+'-----'+terminal_symbol.key+':')
				generation = copy.deepcopy(generation_dict[stack_top_symbol][terminal_symbol.key])
				result_generation_list.append(stack_top_symbol+'--'+terminal_symbol.key+'->'+str(generation))
				#print(generation)
				#fout2.write(terminal_symbol.content + str(generation)+'\n')
				output_str = 'top of the stack is '+stack_top_symbol+' -> '
				output_str = output_str + 'input_str is '+terminal_symbol.key
				output_str = output_str + ' ->new generation:' + terminal_symbol.content + ' -> ' +str(generation)
				print(output_str)
				fout1.write(output_str+'\n')
				if generation == 'synch':
					print(str(terminal_symbol.line)+' '+str(terminal_symbol.col)+':'+'synch error--pop stack')
					fout3.write(str(terminal_symbol.line)+' '+str(terminal_symbol.col)+':'+'synch error--pop stack'+'\n')
					break

				while len(generation) > 0:
					tmp_symbol = generation.pop()
					if tmp_symbol != '@':
						getin_stack.append(tmp_symbol)
			except KeyError:
				value_stack.pop()
				print(stack_top_symbol+'--'+terminal_symbol.key+' : '+str(terminal_symbol.line)+' '+str(terminal_symbol.col)+'No Such Generation !!Error!!')
				error_list.append(stack_top_symbol+'--'+terminal_symbol.key+' : '+str(terminal_symbol.line)+' '+str(terminal_symbol.col)+'No Such Generation !!Error!!')
				fout3.write(stack_top_symbol+'--'+terminal_symbol.key+' : '+str(terminal_symbol.line)+' '+str(terminal_symbol.col)+'No Such Generation !!Error!!'+'\n')
				getin_stack.append(stack_top_symbol)
				i = i+1
				break
			if getin_stack == []:
				#noerror_flag = False
				break
	fout1.close()
	fout3.close()

#输出转换表
def output_dict():
	fileout = open('shit.txt', 'w')
	global generation_dict
	for key in generation_dict.keys():
		for keys in generation_dict[key]:
			fileout.write(key+'->'+keys+' '+str(generation_dict[key][keys])+'\n')

def showerror():
	for item in error_list:
		print(item)

def showgeneration():
	fout2 = open('generation.txt', 'w')
	for item in result_generation_list:
		print(item)
		fout2.write(item+'\n')

def showquater():
	global quaternary_list
	global labele_dict
	print quaternary_list
	print labele_dict
	num = 0
	for item in quaternary_list:
		index = item.find('goto')
		if index != -1:
			index = index + 5
			print str(num)+':'+item[:index]+str(labele_dict[item[index:]])
		else:
			print str(num)+':'+item
		num = num + 1

def showidtable():
	global id_symbol_dict
	print '---------------------------------------------'
	print 'id || type || width' 
	for key in id_symbol_dict.keys():
		value = id_symbol_dict[key].split('#')
		print(key + ' || ' + value[0] + ' || ' + value[1])

def main():
	global quaternary_list
	global first_dict
	filename = sys.argv[1]
	#filename需要被进行词法分析的文件
	init_grammer()
	#print first_dict['declare']
	output_dict()
	#print(generation_dict)
	#check_select()
	do_syntax(filename)
	quaternary_list.append('end')
	#global id_symbol_dict
	#print(id_symbol_dict)
	showquater()
	showidtable()
	#showgeneration()
	showerror()

if __name__ == '__main__':
	main()
