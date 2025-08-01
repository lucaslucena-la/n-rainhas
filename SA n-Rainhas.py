import random
import time
import math

# Função para calcular o número de conflitos entre rainhas
def calcular_conflitos(solucao):
    n = len(solucao)
    conflitos = 0
    for i in range(n):
        for j in range(i + 1, n):
            if solucao[i] == solucao[j]:  # Mesma coluna
                conflitos += 1
            if abs(solucao[i] - solucao[j]) == abs(i - j):  # Mesma diagonal
                conflitos += 1
    return conflitos

# Gerar uma solução inicial (permutação aleatória)
def gerar_solucao(n):
    return random.sample(range(1, n + 1), n)

# Gerar um vizinho: troca de duas posições
def gerar_vizinho(solucao):
    vizinho = solucao.copy()
    n = len(solucao)
    i, j = random.sample(range(n), 2)
    vizinho[i], vizinho[j] = vizinho[j], vizinho[i]  # Troca
    return vizinho

# Simulated Annealing
def simulated_annealing(n, temp_inicial=100.0, taxa_resfriamento=0.95, temp_min=0.01, max_iter_por_temp=100):
    solucao_atual = gerar_solucao(n)
    conflitos_atual = calcular_conflitos(solucao_atual)
    melhor_solucao = solucao_atual.copy()
    melhor_conflitos = conflitos_atual
    temperatura = temp_inicial
    start_time = time.time()
    
    while temperatura > temp_min:
        for _ in range(max_iter_por_temp):
            # Gerar vizinho
            vizinho = gerar_vizinho(solucao_atual)
            conflitos_vizinho = calcular_conflitos(vizinho)
            
            # Calcular diferença de custo
            delta = conflitos_vizinho - conflitos_atual
            
            # Aceitar vizinho se for melhor ou com probabilidade e^(-delta/T)
            if delta <= 0 or random.random() < math.exp(-delta / temperatura):
                solucao_atual = vizinho
                conflitos_atual = conflitos_vizinho
                
                # Atualizar melhor solução
                if conflitos_atual < melhor_conflitos:
                    melhor_solucao = solucao_atual.copy()
                    melhor_conflitos = conflitos_atual
                
                # Parar se encontrar solução
                if conflitos_atual == 0:
                    end_time = time.time()
                    return melhor_solucao, melhor_conflitos, end_time - start_time
        
        # Reduzir temperatura
        temperatura *= taxa_resfriamento
    
    end_time = time.time()
    return melhor_solucao, melhor_conflitos, end_time - start_time

# Função para executar o algoritmo múltiplas vezes e coletar estatísticas
def executar_experimentos(n, num_execucoes=5):
    resultados = []
    for i in range(num_execucoes):
        solucao, conflitos, tempo = simulated_annealing(n)
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