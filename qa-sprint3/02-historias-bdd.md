# 2. Histórias de Usuário, Critérios de Aceite e Pronto (BDD)

Histórias no formato **Como / Quero / Para**, com critérios de aceite em **Gherkin** (Dado / Quando / Então). Os cenários executáveis estão em [`bdd/`](bdd/).

**Personas:** Analista de Inteligência Competitiva · Gestor de Produto · Administrador.

## Definition of Ready (DoR)

- História escrita no formato Como / Quero / Para
- Critérios de aceite em Gherkin
- Dependências identificadas
- Estimada pelo time (Planning Poker)
- Cabe em uma sprint

## Definition of Done (DoD)

- Código revisado via Pull Request
- testes automatizados passando no pipeline
- sem vulnerabilidades críticas/altas no SAST/SCA
- critérios de aceite BDD validados pelo PO
- documentação (Swagger/README) atualizada
- deploy no ambiente de homologação

---

## EP-01 · Fundação da Plataforma e Catálogo de Atributos

**Descrição:** Estabelecer a arquitetura (camadas: App Mobile, API Gateway/Backend, Serviço de Coleta, Motor de Extração IA, Banco de Dados), o ambiente de desenvolvimento, o pipeline CI e o catálogo padrão de atributos técnicos que garante que toda saída tenha o mesmo formato.

**Critério de aceite do épico:** Arquitetura documentada (diagrama de componentes alinhado ao modelo ArchiMate da sprint anterior); pipeline CI executando em todo PR; catálogo com ao menos 40 atributos técnicos padronizados com unidade e categoria.

### FT-01 · Arquitetura e Ambiente de Desenvolvimento

> Como equipe de desenvolvimento, quero uma arquitetura definida e um ambiente com CI, para construir a solução de forma organizada e segura.

**Critério de aceite:** Dado o repositório do projeto, quando um PR é aberto, então o pipeline compila, executa testes e reporta o resultado.

#### PBI-01 · Definir arquitetura da solução e diagrama de componentes

> Como equipe, quero a arquitetura documentada com componentes e responsabilidades, para orientar o desenvolvimento.

```gherkin
Cenário: Diagrama publicado
  Dado que a arquitetura foi modelada no ArchiMate
  Quando a equipe consulta a Wiki do projeto
  Então encontra o diagrama com App Mobile, API, Serviço de Coleta, Motor IA e Banco de Dados e o fluxo de autenticação
```

**Pronto quando:** DoD + Diagrama e descrição de responsabilidades publicados na Wiki do Azure DevOps.

#### PBI-02 · Configurar repositório, estratégia de branches e pipeline CI

> Como desenvolvedor, quero um pipeline que valide cada Pull Request, para evitar que código quebrado chegue à main.

```gherkin
Cenário: PR válido
  Dado um Pull Request com código compilável e testes passando
  Quando o pipeline é executado
  Então o PR fica apto para merge

Cenário: PR com falha
  Dado um Pull Request com teste falhando
  Quando o pipeline é executado
  Então o merge é bloqueado pela branch policy
```

**Pronto quando:** DoD + Branch policy ativa na main exigindo build verde e 1 revisor.

#### PBI-03 · Modelar banco de dados (veículos, atributos, pesquisas, especificações, fontes)

> Como desenvolvedor, quero um modelo de dados normalizado, para armazenar pesquisas e especificações de forma consistente.

```gherkin
Cenário: Migração aplicada
  Dado o script de migração do banco
  Quando é executado em um ambiente limpo
  Então as tabelas Veiculo, Atributo, Pesquisa, Especificacao e Fonte são criadas com suas chaves e relacionamentos
```

**Pronto quando:** DoD + Diagrama ER publicado e migrações versionadas no repositório.

### FT-02 · Catálogo Padrão de Atributos Técnicos

> Como analista de inteligência competitiva, quero um catálogo padrão de atributos técnicos, para que todas as pesquisas sejam comparáveis entre si.

**Critério de aceite:** Dado o catálogo, quando consulto um atributo, então vejo nome padrão, categoria, unidade e sinônimos.

#### PBI-04 · Cadastrar catálogo padrão de atributos técnicos com unidade e categoria

> Como analista, quero um catálogo com atributos padrão (motor, potência, torque, transmissão, tração, dimensões, capacidades, segurança, conforto), para padronizar a saída.

```gherkin
Cenário: Consulta ao catálogo
  Dado que o catálogo foi carregado
  Quando consulto GET /atributos
  Então recebo ao menos 40 atributos, cada um com nome padrão, categoria e unidade

Cenário: Atributo duplicado
  Dado que o atributo 'Potência máxima' já existe
  Quando um administrador tenta cadastrá-lo novamente
  Então recebo 409 Conflict
```

**Pronto quando:** DoD + Seed do catálogo versionado e coberto por teste.

#### PBI-05 · Mapear sinônimos de atributos (ex.: 'cv', 'potência', 'hp')

> Como analista, quero que termos diferentes para o mesmo atributo sejam reconhecidos, para não perder dados por variação de nomenclatura.

```gherkin
Cenário: Sinônimo reconhecido
  Dado que 'hp' é sinônimo de 'Potência máxima'
  Quando informo o atributo 'hp' na pesquisa
  Então o resultado apresenta o campo padrão 'Potência máxima'
```

**Pronto quando:** DoD + Tabela de sinônimos com ao menos 3 variações para os 20 atributos mais usados.

---

## EP-02 · Segurança e Gestão de Acesso

**Descrição:** Garantir que apenas usuários autenticados e autorizados utilizem a ferramenta, com perfis distintos, API protegida e segurança integrada ao pipeline (DevSecOps).

**Critério de aceite do épico:** Autenticação JWT com expiração; perfis Analista, Gestor e Administrador; endpoints públicos e protegidos; pipeline com SAST, SCA e secret scanning.

### FT-03 · Autenticação e Perfis de Acesso

> Como administrador, quero controlar quem acessa a ferramenta e com qual perfil, para proteger dados estratégicos da Ford.

**Critério de aceite:** Dado um usuário sem token, quando acessa um recurso protegido, então recebe 401; dado um perfil sem permissão, então recebe 403.

#### PBI-11 · Cadastro e login com geração e validação de JWT

> Como usuário, quero me autenticar com e-mail e senha, para acessar a ferramenta de forma segura.

```gherkin
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

**Pronto quando:** DoD + Senhas com hash BCrypt; segredo JWT em variável de ambiente/cofre.

#### PBI-12 · Controle de acesso por perfil (Analista, Gestor, Administrador)

> Como administrador, quero atribuir perfis aos usuários, para que cada um acesse apenas o que lhe é permitido.

```gherkin
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

**Pronto quando:** DoD + Matriz de permissões publicada na Wiki.

### FT-04 · Proteção da API e DevSecOps

> Como responsável por segurança, quero a API protegida contra abuso e o código verificado automaticamente, para reduzir riscos antes do deploy.

**Critério de aceite:** Dado um volume de requisições acima do limite, então a API responde 429; dado um PR com segredo exposto, então o pipeline falha.

#### PBI-21 · Hardening da API: rate limit, validação de entrada e padronização de erros

> Como responsável por segurança, quero limitar abusos e validar entradas, para proteger a API contra ataques e dados maliciosos.

```gherkin
Cenário: Rate limit
  Dado um usuário que fez 60 requisições no último minuto
  Quando faz a 61ª requisição
  Então recebe 429 Too Many Requests

Cenário: Entrada maliciosa
  Dado um campo 'modelo' com script '<script>'
  Quando envio a pesquisa
  Então recebo 400 com erro no formato padrão (RFC 7807)
```

**Pronto quando:** DoD + Erros padronizados em todos os endpoints.

#### PBI-22 · Pipeline DevSecOps (SAST, SCA, secret scanning e container scan)

> Como equipe, quero verificações de segurança automáticas no pipeline, para detectar vulnerabilidades antes do deploy.

```gherkin
Cenário: Segredo exposto
  Dado um commit contendo uma chave de API
  Quando o pipeline executa o Gitleaks
  Então o build falha e aponta o arquivo

Cenário: Dependência vulnerável
  Dado uma dependência com CVE crítica
  Quando o pipeline executa o SCA
  Então o build falha com o relatório da vulnerabilidade
```

**Pronto quando:** DoD + Relatórios de SAST/SCA/Trivy publicados como artefatos do pipeline.

---

## EP-03 · Pesquisa de Veículos Concorrentes (Entrada)

**Descrição:** Permitir que o analista informe, a partir de uma entrada simples, Marca, Modelo e Versão do veículo e defina livremente a lista de equipamentos/atributos técnicos que deseja pesquisar.

**Critério de aceite do épico:** Usuário consegue iniciar uma pesquisa informando Marca, Modelo, Versão e uma lista livre de atributos; entradas inválidas são rejeitadas com mensagem clara.

### FT-05 · Identificação do Veículo

> Como analista, quero informar Marca, Modelo e Versão de forma simples, para identificar exatamente o veículo concorrente.

**Critério de aceite:** Dado que informo Marca, Modelo e Versão válidos, quando confirmo, então a pesquisa é criada com status 'Em processamento'.

#### PBI-06 · Informar Marca, Modelo e Versão para iniciar a pesquisa

> Como analista, quero informar Marca, Modelo e Versão, para identificar o veículo concorrente a ser pesquisado.

```gherkin
Cenário: Entrada válida
  Dado que estou autenticado
  Quando envio POST /pesquisas com marca 'Ford', modelo 'Ranger' e versão 'Raptor'
  Então recebo 201 Created com o id da pesquisa e status 'EM_PROCESSAMENTO'

Cenário: Campo obrigatório ausente
  Dado que estou autenticado
  Quando envio a pesquisa sem a versão
  Então recebo 400 Bad Request informando que 'versao' é obrigatória
```

**Pronto quando:** DoD + Endpoint documentado no Swagger com exemplos.

#### PBI-07 · Sugerir (autocompletar) marcas, modelos e versões

> Como analista, quero sugestões enquanto digito, para evitar erros de digitação na identificação do veículo.

```gherkin
Cenário: Sugestão de modelo
  Dado que selecionei a marca 'Toyota'
  Quando digito 'Hil'
  Então vejo a sugestão 'Hilux'
```

**Pronto quando:** DoD + Resposta de sugestões em menos de 500 ms (p95).

### FT-06 · Lista Livre de Atributos

> Como analista, quero definir livremente a lista de equipamentos/atributos que desejo pesquisar, para focar no que importa para cada análise.

**Critério de aceite:** Dado que adiciono atributos do catálogo ou texto livre, quando envio a pesquisa, então todos os atributos informados aparecem no resultado.

#### PBI-08 · Definir livremente a lista de atributos a pesquisar

> Como analista, quero escolher atributos do catálogo ou digitar atributos livres, para montar a pesquisa conforme minha necessidade.

```gherkin
Cenário: Atributos do catálogo e livres
  Dado que informei o veículo
  Quando adiciono 'Torque máximo' do catálogo e o texto livre 'Snorkel'
  Então a pesquisa é registrada com os 2 atributos

Cenário: Lista vazia
  Dado que informei o veículo
  Quando envio a pesquisa sem nenhum atributo
  Então recebo 400 com a mensagem 'Informe ao menos um atributo'
```

**Pronto quando:** DoD + Limite máximo de 100 atributos por pesquisa validado.

#### PBI-36 · Salvar modelos (templates) de listas de atributos

> Como analista, quero salvar listas de atributos usadas com frequência, para agilizar novas pesquisas.

```gherkin
Cenário: Template salvo
  Dado uma lista com 10 atributos
  Quando salvo como 'Picapes médias'
  Então consigo reutilizá-la em uma nova pesquisa
```

**Pronto quando:** DoD + Templates privados por usuário.

---

## EP-04 · Coleta e Extração Inteligente de Dados Técnicos

**Descrição:** Coletar dados técnicos da concorrência em fontes oficiais e secundárias e extrair as especificações com um motor híbrido (IA/LLM + regras), normalizando unidades.

**Critério de aceite do épico:** Para um veículo válido, o motor retorna os atributos solicitados com valor, unidade normalizada e fonte (URL e data de coleta).

### FT-07 · Coleta de Fontes de Dados

> Como analista, quero que a ferramenta busque dados em fontes confiáveis, para não precisar pesquisar manualmente em vários sites.

**Critério de aceite:** Dado um veículo válido, quando a coleta é executada, então o conteúdo das fontes é armazenado com URL e data de coleta.

#### PBI-13 · Conector de coleta em fichas técnicas oficiais das montadoras

> Como analista, quero que a ferramenta colete a ficha técnica no site oficial da montadora, para ter dados de fonte primária.

```gherkin
Cenário: Coleta com sucesso
  Dado uma pesquisa da 'Ford Ranger Raptor'
  Quando o conector é executado
  Então o conteúdo da ficha técnica é salvo com URL e data de coleta

Cenário: Fonte indisponível
  Dado que o site da montadora está fora do ar
  Quando o conector é executado
  Então a falha é registrada e a pesquisa segue para fontes alternativas
```

**Pronto quando:** DoD + Respeita robots.txt e timeout de 15 s por fonte.

#### PBI-14 · Cache de fontes coletadas com data e URL

> Como analista, quero reaproveitar coletas recentes, para obter respostas mais rápidas e reduzir custo.

```gherkin
Cenário: Cache válido
  Dado uma coleta do mesmo veículo feita há menos de 7 dias
  Quando faço nova pesquisa
  Então o conteúdo em cache é utilizado

Cenário: Cache expirado
  Dado uma coleta com mais de 7 dias
  Quando faço nova pesquisa
  Então uma nova coleta é realizada
```

**Pronto quando:** DoD + TTL configurável por variável de ambiente.

#### PBI-28 · Conector para fontes secundárias (portais automotivos especializados)

> Como analista, quero complementar a ficha oficial com portais especializados, para reduzir campos 'Não disponível'.

```gherkin
Cenário: Complemento de dados
  Dado um atributo ausente na ficha oficial
  Quando o conector secundário encontra o valor
  Então o atributo é preenchido com a fonte secundária identificada
```

**Pronto quando:** DoD + Fonte primária sempre tem precedência sobre a secundária.

### FT-08 · Extração de Especificações com IA

> Como analista, quero que a IA extraia e normalize as especificações das fontes, para receber dados precisos e organizados.

**Critério de aceite:** Dado o conteúdo coletado, quando o motor processa, então cada atributo solicitado recebe valor, unidade padrão, fonte e grau de confiança.

#### PBI-15 · Extrair especificações do conteúdo coletado com motor híbrido (LLM + regras)

> Como analista, quero que a IA identifique no texto das fontes os valores dos atributos solicitados, para não ter que ler fichas técnicas manualmente.

```gherkin
Cenário: Extração de atributo existente
  Dado o conteúdo coletado da Ranger Raptor
  Quando o motor extrai 'Potência máxima'
  Então retorna o valor e a unidade encontrados na fonte

Cenário: Atributo não encontrado
  Dado um atributo que não consta em nenhuma fonte
  Quando o motor processa
  Então retorna o atributo sem valor, sem inventar dados
```

**Pronto quando:** DoD + Precisão ≥ 90% no gabarito da Ranger Raptor; prompt e regras versionados.

#### PBI-18 · Normalizar unidades e formatos das especificações

> Como gestor, quero que valores venham em unidades padrão (cv, kgfm, mm, L, kg), para comparar veículos sem conversões manuais.

```gherkin
Cenário: Conversão de unidade
  Dado que a fonte informa '292 kW'
  Quando o normalizador processa o atributo 'Potência máxima'
  Então o valor exibido é '397 cv'

Cenário: Valor já padronizado
  Dado que a fonte informa '397 cv'
  Quando o normalizador processa
  Então o valor permanece '397 cv'
```

**Pronto quando:** DoD + Cobertura de testes unitários ≥ 90% no módulo normalizador.

#### PBI-29 · Indicador de confiança e rastreabilidade de fonte por atributo

> Como gestor, quero saber a confiança e a origem de cada dado, para decidir se posso usá-lo em análises estratégicas.

```gherkin
Cenário: Fontes divergentes
  Dado duas fontes com valores diferentes para 'Torque máximo'
  Quando o motor consolida o resultado
  Então o atributo exibe confiança 'Média' e as duas fontes
```

**Pronto quando:** DoD + Regra de cálculo da confiança documentada.

---

## EP-05 · Saída Padronizada de Especificações Técnicas

**Descrição:** Gerar uma lista de especificações técnicas sempre no mesmo formato, independente do veículo, com campos claros, organizados e comparáveis, explicitando dados inexistentes.

**Critério de aceite do épico:** Saída segue um schema único e versionado; atributos sem informação aparecem como 'Não disponível'; é possível comparar e exportar resultados.

### FT-09 · Lista Padronizada de Especificações

> Como gestor de produto, quero receber as especificações sempre no mesmo formato, para comparar veículos rapidamente.

**Critério de aceite:** Dadas duas pesquisas de veículos diferentes, quando visualizo os resultados, então ambos têm exatamente os mesmos campos na mesma ordem.

#### PBI-19 · Gerar lista de especificações em formato único (schema padronizado)

> Como gestor de produto, quero que a lista de especificações tenha sempre os mesmos campos e ordem, para comparar qualquer veículo.

```gherkin
Cenário: Formato único
  Dado pesquisas concluídas da 'Ford Ranger Raptor' e da 'Toyota Hilux GR-S'
  Quando consulto GET /pesquisas/{id}/especificacoes de cada uma
  Então ambas as respostas seguem o mesmo schema: categoria, atributo, valor, unidade, fonte, dataColeta, confianca

Cenário: Pesquisa inexistente
  Dado um id de pesquisa que não existe
  Quando consulto as especificações
  Então recebo 404 no formato padrão de erro
```

**Pronto quando:** DoD + Schema JSON versionado (v1) e teste de contrato no pipeline.

#### PBI-20 · Explicitar 'Não disponível' quando a informação não existir

> Como analista, quero ver claramente quando um dado não foi encontrado, para não confundir ausência de informação com erro.

```gherkin
Cenário: Dado inexistente
  Dado que o atributo 'Snorkel' não foi encontrado em nenhuma fonte
  Quando consulto o resultado
  Então o atributo aparece com valor 'Não disponível' e motivo 'Não encontrado nas fontes consultadas'
```

**Pronto quando:** DoD + Nenhum campo do schema retorna nulo ou vazio sem o status explícito.

### FT-10 · Comparação, Exportação e Histórico

> Como gestor de produto, quero comparar veículos lado a lado e exportar os dados, para apoiar decisões de preço e pacote de equipamentos.

**Critério de aceite:** Dado dois ou mais resultados, quando comparo, então vejo uma tabela única com as diferenças destacadas e posso exportá-la.

#### PBI-30 · Comparar dois ou mais veículos lado a lado

> Como gestor de produto, quero comparar veículos concorrentes lado a lado, para entender o posicionamento em pacotes de equipamentos.

```gherkin
Cenário: Comparação
  Dado as pesquisas da Ranger Raptor e da Hilux GR-S
  Quando solicito a comparação
  Então vejo uma tabela com os mesmos atributos e as diferenças destacadas
```

**Pronto quando:** DoD + Comparação de até 4 veículos.

#### PBI-32 · Exportar especificações em CSV, XLSX e PDF

> Como gestor, quero exportar os resultados, para compartilhar com outras áreas da Ford.

```gherkin
Cenário: Exportação CSV
  Dado uma pesquisa concluída
  Quando solicito exportação em CSV
  Então recebo um arquivo com os mesmos campos do schema padrão
```

**Pronto quando:** DoD + Arquivos exportados preservam 'Não disponível'.

#### PBI-33 · Histórico de pesquisas do usuário

> Como analista, quero consultar minhas pesquisas anteriores, para reutilizar resultados sem refazer a coleta.

```gherkin
Cenário: Histórico
  Dado que realizei 5 pesquisas
  Quando acesso o histórico
  Então vejo as 5 pesquisas ordenadas da mais recente para a mais antiga
```

**Pronto quando:** DoD + Paginação implementada.

---

## EP-06 · Aplicativo Mobile

**Descrição:** Aplicativo React Native (Expo) com identidade visual consistente, que permite pesquisar, visualizar e comparar especificações, publicado como APK.

**Critério de aceite do épico:** APK instala e executa em dispositivo físico/emulador; todos os fluxos (login, pesquisa, resultado, comparação) funcionam sem erros.

### FT-11 · Telas do Aplicativo

> Como usuário mobile, quero telas consistentes e intuitivas, para pesquisar e consultar especificações em qualquer lugar.

**Critério de aceite:** Dado o app instalado, quando navego pelas telas, então cores, tipografia e componentes seguem o design system.

#### PBI-09 · Criar design system do app (cores, tipografia, componentes)

> Como usuário, quero uma identidade visual consistente, para ter uma experiência profissional em todas as telas.

```gherkin
Cenário: Componentes reutilizáveis
  Dado a biblioteca de componentes do app
  Quando uma nova tela é criada
  Então ela usa apenas tokens de cor, tipografia e componentes do design system
```

**Pronto quando:** DoD + Design system documentado no Figma e implementado como tema no app.

#### PBI-16 · Telas de login e cadastro no app

> Como usuário mobile, quero entrar no app com minhas credenciais, para acessar minhas pesquisas.

```gherkin
Cenário: Login no app
  Dado que estou na tela de login
  Quando informo credenciais válidas
  Então sou direcionado à tela inicial e o token fica em armazenamento seguro

Cenário: Erro de login
  Dado que estou na tela de login
  Quando informo senha errada
  Então vejo a mensagem 'E-mail ou senha inválidos'
```

**Pronto quando:** DoD + Token armazenado com expo-secure-store.

#### PBI-17 · Tela de nova pesquisa (veículo + lista de atributos)

> Como analista mobile, quero informar o veículo e os atributos em uma única tela, para iniciar a pesquisa rapidamente.

```gherkin
Cenário: Pesquisa enviada
  Dado que preenchi Marca, Modelo, Versão e 3 atributos
  Quando toco em 'Pesquisar'
  Então vejo a confirmação e o status 'Em processamento'

Cenário: Campos obrigatórios
  Dado que não preenchi a Versão
  Quando toco em 'Pesquisar'
  Então o campo Versão é destacado com mensagem de obrigatoriedade
```

**Pronto quando:** DoD + Tela validada em Android físico e emulador.

#### PBI-25 · Tela de resultado com a lista padronizada de especificações

> Como analista mobile, quero visualizar as especificações agrupadas por categoria, para consultar os dados de forma clara.

```gherkin
Cenário: Resultado exibido
  Dado uma pesquisa concluída
  Quando abro a tela de resultado
  Então vejo os atributos agrupados por categoria com valor, unidade e fonte

Cenário: Dado indisponível
  Dado um atributo sem informação
  Quando abro a tela de resultado
  Então vejo o selo 'Não disponível' em cinza
```

**Pronto quando:** DoD + Estados de carregando, vazio e erro implementados.

#### PBI-31 · Tela de comparação de veículos no app

> Como analista mobile, quero comparar veículos no app, para apoiar reuniões de negócio.

```gherkin
Cenário: Comparar no app
  Dado que selecionei 2 pesquisas concluídas
  Quando toco em 'Comparar'
  Então vejo a tabela comparativa com rolagem horizontal
```

**Pronto quando:** DoD + Validada em telas de 5" a 6,7".

### FT-12 · Publicação do Aplicativo

> Como avaliador, quero instalar o app via APK, para testar a solução em um dispositivo real.

**Critério de aceite:** Dado o APK gerado pelo EAS Build, quando instalo em um Android, então o app abre e executa todos os fluxos sem erros.

#### PBI-26 · Gerar build APK via Expo EAS Build

> Como avaliador, quero um APK instalável, para testar o app em um dispositivo Android.

```gherkin
Cenário: APK instalável
  Dado o perfil 'preview' configurado no eas.json
  Quando executo o EAS Build
  Então o APK é gerado, instala e abre sem erros em dispositivo físico
```

**Pronto quando:** DoD + Link do APK e evidências (prints) no README.

---

## EP-07 · Qualidade, Validação e Observabilidade

**Descrição:** Assegurar que a solução está operando corretamente, usando a Ford Ranger Raptor como caso de validação oficial, testes automatizados e monitoramento.

**Critério de aceite do épico:** 100% das especificações do slide da Ranger Raptor entregues corretamente pelo teste de aceitação automatizado; logs estruturados e dashboard de monitoramento ativos.

### FT-13 · Validação com Ford Ranger Raptor

> Como Ford (cliente do desafio), quero validar a solução com a Ranger Raptor, para confirmar que ela opera corretamente.

**Critério de aceite:** Dado o gabarito da Ranger Raptor, quando a pesquisa é executada, então todas as especificações do slide são entregues corretamente.

#### PBI-10 · Criar gabarito de referência (massa de teste) da Ford Ranger Raptor

> Como QA, quero o gabarito oficial das especificações da Ranger Raptor, para validar automaticamente a saída da solução.

```gherkin
Cenário: Gabarito completo
  Dado o slide de especificações da Ranger Raptor fornecido pela Ford
  Quando o gabarito JSON é criado
  Então contém todos os atributos do slide com valor e unidade padronizados
```

**Pronto quando:** DoD + Gabarito revisado por 2 membros e versionado em /tests/fixtures.

#### PBI-24 · Teste de aceitação automatizado com a Ford Ranger Raptor

> Como Ford, quero que a solução seja validada automaticamente com a Ranger Raptor, para confirmar que opera corretamente.

```gherkin
Cenário: Validação oficial
  Dado o gabarito da Ford Ranger Raptor
  Quando executo a pesquisa com todos os atributos do slide
  Então 100% das especificações retornadas conferem com o gabarito em valor e unidade

Cenário: Formato consistente
  Dado o resultado da Ranger Raptor
  Quando valido contra o schema v1
  Então a validação passa sem erros
```

**Pronto quando:** DoD + Cenário BDD executando no pipeline e relatório de aderência campo a campo anexado.

### FT-14 · Testes Automatizados e Observabilidade

> Como equipe, quero testes automatizados e monitoramento, para detectar falhas rapidamente e garantir qualidade contínua.

**Critério de aceite:** Dado um deploy, quando os testes rodam, então o relatório é publicado no pipeline; dado um erro em produção, então ele aparece no dashboard.

#### PBI-23 · Testes automatizados da API (sucesso, erro e acesso não autorizado)

> Como QA, quero testes automatizados dos principais comportamentos da API, para garantir que regressões sejam detectadas.

```gherkin
Cenário: Suíte executada no pipeline
  Dado a suíte de testes de API
  Quando o pipeline é executado
  Então os cenários de sucesso, erro (400/404) e não autorizado (401/403) são executados e o relatório é publicado
```

**Pronto quando:** DoD + Cobertura de linhas ≥ 70% na API; relatório JUnit publicado na aba Tests do pipeline.

#### PBI-34 · Logs estruturados, métricas e dashboard de monitoramento

> Como equipe de operação, quero logs e dashboards, para detectar e responder a incidentes rapidamente.

```gherkin
Cenário: Falha de login registrada
  Dado 5 tentativas de login falhas em 1 minuto
  Quando consulto o dashboard
  Então vejo o alerta de possível força bruta com usuário e IP
```

**Pronto quando:** DoD + Dashboard no Grafana/Azure Monitor com latência, erros e taxa de sucesso da extração.

#### PBI-37 · Monitorar custo e latência das chamadas ao modelo de IA

> Como gestor técnico, quero acompanhar custo e tempo do modelo de IA, para controlar o orçamento da solução.

```gherkin
Cenário: Custo monitorado
  Dado chamadas ao LLM durante o dia
  Quando consulto o dashboard
  Então vejo tokens consumidos, custo estimado e latência p95
```

**Pronto quando:** DoD + Alerta quando o custo diário ultrapassar o limite configurado.

---

## EP-08 · Entrega Final e Pitch

**Descrição:** Consolidar documentação e apresentar a solução final à Ford e à FIAP em vídeo pitch/técnico de até 6 minutos.

**Critério de aceite do épico:** README e Swagger completos; vídeo com pitch + parte técnica, até 6 minutos, entregue em todas as disciplinas.

### FT-15 · Documentação e Apresentação Final

> Como professores e Ford, queremos documentação clara e um pitch objetivo, para entender e avaliar a solução.

**Critério de aceite:** Dado o repositório, quando sigo o README, então consigo executar a solução; o vídeo tem no máximo 6 minutos.

#### PBI-27 · Documentação da API (OpenAPI/Swagger) e README de execução

> Como desenvolvedor e avaliador, quero a API documentada e instruções de execução, para usar e avaliar a solução.

```gherkin
Cenário: Swagger disponível
  Dado a API em execução
  Quando acesso /swagger-ui
  Então vejo todos os endpoints com exemplos, códigos de status e esquema de autenticação

Cenário: README executável
  Dado um ambiente limpo
  Quando sigo o README
  Então consigo subir API e app localmente
```

**Pronto quando:** DoD + README revisado por um membro que não participou da escrita.

#### PBI-35 · Produzir vídeo pitch/técnico da solução final (até 6 min)

> Como equipe, queremos apresentar o problema, a solução e a parte técnica em vídeo, para a avaliação final da Ford e FIAP.

```gherkin
Cenário: Vídeo entregue
  Dado o roteiro aprovado pela equipe
  Quando o vídeo é finalizado
  Então tem até 6 minutos, contém pitch e demonstração técnica e o link é entregue em todas as disciplinas
```

**Pronto quando:** DoD + Link do vídeo publicado no Teams de todas as disciplinas.

