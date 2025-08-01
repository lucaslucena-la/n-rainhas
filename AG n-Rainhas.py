import random
import time
import math

# Função para calcular o número de conflitos entre rainhas
def calcular_conflitos(cromossomo):
    n = len(cromossomo)
    conflitos = 0
    for i in range(n):
        for j in range(i + 1, n):
            if cromossomo[i] == cromossomo[j]:  # Mesma coluna
                conflitos += 1
            if abs(cromossomo[i] - cromossomo[j]) == abs(i - j):  # Mesma diagonal
                conflitos += 1
    return conflitos

# Função de fitness: menor número de conflitos = melhor fitness
def fitness(cromossomo):
    max_conflitos = (len(cromossomo) * (len(cromossomo) - 1)) // 2  # Máximo de conflitos possível
    return max_conflitos - calcular_conflitos(cromossomo)

# Gerar um cromossomo inicial (permutação aleatória)
def gerar_cromossomo(n):
    return random.sample(range(1, n + 1), n)

# Gerar população inicial
def gerar_populacao(tam_pop, n):
    return [gerar_cromossomo(n) for _ in range(tam_pop)]

# Seleção por torneio
def selecao_torneio(populacao, fitnesses, tam_torneio):
    torneio = random.sample(list(zip(populacao, fitnesses)), tam_torneio)
    return max(torneio, key=lambda x: x[1])[0]

# Crossover de ordem (OX1)
def crossover(pai1, pai2):
    n = len(pai1)
    ponto1, ponto2 = sorted(random.sample(range(n), 2))
    filho1 = [None] * n
    filho2 = [None] * n
    
    # Copiar segmento do pai1 para filho1 e do pai2 para filho2
    filho1[ponto1:ponto2] = pai1[ponto1:ponto2]
    filho2[ponto1:ponto2] = pai2[ponto1:ponto2]
    
    # Preencher o restante do filho1 com valores do pai2 (mantendo a ordem)
    idx = ponto2
    for val in pai2[ponto2:] + pai2[:ponto2]:
        if val not in filho1[ponto1:ponto2]:
            if idx >= n:
                idx = 0
            while filho1[idx] is not None:
                idx += 1
                if idx >= n:
                    idx = 0
            filho1[idx] = val
            idx += 1
            
    # Preencher o restante do filho2 com valores do pai1 (mantendo a ordem)
    idx = ponto2
    for val in pai1[ponto2:] + pai1[:ponto2]:
        if val not in filho2[ponto1:ponto2]:
            if idx >= n:
                idx = 0
            while filho2[idx] is not None:
                idx += 1
                if idx >= n:
                    idx = 0
            filho2[idx] = val
            idx += 1
            
    return filho1, filho2

# Mutação: troca de duas posições
def mutacao(cromossomo, taxa_mutacao):
    if random.random() < taxa_mutacao:
        n = len(cromossomo)
        i, j = random.sample(range(n), 2)
        cromossomo[i], cromossomo[j] = cromossomo[j], cromossomo[i]
    return cromossomo

# Algoritmo Genético
def algoritmo_genetico(n, tam_pop=100, max_geracoes=1000, taxa_mutacao=0.05, tam_torneio=3):
    populacao = gerar_populacao(tam_pop, n)
    melhor_solucao = None
    melhor_fitness = -math.inf
    start_time = time.time()
    
    for geracao in range(max_geracoes):
        # Avaliar fitness da população
        fitnesses = [fitness(crom) for crom in populacao]
        
        # Atualizar melhor solução
        max_fitness = max(fitnesses)
        idx_melhor = fitnesses.index(max_fitness)
        if max_fitness > melhor_fitness:
            melhor_fitness = max_fitness
            melhor_solucao = populacao[idx_melhor].copy()
        
        # Verificar se encontrou solução (zero conflitos)
        if calcular_conflitos(melhor_solucao) == 0:
            break
        
        # Nova população
        nova_populacao = []
        
        # Elitismo: manter a melhor solução
        nova_populacao.append(melhor_solucao)
        
        # Gerar novos indivíduos
        while len(nova_populacao) < tam_pop:
            pai1 = selecao_torneio(populacao, fitnesses, tam_torneio)
            pai2 = selecao_torneio(populacao, fitnesses, tam_torneio)
            filho1, filho2 = crossover(pai1, pai2)
            filho1 = mutacao(filho1.copy(), taxa_mutacao)
            filho2 = mutacao(filho2.copy(), taxa_mutacao)
            nova_populacao.extend([filho1, filho2])
        
        # Limitar tamanho da população
        populacao = nova_populacao[:tam_pop]
    
    end_time = time.time()
    return melhor_solucao, calcular_conflitos(melhor_solucao), end_time - start_time

# Função para executar o algoritmo múltiplas vezes e coletar estatísticas
def executar_experimentos(n, num_execucoes=5):
    resultados = []
    for i in range(num_execucoes):
        solucao, conflitos, tempo = algoritmo_genetico(n)
        resultados.append({
            'execucao': i + 1,
            'conflitos': conflitos,
            'solucao': solucao,
            'tempo': tempo,
            'encontrou_solucao': conflitos == 0
        })
    return resultados

# Função principal
def main():
    ns = [32, 64, 128]
    for n in ns:
        print(f"\n=== Experimentos para N={n} ===")
        resultados = executar_experimentos(n)
        
        # Calcular estatísticas
        tempos = [r['tempo'] for r in resultados]
        conflitos = [r['conflitos'] for r in resultados]
        solucoes_validas = sum(1 for r in resultados if r['encontrou_solucao'])
        
        print(f"Tempo médio: {sum(tempos) / len(tempos):.2f} segundos")
        print(f"Média de conflitos: {sum(conflitos) / len(conflitos):.2f}")
        print(f"Soluções válidas encontradas: {solucoes_validas}/{len(resultados)}")
        for r in resultados:
            print(f"Execução {r['execucao']}: Conflitos={r['conflitos']}, Tempo={r['tempo']:.2f}s, Solução válida={r['encontrou_solucao']}")

if __name__ == "__main__":
    main()