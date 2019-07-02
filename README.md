# ExcImportData

O ExcImportData é um script processador de arquivos Excel em fase de desenvolvimento, ele tem por objetivo processar tabelas Excel e importar as suas informações para a base de dados. A sua utilização é bem simple, ele não possui uma interface gráfica, as configurações são realizadas no arquivo .properties.

Atualmente a conexão de banco de dados é apenas com o MySQL, em breve será permitido importar dados para o PostgreSQL

#### Configurações básicas para utilização
1. Informe a conexão do banco de dados:
```properties
db.user=
db.password=
db.host=
db.database=
```
2. Configure a estrutura da tabela que irá receber os dados em um arquivo **.json** conforme exemplo, deverá ser configurado também o 
tipo de operação **typeOp**, pois em breve será permitido executar comandos de **update**.

```json
table.json
{
  "table": "contact",
  "typeOp": "insert",
  "fields": ["name", "phone", "email", "address"]
}
```
```properties
table.name=ExempleTableJSON
table.dir=C:/tmp/table/
```
3. Informe o arquivo que possui os dados para serem importados:
```properties
excel.name=dados.xlsx
excel.dir=C:/tmp/
```
4. Informe as configurações de execução
```properties
# Define se o processador ExcImportData irá executar só uma vez e parar ou entrar em 
# execução constante, valor'S ou N'
exec.loop=S
# Define de quanto em quanto tempo ele deve verificar se há um novo arquivo para ser processado, 
# valor (minutos) default 60 minutos
exec.time.sync=10
```
5. Configure a geração de logs
```properties
# Configurações de logs nível "CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
log.level=INFO
log.name=ExcImportData
log.dir=C:/tmp/log/
```
