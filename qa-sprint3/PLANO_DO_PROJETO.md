# Plano do Projeto — Ford Challenge 2026 · Desafio 01: Inteligência Competitiva Automotiva

**Disciplina:** Testing, Compliance and Quality Assurance — Sprint 3  
**Ferramenta:** Azure DevOps (processo Scrum)  
**Projeto no Azure:** `Ford Challenge`

## 1. Visão do produto

Ferramenta que recebe **Marca, Modelo, Versão** e uma **lista livre de atributos técnicos** e devolve uma **lista padronizada de especificações** (sempre no mesmo formato, com campos comparáveis e 'Não disponível' explícito quando o dado não existir). A validação oficial é feita com a **Ford Ranger Raptor**.

**Arquitetura (resumo, alinhada ao modelo ArchiMate):** App Mobile (React Native/Expo) → API REST (JWT, perfis) → Serviço de Coleta (fontes oficiais e secundárias, cache) → Motor de Extração IA (LLM + regras + normalizador) → Banco de Dados (catálogo de atributos, pesquisas, especificações, fontes). Pipeline DevSecOps e observabilidade transversais.

**Personas:** Analista de Inteligência Competitiva · Gestor de Produto · Administrador.

## 2. Critérios de priorização e estimativa

| Prioridade | Significado | Business Value |
|---|---|---|
| **Must** | Obrigatório (Must have) — requisito do desafio Ford, sem ele a solução não é aceita | 100 |
| **Should** | Necessário (Should have) — agrega valor relevante ao negócio, mas não bloqueia a aceitação | 50 |
| **Could** | Opcional (Could have) — melhoria desejável, entra se houver capacidade | 20 |

**Esforço:** Planning Poker com sequência de Fibonacci (1, 2, 3, 5, 8, 13). Referência: 3 pontos = endpoint CRUD simples com testes.

**Definition of Ready (DoR):** história no formato *Como/Quero/Para*, critérios BDD escritos, dependências identificadas, estimada pelo time.  
**Definition of Done (DoD) padrão:** Código revisado via Pull Request; testes automatizados passando no pipeline; sem vulnerabilidades críticas/altas no SAST/SCA; critérios de aceite BDD validados pelo PO; documentação (Swagger/README) atualizada; deploy no ambiente de homologação.

## 3. Backlog do produto (Épicos → Features → PBIs)

### EP-01 — Fundação da Plataforma e Catálogo de Atributos

Estabelecer a arquitetura (camadas: App Mobile, API Gateway/Backend, Serviço de Coleta, Motor de Extração IA, Banco de Dados), o ambiente de desenvolvimento, o pipeline CI e o catálogo padrão de atributos técnicos que garante que toda saída tenha o mesmo formato.  
**Critério de aceite do épico:** Arquitetura documentada (diagrama de componentes alinhado ao modelo ArchiMate da sprint anterior); pipeline CI executando em todo PR; catálogo com ao menos 40 atributos técnicos padronizados com unidade e categoria.

#### FT-01 — Arquitetura e Ambiente de Desenvolvimento

*Como equipe de desenvolvimento, quero uma arquitetura definida e um ambiente com CI, para construir a solução de forma organizada e segura.*  
**Critério de aceite:** Dado o repositório do projeto, quando um PR é aberto, então o pipeline compila, executa testes e reporta o resultado.

**PBI-01 — Definir arquitetura da solução e diagrama de componentes**  
Como equipe, quero a arquitetura documentada com componentes e responsabilidades, para orientar o desenvolvimento.  
Prioridade: **Must** · Esforço: **3 pts** · Depende de: — · Release: **Sprint 1**

```gherkin
Funcionalidade: Definir arquitetura da solução e diagrama de componentes

  Cenário: Diagrama publicado
    Dado que a arquitetura foi modelada no ArchiMate
    Quando a equipe consulta a Wiki do projeto
    Então encontra o diagrama com App Mobile, API, Serviço de Coleta, Motor IA e Banco de Dados e o fluxo de autenticação
```
Pronto quando: DoD padrão + Diagrama e descrição de responsabilidades publicados na Wiki do Azure DevOps.

**PBI-02 — Configurar repositório, estratégia de branches e pipeline CI**  
Como desenvolvedor, quero um pipeline que valide cada Pull Request, para evitar que código quebrado chegue à main.  
Prioridade: **Must** · Esforço: **5 pts** · Depende de: PBI-01 · Release: **Sprint 1**

```gherkin
Funcionalidade: Configurar repositório, estratégia de branches e pipeline CI

  Cenário: PR válido
    Dado um Pull Request com código compilável e testes passando
    Quando o pipeline é executado
    Então o PR fica apto para merge

  Cenário: PR com falha
    Dado um Pull Request com teste falhando
    Quando o pipeline é executado
    Então o merge é bloqueado pela branch policy
```
Pronto quando: DoD padrão + Branch policy ativa na main exigindo build verde e 1 revisor.

**PBI-03 — Modelar banco de dados (veículos, atributos, pesquisas, especificações, fontes)**  
Como desenvolvedor, quero um modelo de dados normalizado, para armazenar pesquisas e especificações de forma consistente.  
Prioridade: **Must** · Esforço: **5 pts** · Depende de: PBI-01 · Release: **Sprint 1**

```gherkin
Funcionalidade: Modelar banco de dados (veículos, atributos, pesquisas, especificações, fontes)

  Cenário: Migração aplicada
    Dado o script de migração do banco
    Quando é executado em um ambiente limpo
    Então as tabelas Veiculo, Atributo, Pesquisa, Especificacao e Fonte são criadas com suas chaves e relacionamentos
```
Pronto quando: DoD padrão + Diagrama ER publicado e migrações versionadas no repositório.

#### FT-02 — Catálogo Padrão de Atributos Técnicos

*Como analista de inteligência competitiva, quero um catálogo padrão de atributos técnicos, para que todas as pesquisas sejam comparáveis entre si.*  
**Critério de aceite:** Dado o catálogo, quando consulto um atributo, então vejo nome padrão, categoria, unidade e sinônimos.

**PBI-04 — Cadastrar catálogo padrão de atributos técnicos com unidade e categoria**  
Como analista, quero um catálogo com atributos padrão (motor, potência, torque, transmissão, tração, dimensões, capacidades, segurança, conforto), para padronizar a saída.  
Prioridade: **Must** · Esforço: **5 pts** · Depende de: PBI-03 · Release: **Sprint 1**

```gherkin
Funcionalidade: Cadastrar catálogo padrão de atributos técnicos com unidade e categoria

  Cenário: Consulta ao catálogo
    Dado que o catálogo foi carregado
    Quando consulto GET /atributos
    Então recebo ao menos 40 atributos, cada um com nome padrão, categoria e unidade

  Cenário: Atributo duplicado
    Dado que o atributo 'Potência máxima' já existe
    Quando um administrador tenta cadastrá-lo novamente
    Então recebo 409 Conflict
```
Pronto quando: DoD padrão + Seed do catálogo versionado e coberto por teste.

**PBI-05 — Mapear sinônimos de atributos (ex.: 'cv', 'potência', 'hp')**  
Como analista, quero que termos diferentes para o mesmo atributo sejam reconhecidos, para não perder dados por variação de nomenclatura.  
Prioridade: **Should** · Esforço: **3 pts** · Depende de: PBI-04 · Release: **Sprint 1**

```gherkin
Funcionalidade: Mapear sinônimos de atributos (ex.: 'cv', 'potência', 'hp')

  Cenário: Sinônimo reconhecido
    Dado que 'hp' é sinônimo de 'Potência máxima'
    Quando informo o atributo 'hp' na pesquisa
    Então o resultado apresenta o campo padrão 'Potência máxima'
```
Pronto quando: DoD padrão + Tabela de sinônimos com ao menos 3 variações para os 20 atributos mais usados.

### EP-02 — Segurança e Gestão de Acesso

Garantir que apenas usuários autenticados e autorizados utilizem a ferramenta, com perfis distintos, API protegida e segurança integrada ao pipeline (DevSecOps).  
**Critério de aceite do épico:** Autenticação JWT com expiração; perfis Analista, Gestor e Administrador; endpoints públicos e protegidos; pipeline com SAST, SCA e secret scanning.

#### FT-03 — Autenticação e Perfis de Acesso

*Como administrador, quero controlar quem acessa a ferramenta e com qual perfil, para proteger dados estratégicos da Ford.*  
**Critério de aceite:** Dado um usuário sem token, quando acessa um recurso protegido, então recebe 401; dado um perfil sem permissão, então recebe 403.

**PBI-11 — Cadastro e login com geração e validação de JWT**  
Como usuário, quero me autenticar com e-mail e senha, para acessar a ferramenta de forma segura.  
Prioridade: **Must** · Esforço: **8 pts** · Depende de: PBI-02, PBI-03 · Release: **Sprint 2**

```gherkin
Funcionalidade: Cadastro e login com geração e validação de JWT

  Cenário: Login válido
    Dado um usuário cadastrado
    Quando envio POST /auth/login com credenciais corretas
    Então recebo 200 com um JWT que expira em 1 hora

  Cenário: Credenciais inválidas
    Dado um usuário cadastrado
    Quando envio senha incorreta
    Então recebo 401 sem indicar qual campo está errado

  Cenário: Token expirado
    Dado um JWT expirado
    Quando acesso GET /pesquisas
    Então recebo 401 'Token expirado'
```
Pronto quando: DoD padrão + Senhas com hash BCrypt; segredo JWT em variável de ambiente/cofre.

**PBI-12 — Controle de acesso por perfil (Analista, Gestor, Administrador)**  
Como administrador, quero atribuir perfis aos usuários, para que cada um acesse apenas o que lhe é permitido.  
Prioridade: **Must** · Esforço: **5 pts** · Depende de: PBI-11 · Release: **Sprint 2**

```gherkin
Funcionalidade: Controle de acesso por perfil (Analista, Gestor, Administrador)

  Cenário: Analista cria pesquisa
    Dado um usuário com perfil Analista
    Quando cria uma pesquisa
    Então recebe 201

  Cenário: Analista tenta gerenciar catálogo
    Dado um usuário com perfil Analista
    Quando envia POST /atributos
    Então recebe 403 Forbidden

  Cenário: Admin gerencia usuários
    Dado um usuário com perfil Administrador
    Quando altera o perfil de outro usuário
    Então recebe 200
```
Pronto quando: DoD padrão + Matriz de permissões publicada na Wiki.

#### FT-04 — Proteção da API e DevSecOps

*Como responsável por segurança, quero a API protegida contra abuso e o código verificado automaticamente, para reduzir riscos antes do deploy.*  
**Critério de aceite:** Dado um volume de requisições acima do limite, então a API responde 429; dado um PR com segredo exposto, então o pipeline falha.

**PBI-21 — Hardening da API: rate limit, validação de entrada e padronização de erros**  
Como responsável por segurança, quero limitar abusos e validar entradas, para proteger a API contra ataques e dados maliciosos.  
Prioridade: **Must** · Esforço: **3 pts** · Depende de: PBI-11 · Release: **Sprint 3**

```gherkin
Funcionalidade: Hardening da API: rate limit, validação de entrada e padronização de erros

  Cenário: Rate limit
    Dado um usuário que fez 60 requisições no último minuto
    Quando faz a 61ª requisição
    Então recebe 429 Too Many Requests

  Cenário: Entrada maliciosa
    Dado um campo 'modelo' com script '<script>'
    Quando envio a pesquisa
    Então recebo 400 com erro no formato padrão (RFC 7807)
```
Pronto quando: DoD padrão + Erros padronizados em todos os endpoints.

**PBI-22 — Pipeline DevSecOps (SAST, SCA, secret scanning e container scan)**  
Como equipe, quero verificações de segurança automáticas no pipeline, para detectar vulnerabilidades antes do deploy.  
Prioridade: **Should** · Esforço: **5 pts** · Depende de: PBI-02 · Release: **Sprint 3**

```gherkin
Funcionalidade: Pipeline DevSecOps (SAST, SCA, secret scanning e container scan)

  Cenário: Segredo exposto
    Dado um commit contendo uma chave de API
    Quando o pipeline executa o Gitleaks
    Então o build falha e aponta o arquivo

  Cenário: Dependência vulnerável
    Dado uma dependência com CVE crítica
    Quando o pipeline executa o SCA
    Então o build falha com o relatório da vulnerabilidade
```
Pronto quando: DoD padrão + Relatórios de SAST/SCA/Trivy publicados como artefatos do pipeline.

### EP-03 — Pesquisa de Veículos Concorrentes (Entrada)

Permitir que o analista informe, a partir de uma entrada simples, Marca, Modelo e Versão do veículo e defina livremente a lista de equipamentos/atributos técnicos que deseja pesquisar.  
**Critério de aceite do épico:** Usuário consegue iniciar uma pesquisa informando Marca, Modelo, Versão e uma lista livre de atributos; entradas inválidas são rejeitadas com mensagem clara.

#### FT-05 — Identificação do Veículo

*Como analista, quero informar Marca, Modelo e Versão de forma simples, para identificar exatamente o veículo concorrente.*  
**Critério de aceite:** Dado que informo Marca, Modelo e Versão válidos, quando confirmo, então a pesquisa é criada com status 'Em processamento'.

**PBI-06 — Informar Marca, Modelo e Versão para iniciar a pesquisa**  
Como analista, quero informar Marca, Modelo e Versão, para identificar o veículo concorrente a ser pesquisado.  
Prioridade: **Must** · Esforço: **5 pts** · Depende de: PBI-03 · Release: **Sprint 1**

```gherkin
Funcionalidade: Informar Marca, Modelo e Versão para iniciar a pesquisa

  Cenário: Entrada válida
    Dado que estou autenticado
    Quando envio POST /pesquisas com marca 'Ford', modelo 'Ranger' e versão 'Raptor'
    Então recebo 201 Created com o id da pesquisa e status 'EM_PROCESSAMENTO'

  Cenário: Campo obrigatório ausente
    Dado que estou autenticado
    Quando envio a pesquisa sem a versão
    Então recebo 400 Bad Request informando que 'versao' é obrigatória
```
Pronto quando: DoD padrão + Endpoint documentado no Swagger com exemplos.

**PBI-07 — Sugerir (autocompletar) marcas, modelos e versões**  
Como analista, quero sugestões enquanto digito, para evitar erros de digitação na identificação do veículo.  
Prioridade: **Should** · Esforço: **3 pts** · Depende de: PBI-06 · Release: **Sprint 1**

```gherkin
Funcionalidade: Sugerir (autocompletar) marcas, modelos e versões

  Cenário: Sugestão de modelo
    Dado que selecionei a marca 'Toyota'
    Quando digito 'Hil'
    Então vejo a sugestão 'Hilux'
```
Pronto quando: DoD padrão + Resposta de sugestões em menos de 500 ms (p95).

#### FT-06 — Lista Livre de Atributos

*Como analista, quero definir livremente a lista de equipamentos/atributos que desejo pesquisar, para focar no que importa para cada análise.*  
**Critério de aceite:** Dado que adiciono atributos do catálogo ou texto livre, quando envio a pesquisa, então todos os atributos informados aparecem no resultado.

**PBI-08 — Definir livremente a lista de atributos a pesquisar**  
Como analista, quero escolher atributos do catálogo ou digitar atributos livres, para montar a pesquisa conforme minha necessidade.  
Prioridade: **Must** · Esforço: **5 pts** · Depende de: PBI-04, PBI-06 · Release: **Sprint 1**

```gherkin
Funcionalidade: Definir livremente a lista de atributos a pesquisar

  Cenário: Atributos do catálogo e livres
    Dado que informei o veículo
    Quando adiciono 'Torque máximo' do catálogo e o texto livre 'Snorkel'
    Então a pesquisa é registrada com os 2 atributos

  Cenário: Lista vazia
    Dado que informei o veículo
    Quando envio a pesquisa sem nenhum atributo
    Então recebo 400 com a mensagem 'Informe ao menos um atributo'
```
Pronto quando: DoD padrão + Limite máximo de 100 atributos por pesquisa validado.

**PBI-36 — Salvar modelos (templates) de listas de atributos**  
Como analista, quero salvar listas de atributos usadas com frequência, para agilizar novas pesquisas.  
Prioridade: **Could** · Esforço: **3 pts** · Depende de: PBI-08 · Release: **Backlog futuro**

```gherkin
Funcionalidade: Salvar modelos (templates) de listas de atributos

  Cenário: Template salvo
    Dado uma lista com 10 atributos
    Quando salvo como 'Picapes médias'
    Então consigo reutilizá-la em uma nova pesquisa
```
Pronto quando: DoD padrão + Templates privados por usuário.

### EP-04 — Coleta e Extração Inteligente de Dados Técnicos

Coletar dados técnicos da concorrência em fontes oficiais e secundárias e extrair as especificações com um motor híbrido (IA/LLM + regras), normalizando unidades.  
**Critério de aceite do épico:** Para um veículo válido, o motor retorna os atributos solicitados com valor, unidade normalizada e fonte (URL e data de coleta).

#### FT-07 — Coleta de Fontes de Dados

*Como analista, quero que a ferramenta busque dados em fontes confiáveis, para não precisar pesquisar manualmente em vários sites.*  
**Critério de aceite:** Dado um veículo válido, quando a coleta é executada, então o conteúdo das fontes é armazenado com URL e data de coleta.

**PBI-13 — Conector de coleta em fichas técnicas oficiais das montadoras**  
Como analista, quero que a ferramenta colete a ficha técnica no site oficial da montadora, para ter dados de fonte primária.  
Prioridade: **Must** · Esforço: **8 pts** · Depende de: PBI-03, PBI-06 · Release: **Sprint 2**

```gherkin
Funcionalidade: Conector de coleta em fichas técnicas oficiais das montadoras

  Cenário: Coleta com sucesso
    Dado uma pesquisa da 'Ford Ranger Raptor'
    Quando o conector é executado
    Então o conteúdo da ficha técnica é salvo com URL e data de coleta

  Cenário: Fonte indisponível
    Dado que o site da montadora está fora do ar
    Quando o conector é executado
    Então a falha é registrada e a pesquisa segue para fontes alternativas
```
Pronto quando: DoD padrão + Respeita robots.txt e timeout de 15 s por fonte.

**PBI-14 — Cache de fontes coletadas com data e URL**  
Como analista, quero reaproveitar coletas recentes, para obter respostas mais rápidas e reduzir custo.  
Prioridade: **Should** · Esforço: **3 pts** · Depende de: PBI-13 · Release: **Sprint 2**

```gherkin
Funcionalidade: Cache de fontes coletadas com data e URL

  Cenário: Cache válido
    Dado uma coleta do mesmo veículo feita há menos de 7 dias
    Quando faço nova pesquisa
    Então o conteúdo em cache é utilizado

  Cenário: Cache expirado
    Dado uma coleta com mais de 7 dias
    Quando faço nova pesquisa
    Então uma nova coleta é realizada
```
Pronto quando: DoD padrão + TTL configurável por variável de ambiente.

**PBI-28 — Conector para fontes secundárias (portais automotivos especializados)**  
Como analista, quero complementar a ficha oficial com portais especializados, para reduzir campos 'Não disponível'.  
Prioridade: **Should** · Esforço: **5 pts** · Depende de: PBI-13 · Release: **Sprint 4**

```gherkin
Funcionalidade: Conector para fontes secundárias (portais automotivos especializados)

  Cenário: Complemento de dados
    Dado um atributo ausente na ficha oficial
    Quando o conector secundário encontra o valor
    Então o atributo é preenchido com a fonte secundária identificada
```
Pronto quando: DoD padrão + Fonte primária sempre tem precedência sobre a secundária.

#### FT-08 — Extração de Especificações com IA

*Como analista, quero que a IA extraia e normalize as especificações das fontes, para receber dados precisos e organizados.*  
**Critério de aceite:** Dado o conteúdo coletado, quando o motor processa, então cada atributo solicitado recebe valor, unidade padrão, fonte e grau de confiança.

**PBI-15 — Extrair especificações do conteúdo coletado com motor híbrido (LLM + regras)**  
Como analista, quero que a IA identifique no texto das fontes os valores dos atributos solicitados, para não ter que ler fichas técnicas manualmente.  
Prioridade: **Must** · Esforço: **13 pts** · Depende de: PBI-04, PBI-13 · Release: **Sprint 2**

```gherkin
Funcionalidade: Extrair especificações do conteúdo coletado com motor híbrido (LLM + regras)

  Cenário: Extração de atributo existente
    Dado o conteúdo coletado da Ranger Raptor
    Quando o motor extrai 'Potência máxima'
    Então retorna o valor e a unidade encontrados na fonte

  Cenário: Atributo não encontrado
    Dado um atributo que não consta em nenhuma fonte
    Quando o motor processa
    Então retorna o atributo sem valor, sem inventar dados
```
Pronto quando: DoD padrão + Precisão ≥ 90% no gabarito da Ranger Raptor; prompt e regras versionados.

**PBI-18 — Normalizar unidades e formatos das especificações**  
Como gestor, quero que valores venham em unidades padrão (cv, kgfm, mm, L, kg), para comparar veículos sem conversões manuais.  
Prioridade: **Must** · Esforço: **5 pts** · Depende de: PBI-15 · Release: **Sprint 3**

```gherkin
Funcionalidade: Normalizar unidades e formatos das especificações

  Cenário: Conversão de unidade
    Dado que a fonte informa '292 kW'
    Quando o normalizador processa o atributo 'Potência máxima'
    Então o valor exibido é '397 cv'

  Cenário: Valor já padronizado
    Dado que a fonte informa '397 cv'
    Quando o normalizador processa
    Então o valor permanece '397 cv'
```
Pronto quando: DoD padrão + Cobertura de testes unitários ≥ 90% no módulo normalizador.

**PBI-29 — Indicador de confiança e rastreabilidade de fonte por atributo**  
Como gestor, quero saber a confiança e a origem de cada dado, para decidir se posso usá-lo em análises estratégicas.  
Prioridade: **Should** · Esforço: **5 pts** · Depende de: PBI-15 · Release: **Sprint 4**

```gherkin
Funcionalidade: Indicador de confiança e rastreabilidade de fonte por atributo

  Cenário: Fontes divergentes
    Dado duas fontes com valores diferentes para 'Torque máximo'
    Quando o motor consolida o resultado
    Então o atributo exibe confiança 'Média' e as duas fontes
```
Pronto quando: DoD padrão + Regra de cálculo da confiança documentada.

### EP-05 — Saída Padronizada de Especificações Técnicas

Gerar uma lista de especificações técnicas sempre no mesmo formato, independente do veículo, com campos claros, organizados e comparáveis, explicitando dados inexistentes.  
**Critério de aceite do épico:** Saída segue um schema único e versionado; atributos sem informação aparecem como 'Não disponível'; é possível comparar e exportar resultados.

#### FT-09 — Lista Padronizada de Especificações

*Como gestor de produto, quero receber as especificações sempre no mesmo formato, para comparar veículos rapidamente.*  
**Critério de aceite:** Dadas duas pesquisas de veículos diferentes, quando visualizo os resultados, então ambos têm exatamente os mesmos campos na mesma ordem.

**PBI-19 — Gerar lista de especificações em formato único (schema padronizado)**  
Como gestor de produto, quero que a lista de especificações tenha sempre os mesmos campos e ordem, para comparar qualquer veículo.  
Prioridade: **Must** · Esforço: **8 pts** · Depende de: PBI-08, PBI-18 · Release: **Sprint 3**

```gherkin
Funcionalidade: Gerar lista de especificações em formato único (schema padronizado)

  Cenário: Formato único
    Dado pesquisas concluídas da 'Ford Ranger Raptor' e da 'Toyota Hilux GR-S'
    Quando consulto GET /pesquisas/{id}/especificacoes de cada uma
    Então ambas as respostas seguem o mesmo schema: categoria, atributo, valor, unidade, fonte, dataColeta, confianca

  Cenário: Pesquisa inexistente
    Dado um id de pesquisa que não existe
    Quando consulto as especificações
    Então recebo 404 no formato padrão de erro
```
Pronto quando: DoD padrão + Schema JSON versionado (v1) e teste de contrato no pipeline.

**PBI-20 — Explicitar 'Não disponível' quando a informação não existir**  
Como analista, quero ver claramente quando um dado não foi encontrado, para não confundir ausência de informação com erro.  
Prioridade: **Must** · Esforço: **2 pts** · Depende de: PBI-19 · Release: **Sprint 3**

```gherkin
Funcionalidade: Explicitar 'Não disponível' quando a informação não existir

  Cenário: Dado inexistente
    Dado que o atributo 'Snorkel' não foi encontrado em nenhuma fonte
    Quando consulto o resultado
    Então o atributo aparece com valor 'Não disponível' e motivo 'Não encontrado nas fontes consultadas'
```
Pronto quando: DoD padrão + Nenhum campo do schema retorna nulo ou vazio sem o status explícito.

#### FT-10 — Comparação, Exportação e Histórico

*Como gestor de produto, quero comparar veículos lado a lado e exportar os dados, para apoiar decisões de preço e pacote de equipamentos.*  
**Critério de aceite:** Dado dois ou mais resultados, quando comparo, então vejo uma tabela única com as diferenças destacadas e posso exportá-la.

**PBI-30 — Comparar dois ou mais veículos lado a lado**  
Como gestor de produto, quero comparar veículos concorrentes lado a lado, para entender o posicionamento em pacotes de equipamentos.  
Prioridade: **Should** · Esforço: **8 pts** · Depende de: PBI-19 · Release: **Sprint 4**

```gherkin
Funcionalidade: Comparar dois ou mais veículos lado a lado

  Cenário: Comparação
    Dado as pesquisas da Ranger Raptor e da Hilux GR-S
    Quando solicito a comparação
    Então vejo uma tabela com os mesmos atributos e as diferenças destacadas
```
Pronto quando: DoD padrão + Comparação de até 4 veículos.

**PBI-32 — Exportar especificações em CSV, XLSX e PDF**  
Como gestor, quero exportar os resultados, para compartilhar com outras áreas da Ford.  
Prioridade: **Should** · Esforço: **5 pts** · Depende de: PBI-19 · Release: **Sprint 4**

```gherkin
Funcionalidade: Exportar especificações em CSV, XLSX e PDF

  Cenário: Exportação CSV
    Dado uma pesquisa concluída
    Quando solicito exportação em CSV
    Então recebo um arquivo com os mesmos campos do schema padrão
```
Pronto quando: DoD padrão + Arquivos exportados preservam 'Não disponível'.

**PBI-33 — Histórico de pesquisas do usuário**  
Como analista, quero consultar minhas pesquisas anteriores, para reutilizar resultados sem refazer a coleta.  
Prioridade: **Could** · Esforço: **3 pts** · Depende de: PBI-12, PBI-19 · Release: **Sprint 4**

```gherkin
Funcionalidade: Histórico de pesquisas do usuário

  Cenário: Histórico
    Dado que realizei 5 pesquisas
    Quando acesso o histórico
    Então vejo as 5 pesquisas ordenadas da mais recente para a mais antiga
```
Pronto quando: DoD padrão + Paginação implementada.

### EP-06 — Aplicativo Mobile

Aplicativo React Native (Expo) com identidade visual consistente, que permite pesquisar, visualizar e comparar especificações, publicado como APK.  
**Critério de aceite do épico:** APK instala e executa em dispositivo físico/emulador; todos os fluxos (login, pesquisa, resultado, comparação) funcionam sem erros.

#### FT-11 — Telas do Aplicativo

*Como usuário mobile, quero telas consistentes e intuitivas, para pesquisar e consultar especificações em qualquer lugar.*  
**Critério de aceite:** Dado o app instalado, quando navego pelas telas, então cores, tipografia e componentes seguem o design system.

**PBI-09 — Criar design system do app (cores, tipografia, componentes)**  
Como usuário, quero uma identidade visual consistente, para ter uma experiência profissional em todas as telas.  
Prioridade: **Must** · Esforço: **3 pts** · Depende de: — · Release: **Sprint 1**

```gherkin
Funcionalidade: Criar design system do app (cores, tipografia, componentes)

  Cenário: Componentes reutilizáveis
    Dado a biblioteca de componentes do app
    Quando uma nova tela é criada
    Então ela usa apenas tokens de cor, tipografia e componentes do design system
```
Pronto quando: DoD padrão + Design system documentado no Figma e implementado como tema no app.

**PBI-16 — Telas de login e cadastro no app**  
Como usuário mobile, quero entrar no app com minhas credenciais, para acessar minhas pesquisas.  
Prioridade: **Must** · Esforço: **3 pts** · Depende de: PBI-09, PBI-11 · Release: **Sprint 2**

```gherkin
Funcionalidade: Telas de login e cadastro no app

  Cenário: Login no app
    Dado que estou na tela de login
    Quando informo credenciais válidas
    Então sou direcionado à tela inicial e o token fica em armazenamento seguro

  Cenário: Erro de login
    Dado que estou na tela de login
    Quando informo senha errada
    Então vejo a mensagem 'E-mail ou senha inválidos'
```
Pronto quando: DoD padrão + Token armazenado com expo-secure-store.

**PBI-17 — Tela de nova pesquisa (veículo + lista de atributos)**  
Como analista mobile, quero informar o veículo e os atributos em uma única tela, para iniciar a pesquisa rapidamente.  
Prioridade: **Must** · Esforço: **5 pts** · Depende de: PBI-06, PBI-08, PBI-09 · Release: **Sprint 2**

```gherkin
Funcionalidade: Tela de nova pesquisa (veículo + lista de atributos)

  Cenário: Pesquisa enviada
    Dado que preenchi Marca, Modelo, Versão e 3 atributos
    Quando toco em 'Pesquisar'
    Então vejo a confirmação e o status 'Em processamento'

  Cenário: Campos obrigatórios
    Dado que não preenchi a Versão
    Quando toco em 'Pesquisar'
    Então o campo Versão é destacado com mensagem de obrigatoriedade
```
Pronto quando: DoD padrão + Tela validada em Android físico e emulador.

**PBI-25 — Tela de resultado com a lista padronizada de especificações**  
Como analista mobile, quero visualizar as especificações agrupadas por categoria, para consultar os dados de forma clara.  
Prioridade: **Must** · Esforço: **5 pts** · Depende de: PBI-17, PBI-19 · Release: **Sprint 3**

```gherkin
Funcionalidade: Tela de resultado com a lista padronizada de especificações

  Cenário: Resultado exibido
    Dado uma pesquisa concluída
    Quando abro a tela de resultado
    Então vejo os atributos agrupados por categoria com valor, unidade e fonte

  Cenário: Dado indisponível
    Dado um atributo sem informação
    Quando abro a tela de resultado
    Então vejo o selo 'Não disponível' em cinza
```
Pronto quando: DoD padrão + Estados de carregando, vazio e erro implementados.

**PBI-31 — Tela de comparação de veículos no app**  
Como analista mobile, quero comparar veículos no app, para apoiar reuniões de negócio.  
Prioridade: **Should** · Esforço: **5 pts** · Depende de: PBI-25, PBI-30 · Release: **Sprint 4**

```gherkin
Funcionalidade: Tela de comparação de veículos no app

  Cenário: Comparar no app
    Dado que selecionei 2 pesquisas concluídas
    Quando toco em 'Comparar'
    Então vejo a tabela comparativa com rolagem horizontal
```
Pronto quando: DoD padrão + Validada em telas de 5" a 6,7".

#### FT-12 — Publicação do Aplicativo

*Como avaliador, quero instalar o app via APK, para testar a solução em um dispositivo real.*  
**Critério de aceite:** Dado o APK gerado pelo EAS Build, quando instalo em um Android, então o app abre e executa todos os fluxos sem erros.

**PBI-26 — Gerar build APK via Expo EAS Build**  
Como avaliador, quero um APK instalável, para testar o app em um dispositivo Android.  
Prioridade: **Must** · Esforço: **3 pts** · Depende de: PBI-25 · Release: **Sprint 3**

```gherkin
Funcionalidade: Gerar build APK via Expo EAS Build

  Cenário: APK instalável
    Dado o perfil 'preview' configurado no eas.json
    Quando executo o EAS Build
    Então o APK é gerado, instala e abre sem erros em dispositivo físico
```
Pronto quando: DoD padrão + Link do APK e evidências (prints) no README.

### EP-07 — Qualidade, Validação e Observabilidade

Assegurar que a solução está operando corretamente, usando a Ford Ranger Raptor como caso de validação oficial, testes automatizados e monitoramento.  
**Critério de aceite do épico:** 100% das especificações do slide da Ranger Raptor entregues corretamente pelo teste de aceitação automatizado; logs estruturados e dashboard de monitoramento ativos.

#### FT-13 — Validação com Ford Ranger Raptor

*Como Ford (cliente do desafio), quero validar a solução com a Ranger Raptor, para confirmar que ela opera corretamente.*  
**Critério de aceite:** Dado o gabarito da Ranger Raptor, quando a pesquisa é executada, então todas as especificações do slide são entregues corretamente.

**PBI-10 — Criar gabarito de referência (massa de teste) da Ford Ranger Raptor**  
Como QA, quero o gabarito oficial das especificações da Ranger Raptor, para validar automaticamente a saída da solução.  
Prioridade: **Must** · Esforço: **3 pts** · Depende de: PBI-04 · Release: **Sprint 1**

```gherkin
Funcionalidade: Criar gabarito de referência (massa de teste) da Ford Ranger Raptor

  Cenário: Gabarito completo
    Dado o slide de especificações da Ranger Raptor fornecido pela Ford
    Quando o gabarito JSON é criado
    Então contém todos os atributos do slide com valor e unidade padronizados
```
Pronto quando: DoD padrão + Gabarito revisado por 2 membros e versionado em /tests/fixtures.

**PBI-24 — Teste de aceitação automatizado com a Ford Ranger Raptor**  
Como Ford, quero que a solução seja validada automaticamente com a Ranger Raptor, para confirmar que opera corretamente.  
Prioridade: **Must** · Esforço: **5 pts** · Depende de: PBI-10, PBI-20 · Release: **Sprint 3**

```gherkin
Funcionalidade: Teste de aceitação automatizado com a Ford Ranger Raptor

  Cenário: Validação oficial
    Dado o gabarito da Ford Ranger Raptor
    Quando executo a pesquisa com todos os atributos do slide
    Então 100% das especificações retornadas conferem com o gabarito em valor e unidade

  Cenário: Formato consistente
    Dado o resultado da Ranger Raptor
    Quando valido contra o schema v1
    Então a validação passa sem erros
```
Pronto quando: DoD padrão + Cenário BDD executando no pipeline e relatório de aderência campo a campo anexado.

#### FT-14 — Testes Automatizados e Observabilidade

*Como equipe, quero testes automatizados e monitoramento, para detectar falhas rapidamente e garantir qualidade contínua.*  
**Critério de aceite:** Dado um deploy, quando os testes rodam, então o relatório é publicado no pipeline; dado um erro em produção, então ele aparece no dashboard.

**PBI-23 — Testes automatizados da API (sucesso, erro e acesso não autorizado)**  
Como QA, quero testes automatizados dos principais comportamentos da API, para garantir que regressões sejam detectadas.  
Prioridade: **Must** · Esforço: **5 pts** · Depende de: PBI-12, PBI-19 · Release: **Sprint 3**

```gherkin
Funcionalidade: Testes automatizados da API (sucesso, erro e acesso não autorizado)

  Cenário: Suíte executada no pipeline
    Dado a suíte de testes de API
    Quando o pipeline é executado
    Então os cenários de sucesso, erro (400/404) e não autorizado (401/403) são executados e o relatório é publicado
```
Pronto quando: DoD padrão + Cobertura de linhas ≥ 70% na API; relatório JUnit publicado na aba Tests do pipeline.

**PBI-34 — Logs estruturados, métricas e dashboard de monitoramento**  
Como equipe de operação, quero logs e dashboards, para detectar e responder a incidentes rapidamente.  
Prioridade: **Should** · Esforço: **5 pts** · Depende de: PBI-11 · Release: **Sprint 4**

```gherkin
Funcionalidade: Logs estruturados, métricas e dashboard de monitoramento

  Cenário: Falha de login registrada
    Dado 5 tentativas de login falhas em 1 minuto
    Quando consulto o dashboard
    Então vejo o alerta de possível força bruta com usuário e IP
```
Pronto quando: DoD padrão + Dashboard no Grafana/Azure Monitor com latência, erros e taxa de sucesso da extração.

**PBI-37 — Monitorar custo e latência das chamadas ao modelo de IA**  
Como gestor técnico, quero acompanhar custo e tempo do modelo de IA, para controlar o orçamento da solução.  
Prioridade: **Could** · Esforço: **3 pts** · Depende de: PBI-15, PBI-34 · Release: **Backlog futuro**

```gherkin
Funcionalidade: Monitorar custo e latência das chamadas ao modelo de IA

  Cenário: Custo monitorado
    Dado chamadas ao LLM durante o dia
    Quando consulto o dashboard
    Então vejo tokens consumidos, custo estimado e latência p95
```
Pronto quando: DoD padrão + Alerta quando o custo diário ultrapassar o limite configurado.

### EP-08 — Entrega Final e Pitch

Consolidar documentação e apresentar a solução final à Ford e à FIAP em vídeo pitch/técnico de até 6 minutos.  
**Critério de aceite do épico:** README e Swagger completos; vídeo com pitch + parte técnica, até 6 minutos, entregue em todas as disciplinas.

#### FT-15 — Documentação e Apresentação Final

*Como professores e Ford, queremos documentação clara e um pitch objetivo, para entender e avaliar a solução.*  
**Critério de aceite:** Dado o repositório, quando sigo o README, então consigo executar a solução; o vídeo tem no máximo 6 minutos.

**PBI-27 — Documentação da API (OpenAPI/Swagger) e README de execução**  
Como desenvolvedor e avaliador, quero a API documentada e instruções de execução, para usar e avaliar a solução.  
Prioridade: **Must** · Esforço: **3 pts** · Depende de: PBI-19, PBI-21 · Release: **Sprint 3**

```gherkin
Funcionalidade: Documentação da API (OpenAPI/Swagger) e README de execução

  Cenário: Swagger disponível
    Dado a API em execução
    Quando acesso /swagger-ui
    Então vejo todos os endpoints com exemplos, códigos de status e esquema de autenticação

  Cenário: README executável
    Dado um ambiente limpo
    Quando sigo o README
    Então consigo subir API e app localmente
```
Pronto quando: DoD padrão + README revisado por um membro que não participou da escrita.

**PBI-35 — Produzir vídeo pitch/técnico da solução final (até 6 min)**  
Como equipe, queremos apresentar o problema, a solução e a parte técnica em vídeo, para a avaliação final da Ford e FIAP.  
Prioridade: **Must** · Esforço: **5 pts** · Depende de: PBI-24, PBI-26 · Release: **Sprint 4**

```gherkin
Funcionalidade: Produzir vídeo pitch/técnico da solução final (até 6 min)

  Cenário: Vídeo entregue
    Dado o roteiro aprovado pela equipe
    Quando o vídeo é finalizado
    Então tem até 6 minutos, contém pitch e demonstração técnica e o link é entregue em todas as disciplinas
```
Pronto quando: DoD padrão + Link do vídeo publicado no Teams de todas as disciplinas.

## 4. Backlog ordenado (sequência de implementação)

| # | PBI | Título | Prioridade | Esforço | Depende de | Sprint |
|---|---|---|---|---|---|---|
| 1 | PBI-01 | Definir arquitetura da solução e diagrama de componentes | Must | 3 | — | Sprint 1 |
| 2 | PBI-02 | Configurar repositório, estratégia de branches e pipeline CI | Must | 5 | PBI-01 | Sprint 1 |
| 3 | PBI-03 | Modelar banco de dados (veículos, atributos, pesquisas, especificações, fontes) | Must | 5 | PBI-01 | Sprint 1 |
| 4 | PBI-04 | Cadastrar catálogo padrão de atributos técnicos com unidade e categoria | Must | 5 | PBI-03 | Sprint 1 |
| 5 | PBI-05 | Mapear sinônimos de atributos (ex.: 'cv', 'potência', 'hp') | Should | 3 | PBI-04 | Sprint 1 |
| 6 | PBI-06 | Informar Marca, Modelo e Versão para iniciar a pesquisa | Must | 5 | PBI-03 | Sprint 1 |
| 7 | PBI-07 | Sugerir (autocompletar) marcas, modelos e versões | Should | 3 | PBI-06 | Sprint 1 |
| 8 | PBI-08 | Definir livremente a lista de atributos a pesquisar | Must | 5 | PBI-04, PBI-06 | Sprint 1 |
| 9 | PBI-09 | Criar design system do app (cores, tipografia, componentes) | Must | 3 | — | Sprint 1 |
| 10 | PBI-10 | Criar gabarito de referência (massa de teste) da Ford Ranger Raptor | Must | 3 | PBI-04 | Sprint 1 |
| 11 | PBI-11 | Cadastro e login com geração e validação de JWT | Must | 8 | PBI-02, PBI-03 | Sprint 2 |
| 12 | PBI-12 | Controle de acesso por perfil (Analista, Gestor, Administrador) | Must | 5 | PBI-11 | Sprint 2 |
| 13 | PBI-13 | Conector de coleta em fichas técnicas oficiais das montadoras | Must | 8 | PBI-03, PBI-06 | Sprint 2 |
| 14 | PBI-14 | Cache de fontes coletadas com data e URL | Should | 3 | PBI-13 | Sprint 2 |
| 15 | PBI-15 | Extrair especificações do conteúdo coletado com motor híbrido (LLM + regras) | Must | 13 | PBI-04, PBI-13 | Sprint 2 |
| 16 | PBI-16 | Telas de login e cadastro no app | Must | 3 | PBI-09, PBI-11 | Sprint 2 |
| 17 | PBI-17 | Tela de nova pesquisa (veículo + lista de atributos) | Must | 5 | PBI-06, PBI-08, PBI-09 | Sprint 2 |
| 18 | PBI-18 | Normalizar unidades e formatos das especificações | Must | 5 | PBI-15 | Sprint 3 |
| 19 | PBI-19 | Gerar lista de especificações em formato único (schema padronizado) | Must | 8 | PBI-08, PBI-18 | Sprint 3 |
| 20 | PBI-20 | Explicitar 'Não disponível' quando a informação não existir | Must | 2 | PBI-19 | Sprint 3 |
| 21 | PBI-21 | Hardening da API: rate limit, validação de entrada e padronização de erros | Must | 3 | PBI-11 | Sprint 3 |
| 22 | PBI-22 | Pipeline DevSecOps (SAST, SCA, secret scanning e container scan) | Should | 5 | PBI-02 | Sprint 3 |
| 23 | PBI-23 | Testes automatizados da API (sucesso, erro e acesso não autorizado) | Must | 5 | PBI-12, PBI-19 | Sprint 3 |
| 24 | PBI-24 | Teste de aceitação automatizado com a Ford Ranger Raptor | Must | 5 | PBI-10, PBI-20 | Sprint 3 |
| 25 | PBI-25 | Tela de resultado com a lista padronizada de especificações | Must | 5 | PBI-17, PBI-19 | Sprint 3 |
| 26 | PBI-26 | Gerar build APK via Expo EAS Build | Must | 3 | PBI-25 | Sprint 3 |
| 27 | PBI-27 | Documentação da API (OpenAPI/Swagger) e README de execução | Must | 3 | PBI-19, PBI-21 | Sprint 3 |
| 28 | PBI-28 | Conector para fontes secundárias (portais automotivos especializados) | Should | 5 | PBI-13 | Sprint 4 |
| 29 | PBI-29 | Indicador de confiança e rastreabilidade de fonte por atributo | Should | 5 | PBI-15 | Sprint 4 |
| 30 | PBI-30 | Comparar dois ou mais veículos lado a lado | Should | 8 | PBI-19 | Sprint 4 |
| 31 | PBI-31 | Tela de comparação de veículos no app | Should | 5 | PBI-25, PBI-30 | Sprint 4 |
| 32 | PBI-32 | Exportar especificações em CSV, XLSX e PDF | Should | 5 | PBI-19 | Sprint 4 |
| 33 | PBI-33 | Histórico de pesquisas do usuário | Could | 3 | PBI-12, PBI-19 | Sprint 4 |
| 34 | PBI-34 | Logs estruturados, métricas e dashboard de monitoramento | Should | 5 | PBI-11 | Sprint 4 |
| 35 | PBI-35 | Produzir vídeo pitch/técnico da solução final (até 6 min) | Must | 5 | PBI-24, PBI-26 | Sprint 4 |
| 36 | PBI-36 | Salvar modelos (templates) de listas de atributos | Could | 3 | PBI-08 | Backlog futuro |
| 37 | PBI-37 | Monitorar custo e latência das chamadas ao modelo de IA | Could | 3 | PBI-15, PBI-34 | Backlog futuro |

## 5. Release plan (roadmap de entregas)

| Sprint | Período | Objetivo | PBIs | Pontos |
|---|---|---|---|---|
| **Sprint 1** | 16/02/2026 – 12/04/2026 | Fundação, catálogo de atributos e entrada da pesquisa | PBI-01, PBI-02, PBI-03, PBI-04, PBI-05, PBI-06, PBI-07, PBI-08, PBI-09, PBI-10 | **40** |
| **Sprint 2** | 13/04/2026 – 07/06/2026 | Autenticação, coleta de fontes e extração com IA | PBI-11, PBI-12, PBI-13, PBI-14, PBI-15, PBI-16, PBI-17 | **45** |
| **Sprint 3** | 03/08/2026 – 27/09/2026 | Saída padronizada, validação Ranger Raptor, APK e segurança | PBI-18, PBI-19, PBI-20, PBI-21, PBI-22, PBI-23, PBI-24, PBI-25, PBI-26, PBI-27 | **44** |
| **Sprint 4** | 28/09/2026 – 11/10/2026 | Comparação, exportação, observabilidade e vídeo pitch | PBI-28, PBI-29, PBI-30, PBI-31, PBI-32, PBI-33, PBI-34, PBI-35 | **41** |
| **Backlog futuro** | - – - | Itens opcionais não planejados nesta release | PBI-36, PBI-37 | **6** |

Total planejado: **170 pontos** em 4 sprints (média de **42 pontos/sprint**, variação máxima de ±5 pontos). Itens *Could* sem capacidade ficam no Backlog futuro.

## 6. Sprint atual — Sprint 3 (03/08/2026 – 27/09/2026)

**Meta da sprint:** entregar a lista padronizada de especificações validada com a Ford Ranger Raptor, o APK do app e a API protegida com pipeline DevSecOps.

**Capacidade comprometida:** 44 pontos · 87 horas de tarefas.

| Tarefa | PBI | Descrição | Atividade | Esforço (h) | Depende de |
|---|---|---|---|---|---|
| T-01 | PBI-18 | Criar tabela de conversão de unidades (kW→cv, Nm→kgfm, pol→mm) | Development | 4 | — |
| T-02 | PBI-18 | Implementar serviço normalizador de valores e unidades | Development | 6 | T-01 |
| T-03 | PBI-18 | Testes unitários do normalizador (casos de borda e unidades desconhecidas) | Testing | 3 | T-02 |
| T-04 | PBI-19 | Definir schema JSON v1 da lista de especificações | Design | 3 | — |
| T-05 | PBI-19 | Implementar endpoint GET /pesquisas/{id}/especificacoes | Development | 6 | T-04, T-02 |
| T-06 | PBI-19 | Agrupar e ordenar atributos por categoria do catálogo | Development | 3 | T-05 |
| T-07 | PBI-19 | Teste de contrato do schema v1 no pipeline | Testing | 3 | T-05 |
| T-08 | PBI-20 | Regra de preenchimento 'Não disponível' com motivo | Development | 2 | T-05 |
| T-09 | PBI-20 | Testes de atributos inexistentes e texto livre não reconhecido | Testing | 2 | T-08 |
| T-10 | PBI-21 | Implementar rate limit por usuário/IP (60 req/min) | Development | 3 | — |
| T-11 | PBI-21 | Validação e sanitização de entrada em todos os DTOs | Development | 3 | — |
| T-12 | PBI-21 | Padronizar respostas de erro (RFC 7807 Problem Details) | Development | 2 | T-11 |
| T-13 | PBI-22 | Adicionar SAST (Semgrep/SonarCloud) ao pipeline | Deployment | 3 | — |
| T-14 | PBI-22 | Habilitar SCA (Dependabot/Snyk) nas dependências da API e do app | Deployment | 2 | — |
| T-15 | PBI-22 | Adicionar secret scanning (Gitleaks) ao pipeline | Deployment | 2 | — |
| T-16 | PBI-22 | Adicionar scan de imagem Docker (Trivy) | Deployment | 2 | T-13 |
| T-17 | PBI-23 | Testes de autenticação e perfis (401/403) | Testing | 4 | T-12 |
| T-18 | PBI-23 | Testes de pesquisa: sucesso, 400 e 404 | Testing | 4 | T-05, T-12 |
| T-19 | PBI-23 | Publicar relatório de testes e cobertura no pipeline | Deployment | 2 | T-17, T-18 |
| T-20 | PBI-24 | Automatizar cenário BDD da Ranger Raptor (Gherkin + step definitions) | Testing | 5 | T-05, T-08 |
| T-21 | PBI-24 | Gerar relatório de aderência campo a campo vs. gabarito | Testing | 3 | T-20 |
| T-22 | PBI-25 | Layout da tela de resultado agrupada por categoria | Design | 4 | — |
| T-23 | PBI-25 | Integrar tela de resultado ao endpoint de especificações | Development | 4 | T-05, T-22 |
| T-24 | PBI-25 | Estados de carregando, vazio, erro e selo 'Não disponível' | Development | 2 | T-23 |
| T-25 | PBI-26 | Configurar eas.json (perfil preview) e variáveis de ambiente | Deployment | 2 | — |
| T-26 | PBI-26 | Gerar APK e testar instalação em dispositivo físico e emulador | Deployment | 3 | T-24, T-25 |
| T-27 | PBI-27 | Documentar endpoints no OpenAPI/Swagger com exemplos | Documentation | 3 | T-05, T-12 |
| T-28 | PBI-27 | Escrever README (execução, prints das telas, link do APK) | Documentation | 2 | T-26 |

**Caminho crítico:** T-01 → T-02 → T-05 → T-08 → T-20 → T-21 (validação Ranger Raptor) e T-05 → T-23 → T-24 → T-26 → T-28 (APK + README).
