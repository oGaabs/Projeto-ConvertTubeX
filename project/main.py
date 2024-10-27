"""
Esse script utiliza pytube e moviepy para baixar videos do youtube,
fique claro que você esta sujeito a licença desses dois softwares.
O download do arquivo mp3/mp4 é feito utilizando a URL do vídeo de origem
contudo, caso queira utilizar o conteudo para meio não pessoal,
é preciso pedir permissão para o autor.
Você é plenamente responsável pelo uso do script
e está sujeito à lei do seu país, o script é de uso livre, lembrando que
não damos qualquer garantia ou direitos sobre os videos, não é preciso
fazer atribuição do script, mas aprecio a mesma.

Autor: Gabriel Santana
Date: 20/02/22

"""
import sys
from PySide6.QtWidgets import QApplication
from gui.window_manager import WindowManager

def main():
    """Main function to initialize the application."""
    app = QApplication(sys.argv)
    window_manager = WindowManager()
    window_manager.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()