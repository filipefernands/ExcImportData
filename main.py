"""
    O ExcImportData é um script processador de arquivos Excel em fase de desenvolvimento, ele tem por objetivo processar
    tabelas Excel e importar as suas informações para a base de dados. A sua utilização é bem simple, ele não possui uma
    interface gráfica, as configurações são realizadas no arquivo .properties

    ### INSTRUÇÕES DE USO ###
    1º - Configure o arquivo .properties conforme as instruções contidas nele;
    2º - Defina a estrutura da tabela que receberá os dados em um arquivo .json, conforme exemplo:
     {
        "table": "pessoa",
        "typeOp": "insert",
        "fields": []
     }
    3º - Execute o aplicativo;
"""
__author__ = "FILIPE FERNANDES"
__date__ = "2019-06-19"
__license__ = "GNU General Public License"
__version__ = "1.0.0"
__email__ = "filipe.fsrocha@gmail.com"
__status__ = "Prototype"


import time

from processors.processors import Processors
from config.logger import Logger
from config.config import ConfigGlobal


def main():

    log = Logger(__name__).log_config()
    log.info("Iniciando aplicativo ExcImportData")

    config = ConfigGlobal()

    _exec = Processors()

    while True:

        _exec.processes_data()

        wait = 60 * int(config.prop['exec.time.sync'])

        if config.prop['exec.loop'] == 'N':
            break

        time.sleep(wait)
        print('Fim: %s' % time.ctime())


if __name__ == "__main__":
    main()
