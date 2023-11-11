
from customtkinter import CTk, CTkFrame, CTkButton, CTkEntry, CTkLabel, CTkCheckBox
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
        self.frame_plot.grid(column = 0, row = 2, sticky = 'nsew', padx = 50, pady = 50, columnspan =1)


        self.fram_option.columnconfigure(0, weight = 1)
        self.fram_option.rowconfigure((0,1,2,3,4,5,6,7), weight = 1)

        self.frame_plot.rowconfigure(0, weight = 1)
        self.frame_plot.columnconfigure(0, weight = 1)

        


        self.columnconfigure((0,1,2,3,4), weight = 1)
        self.rowconfigure((0,1,2,3,4), weight = 1)


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


        self.run_sim = CTkButton(self.fram_option, font = ('sans rerif',12),corner_radius=12, border_color = c_green, 
                            fg_color=c_black, text= "Simular", text_color = c_green, width=220, height=40,
                            border_width=2, command = self.run_sim_callback)


        self.run_sim.grid(columnspan=2, row = 6, padx = 1, pady = 1)

        self.clean_graph = CTkButton(self.fram_option, font = ('sans rerif',12),corner_radius=12, border_color = c_green, 
                            fg_color=c_black, text= "Limpiar el grafo", text_color = c_green, width=220, height=40,
                            border_width=2, command = self.destroy_canvas)


        self.clean_graph.grid(columnspan=2, row = 7, padx = 1, pady = 1)

        self.plot_sim = CTkButton(self.frame_plot, font = ('sans rerif',12),corner_radius=12, border_color = c_green, 
                            fg_color=c_black, text= "Graficar simulación", text_color = c_green, width=220, height=40,
                            border_width=2, command = self.simulation_plot)
        self.plot_sim.configure(state= 'disabled')

        self.plot_sim.grid(row=0, columnspan = 1, padx = 1, pady = 1)



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
        
            self.sim = Simulation(people,time,240,prob_of_edges,mosquitos, prob_bite, prob_inf)

            self.graph = self.sim.run_simulation()

            self.plot_sim.configure(state = 'normal')

            # layout = self.graph.layout('kk')
            layout = self.graph.layout_kamada_kawai()

            fig, ax = plt.subplots()

            ig.plot(self.graph, layout=layout, target=ax,vertex_size=10)

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
        cont = [0 for x in range(int(len(pers_hour)/24))]
        pers_counted = []
        count = -1
        indice = 0
        for lista in pers_hour.values():
            count +=1
            if count == 24:
                count = -1
                indice += 1
                pers_counted.clear()
            for i in range(len(lista)):
                if lista[i][1] and lista[i][0] not in pers_counted:
                    pers_counted.append(lista[i][0])
                    cont[indice] += 1
            
        
        ventana_grafico.title("Gráfico")
        plt.clf()

        plt.plot(cont)
        plt.xlabel('Dias de simulacion')
        plt.ylabel('Personas enfermas')
        plt.title('Grafico de la simulacion')
        plt.show()










