import os
import logging

from config.config import ConfigGlobal


class Logger:
    """
    Classe de manipulação do arquivo de logs
    """

    print_conn_success = True

    def __init__(self, _name):
        self.class_name = _name
        self.config = ConfigGlobal()

    def log_config(self):

        """
        Configurações de logs
        :return: logger
        """

        path_file = self.config.prop['log.dir'] + self.config.prop['log.name'] + ".log"

        # Caso o diretório de log não exista ele será criado
        if not os.path.exists(self.config.prop['log.dir']):
            os.mkdir(self.config.prop['log.dir'])

        # Caso o arquivo de logs não exista ele será criado junto como cabeçalho do log
        if not os.path.isfile(path_file):

            arq_log = open(path_file, 'w+')

            arq_log.writelines(u'#Aplicativo ExcImportData\n')
            arq_log.writelines(u'#Desenvolvidor: Filipe Fernandes\n')
            arq_log.writelines(u'#Versão: 1.0.0\n\n')

        # Define as configurações do log
        logging.basicConfig(level=self.log_level(self.config.prop['log.level']))

        logger = logging.getLogger(self.class_name)
        logger.setLevel(self.log_level(self.config.prop['log.level']))

        # Cria o manipulador de arquivos
        handler = logging.FileHandler(path_file)
        handler.setLevel(self.log_level(self.config.prop['log.level']))

        # Cria o formato de log
        formatter = logging.Formatter('%(asctime)s |%(process)d| %(name)s %(funcName)s | %(levelname)s: %(message)s')
        handler.setFormatter(formatter)

        # Adiciona o manipulador de arquivos ao logger
        logger.addHandler(handler)

        return logger

    @staticmethod
    def log_level(level_name):
        """
        Verifica qual o nível de lgo deve ser gerado
        :param level_name: recebe o nível de log que deve ser gerado
        :return: levels: retorna o nível do log
        """

        levels = {
            'CRITICAL': 50,
            'ERROR': 40,
            'WARNING': 30,
            'INFO': 20,
            'DEBUG': 10,
            'NOTSET': 0
        }

        # Se o nível de log não for identificado ele assumo o padrão INFO
        return levels.get(level_name, 20)

