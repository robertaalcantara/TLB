import numpy as np
import matplotlib.pyplot as plt

def grafico(v1, v2):
    plt.plot(v1, v2)
    plt.title('Resultados')
    plt.xlabel('Contadores') #rotula o eixo x
    plt.ylabel('Tamanho') #rotula o eixo y
    plt.ylim(0, 4096) #limites do eixo x
    plt.show()
    

#lê os arquivos para cada tamanho de TLB e retorna as taxas
def simulador(tamanho):
    # arquivos = ['bigone', 'bzip', 'gcc', 'sixpack', 'swim']
    arquivos = ['bzip', 'gcc']
    tlb = []
    #variaveis que retornam todos os valores calculados dai
    taxasAcerto = []
    taxasAdd = []
    taxasSub = []
    contInTlb = []
    contNewTlb = []
    contSubTlb = []

    for arquivo in arquivos:

        inTlb = 0 #ja esta na tlb
        newTlb = 0 #nao esta na tlb, e acrescenta na tlb
        subTlb = 0 #substitui um valor ja escrito

        file = open('Arquivos/'+arquivo+'.trace', 'r')

        linhas = file.readlines()

        for linha in linhas:
            endereco = linha[:5] #pega os 5 primeiros números, referentes ao endereço

            #verifica se o endereço já se encontra na TLB
            if(endereco in tlb):
                inTlb += 1
            #verifica se existe espaço livre na TLB e adiciona o endereço ao final
            elif(len(tlb) < tamanho):
                newTlb += 1
                tlb.append(endereco)
            #elimina o endereço da primeira posição da TLB para liberar espaço (FIFO)
            #adiciona o endereço atual ao final da TLB
            else:
                subTlb += 1
                tlb.pop(0)
                tlb.append(endereco)
        
        taxaAcerto = inTlb / len(linhas) 
        taxasAcerto.append(taxaAcerto)
        contInTlb.append(inTlb)
        
        taxaAdd = newTlb / len(linhas) #taxa de adições à TLB com espaço livre
        taxasAdd.append(taxaAdd)
        contNewTlb.append(newTlb)
        
        taxaSub = subTlb / len(linhas) #taxa de substituições na TLB
        taxasSub.append(taxaSub)
        contSubTlb.append(subTlb)

    file.close()
    return contInTlb, taxasAcerto, contNewTlb, taxasAdd, contSubTlb, taxasSub
    

if __name__ == "__main__":
    tm = 150
    tTlb = 60
    tmac = [] #tempo médio de acesso

    for i in range(1,13):
        
        tam = pow(2,i)
        # print(tam)

        contInTlb, taxasAcerto, contNewTlb, taxasAdd, contSubTlb, taxasSub = simulador(tam)
        print(contInTlb, taxasAcerto, contNewTlb, taxasAdd, contSubTlb, taxasSub)

        for i in taxasAcerto:
            time = i * (tTlb+tm) + (1 - i) * (tTlb + 2 * tm)
            tmac.append(time)

        # print("tamanho: ", tam)
        # print("tmac: ", tmac)
        # tmac = alfa(Ttlb+Tm)+(1 - alfa)(Ttlb + 2 * Tm),onde:
        # taxasAcerto[i] = taxa de acerto da tlb
        # tTlb = tempo de acesso à tlb
        # tm = tempo médio
        
    tamanho = [2,4,8,16,32,64,128,256,512,1024,2048,4096]
    # print(contNewTlb)
    # plt.plot(tamanho,np.array(contInTlb))
    # plt.show()
    # grafico(contInTlb, tamanho)
