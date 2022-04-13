left = 0
with open('rio_comentario.txt') as s:
	ix = []
	lns=[]
	for i,y in enumerate(s.readlines()):
		lns+=[y]
		if '...' in y:
			left+=1
			ix+=[i]
	k=[]
	for i in ix:
		k+=[lns[i-1].strip()]
	print(1 - left/77, left)
	import random as s
	print(s.choice(k),'!')