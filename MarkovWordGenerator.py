import re,random,sqlite3

fpath = 'GrimmFairyTales.txt'
f = open(fpath,'rb')
r = f.read()

markovdb = {}
prefixlength = 2
prefix = []
inorder = []
regex = re.compile('[\/]')#specify symbols to remove from the text

for word in r.split():
	word = regex.sub('',word.decode('utf-8')).lower()
	
	if (len(prefix)==prefixlength):
		newkey = ' '.join(prefix)
		if (newkey in markovdb.keys()):
			markovdb[newkey].append(word)
		else:
			markovdb[newkey]=[word]
		inorder.append(' '.join(prefix))
		if (len(prefix)>1):
			prefix = prefix[1:]
		else:
			prefix = []
		prefix.append(word)
	else:
		prefix.append(word)

'''	
for k in inorder:
	print('{}:{}'.format(k,markovdb[k]))
'''	
	
def write_sentence(seed):
	#starters = [s for s in starters if len(s.split(' '))==prefixlength]
	starters = [k for k in markovdb.keys() if k.lower().startswith(seed.lower())]
	if len(starters)==0:
		#print('Starters list blank or invalid - generating random')
		starters=[key for key in markovdb.keys() if key not in ['and']]
	outputstring = random.choice(starters)
	searchword = outputstring
	while(searchword.lower() in markovdb.keys() and not ('.' in searchword) and not('!' in searchword) and not('?' in searchword)):
		nextwords = markovdb[searchword.lower()]
		chosen = random.choice(nextwords)
		outputstring = outputstring+' '+chosen
		searchword = ' '.join(outputstring.split(' ')[-prefixlength:])
	print(outputstring[:1].upper()+outputstring[1:])

def makeSQLDB():
	conn = sqlite3.connect('markov.sqldb')
	c = conn.cursor()
	c.execute('drop table markov')
	c.execute('create table markov (id INTEGER, prefix STRING, next STRING)')
	nextid = 1
	totalkeys = len(markovdb.keys())
	keyno=0
	aposreg = re.compile("[']")
	for key in markovdb.keys():
		keyno +=1
		if (keyno%2000==0):
			print('{0:.2f}%'.format(keyno/totalkeys*100))
		for val in markovdb[key]:
			k = aposreg.sub("''",key)
			v = aposreg.sub("''",val)
			c.execute("insert into markov (id,prefix,next) values ({},'{}','{}')".format(nextid,k,v))
			nextid+=1
	print('100%')
	conn.commit()
	conn.close()
	print('Connection closed')

def openconn():
	conn = sqlite3.connect('markov.sqldb')
	c = conn.cursor()
	print('ready')
	co = True
	while(co):
		comm = input('-->')
		if comm == 'q':
			co = False
		else:
			for each in c.execute(comm):
				print(str(each)[1:-2])
	conn.commit()
	conn.close()
	print('Connection closed')
	
for i in range(10):
	write_sentence('The')
	print()
