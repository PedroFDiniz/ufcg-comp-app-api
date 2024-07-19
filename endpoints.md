Aqui está a documentação estilo Swagger em Markdown para os endpoints presentes no arquivo `router.py`:

# API de Autenticação e Atividades

## Endpoints

### Autenticação

#### Autenticar Estudante

`POST /auth/user/student`

Autentica um usuário estudante via Google OAuth.

**Headers:**

- `Authorization` (string, obrigatório): Token de autorização.

**Responses:**

- `200 OK`: Usuário autenticado com sucesso.
- `401 Unauthorized`: Autenticação falhou.

#### Autenticar Revisor e Coordenador

`POST /auth/user/reviewer_and_coordinator`

Autentica um usuário revisor ou coordenador via Google OAuth.

**Headers:**

- `Authorization` (string, obrigatório): Token de autorização.

**Responses:**

- `200 OK`: Usuário autenticado com sucesso.
- `401 Unauthorized`: Autenticação falhou.

### Usuário

#### Registrar Usuário

`POST /user/register`

Registra um novo usuário. Apenas coordenadores podem realizar esta ação.

**Headers:**

- `Authorization` (string, obrigatório): Token de autorização.

**Parameters:**

- `name` (string, obrigatório): Nome do usuário.
- `email` (string, obrigatório): Email do usuário.
- `role` (string, obrigatório): Função do usuário.

**Responses:**

- `200 OK`: Usuário criado com sucesso.
- `401 Unauthorized`: Autenticação falhou.

#### Buscar Usuário por Email

`GET /user/email/{email}`

Retorna as informações de um usuário baseado no email fornecido.

**Parameters:**

- `email` (string, obrigatório): Email do usuário.

**Responses:**

- `200 OK`: Usuário encontrado.
- `404 Not Found`: Usuário não encontrado.

#### Buscar Usuários por Função

`GET /user/role/{role}`

Retorna uma lista de usuários com a função especificada.

**Parameters:**

- `role` (string, obrigatório): Função dos usuários.

**Responses:**

- `200 OK`: Usuários encontrados.
- `404 Not Found`: Usuários não encontrados.

#### Atualizar Matrícula de Usuário

`PUT /user/update/enroll`

Atualiza a matrícula de um usuário. Apenas coordenadores podem realizar esta ação.

**Headers:**

- `Authorization` (string, obrigatório): Token de autorização.

**Parameters:**

- `email` (string, obrigatório): Email do usuário.
- `enroll` (integer, obrigatório): Número de matrícula.

**Responses:**

- `200 OK`: Matrícula atualizada com sucesso.
- `401 Unauthorized`: Autenticação falhou.

### Atividade

#### Registrar Atividade

`POST /activity/register`

Registra uma nova atividade. Apenas estudantes podem realizar esta ação.

**Headers:**

- `Authorization` (string, obrigatório): Token de autorização.

**Parameters:**

- `voucher` (file, obrigatório): Arquivo de comprovante.
- `owner_email` (string, obrigatório): Email do dono da atividade.
- `kind` (string, obrigatório): Tipo da atividade.
- `description` (string, obrigatório): Descrição da atividade.
- `workload` (string, obrigatório): Carga horária.
- `start_date` (string, obrigatório): Data de início.
- `end_date` (string, obrigatório): Data de término.

**Responses:**

- `200 OK`: Atividade registrada com sucesso.
- `401 Unauthorized`: Autenticação falhou.

#### Listar Todas as Atividades

`GET /activities/find_all`

Retorna uma lista de todas as atividades submetidas.

**Parameters:**

- `page` (integer, opcional): Página de resultados.
- `size` (integer, opcional): Tamanho da página.
- `sort` (string, opcional): Campo de ordenação.
- `order` (string, opcional): Ordem de ordenação.

**Responses:**

- `200 OK`: Atividades listadas com sucesso.
- `404 Not Found`: Nenhuma atividade encontrada.

#### Buscar Atividades por Dono ou Estado

`POST /activities/find_by_owner_state`

Retorna uma lista de atividades baseadas no dono ou no estado especificado.

**Parameters:**

- `owner_email` (string, obrigatório): Email do dono das atividades.
- `states` (string, opcional): Estados das atividades.
- `page` (integer, obrigatório): Página de resultados.
- `size` (integer, obrigatório): Tamanho da página.
- `sort` (string, obrigatório): Campo de ordenação.
- `order` (string, obrigatório): Ordem de ordenação.

**Responses:**

- `200 OK`: Atividades encontradas com sucesso.
- `404 Not Found`: Nenhuma atividade encontrada.

#### Atribuir Atividade

`PUT /activity/assign/{activity_id}`

Atribui uma atividade a um revisor. Apenas coordenadores podem realizar esta ação.

**Headers:**

- `Authorization` (string, obrigatório): Token de autorização.

**Parameters:**

- `activity_id` (integer, obrigatório): ID da atividade.
- `reviewer_email` (string, obrigatório): Email do revisor.

**Responses:**

- `200 OK`: Atividade atribuída com sucesso.
- `401 Unauthorized`: Autenticação falhou.

#### Validar Atividade

`PUT /activity/validate/{activity_id}`

Valida uma atividade. Apenas revisores podem realizar esta ação.

**Headers:**

- `Authorization` (string, obrigatório): Token de autorização.

**Parameters:**

- `activity_id` (integer, obrigatório): ID da atividade.
- `reviewer_email` (string, obrigatório): Email do revisor.
- `computed_credits` (string, obrigatório): Créditos computados.
- `justify` (string, obrigatório): Justificativa.
- `state` (string, obrigatório): Estado.

**Responses:**

- `200 OK`: Atividade validada com sucesso.
- `401 Unauthorized`: Autenticação falhou.

#### Contar Atividades por Estado

`POST /activities/count_by_owner_state`

Retorna a contagem de atividades por estado e dono.

**Parameters:**

- `owner_email` (string, obrigatório): Email do dono das atividades.
- `states` (string, opcional): Estados das atividades.

**Responses:**

- `200 OK`: Contagem de atividades retornada com sucesso.
- `404 Not Found`: Nenhuma atividade encontrada.

#### Calcular Créditos de Atividades

`GET /activities/computeCredits/{owner_email}`

Calcula os créditos de atividades para um usuário específico.

**Parameters:**

- `owner_email` (string, obrigatório): Email do dono das atividades.

**Responses:**

- `200 OK`: Créditos calculados com sucesso.
- `404 Not Found`: Nenhuma atividade encontrada.

#### Baixar Comprovante de Atividade

`GET /activity/voucher/download`

Baixa o comprovante de uma atividade.

**Parameters:**

- `path` (string, obrigatório): Caminho do arquivo de comprovante.

**Responses:**

- `200 OK`: Comprovante baixado com sucesso.
- `404 Not Found`: Arquivo não encontrado.

#### Obter Métricas de Atividades

`GET /activities/metrics`

Retorna métricas das atividades.

**Responses:**

- `200 OK`: Métricas retornadas com sucesso.
- `404 Not Found`: Nenhuma métrica encontrada.

### Processo

#### Gerar Processo

`POST /process/generate`

Gera um processo para o usuário. Apenas estudantes podem realizar esta ação.

**Headers:**

- `Authorization` (string, obrigatório): Token de autorização.

**Parameters:**

- `owner_email` (string, obrigatório): Email do dono do processo.

**Responses:**

- `200 OK`: Processo gerado com sucesso.
- `404 Not Found`: Usuário não encontrado.

#### Verificar Processo

`POST /process/check`

Verifica a validade de um processo. Apenas coordenadores podem realizar esta ação.

**Headers:**

- `Authorization` (string, obrigatório): Token de autorização.

**Parameters:**

- `voucher` (file, obrigatório): Arquivo de comprovante.
- `user_enroll` (integer, obrigatório): Matrícula do usuário.

**Responses:**

- `200 OK`: Processo verificado com sucesso.
- `404 Not Found`: Arquivo não encontrado.

### Guias do Usuário

#### Guia de Atividades

`GET /guide/activities`

Retorna o guia de usuário para atividades.

**Responses:**

- `200 OK`: Guia retornado com sucesso.

### CORS

Adiciona cabeçalhos CORS a todas as respostas.

**Headers Adicionados:**

- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Headers: Content-Type,Authorization`
- `Access-Control-Allow-Methods: GET,PUT,POST,DELETE,PATCH`