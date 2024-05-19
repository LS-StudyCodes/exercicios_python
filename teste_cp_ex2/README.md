## Sistema de Estacionamento - Django e Vue.js

Este projeto implementa um sistema de estacionamento com backend em Django e frontend em Vue.js. O sistema permite cadastrar clientes, veículos, planos de mensalistas, contratos para clientes rotativos e gerenciar movimentos de entrada e saída de veículos no estacionamento.

### Estrutura do Projeto

O projeto está organizado da seguinte forma:

- **backend:** Pasta principal do projeto Django.
    - **backend/core/settings.py:** Configurações do projeto Django.
    - **backend/core/urls.py:** Rotas da API.
    - **backend/core/wsgi.py:** Arquivo de configuração do servidor WSGI.
- **backend/parking_system:** Aplicação Django que contém a lógica do sistema de estacionamento.
    - **backend/parking_system/models.py:** Modelos de dados do sistema.
    - **backend/parking_system/serializers.py:** Serializadores para converter modelos de dados em JSON.
    - **backend/parking_system/views.py:** Views REST que definem as APIs.
    - **backend/parking_system/admin.py:** Registra os modelos para a interface administrativa.
- **frontend:** Pasta do projeto Vue.js.
    - **frontend/src/main.js:** Arquivo principal da aplicação Vue.js.
    - **frontend/src/router.js:** Define as rotas da aplicação.
    - **frontend/src/App.vue:** Componente principal da aplicação Vue.js.
    - **frontend/src/components/:** Pasta que contém os componentes de cada página.
        - **Operation.vue:** Página principal de operação do sistema de estacionamento.
        - **Vehicle.vue:** Página para cadastrar e editar veículos.
        - **Customer.vue:** Página para cadastrar e editar clientes.
        - **Plan.vue:** Página para cadastrar e editar planos de mensalistas.
        - **Contract.vue:** Página para cadastrar e editar contratos para clientes rotativos.
        - **ExitConfirmation.vue:** Componente de popup para exibir informações do veículo ao registrar a saída.
    - **frontend/package.json:** Arquivo de configuração do projeto Vue.js.
    - **frontend/requirements.txt:** Lista de dependências Python para o backend.

### Documentação do Código

#### Backend (Django)

##### 1. Modelos (models.py)

- **Customer:**
    - Modelo para representar clientes, com nome e ID do cartão.

    | Campos | Detalhes |
    | --- | --- |
    | name | Nome do cliente |
    | card_id | ID do cartão do cliente, único e opcional |
- **Vehicle:**
    - Modelo para representar veículos, com placa, modelo, descrição e um relacionamento com um cliente.

    | Campos | Detalhes |
    | --- | --- |
    | plate | Placa do veículo, única. |
    | model | Modelo do veículo, opcional |
    | description | Descrição do veículo, opcional |
    | customer | Cliente associado ao veículo, opcional |
- **Plan:**
    - Modelo para representar planos de mensalistas, com descrição e valor.

    | Campos | Detalhes |
    | --- | --- |
    | description | Descrição do plano |
    | value | Valor do plano |
- **CustomerPlan:**
    - Modelo para representar a relação entre um cliente e um plano, com data de vencimento.

    | Campos | Detalhes |
    | --- | --- |
    | customer | Cliente associado ao plano |
    | plan | Plano de estacionamento associado ao cliente |
    | due_date | Data de vencimento do plano, opcional |
- **Contract:**
    - Modelo para representar contratos para clientes rotativos, com descrição e valor máximo.

    | Campos | Detalhes |
    | --- | --- |
    | description | Descrição do contrato |
    | max_value | Valor máximo cobrado pelo contrato, opcional |
- **ContractRule:**
    - Modelo para representar regras de cálculo para contratos, com tempo limite e valor.

    | Campos | Detalhes |
    | --- | --- |
    | contract | Contrato ao qual a regra pertence |
    | until | Tempo limite em minutos para aplicação da regra |
    | value | Valor cobrado pela regra |
- **ParkMovement:**
    - Modelo para representar movimentos de entrada e saída de veículos no estacionamento, com data de entrada, data de saída, veículo e valor.

    | Campos | Detalhes |
    | --- | --- |
    | entry_date | Data e hora de entrada do veículo, preenchida automaticamente |
    | exit_date | Data e hora de saída do veículo, opcional |
    | vehicle | Veículo associado a movimentação |
    | value | Valor cobrado pela estadia, opcional |

##### 2. Serializadores (serializers.py)

Cada modelo possui um serializer correspondente, responsável por serializar os dados em formato JSON para as respostas da API:

- **CustomerSerializer:**
    - Serializa um objeto Customer.
- **VehicleSerializer:**
    - Serializa um objeto Vehicle, incluindo o cliente associado.
    - Define o campo customer como read_only e usa o CustomerSerializer para serializar o cliente associado ao veículo.
- **PlanSerializer:**
    - Serializa um objeto Plan.
- **CustomerPlanSerializer:**
    - Serializa um objeto CustomerPlan.
- **ContractSerializer:**
    - Serializa um objeto Contract,.
    - Adiciona um campo rules usando SerializerMethodField para representar as regras do contrato.
    - Implementa os métodos create e update para lidar com a criação e atualização de contratos e suas regras.
    - O método get_rules busca as regras associadas ao contrato e as serializa usando o ContractRuleSerializer.
- **ContractRuleSerializer:**
    - Serializa um objeto ContractRule.
- **ParkMovementSerializer:**
    - Serializa um objeto ParkMovement, incluindo informações sobre o veículo e o cliente associados.
    - Define os campos plate e card_id como read_only e utiliza dados aninhados do modelo Vehicle e Customer para preenchê-los.

##### 3. Views (views.py)

- **CustomerViewSet:**
    - Viewset para gerenciar os clientes.
- **VehicleViewSet:**
    - Viewset para gerenciar os veículos.
    - Possui lógica adicional no método create para:
        - Verificar se já existe um veículo com a placa informada.
        - Se existir e não tiver um cliente associado, retorna o veículo existente.
        - Se existir e já tiver um cliente, retorna um erro informando que o veículo já está registrado.
        - Caso contrário, cria um novo veículo.
- **PlanViewSet:**
    - Viewset para gerenciar os planos.
- **CustomerPlanViewSet:**
    - Viewset para gerenciar a relação entre clientes e planos.
- **ContractViewSet:**
    - Viewset para gerenciar os contratos.
    - Implementa métodos adicionais para lidar com as regras de contrato:
        - create: Cria um novo contrato e suas regras associadas.
        - update: Atualiza um contrato existente e suas regras.
        - get_rules: Retorna as regras associadas a um contrato.
- **ContractRuleViewSet:**
    - Viewset para gerenciar as regras de contratos.
- **ParkMovementViewSet:**
    - Viewset para gerenciar os movimentos de estacionamento.
    - Possui métodos adicionais para lidar com a entrada e saída de veículos:
        - create:
            - Valida se a placa ou o ID do cartão foram informados.
            - Verifica se o ID do cartão é válido, caso seja fornecido.
            - Busca um veículo existente pela placa ou pelo cliente associado ao cartão.
            - Cria um novo veículo se não encontrar um existente pela placa.
            - Verifica se o veículo já está estacionado.
            - Cria um novo movimento de estacionamento, registrando a entrada do veículo.
        - update:
            - Verifica se o veículo já saiu do estacionamento.
            - Define a data e hora de saída.
            - Calcula o valor da estadia:
                - Se o veículo não estiver associado a um cliente, utiliza o primeiro contrato encontrado e aplica suas regras de cobrança com base no tempo de permanência.
                - Se o veículo estiver associado a um cliente, utiliza o plano do cliente para calcular o valor.
            - Salva o movimento de estacionamento atualizado.

##### 4. URLs (urls.py)

- Define as URLs para acessar as views, expondo a API REST.

##### 5. Configurações (settings.py)

- Configurações gerais do projeto Django.

#### Frontend (Vue.js)

##### 1. Componente Principal (App.vue)

- Componente principal da aplicação.
- Renderiza a barra de navegação e o componente de visualização de rotas (<router-view>).
- Define a estrutura básica da interface, incluindo o cabeçalho com links para as diferentes seções do sistema.

##### 2. Rotas (router/index.js)

- Define as rotas para cada página da aplicação Vue.js. Cada rota é mapeada para um componente específico.
    - /: Rota principal, renderiza o componente Operation.
    - /vehicles: Renderiza o componente Vehicle.
    - /customers: Renderiza o componente Customer.
    - /plans: Renderiza o componente Plan.
    - /contracts: Renderiza o componente Contract.

##### 3. Componentes de Páginas

- **Operation.vue:**
    - Exibe a página principal de operação do sistema de estacionamento.
    - Possui campos para registrar a entrada de veículos, com placa e ID do cartão (opcional).
    - Exibe uma tabela com os veículos que estão no pátio, ordenados pela data de entrada mais recente.
    - Inclui um botão para registrar a saída de veículos.
    - Utiliza o componente ExitConfirmation para exibir as informações do veículo que está saindo.
    - Realiza chamadas de API para o backend:
        - POST /api/v1/park-movements/: registrar entrada de veículos.
        - PATCH /api/v1/park-movements/{id}/: registrar saída de veículos.
        - GET /api/v1/park-movements/: buscar a lista de veículos estacionados.
- **Vehicle.vue:**
    - Exibe a página para cadastrar e editar veículos.
    - Possui campos para placa, modelo, descrição e cliente.
    - Exibe uma tabela com a lista de veículos.
    - Realiza chamadas de API para o backend:
        - POST /api/v1/vehicles/: cadastrar novos veículos.
        - PUT /api/v1/vehicles/{id}/: editar veículos existentes.
        - DELETE /api/v1/vehicles/{id}/: excluir veículos.
        - GET /api/v1/vehicles/: buscar a lista de veículos cadastrados.
- **Customer.vue:**
    - Exibe a página para cadastrar e editar clientes.
    - Possui campos para nome e ID do cartão (opcional).
    - Exibe uma tabela com a lista de clientes.
    - Realiza chamadas de API para o backend:
        - POST /api/v1/customers/: cadastrar novos clientes.
        - PUT /api/v1/customers/{id}/: editar clientes existentes.
        - DELETE /api/v1/customers/{id}/: excluir clientes.
        - GET /api/v1/customers/: buscar a lista de clientes cadastrados.
- **Plan.vue:**
    - Exibe a página para cadastrar e editar planos de mensalistas.
    - Possui campos para descrição e valor.
    - Exibe uma tabela com a lista de planos.
    - Realiza chamadas de API para o backend:
        - POST /api/v1/plans/: criar novos planos.
        - PUT /api/v1/plans/{id}/: editar planos existentes.
        - DELETE /api/v1/plans/{id}/: excluir planos.
        - GET /api/v1/plans/: buscar a lista de planos disponíveis.
- **Contract.vue:**
    - Exibe a página para cadastrar e editar contratos para clientes rotativos.
    - Possui campos para descrição, valor máximo e regras.
    - Permite adicionar, editar e remover regras para o contrato.
    - Realiza chamadas de API para o backend:
        - POST /api/v1/contracts/: criar novos contratos.
        - PUT /api/v1/contracts/{id}/: editar contratos existentes.
        - DELETE /api/v1/contracts/{id}/: excluir contratos.
        - GET /api/v1/contracts/: buscar a lista de contratos existentes.

##### 4. ExitConfirmation.vue (Componente de PopUp)

- Exibe um popup com as informações do veículo que está saindo, como placa, ID do cartão, data de entrada, data de saída e valor a ser cobrado.
- Possui um botão "OK" para fechar o popUp.

##### 5. Configurações do Frontend (main.js)

- Cria a instância do Vue.js e configura a aplicação, incluindo Vue Router e a biblioteca Axios para realizar requisições HTTP.

##### 6. Estilos (CSS)

- Define os estilos da aplicação Vue.js, usando Bootstrap para estilização.

### Passo a Passo para Executar o Projeto

#### Pré-requisitos

- Python 3.7+
- Node.js e npm
- Git

#### Instalação

1. **Abrir o terminal na pasta raiz do projeto**
2. **Clonar o Repositório:**

    `git clone <url do repositório>`
    
3. **Criar um Ambiente Virtual:**

    `python -m venv .venv`
    
4. **Ativar o Ambiente Virtual:**

     `.venv\Scripts\activate`
    
5. **Navegar até a pasta do backend**

    `cd .\backend\`
    
6. **Instalar as Dependências:**

    `pip install -r requirements.txt`
    
7. **Migrar o Banco de Dados:**

    `python manage.py makemigrations
    python manage.py migrate`
    
8. **Criar um Superusuário:**

    `python manage.py createsuperuser`
    
9. **Iniciar o Servidor de Desenvolvimento:**

    `python manage.py runserver`
    

#### Frontend

1. **Abrir o terminal na pasta raiz do projeto**
2. **Ativar o Ambiente Virtual:**

     `.venv\Scripts\activate`
    
3. **Navegar até a pasta do frontend**

    `cd .\frontend\`
    
4. **Instalar as dependências:** Execute o comando
    - `npm install`
5. **Iniciar a aplicação:** Execute o comando npm run serve.
    - `npm run serve`

#### Acesso à Aplicação

- Acesse a aplicação no navegador no endereço apresentado no terminal.

### Documentação do Processo de Desenvolvimento

#### Backend (Django)

1. **Criar um projeto Django:**

    `django-admin startproject core`
    
2. **Criar uma aplicação Django:**

    `python manage.py startapp parking_system`
    
3. **Criar modelos:**
    - Criar modelos de dados em parking_system/models.py.
4. **Criar serializadores:**
    - Criar serializadores para converter modelos de dados em JSON em parking_system/serializers.py.
5. **Criar views:**
    - Criar views para as operações CRUD em parking_system/views.py.
6. **Definir URLs:**
    - Definir as URLs para acessar as views em core/urls.py.
7. **Migrar o banco de dados:**

    `python manage.py makemigrations
    python manage.py migrate`
    
8. **Criar um superusuário:**

    `python manage.py createsuperuser`
    
9. **Iniciar o servidor de desenvolvimento:**

    `python manage.py runserver`
    

#### Frontend (Vue.js)

1. **Criar projeto Vue.js:**
    - Criar um projeto Vue.js usando Vue CLI (opcional).
    - Criar componentes Vue.js para cada página.
2. **Configurar as rotas:**
    - Definir as rotas em frontend/router/index.js.
3. **Configurar o Axios:**
    - Instalar o Axios e configurar a comunicação com o backend.
4. **Testar e depurar a aplicação:**
    - Executar testes e solucionar erros no backend e frontend.
5. **Criar documentação:**
    - Documentar o código e as funcionalidades do projeto.
