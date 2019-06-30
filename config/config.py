import os

from datetime import datetime
from properties.p import Property


# noinspection PyTypeChecker
class ConfigGlobal:
    """
    Class para definição de configurações globais e do arquivo .properties
    """

    data_base_config = ""
    prop_config = ""
    prop = ""
    new_file = {"geraLog": True}

    def __init__(self):

        self.prop_config = Property()
        self.prop = self.prop_config.load_property_files('./config.properties')

    def db_config(self):
        """
        Gera um objeto com as configurações do banco de dados informada a partir do arquivo .properties
        :return: db_json_config
        """
        db_json_config = {
            'user': self.prop['db.user'],
            'password': self.prop['db.password'],
            'host': self.prop['db.host'],
            'database': self.prop['db.database'],
            'raise_on_warnings': True
        }

        return db_json_config

    def file_path(self, prop_name, _dir):
        """
        Retorna o arquivo com a estrutura da tabela
        :param prop_name: Nome do arquivo que deverá ser processado
        :param _dir: Diretório do arquivo que deverá ser localizado
        :return: path
        """
        path = self.prop[_dir]
        file_name = None

        for file in os.listdir(path):

            file = str(file).split(".")

            if file[0] == self.prop[prop_name] and file[1] == 'json':
                file_name = file[0] + "." + file[1]

        if file_name is not None:
            path = path + file_name
        else:
            self.log.info("O arquivo informado na propriedade: {0}, não localizado no diretório: {1}"
                          .format(prop_name, path))

        return path

    def file_data(self):
        """
        Retorna o arquivo em excel com os dados que serão processados
        :return: file
        """
        file = self.prop['excel.dir'] + self.prop['excel.name']
        return file

    def rename_file_processed(self):
        """
        Renomeia os arquivos processados
        :return: void:
        """
        path = self.prop['excel.dir'] + self.prop['excel.name']

        if os.path.isfile(path):

            date = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')

            for file in os.listdir(self.prop['excel.dir']):

                if file == self.prop['excel.name']:
                    file = str(file).split(".")
                    new_name = date + "_" + file[0] + "." + file[1]

                    os.rename(self.prop['excel.dir'] + self.prop['excel.name'], self.prop['excel.dir'] + new_name)

                    self.new_file['oldFile'] = file[0]
                    self.new_file['newFile'] = str(new_name).split(".")[0]

        else:
            self.new_file['gerLog'] = False
