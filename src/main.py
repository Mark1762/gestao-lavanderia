import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QAbstractItemView,
    QWidget, QVBoxLayout, QTableView, QLineEdit, QHeaderView
)
from PyQt5.QtCore import QPropertyAnimation, QPoint, QModelIndex
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

# Importe as classes geradas
from login_ui import Ui_Dialog as Ui_LoginDialog
from mainwindow_ui import Ui_MainWindow
from Tabela import Ui_Dialog as Ui_TabelaDialog


# Janela da tabela "entrada_cortes"
class TabelaCortesWindow(QDialog, Ui_TabelaDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Entrada de Cortes - Portal Jeans")

        # Conexão com o banco de dados
        self.db = QSqlDatabase.addDatabase("QSQLITE", "conexao_entrada_cortes")
        self.db.setDatabaseName("db1.db")

        if not self.db.open():
            print("Erro ao abrir banco de dados")
            return

        self.model = QSqlTableModel(self, self.db)
        self.model.setTable("entrada_cortes")
        # Altera a estratégia para que as alterações só sejam salvas com o botão "Salvar"
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.select()
        
        # Conecta o modelo à visualização (Tabela)
        self.tableView.setModel(self.model)
        
        # Ajusta as colunas para o tamanho do conteúdo
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # Estica a última coluna para preencher o espaço restante
        self.tableView.horizontalHeader().setStretchLastSection(True)
        
        # Permite a edição com dois cliques
        self.tableView.setEditTriggers(QAbstractItemView.DoubleClicked)
        
        # Conecta os botões
        self.btnSalvarRegistro.clicked.connect(self.salvar_registro)
        self.btnExcluirLinha.clicked.connect(self.excluir_linha)
        self.btnHistorico.clicked.connect(self.historico_de_registro)
        self.btnFechar.clicked.connect(self.fechar_janela)
        # Conectando o botão de adicionar linha com o nome correto
        self.btnAdicionarRegistro.clicked.connect(self.adicionar_linha)


    def salvar_registro(self):
        # Envia todas as alterações para o banco de dados
        self.model.submitAll()
        self.model.select() # Recarrega a tabela para mostrar as mudanças


    def adicionar_linha(self):
        # Insere uma nova linha em branco na última posição
        row = self.model.rowCount()
        self.model.insertRows(row, 1)

        # Move a visualização para o final, seleciona a nova linha e coloca em modo de edição
        index = self.model.index(row, 0)
        self.tableView.scrollToBottom()
        self.tableView.setCurrentIndex(index)
        self.tableView.edit(index)


    def excluir_linha(self):
        # Remove a linha selecionada
        index = self.tableView.currentIndex()
        if index.isValid():
            self.model.removeRow(index.row())
            self.model.submitAll() # Salva a exclusão no banco de dados


    def historico_de_registro(self):
        # Esta função ainda não será implementada.
        print("Botão de histórico clicado!")


    def fechar_janela(self):
        self.close()


# Janela principal
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn1.clicked.connect(self.abrir_tabela_cortes)

    def abrir_tabela_cortes(self):
        self.tabela_window = TabelaCortesWindow()
        self.tabela_window.show()


# Janela de Login
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginDialog()
        self.ui.setupUi(self)
        
        # A forma correta de usar o QLineEdit.Password
        self.ui.lineEditPass.setEchoMode(QLineEdit.Password)
        
        self.ui.labelAviso.setText("")
        self.ui.btnLogin.clicked.connect(self.handle_login)
        
    def handle_login(self):
        user = self.ui.lineEditUser.text()
        password = self.ui.lineEditPass.text()

        if user == "admin" and password == "admin":
            self.main = MainWindow()
            self.main.show()
            self.close()
        else:
            self.ui.labelAviso.setText("Login ou senha incorretos!")


# Execução do aplicativo
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())