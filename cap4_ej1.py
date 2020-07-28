# Teoria de deteccion y estimacion - FIUBA 
# 1er cuatrimestre de 2020

# Autor: PABLO HSIEH 
# Padron: 97363

# Ejercicio computacional 1 del cap 4 del Duda-HArt-Stork


import numpy as np
import matplotlib.pyplot as plt


def puntos(n):
# Se generan n puntos en d dimensiones
    return np.random.uniform(-1/2,1/2,size=(1,n,3)),np.random.normal(0,1,size=(1,n,3))
    

# PARZEN
def pdf0_parzen(muestras,h):
# pdf estimada para un cubo de long h en el origen
    V = h**3
    N = np.size(muestras,1)
# debo contar cuantos k puntos hay dentro de un volumen V
# para cada set x=(x1,x2,x3) el punto esta dentro de V si abs(max(x))<h
    array_maximos = np.max(muestras,axis=2)
    array_boolean = array_maximos <= h #array booleano 
    k = np.sum(array_boolean)
    return k/N/V

# Kn    
def pdf0_kn(muestras,k):
#    N = np.size(muestras,1)
    distancia = np.zeros(0)
    for i in range(np.size(muestras,1)):
        distancia = np.append(distancia,max(abs(muestras[0,i,:])))
        
    distancia_ordenada = sorted(distancia)
    h = 2*distancia_ordenada[k-1]
    V = h**3
    N = np.size(muestras,1)
    return k/N/V
    

def graf(x,y,label_title,label_x,label_y,y_0,label_pdf0):
    fig = plt.figure()
    plt.plot(x,y,'o',linewidth=1)
    plt.axhline(y=y_0, color='r', linestyle='solid',linewidth=1,label=label_pdf0)
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.title(label_title)
    plt.grid()
    plt.legend(loc="best")
    plt.show()
    return fig    

    
def graficar_3d(x,y,z,unif,imprimir,n):
    if unif == 0:
        a = 4
        label_title = str(n)+str(' muestras Normal(0,I)')
    else:
        a = 1
        label_title = str(n)+str(' muestras Uniforme(-1/2;1/2)')        
    fig_graf = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter(x,y,z, marker='o')
    ax.set_xlim3d(-a,a)
    ax.set_ylim3d(-a,a)
    ax.set_zlim3d(-a,a)
    ax.set_xlabel('x_1')
    ax.set_ylabel('x_2')    
    ax.set_zlabel('x_3')
    plt.title(label_title)
#    plt.legend()
    plt.show()
    if imprimir == 1:
        if unif == 1:
            output_filename = 'fig_a-samples_unif.png' 
        else:
            output_filename = 'fig_a-samples_norm.png'          
        fig_graf.savefig(output_filename,bbox_inches='tight')



def hacer_parzen(muestras,imprimir,unif):
# si imprimir = 1 voy a imprimir el grafico
# si unif = 1, la distribucion que vino es uniforme, sino es la gaussiana
    h = np.linspace(0.1,1,50)
    pdf = np.zeros(0)
    
    for i in h:
        pdf= np.append( pdf, pdf0_parzen(muestras,i) )
    
    if unif == 1:
        label_title = str('Estimación de pdf Uniforme(-1/2;1/2) con ventanas de Parzen')
        label_pdf0 = str('pdf(0)=1')
        pdf0=1

    else:
        label_title = str('Estimación de pdf Normal(0,I) con ventanas de Parzen')
        pdf0 = (1/(np.sqrt(2*np.pi)))**3
        label_pdf0 = str('pdf(0)=')+str(round(pdf0,4))

    
    label_x = str('Ventana de longitud h')
    label_y = str('Estimación pdf en el origen')
    
    fig_graf = graf(h,pdf,label_title,label_x,label_y,pdf0,label_pdf0)
    if imprimir == 1:
        if unif == 1:
            output_filename = 'fig_b-pdf_vs_h(parzen)_unif.png'
        else:
            output_filename = 'fig_b-pdf_vs_h(parzen)_normal.png'            
        fig_graf.savefig(output_filename,bbox_inches='tight')
        
        
def hacer_Kn(muestras,imprimir,unif):
#    k = np.linspace(0.1,1,50)
    k = np.linspace(1,np.size(muestras,1),100,dtype = int)
    pdf = np.zeros(0)
    
    for i in k:
        pdf = np.append( pdf , pdf0_kn(muestras, i))

    
    if unif == 1:
        label_title = str('Estimación de pdf Uniforme(-1/2;1/2) con Kn vecinos')
        label_pdf0 = str('pdf(0)=1')
        pdf0=1

    else:
        label_title = str('Estimación de pdf Normal(0,I) con Kn vecinos')
        pdf0 = (1/(np.sqrt(2*np.pi)))**3
        label_pdf0 = str('pdf(0)=')+str(round(pdf0,4))

    
    label_x = str('k vecinos')
    label_y = str('Estimación pdf en el origen')
    
    fig_graf = graf(k,pdf,label_title,label_x,label_y,pdf0,label_pdf0)
    if imprimir == 1:
        if unif == 1:
            output_filename = 'fig_c-pdf_vs_k(Kn)_unif.png'
        else:
            output_filename = 'fig_c-pdf_vs_k(Kn)_normal.png'            
        fig_graf.savefig(output_filename,bbox_inches='tight')
        

######################
####### MAIN() #######
######################        
    
n=10000
imprimir = 0 # para imprimir figura, poner en 1

# Genero las muestras uniforme y normal
samples_unif , samples_norm = puntos(n)


graficar_3d(samples_unif[:,:,0],samples_unif[:,:,1],samples_unif[:,:,2],1,imprimir,n)
graficar_3d(samples_norm[:,:,0],samples_norm[:,:,1],samples_norm[:,:,2],0,imprimir,n)

hacer_parzen(samples_unif, imprimir, 1)
hacer_parzen(samples_norm, imprimir, 0)

hacer_Kn(samples_unif, imprimir, 1)
hacer_Kn(samples_norm, imprimir, 0)




