## Gerenciador de Configurações JSON

Este script Python permite que você leia e salve configurações em um arquivo JSON chamado `config.json`.

### Funcionalidades

* **`read_configurations()`**: Lê o arquivo `config.json` e imprime as configurações no console. Trata exceções caso o arquivo não exista ou seja inválido.
* **`save_configurations()`**: Solicita ao usuário que insira o nome do servidor, IP e senha. Salva essas informações em um dicionário. Escreve o dicionário no arquivo `config.json` em formato JSON. Trata exceções caso ocorra algum erro durante a escrita no arquivo.
* **`main()`**: Exibe um menu com as opções disponíveis:
    * **1 - Ler configuração**: Chama a função `read_configurations()`.
    * **2 - Salvar configuração**: Chama a função `save_configurations()`.
    * **3 - Sair**: Encerra o script.
    Permite ao usuário escolher uma opção e executa a ação correspondente. Valida a entrada do usuário e exibe mensagens de erro caso a opção seja inválida.

### Uso

1. Crie um arquivo chamado `config.json` no mesmo diretório do script `main.py`.
2. Execute o script `main.py`.
3. Escolha a opção desejada no menu:
    * **Ler configuração**: Exibe as configurações salvas no arquivo `config.json`.
    * **Salvar configuração**: Solicita ao usuário que insira as informações do servidor e salva-as no arquivo `config.json`.
    * **Sair**: Encerra o script.

### Observações

* O arquivo `config.json` é criado caso não exista.
* O script verifica se o arquivo `config.json` é válido e exibe mensagens de erro caso seja inválido.
* O usuário pode editar as configurações diretamente no arquivo `config.json`.
