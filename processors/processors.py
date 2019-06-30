import os
import json
import xlrd

from unicodedata import normalize
from datetime import datetime

from config.config import ConfigGlobal
from database.SQLCommand import SQLCommand
from config.logger import Logger


class Processors:
    """
    Class de processamentos dos conjuntos de informações .properties e arquivo excel para carregar as informações no
    banco de dados informado
    """

    params_plan = None  # Recebe o cabeçalho da planilha para passar como parâmetros nas query's
    sql_command = None  # Recebe o comando SQL que será executado no banco de dados

    def __init__(self, xQuery=SQLCommand()):

        self.config = ConfigGlobal()
        self.log = Logger(__name__).log_config()
        self.xQuery = xQuery

    def monta_query(self):
        """
        Gera a query SQL para executar as operações no banco de dados
        :return: void
        """

        path = self.config.file_path("table.name", "table.dir")
        table = json.loads(open(path).read())

        params = []

        if self.params_plan is not None:

            for field in self.params_plan:
                field = "%(" + field + ")s"
                params.append(field)

        if Processors.command_type(table['typeOp']) == 30:

            """
                {0} - typeOp
                {1} - table
                {2} - fields
                {3} - params
            """
            self.sql_command = "{0} into {1} ({2}) values ({3})" \
                .format(table['typeOp'], table['table'], ", ".join(table['fields']), ", ".join(params))

        else:
            self.log.info("Tipo de comando SQL não identificado!!!")

    @staticmethod
    def command_type(_type):
        """
        Retorna o tipo de comando que deverá ser executado no banco de dados
        :param _type:
        :return:
        """

        types = {

            'INSERT': 30,
            'UPDATE': 20,
            'SELECT': 10,
            'DELETE': 0

        }

        _type = types.get(_type.upper())

        return _type

    def ready_file_excel(self):
        """
        Processa o arquivo Excel e a partir dele gera uma lista de dados para ser gravar no banco de dados
        :return:
        """
        path = self.config.file_data()
        row_value = []  # Recebe os valores de cada col/row
        data_list = []  # Monta uma lista de dados com as informações lidas da planilha

        if os.path.isfile(path):

            file_sheet = xlrd.open_workbook(path)
            plan = file_sheet.sheets()[0]

            count = 0

            # Percorre cada linha da planilha
            for rownum in range(0, plan.nrows):

                # Pega a primeira linha para gerar o cabeçalho
                if rownum == 0:

                    col_name = plan.row_values(rownum)
                    self.cab_plan(col_name)

                else:

                    row = plan.row_values(rownum)

                    '''
                    Este trecho do código valida o tipo de dado armazenado em cada coluna, para então verifica os 
                    que são 'date' pois estes na leitura do arquivo são gerados como float e deve ser convertidos 
                    novamente para o formato data
                    '''
                    for col in range(len(plan.row_values(rownum))):

                        cell = plan.cell(rownum, col)
                        value = cell.value

                        if cell.ctype == 3:

                            valid_date = str(value).split(".")
                            value = datetime(*xlrd.xldate_as_tuple(value, file_sheet.datemode))

                            # Valida se a casa decimal da data é maior que zero, caso seja retorna a data + hora
                            if int(valid_date[1]) > 0:
                                row[col] = value.strftime('%Y-%m-%d %H:%M:%S')
                            else:
                                row[col] = value.strftime('%Y-%m-%d')

                    row_value.append(row)
                    count += 1

            col_name = self.params_plan

            # Laços de repetição para montar o dicionário de dados que será passado como parâmetro no insert
            for x_row in range(len(row_value)):

                # Irá receber um dicionário de dados contendo o nome da coluna e o seu valor
                row_dic = {}

                for y_col in range(len(col_name)):
                    col_name[y_col] = str(col_name[y_col]).replace(" ", "_").strip(" ")
                    row_dic[col_name[y_col]] = row_value[x_row][y_col]

                data_list.append(row_dic)

            return data_list

        else:
            self.log.error("O arquivo '{0}' não foi encontrado".format(path))

    def cab_plan(self, list_cab):
        """
        Recebe o cabeçalho da planilha e retorna ele removendo os caracteres utf-8 para gerar as os parâmetros das
        query's
        :param list_cab:
        """
        new_cab = []

        for col in list_cab:
            col = str(col).replace(" ", "_").strip(" ")
            col = normalize('NFKD', col).encode('ASCII', 'ignore').decode('ASCII')
            new_cab.append(col)

        self.params_plan = new_cab

    def processes_data(self):
        """
        Processa a lista de dados geradas a partir do arquivo excel e insere na tabela informado no arquivo .json que
        deve ser criado contendo a estrutura da tabela
        :return: void:
        """

        data = self.ready_file_excel()
        count = 0

        try:

            self.log.info("Processamento de dados iniciado...")
            self.xQuery.open()
            self.monta_query()

            if data is not None:

                for sql_param in data:

                    self.xQuery.exec_query(self.sql_command, sql_param)
                    count += 1

                self.config.rename_file_processed()
                self.log.info("Arquivo renomeando arquivo de '{0}' para '{1}'".format(self.config.new_file['oldFile'],
                                                                                      self.config.new_file['newFile']))
            else:

                self.log.info("A lista de dados para importação não foi gerada, isso pode ocorrer se o arquivo que "
                              "contém os dados não for encontrado no diretório informado...")

            self.xQuery.close()
            self.log.info("Processamento de dados finalizado...")
            self.log.info("Total de registros processados: {}".format(count))

        except Exception as err:
            self.log.error("Ocorreu um erro ao iniciar o processamento de dados...")
            self.log.exception(err)
