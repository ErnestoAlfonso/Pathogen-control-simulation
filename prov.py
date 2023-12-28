from simulation.dinamic_control_dengue import Simulation
import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots()

cntd_personas = 30
cntd_dias = 5
valor_mercado = 250
prob_arista = 0.2
cntd_mosq_por_lugar = 20
prob_picar = 0.04
prob_infectarse = 0.2
prob_morir_por_hora = 0.0001

salvar_figura = f"AP{str(cntd_personas)}AD{str(cntd_dias)}MV{str(valor_mercado)}PAR{str(prob_arista)}AM{str(cntd_mosq_por_lugar)}PB{str(prob_picar)}PI{str(prob_infectarse)}PM{prob_morir_por_hora}.png"


sim = Simulation(cntd_personas,cntd_dias, valor_mercado, prob_arista, cntd_mosq_por_lugar, prob_picar, prob_infectarse, prob_morir_por_hora)

sim.run_simulation()
contact = []
pos = None
pers_hour = sim.dictOfHours
infected_people = [0 for x in range(int(len(pers_hour)/24))]
healthy_people = [0 for x in range(int(len(pers_hour)/24))]
dead_people = [0 for x in range(int(len(pers_hour)/24))]
pers_counted_i = []
pers_counted_h = []
pers_counted_d = []
count = -1
indice = 0
for lista in pers_hour.values():
    count +=1
    if count == 24:
        count = -1
        indice += 1
        pers_counted_i.clear()
        pers_counted_h.clear()
        pers_counted_d.clear()
    for i in range(len(lista)):
        if lista[i][1] and lista[i][0] not in pers_counted_i:
            pers_counted_i.append(lista[i][0])
            infected_people[indice] += 1
        elif not lista[i][1] and lista[i][0] not in pers_counted_h:
            pers_counted_h.append(lista[i][0])
            healthy_people[indice] += 1
        elif lista[i][1] == "Muerta":
            pers_counted_d.append(lista[i][0])
            dead_people[indice] += 1

for item in sim.graph.graph.vs:
    contact.append(len(sim.graph.graph.neighbors(item)))
contact_per_person_count = [0 for l in range(len(contact))]
for i in range(len(contact)):
    contact_per_person_count[i] = contact.count(i)

for j in range(len(contact_per_person_count)):
    if contact_per_person_count[j] != 0:
        pos = j
        
if pos is not None:
    contact_per_person_count = contact_per_person_count[:pos+1]

fig, ax = plt.subplots(2,2,sharey=True)

fig.set_size_inches(16, 16)

r = [x+1 for x in range(len(sim.person_per_places))]
print(sim.person_per_places)
ax[0,0].bar(r,sim.person_per_places)
ax[0,0].set_ylabel('No. de personas')
ax[0,0].set_xlabel('No. de localizaciones visitadas')

ax[0,1].plot(infected_people, color = 'red', label= 'Personas Infectadas')
ax[0,1].plot(healthy_people, color = 'green', label = 'Personas Sanas')
ax[0,1].plot(dead_people, color = 'black', label = 'Personas Fallecidas')
ax[0,1].set_xlabel('Dias de simulacion')
ax[0,1].set_ylabel('Personas enfermas')
ax[0,1].legend(loc = 'upper right')

ax[1,0].scatter([x for x in range(len(contact_per_person_count))], contact_per_person_count)
ax[1,0].set_ylabel('No. de personas con k contactos')
ax[1,0].set_xlabel('No. de contactos')


plt.savefig(salvar_figura)

plt.show()


# l = [1,2,3]
# b = set()
# b.add(l[1])
# b.add(l[2])
# b.add(l[0])

# print(len(b))


# from frontend.visual import App

# app = App()
# app.mainloop()

# a = {'a': 1, 'b': 2, 'c': 3}


