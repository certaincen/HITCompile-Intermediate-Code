fin1 = open('my_production.txt', 'r')
fin2 = open('my_production_action.txt', 'r')
list1 = []
list2 = []
while True:
	line = fin1.readline()
	if not line:
		break
	list1.append(line[:-2])
fin1.close()
while True:
	line = fin2.readline()
	if not line:
		break
	list2.append(line[:-2])
fin2.close()
#print(list1)
#print(list2)
fout1 = open('new_my.txt','w')
fout2 = open('new_my_ac.txt','w')
for item in list1:
	fout1.write(item + '\n')
fout1.close()
for item in list2:
	fout2.write(item + '\n')
fout2.close()