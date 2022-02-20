def clear():
    # Limpa o console e volta pra primeira linha, sem precisar importar OS
    print("\033[H\033[J", end="")


class Stats:
    def __init__(self):
        self._status_list = []
        self._status_list_cont = 0
        self.separador_cima = "------------------------------\n"
        self.separador_baixo = "\n------------------------------\n"

    @property
    def status_list(self):
        """Return the current status with separators."""
        return self.separador_cima + "\n".join(map(str, self._status_list)) + self.separador_baixo

    @status_list.setter
    def status_list(self, value):
        self._status_list = value

    def create_str_status(self, content):
        content = "".join(content).split('\n')
        try:
            return self.separador_cima + "\n".join(map(str, content)) + self.separador_baixo
        except Exception:
            return ("------------------------------\n"
                    + "\n".join(map(str, content))
                    + "\n------------------------------\n")

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
