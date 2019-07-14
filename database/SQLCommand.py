from database.databaseConnection import DatabaseConnection
from config.logger import Logger


class SQLCommand:
    """
    Classe de execução de scripts no banco de dados
    """

    conn = None

    def __init__(self):
        self.db = DatabaseConnection()
        self.log = Logger(__name__).log_config()

    def exec_query(self, query, params=None, x_return=False):

        """
        Executa as Query's
        :param query: Recebe a query a que será executada
        :param params: (Opcional) recebe os parâmetros da query caso houver
        :param x_return: (Opcional) passar como True se query tiver retorno
        :return: result
        """

        # Abre conexão com banco de dados

        try:

            cur = self.conn.cursor(dictionary=True)

            if x_return is False:

                if self.check_param(params):
                    cur.execute(query)
                    self.log.debug("Command: %s", cur.statement)
                else:
                    cur.execute(query, params)
                    self.log.debug("Command: %s", cur.statement)

                self.conn.commit()

            else:

                if self.check_param(params):
                    cur.execute(query)
                    self.log.debug("Command: %s", cur.statement)
                else:
                    cur.execute(query, params)
                    self.log.debug("Command: %s", cur.statement)

                result = cur.fetchall()

                # Se o resultado do select for > 1 retorna uma lista de objeto, se não retorna apenas o objeto

                if cur.rowcount > 1:
                    return result
                else:
                    return result[0]

            cur.close()

        except Exception as err:
            self.log.exception(err)

    def open(self):
        """
        Abre a conexão com banco de dados
        :return: void
        """
        self.conn = self.db.conn_open()

    def close(self):
        """
        Fecha a conexão com banco de dados
        :return:
        """
        self.conn.close()

    @staticmethod
    def check_param(params):
        """
        :param params: Verifica se algum parâmetro foi informado para ser repassado na execução da query
        :return: True or False
        """
        if params is None:
            return True
        else:
            return False
