#!/usr/bin/env python
#coding: utf-8

'''cidade de partida lisboa'''
'''o indice da cidade de partida (começando em 0) , neste caso é 7, pois é a 8ª cidade a aparecer no .csv'''
start_city = 7

'''cidade destino amsterdao'''
'''o indice da cidade destino, neste caso é 0, pois é o primeiro que aparece no .csv'''
dest_city = 0

cities = []
current_solution = []
best = 0
size = 0
bVisited = 0

'''função recursiva'''
def func(current_cost,current_city,visited):
	global cities, current_solution,best,size,dest_city,start_city,bVisited
	tempVisited = bVisited
	if( bVisited in cities[current_city][3]):
		if(current_cost + cities[current_city][3][bVisited] < best):
			best = current_cost + cities[current_city][3][bVisited]
		return cities[current_city][3][bVisited]
	
	if(visited >= size):
		'''caminho melhor até ao momento'''
		if(current_cost < best):
			best = current_cost
		return 0

	bVisited = (1<<current_city) | bVisited

	for city in cities[current_city][1]:
		if(((bVisited >> city[0]) & 1) == 0):
			if((city[0] == dest_city and visited+1 < size)):
				continue
			temp = func(current_cost+city[1],city[0],visited+1)
			if( (tempVisited in cities[current_city][3]) ):
				if cities[current_city][3][tempVisited] > (temp + city[1]):
					cities[current_city][3][tempVisited] = (temp + city[1])
					cities[current_city][2][tempVisited] = city[0]
			else:
				cities[current_city][3][tempVisited] = temp + city[1]
				cities[current_city][2][tempVisited] = city[0]
				
	bVisited = (~(1<<current_city)) & bVisited
	return cities[current_city][3][bVisited]

def doIt(file_name):
	global cities, current_solution,best,size,dest_city,start_city,bVisited

	'''inicializar as variáveis para cada um dos tres casos de teste'''
	current_solution = []
	cities = []
	best = 0
	size = 0
	bVisited = 0

	f = open(file_name, 'r')
	lines = f.readlines()

	'''ler o cabeçalho do ficheiro para obter as cidades'''
	line = lines[0].split(';')

	for i in range(1,len(line)):
		cities.append([line[i].split('\n')[0],[],{},{}])

	'''ler o resto das linhas para obter distancias/custo/tempo entre as cidades'''
	for i in range(0,len(lines)-1):
		line = lines[i+1].split(';')
		for j in range(1,len(line)):
			if(len(line[j])>0):
				'''insere os valores em ambas as cidades'''
				if(j-1 != i):
					cities[j-1][1].append([i,float(line[j])])
					cities[i][1].append([j-1,float(line[j])])
					best += float(line[j])
				else:
					cities[i][1].append([j-1,float(line[j])])

	'''ordenamos o array dos custos para outras cidades de cada cidade, por ordem crescente'''
	for city in cities:
		city[1].sort(key=lambda x: x[1], reverse=False)

	size = len(cities)

	'''7 é o indice da cidade Lisboa, é só trocar para outro indice qualquer'''
	func(0,start_city,1)
	
def printCities(out_temp):
	global cities
	city = start_city
	bVisited = 0
	out_temp += cities[start_city][0]+ ' e terminando em ' + cities[dest_city][0] + ' segue o percurso: '
	while city != dest_city:
		out_temp += (cities[city][0]+', ')

		temp_city = city
		city = cities[city][2][bVisited]
		bVisited = (1<<temp_city) | bVisited
	out_temp += (cities[city][0]+' ')
	return out_temp



'''main'''
#custo
print("A calcular o menor custo...")
doIt('cost.csv')
out_temp = printCities("A rota com menor custo começando em ")
out_temp += 'custando um total de ' + ('%.2f' % best) + ' euros.\n'
print(out_temp)

#tempo
print("A calcular o menor tempo...")
doIt('time.csv')
out_temp = printCities('A rota que demora menos tempo começando em ')
out_temp += 'demorando um total de ' + ('%.2f' % best) + ' horas.\n'
print(out_temp)

#distância
print("A calcular a menor distância...")
doIt('distance.csv')
out_temp = printCities('A rota que percorre menos distância começando em ')
out_temp += 'percorrendo um total de ' + ('%.2f' % best) + ' km.'
print(out_temp)
