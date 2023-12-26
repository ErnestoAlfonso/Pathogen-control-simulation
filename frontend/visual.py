
from customtkinter import CTk,CTkToplevel, CTkFrame, CTkButton, CTkEntry, CTkLabel, CTkCheckBox, CTkCanvas
from tkinter import PhotoImage
from simulation.dinamic_control_dengue import Simulation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import igraph as ig


c_black = '#010101'
c_violet = '#7f5af0'
c_green = '#2cb67d'

class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('500x600+350+20')
        self.minsize(480,500)
        self.config(bg = c_black)
        self.title("Simulador de Dengue")

        self.graph = 0
        self.available = False

        
        label = CTkLabel(self, font=('sans rerif', 32), text="Bienvenido", fg_color=c_black, bg_color=c_black)
        label.grid(row=0, sticky = 'new', columnspan = 5)

        self.fram_option = CTkFrame(self, fg_color= c_black, bg_color=c_black, border_color= c_black)
        self.fram_option.grid(column = 0, row = 1, sticky = 'ns', padx = 100, pady = 100)

        self.frame_graph = CTkFrame(self,fg_color= c_black, bg_color=c_black, border_color= c_black)
        self.frame_graph.grid(column = 1, row = 1, sticky = 'nsew', padx = 50, pady = 50, columnspan = 3, rowspan = 3)

        self.frame_plot = CTkFrame(self,fg_color= c_black, bg_color=c_black, border_color= c_black)
        self.frame_plot.grid(column = 0, row = 3, sticky = 'nsew', padx = 50, pady = 50, columnspan =1)

        self.frame_legend = CTkFrame(self,fg_color = c_black, bg_color = c_black, border_color = c_black)
        self.frame_legend.grid(column = 1, row = 3, sticky = 'nsew', padx = 50, pady = 50, columnspan = 3)


        self.fram_option.columnconfigure(0, weight = 1)
        self.fram_option.rowconfigure((0,1,2,3,4,5,6,7,8), weight = 1)

        self.frame_legend.columnconfigure((0,1,2,3,4,5,6,7,8), weight = 1, pad=0)
        self.frame_legend.rowconfigure((0,1), weight = 1)

        self.frame_plot.rowconfigure(0, weight = 1)
        self.frame_plot.columnconfigure(0, weight = 1)

        


        self.columnconfigure((0,1,2,3,4,5), weight = 1)
        self.rowconfigure((0,1,2,3,4,5), weight = 1)


        self.people = CTkEntry(self.fram_option, font = ('sans rerif', 12), placeholder_text = "Tamaño de la población",
                        border_color = c_green, fg_color = c_black, width = 220, height = 40)
        
        self.people.grid(columnspan = 2, row = 0, padx = 1, pady = 1)

        self.time = CTkEntry(self.fram_option, font = ('sans rerif', 12), placeholder_text = "Tiempo a simular",
                        border_color = c_green, fg_color = c_black, width = 220, height = 40)
        
        self.time.grid(columnspan = 2, row = 1, padx = 1, pady = 1)

        self.prob_edges = CTkEntry(self.fram_option, font = ('sans rerif', 12), placeholder_text = "Probabilidad de Aristas",
                        border_color = c_green, fg_color = c_black, width = 220, height = 40)
        
        self.prob_edges.grid(columnspan = 2, row = 2, padx = 1, pady = 1) 

        self.mosq = CTkEntry(self.fram_option, font = ('sans rerif', 12), placeholder_text = "Mosquitos por Lugares",
                        border_color = c_green, fg_color = c_black, width = 220, height = 40)

        self.mosq.grid(columnspan = 2, row = 3, padx = 1, pady = 1)

        self.mosq_prob_bite_ap = CTkEntry(self.fram_option, font = ('sans rerif', 12), placeholder_text = "Probabilidad de picar por hora",
                        border_color = c_green, fg_color = c_black, width = 220, height = 40)

        self.mosq_prob_bite_ap.grid(columnspan = 2, row = 4, padx = 1, pady = 1) 

        self.mosq_inf_if_bite = CTkEntry(self.fram_option, font = ('sans rerif', 12), placeholder_text = "Probabilidad de infectarse",
                        border_color = c_green, fg_color = c_black, width = 220, height = 40)

        self.mosq_inf_if_bite.grid(columnspan = 2, row = 5, padx = 1, pady = 1) 

        self.prob_die_h = CTkEntry(self.fram_option, font = ('sans rerif', 12), placeholder_text = "Probabilidad de morir infectado/d",
                        border_color = c_green, fg_color = c_black, width = 220, height = 40)

        self.prob_die_h.grid(columnspan = 2, row = 6, padx = 1, pady = 1)

        self.run_sim = CTkButton(self.fram_option, font = ('sans rerif',12),corner_radius=12, border_color = c_green, 
                            fg_color=c_black, text= "Simular", text_color = c_green, width=220, height=40,
                            border_width=2, command = self.run_sim_callback)


        self.run_sim.grid(columnspan=2, row = 7, padx = 1, pady = 1)

        self.clean_graph = CTkButton(self.fram_option, font = ('sans rerif',12),corner_radius=12, border_color = c_green, 
                            fg_color=c_black, text= "Limpiar el grafo", text_color = c_green, width=220, height=40,
                            border_width=2, command = self.destroy_canvas)


        self.clean_graph.grid(columnspan=2, row = 8, padx = 1, pady = 1)

        self.plot_sim = CTkButton(self.frame_plot, font = ('sans rerif',12),corner_radius=12, border_color = c_green, 
                            fg_color=c_black, text= "Graficar simulación", text_color = c_green, width=220, height=40,
                            border_width=2, command = self.simulation_plot)
        self.plot_sim.configure(state = 'disabled')
        self.plot_sim.grid(row=0, columnspan = 1, padx = 1, pady = 1)

        self.person_action_per_day = CTkButton(self.frame_plot, font = ('sans rerif',12),corner_radius=12, border_color = c_green, 
                            fg_color=c_black, text= "Acciones realizadas", text_color = c_green, width=220, height=40,
                            border_width=2, command = self.actions)
        self.person_action_per_day.configure(state = 'disabled')
        self.person_action_per_day.grid(row=1, columnspan = 1, padx = 1, pady = 1)

        self.legend = CTkLabel(self.frame_legend,font = ('sans rerif',12),corner_radius=12, anchor='e',
                            fg_color=c_black, text = "Leyenda:", text_color = c_green, width=220, height=40,)
        
        self.legend.grid(row = 0, column = 0, padx=1, pady=1)
        




        self.people_h = CTkLabel(self.frame_legend,font = ('sans rerif',12),corner_radius=12,anchor='e',
                            fg_color=c_black, text = "Personas sanas:", text_color = c_green, width=100, height=40)
        self.people_h.grid(row = 1, column = 0, padx=1, pady=1)

        self.people_s = CTkLabel(self.frame_legend,font = ('sans rerif',12),corner_radius=12,anchor='e',
                            fg_color=c_black, text = "Personas enfermas:", text_color = c_green, width=100, height=40)

        self.people_s.grid(row = 1, column = 3, padx=1, pady=1)

        red_circle = CTkCanvas(self.frame_legend, height = 14, width = 14,highlightthickness=0,background= c_black)
        red_circle.grid(row = 1, column = 1, padx=1, pady=1, sticky='w')
        red_circle.grid_columnconfigure(0, weight=1,pad=2)
        red_circle.grid_rowconfigure(0, weight=1,pad=2)
        x = 6 # Coordenada x del centro del círculo
        y = 6 # Coordenada y del centro del círculo
        radio = 6  # Radio del círculo
        red_circle.create_oval(x - radio, y - radio, x + radio, y + radio, fill="red")


        black_circle = CTkCanvas(self.frame_legend, height = 14, width = 14,highlightthickness=0,background= c_black)
        black_circle.grid(row = 1, column = 4, padx=1, pady=1, sticky='w')
        black_circle.grid_rowconfigure(0, weight=1, pad=2)
        black_circle.grid_columnconfigure(0, weight=1, pad=2)
        x = 6 # Coordenada x del centro del círculo
        y = 6 # Coordenada y del centro del círculo
        radio = 6  # Radio del círculo
        black_circle.create_oval(x - radio, y - radio, x + radio, y + radio, fill="black",outline="white")



    def destroy_canvas(self):
        try:
            self.canvas.get_tk_widget().destroy()
        
        except:
            return "ERROR: No existe un canvas a destruir"

    
    def run_sim_callback(self):
        try:
            if self.available:
                self.canvas.get_tk_widget().destroy()
            people = int(self.people.get())
            time = int(self.time.get())
            prob_of_edges = float(self.prob_edges.get())
            mosquitos = int(self.mosq.get())
            prob_bite = float(self.mosq_prob_bite_ap.get())
            prob_inf = float(self.mosq_inf_if_bite.get())
            prob_die_h = float(self.prob_die_h.get())
        
            self.sim = Simulation(people,time,240,prob_of_edges,mosquitos, prob_bite, prob_inf, prob_die_h)

            self.graph = self.sim.run_simulation()

            self.plot_sim.configure(state = 'normal')
            self.person_action_per_day.configure(state = 'normal')

            color_dict = {"I": "black", "NI": "red"}
            self.graph.vs["color"] = [color_dict[infected] for infected in self.graph.vs["infected"]]
            # layout = self.graph.layout('kk')
            layout = self.graph.layout_kamada_kawai()

            fig, ax = plt.subplots()

            ig.plot(self.graph, layout=layout, target=ax,vertex_size=10)

            # print("Nodes")
            # print(nodes)
            # for node in self.graph.vs["person"]:
            #     if node.infected > 0:
            #         nodes._facecolors[node.index] = 'black'
                
            self.canvas = FigureCanvasTkAgg(fig, master=self.frame_graph)
            self.canvas.draw()
            self.canvas.get_tk_widget().grid(sticky='nsew')

            self.frame_graph.columnconfigure(0,weight=1)
            self.frame_graph.rowconfigure(0,weight=1)

            self.available = True

        
        except Exception as e:
            print(e)
            # return "ERROR: el valor de las personas, el tiempo y la probabilidad de aristas debe ser un numero"
    
    def simulation_plot(self):
        ventana_grafico = CTk()
        pers_hour = self.sim.dictOfHours
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
            
        
        ventana_grafico.title("Gráfico")
        plt.clf()

        plt.plot(infected_people, color = 'red')
        plt.plot(healthy_people, color = 'green')
        plt.plot(dead_people, color = 'black')
        plt.xlabel('Dias de simulacion')
        plt.ylabel('Personas enfermas')
        plt.title('Grafico de la simulacion')
        plt.show()


    def actions(self):
        self.ventana_grafico = CTkToplevel()
        self.ventana_grafico.geometry('500x600+350+20')
        self.ventana_grafico.minsize(480,500)
        self.ventana_grafico.config(bg = c_black)
        self.ventana_grafico.title("Simulador de Dengue")


        self.fram_op = CTkFrame(self.ventana_grafico, fg_color= c_black, bg_color=c_black, border_color= c_black)
        self.fram_op.grid(column = 0, row = 1, sticky = 'ns', padx = 100, pady = 100)

        self.frame_actions = CTkFrame(self.ventana_grafico,fg_color= c_black, bg_color=c_black, border_color= c_black)
        self.frame_actions.grid(column = 1, row = 1, sticky = 'nsew', padx = 50, pady = 50, columnspan = 9, rowspan = 8)
        

        self.person = CTkEntry(self.fram_op, font = ('sans rerif', 12), placeholder_text = "Seleccione la persona",
                        border_color = c_green, fg_color = c_black, width = 220, height = 40)
        
        self.person.grid(columnspan = 2, row = 0, padx = 1, pady = 1)

        self.day = CTkEntry(self.fram_op, font = ('sans rerif', 12), placeholder_text = "Seleccione el día",
                        border_color = c_green, fg_color = c_black, width = 220, height = 40)
        
        self.day.grid(columnspan = 2, row = 1, padx = 1, pady = 1)

        self.run_actions = CTkButton(self.fram_op, font = ('sans rerif',12),corner_radius=12, border_color = c_green, 
                            fg_color=c_black, text= "Mostrar", text_color = c_green, width=220, height=40,
                            border_width=2, command = self.show_actions)


        self.run_actions.grid(columnspan=2, row = 6, padx = 1, pady = 1)

        self.clean_actions = CTkButton(self.fram_op, font = ('sans rerif',12),corner_radius=12, border_color = c_green, 
                            fg_color=c_black, text= "Limpiar acciones", text_color = c_green, width=220, height=40,
                            border_width=2, command = self.destroy_actions)


        self.clean_actions.grid(columnspan=2, row = 7, padx = 1, pady = 1)
    

    def show_actions(self):
        person = int(self.person.get())
        day = int(self.day.get()) - 1
        start = day*24
        

        self.list_action = []
        self.list_label = []
        for x in range(start,start+24):
            self.list_action.append(self.sim.dictOfAction[person][x])
        i = 0
        j = 0
        for item in self.list_action:
            label = CTkLabel(self.frame_actions,font = ('sans rerif',12),corner_radius=12, 
                            fg_color=c_black, text = item, text_color = c_green, width=220, height=40)
            label.grid(columnspan = 3, row = i, column = j, padx = 1, pady = 1)
            self.list_label.append(label)
            i+=1
            if i == 10:
                j += 4
                i = 0
    
    def destroy_actions(self):
        self.frame_actions.destroy()
        self.list_action.clear()
        for item in self.list_label:
            item.destroy()
        self.frame_actions = CTkFrame(self.ventana_grafico,fg_color= c_black, bg_color=c_black, border_color= c_black)
        self.frame_actions.grid(column = 1, row = 1, sticky = 'nsew', padx = 50, pady = 50, columnspan = 9, rowspan = 8)


