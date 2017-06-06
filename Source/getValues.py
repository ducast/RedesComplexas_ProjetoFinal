import os
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
	log_path = "log.txt"
	grau_medio = []
	comp_conx = []
	with open(log_path, 'r') as logFile:
		for line in logFile:
			if 'Conected comp.:' in line:
				comp_size = int(line.split('[')[-1].split(']')[0].split(' ')[0])
				comp_conx.append(comp_size)
			if 'Grau total' in line:
				grau = float(line.split('media')[-1].split('|')[0].split(' ')[5])
				grau_medio.append(grau)


	plt.figure(figsize=(6,4))
	plt.title("Tamanho da Maior Componente Conexa")
	myX = np.arange(len(comp_conx))
	plt.gca().plot(myX, comp_conx, 'b+')
	plt.xlabel("Iteracao")
	plt.ylabel("Tamanho da Componente")
	plt.tight_layout()
	plt.savefig("componenteConexa.pdf")


	plt.figure(figsize=(6,4))
	plt.title("Grau Medio")
	myX = np.arange(len(grau_medio))
	plt.gca().plot(myX, grau_medio, 'b+')
	plt.xlabel("Iteracao")
	plt.ylabel("Grau Medio")
	plt.tight_layout()
	plt.savefig("grauMedio.pdf")
