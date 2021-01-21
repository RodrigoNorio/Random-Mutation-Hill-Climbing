import os 
import random
import math
import sys
import getopt

parametros = "-targetlibinfo -tti -tbaa -scoped-noalias -assumption-cache-tracker -profile-summary-info -forceattrs -inferattrs -callsite-splitting -ipsccp -called-value-propagation -globalopt -domtree -mem2reg -deadargelim -domtree -basicaa -aa -loops -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -instcombine -simplifycfg -basiccg -globals-aa -prune-eh -inline -functionattrs -argpromotion -domtree -sroa -basicaa -aa -memoryssa -early-cse-memssa -speculative-execution -domtree -basicaa -aa -lazy-value-info -jump-threading -lazy-value-info -correlated-propagation -simplifycfg -domtree -basicaa -aa -loops -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -instcombine -libcalls-shrinkwrap -loops -branch-prob -block-freq -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -pgo-memop-opt -domtree -basicaa -aa -loops -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -tailcallelim -simplifycfg -reassociate -domtree -loops -loop-simplify -lcssa-verification -lcssa -basicaa -aa -scalar-evolution -loop-rotate -licm -loop-unswitch -simplifycfg -domtree -basicaa -aa -loops -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -instcombine -loop-simplify -lcssa-verification -lcssa -scalar-evolution -indvars -loop-idiom -loop-deletion -loop-unroll -mldst-motion -aa -memdep -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -gvn -basicaa -aa -memdep -memcpyopt -sccp -domtree -demanded-bits -bdce -basicaa -aa -loops -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -instcombine -lazy-value-info -jump-threading -lazy-value-info -correlated-propagation -domtree -basicaa -aa -memdep -dse -loops -loop-simplify -lcssa-verification -lcssa -aa -scalar-evolution -licm -postdomtree -adce -simplifycfg -domtree -basicaa -aa -loops -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -instcombine -barrier -elim-avail-extern -basiccg -rpo-functionattrs -globalopt -globaldce -basiccg -globals-aa -float2int -domtree -loops -loop-simplify -lcssa-verification -lcssa -basicaa -aa -scalar-evolution -loop-rotate -loop-accesses -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -loop-distribute -branch-prob -block-freq -scalar-evolution -basicaa -aa -loop-accesses -demanded-bits -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -loop-vectorize -loop-simplify -scalar-evolution -aa -loop-accesses -loop-load-elim -basicaa -aa -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -instcombine -simplifycfg -domtree -loops -scalar-evolution -basicaa -aa -demanded-bits -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -slp-vectorizer -opt-remark-emitter -instcombine -loop-simplify -lcssa-verification -lcssa -scalar-evolution -loop-unroll -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -instcombine -loop-simplify -lcssa-verification -lcssa -scalar-evolution -licm -alignment-from-assumptions -strip-dead-prototypes -globaldce -constmerge -domtree -loops -branch-prob -block-freq -loop-simplify -lcssa-verification -lcssa -basicaa -aa -scalar-evolution -branch-prob -block-freq -loop-sink -lazy-branch-prob -lazy-block-freq -opt-remark-emitter -instsimplify -div-rem-pairs -simplifycfg -verify"
###########################################################################################
#FUNCOES AUXILIARES

#FUNCAO PARA LER ARQUIVO run.log
def ler_arquivo ():
    arquivo = open("run.log","r")  
    linha1 = arquivo.readline()
    linha2 = arquivo.readline()
    linha2 = linha2.split()
    arquivo.close()
    return float(linha2[3])

#FUNCAO PARA ESCREVER ARQUIVO
def escrever_arquivo_o3(nome_arquivo):
    arq = open('run.log', 'r')
    texto = arq.read()
    arq.close()

    arq = open(nome_arquivo, 'w')
    arq.write(texto)
    arq.close()

#FUNCAO PARA ESCREVER MELHOR CONJUNTO
def escrever_melhor_conjunto(novo_parametro1, nome_arquivo1):
    arq = open('run.log', 'r')
    texto = arq.read()
    arq.close()

    arq = open(nome_arquivo1, 'w')
    arq.write(texto)
    arq.write('\n\n'+'Conjunto otimizado:')
    arq.write('\n'+novo_parametro1)
    arq.close()

#FUNCAO ESCREVER TODOS OS TEMPOS DOS LOGS
def escrever_todos_tempos(tempo_logs, todos_tempos):
    k = ''
    for i in tempo_logs:
        k += str(i)+' '
    arq = open(todos_tempos, 'w')
    arq.write('\n\n'+'Todos os tempos:')
    arq.write('\n')
    arq.write(k)
    arq.close()

#FUNCAO DE AVISO -h
def aviso():
        print('\n\npython RMHC.py -x -i <int> \n')
        print('python RMHC [-x | -y | -z | -w] [-i <iteracoes>]  \n')  
        print('[-x]     Mutacao - remove parametro de O3\n')
        print('[-y]     Mutacao - insere parametro em O3\n')
        print('[-z]     Mutacao - swap entre elementos de O3\n')
        print('[-w]     Mutacao - troca elementos de O3 com elementos de uma lista de parametros\n')
        print('Exemplo: python RMHC.py -x -i 1000')

#################################################################################################
#INICIO FUNCOES DO RMHC

#FUNCAO QUE INVOCA O TF
def invoca_tf(parametros):    
    cmd = ('COMPILE=1 EXEC=1 OPT="{}" ./run.sh').format(parametros)
    os.system(cmd)  

#SWITCH CASE PARA SELECIONAR A MUTACAO
def escolhe_mutacao(opt, vet_parametros, guardar_parametros, ordenado):
    if opt == 1:
        vet_parametros = mutacao_deleta(vet_parametros, guardar_parametros)
        return vet_parametros
    elif opt == 2:
        vet_parametros = mutacao_insere(vet_parametros, ordenado)
        return vet_parametros
    elif opt == 3:
        vet_parametros = mutacao_swap(vet_parametros)
        return vet_parametros
    elif opt == 4:
        vet_parametros = mutacao_troca(vet_parametros, ordenado)
        return vet_parametros

#MUTACAO - DELETA ELEMENTO DE 03 (ALEATORIO)
def mutacao_deleta(vet_parametros, guardar_parametros):
    bit_random = random.randint(0, len(vet_parametros)-1)
    if len(vet_parametros) == 2:
        vet_parametros.extend(guardar_parametros)
        return vet_parametros
    else:
        guardar_parametros.append(vet_parametros[bit_random])
        del(vet_parametros[bit_random])
        return vet_parametros

#MUTACAO - INSERE ELEMENTO EM O3 (ALEATORIO)
def mutacao_insere(vet_parametros, ordenado):
    bit_random = random.randint(0, len(vet_parametros)-1)
    bit_random2 = random.randint(0, 79)
    if bit_random == bit_random2:
        while bit_random == bit_random2:
            bit_random = random.randint(0, len(vet_parametros)-1)
            bit_random2 = random.randint(0, 79)
        vet_parametros.insert(bit_random, ordenado[bit_random2])
        return vet_parametros
    else:
        vet_parametros.insert(bit_random, ordenado[bit_random2])
        return vet_parametros

#MUTACAO - SWAP ENTRE ELEMENTOS DE O3 (ALEATORIO)
def mutacao_swap(vet_parametros):
    bit_random = random.randint(0, len(vet_parametros)-1)
    bit_random2 = random.randint(0, len(vet_parametros)-1)
    if bit_random == bit_random2:
        while bit_random == bit_random2:
            bit_random = random.randint(0, len(vet_parametros)-1)
            bit_random2 = random.randint(0, len(vet_parametros)-1)
        vet_parametros[bit_random], vet_parametros[bit_random2] = vet_parametros[bit_random2], vet_parametros[bit_random]
        return vet_parametros
    else:
        vet_parametros[bit_random], vet_parametros[bit_random2] = vet_parametros[bit_random2], vet_parametros[bit_random]
        return vet_parametros

#MUTACAO - TROCA UM ELEMENTOS DE O3 COM ELEMENTO DE UMA LISTA SEM REPETICAO DE PARAMETROS(ALEATORIO)
def mutacao_troca(vet_parametros, ordenado):
    bit_random = random.randint(0, len(vet_parametros)-1)
    bit_random2 = random.randint(0, 79)
    if bit_random == bit_random2:
        while bit_random == bit_random2:
            bit_random = random.randint(0, len(vet_parametros)-1)
            bit_random2 = random.randint(0, 79)
        vet_parametros[bit_random] = ordenado[bit_random2]
        return vet_parametros
    else:
        vet_parametros[bit_random] = ordenado[bit_random2]
        return vet_parametros



#RMHC      
def RMHC(tempo_o3, vet_parametros, nome_arquivo, nome_arquivo1, nome_arquivo3, todos_tempos, tempo_logs, ordenado, opt, iteracoes):
    guardar_parametros = []
    melhor_fitness = tempo_o3
    novo_parametro1 = ''
    for ml in vet_parametros: #transformar em list em string
        novo_parametro1 += ml+' '
    escrever_melhor_conjunto(novo_parametro1, nome_arquivo1) #caso o melhor tempo seja o primeiro
    for i in range(iteracoes-1):   
        vet_parametros = escolhe_mutacao(opt, vet_parametros, guardar_parametros, ordenado)
        fitness = ler_arquivo()
        if fitness < melhor_fitness:
            melhor_fitness = fitness
            novo_parametro1 = ''
            for ml in vet_parametros: #transformar em list em string
                novo_parametro1 += ml+' '
            escrever_melhor_conjunto(novo_parametro1, nome_arquivo1)
        novo_parametro = ''
        for ml in vet_parametros:
            novo_parametro += ml+' '
        escrever_arquivo_o3(nome_arquivo3)
        invoca_tf(novo_parametro)
        tempo_logs.append(fitness)
    
    escrever_todos_tempos(tempo_logs, todos_tempos)
    
    
########################################################################################
#MAIN

try:
    (opts, args) = getopt.getopt(sys.argv[1:], 'hxyzwi:', [])

except getopt.GetoptError as err:
    print(err)
    sys.exit(2)
 
iteracoes = opt = None
if len(opts) != 0:
    for (o, a) in opts:
        if o in ('-h'):
            aviso()
        elif o in ('-x'):
            opt = 1
        elif o in ('-y'):
            opt = 2
        elif o in ('-z'):
            opt = 3
        elif o in ('-w'):
            opt = 4
        elif o in ('-i'):
            iteracoes = int(a)
        else:
            aviso()
            sys.exit(2)
else:
    aviso()
    sys.exit(2)


for i in range(3):
    nome_arquivo = "inirun"+str(i)+".log"
    nome_arquivo1 = "bestout"+str(i)+".log"
    nome_arquivo3 = "lastrun"+str(i)+".log"
    todos_tempos = "tempos"+str(i)+".log"
    tempo_logs = []
    invoca_tf(parametros)
    escrever_arquivo_o3(nome_arquivo)
    vet_parametros = parametros.split(" ")
    ordenado = sorted(set(vet_parametros))
    tempo_o3 = ler_arquivo()
    RMHC(tempo_o3, vet_parametros, nome_arquivo, nome_arquivo1, nome_arquivo3, todos_tempos,     tempo_logs, ordenado, opt, int(iteracoes))
    


##parametrizar iteracoes
##parametrizar mutacoes
##mutacao swap, mutacao inserir de outra lista

##grafico de tempo -- salvar o tempo de todos os logs para mostrar 
##guardar log inicial, melhor log e log final

#relatorio
#resumo 
#intro
#desenv
#resultados
#ref



