import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_graph(self, e):
        nodes, n_edges, e_min, e_max = self._model.build_graph()
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Numero di vertici:  {nodes}, numero di archi: {n_edges}"))
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Informazioni sui pesi degli archi: -valore minimo: {e_min} e valore massimo: {e_max}"))
        self._view.update()
    def handle_conta_edges(self, e):
        input = float(self._view.txt_name.value)
        n_edges_over, n_edges_under = self._model.count_edges(input)
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Numero archi con peso maggiore della soglia: {n_edges_over}"))
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Numero archi con peso minore della soglia: {n_edges_under}"))
        self._view.update()

    def handle_ricerca(self, e):
        input = float(self._view.txt_name.value)
        sol_ott, dist_ott = self._model.ricerca_cammino(input)
        self._view.lista_visualizzazione_3.controls.clear()
        self._view.lista_visualizzazione_3.controls.append(ft.Text(f"Numero archi percorso più lungo: {len(sol_ott)}"))
        self._view.lista_visualizzazione_3.controls.append(ft.Text(f"Peso cammino massimo: {dist_ott}"))
        for e in sol_ott:
            self._view.lista_visualizzazione_3.controls.append(ft.Text(f"{e[0]} --> {e[1]}: {e[2]}"))

        self._view.update()
