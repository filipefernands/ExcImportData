import mysql.connector

from mysql.connector import errorcode
from config.config import ConfigGlobal
from config.logger import Logger


class DatabaseConnection:
    """
    Class de conexão com o banco de dados
    """

    conn = None
    info_conn = True

    def __init__(self, config=ConfigGlobal(), log=Logger(__name__).log_config()):
        self.log = log
        self.db_config = config.db_config()

    def conn_open(self):
        """
        Abre a conexão como banco de dados
        :return: conn
        """

        try:

            self.conn = mysql.connector.connect(**self.db_config)

            if self.conn and self.info_conn:

                self.info_conn = False
                self.log.info("Iniciando conexão com o banco de dados")
                self.log.debug("User: %s - Host: %s - Database: %s", self.db_config['user'], self.db_config['host'],
                               self.db_config['database'])
                self.log.info("Conexão estabelecida com sucesso!")

            return self.conn

        except mysql.connector.Error as err:

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.log.error("Erro de conexão com o banco de dados, usuário e/ou senha incorretos.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                self.log.error("O banco de dados informado no arquivo .properties não foi encontrado.")
            else:
                self.log.exception(err.msg)
