import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        countries=self._model.getAllCountries()
        for c in countries:
            self._view.ddcountry.options.append(ft.dropdown.Option(c))

        for i in range(2015,2019):
            self._view.ddyear.options.append(ft.dropdown.Option(i))


    def handle_graph(self, e):

        country=self._view.ddcountry.value
        anno=self._view.ddyear.value

        if country==None or country=="":
            self._view.create_alert("Seleziona un paese!")
            return

        if anno==None or anno=="":
            self._view.create_alert("Seleziona un anno!")
            return

        #posso creare il grafo
        self._model.buildGraph(country, anno)
        numNodes=self._model.getNumNodes()
        numArchi=self._model.getNumEdges()
        if numNodes==0:
            self._view.txt_result.controls.append(ft.Text(f"Non esiste un grafo con i parametri indicati"))
            return

        self._view.btn_volume.disabled=False
        self._view.txtN.disabled=False
        self._view.btn_path.disabled=False

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {numNodes} Numero di archi: {numArchi}"))


        self._view.update_page()



    def handle_volume(self, e):
        self._view.txtOut2.controls.clear()
        volumiVendita = self._model.getVolumeDiVendita()
        if volumiVendita != []:
            for v in volumiVendita:
                self._view.txtOut2.controls.append(ft.Text(f"{str(v[0])} --> {str(v[1])}"))

        self._view.update_page()


    def handle_path(self, e):
        num=self._view.txtN.value
        self._view.txtOut3.controls.clear()

        if num=="":
            self._view.create_alert("Inserire un numero!")
            return

        try:
            numInt=int(num)
        except ValueError:
            self._view.txtOut3.controls.append(ft.Text("Inserire un numero intero!", color="red"))
            self._view.update_page()
            return

        if numInt<=1:
            self._view.txtOut3.controls.append(ft.Text("Inserire un numero maggiore di 1!", color="red"))
            self._view.update_page()
            return

        path, costo= self._model.getPercorsoOpt(numInt)
        if costo==0:
            self._view.txtOut3.controls.append(ft.Text("Non esiste un cammino con il numero di tratte inserito."))
            self._view.update_page()
            return

        self._view.txtOut3.controls.append(ft.Text(f"Peso cammino massimo: {costo}"))
        for i in range(0, len(path)-1):
            peso=self._model.getPeso(path[i], path[i+1])
            self._view.txtOut3.controls.append(ft.Text(f"{str(path[i])} --> {str(path[i+1])}: {peso}"))

        self._view.update_page()

