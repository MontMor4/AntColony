import csv
import math
import random
import multiprocessing


with open('Col2.csv', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    cities = [(row['Cidade'], int(row['X']), int(row['Y'])) for row in reader]


def distCalculator(ponto1, ponto2):
    return math.sqrt((ponto1[1] - ponto2[1]) ** 2 + (ponto1[2] - ponto2[2]) ** 2)


def initialize_graph(cities, initialPhero=1):
    grafo = []
    for i in cities:
        arestas = []
        for j in cities:
            dist = distCalculator(i, j)
            inverseDist = 0 if dist == 0 else 1 / dist
            arestas.append({
                'dist': dist,
                'phero': initialPhero,
                'invDist': inverseDist,
                'heuristic': initialPhero * inverseDist,
                'prob': 0
            })
        grafo.append(arestas)
    return grafo


def atualizaHeur(grafo, alpha, beta):
    for i in grafo:
        for j in i:
            j['heuristic'] = (j['phero'] ** alpha) * (j['invDist'] ** beta)

def atualizaProb(grafo):
    for i in grafo:
        somaHeuristica = sum(j['heuristic'] for j in i)
        for j in i:
            j['prob'] = j['heuristic'] / somaHeuristica

def roleta(cidadeAtual, javisitados, cities, grafo):
    roleta = []
    soma = 0
    for j in range(len(cities)):
        if j not in javisitados:
            roleta.append((j, grafo[cidadeAtual][j]['prob'] + soma))
            soma += grafo[cidadeAtual][j]['prob']
    gerado = random.uniform(0, roleta[-1][1])
    for j in roleta:
        if gerado <= j[1]:
            return j[0]

def caminhar(cities, grafo):
    pathsAndDist = []
    for i in range(len(cities)):
        javisitados = {i: 1}
        cidadeAtual = i
        distanciaPercorrida = 0
        path = [i]
        while len(javisitados) < len(cities):
            selecionado = roleta(cidadeAtual, javisitados, cities, grafo)
            javisitados[selecionado] = 1
            path.append(selecionado)
            distanciaPercorrida += grafo[cidadeAtual][selecionado]['dist']
            cidadeAtual = selecionado

        distanciaPercorrida += grafo[cidadeAtual][i]['dist']
        path.append(i)
        pathsAndDist.append((path, distanciaPercorrida))
    return pathsAndDist

def atualizaFero(pathsAndDist, grafo, evaporacao, pheroAmount):
    for i in pathsAndDist:
        path = i[0]
        dist = i[1]
        pheroPorRota = pheroAmount / dist
        for j in range(1, len(path)):
            grafo[path[j]][path[j-1]]['phero'] = (1-evaporacao)*grafo[path[j]][path[j-1]]['phero'] + pheroPorRota
            grafo[path[j-1]][path[j]]['phero'] = (1-evaporacao)*grafo[path[j-1]][path[j]]['phero'] + pheroPorRota

def run_simulation(alpha, beta, evaporacao, pheroAmount):
    grafo = initialize_graph(cities)
    data = []
    for _ in range(100):
        pathsAndDist = caminhar(cities, grafo)
        avg_distance = sum([i[1] for i in pathsAndDist]) / len(pathsAndDist)
        data.append(avg_distance)
        atualizaFero(pathsAndDist, grafo, evaporacao, pheroAmount)
        atualizaHeur(grafo, alpha, beta)
        atualizaProb(grafo)
    return data

def worker(params):
    alpha, beta, evaporacao, pheroAmount = params
    result = run_simulation(alpha, beta, evaporacao, pheroAmount)
    print(f"Params: alpha={alpha}, beta={beta}, evaporacao={evaporacao}, pheroAmount={pheroAmount} -> Result: {result[-1]}")
    return result

if __name__ == '__main__':
    menores = [] 
    for _ in range(10):
       
        instancenums = 20
        
        parameter_sets = [(random.uniform(0, 5), random.uniform(0, 5), random.uniform(0, 1), random.uniform(0, 300)) for _ in range(instancenums)]
        
        with multiprocessing.Pool(processes=len(parameter_sets)) as pool:
            results = pool.map(worker, parameter_sets)
        
        final_results = []
        for i in range(len(results)):
            final_results.append((parameter_sets[i], results[i][-1]))
        final_results.sort(key=lambda x: x[1])
        menores = menores + final_results[:5]
        menores.sort(key=lambda x: x[1])
        menores = menores[:5]


   
    print("5 melhores resultados:")
    for i in menores:
        print(i)
        
