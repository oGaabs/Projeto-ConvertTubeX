class Stats:
    """docstring for Stats."""

    def __init__(self):
        self._status_list = []
        self._status_list_cont = 0
        self._separador_cima = "-" * 30 + "\n"
        self._separador_baixo = "\n" + "-" * 30 + "\n"

    @property
    def status_list(self):
        """The status property."""
        return (
            self.separador_cima
            + "\n".join(map(str, self._status_list))
            + self.separador_baixo
        )

    @status_list.setter
    def status_list(self, value):
        self._status_list = value

    @property
    def separador_baixo(self):
        """The separador_baixo property."""
        return self._separador_baixo

    @separador_baixo.setter
    def separador_baixo(self, value):
        self._separador_baixo = value

    @property
    def separador_cima(self):
        """The separador_cima property."""
        return self._separador_cima

    @separador_cima.setter
    def separador_cima(self, value):
        self._separador_cima = value

    def add(self, value):
        self._status_list.append(value)
        self._status_list_cont += 1

    def remove(self, value):
        self.status_list.remove(value)
        self._status_list_cont -= 1

    def pop(self, index):
        self._status_list.pop(index)
        self._status_list_cont -= 1

    def clear_list(self):
        self._status_list.clear()
        self._status_list_cont = 0
