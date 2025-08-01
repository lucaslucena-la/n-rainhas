import random
import time

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

# Gerar vizinhos: todas as trocas possíveis de duas posições
def gerar_vizinhos(solucao):
    vizinhos = []
    n = len(solucao)
    for i in range(n):
        for j in range(i + 1, n):
            vizinho = solucao.copy()
            vizinho[i], vizinho[j] = vizinho[j], vizinho[i]  # Troca
            vizinhos.append(vizinho)
    return vizinhos

# Hill Climbing com reinícios aleatórios
def hill_climbing(n, max_iter=1000, max_restarts=100):
    melhor_solucao = None
    melhor_conflitos = float('inf')
    start_time = time.time()
    
    for restart in range(max_restarts):
        # Gerar solução inicial
        solucao_atual = gerar_solucao(n)
        conflitos_atual = calcular_conflitos(solucao_atual)
        
        # Atualizar melhor solução
        if conflitos_atual < melhor_conflitos:
            melhor_solucao = solucao_atual.copy()
            melhor_conflitos = conflitos_atual
        
        # Parar se encontrar solução
        if melhor_conflitos == 0:
            break
        
        # Busca local
        for _ in range(max_iter):
            # Gerar vizinhos
            vizinhos = gerar_vizinhos(solucao_atual)
            # Encontrar o melhor vizinho
            melhor_vizinho = solucao_atual
            conflitos_vizinho = conflitos_atual
            
            for vizinho in vizinhos:
                conflitos = calcular_conflitos(vizinho)
                if conflitos < conflitos_vizinho:
                    melhor_vizinho = vizinho
                    conflitos_vizinho = conflitos
            
            # Se não houver改善, parar esta iteração
            if conflitos_vizinho >= conflitos_atual:
                break
            
            # Mover para o melhor vizinho
            solucao_atual = melhor_vizinho
            conflitos_atual = conflitos_vizinho
            
            # Atualizar melhor solução
            if conflitos_atual < melhor_conflitos:
                melhor_solucao = solucao_atual.copy()
                melhor_conflitos = conflitos_atual
            
            # Parar se encontrar solução
            if conflitos_atual == 0:
                break
        
        # Parar se encontrar solução
        if melhor_conflitos == 0:
            break
    
    end_time = time.time()
    return melhor_solucao, melhor_conflitos, end_time - start_time

# Função para executar o algoritmo múltiplas vezes e coletar estatísticas
def executar_experimentos(n, num_execucoes=5):
    resultados = []
    for i in range(num_execucoes):
        solucao, conflitos, tempo = hill_climbing(n)
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