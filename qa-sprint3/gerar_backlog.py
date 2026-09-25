# -*- coding: utf-8 -*-
"""
Gera o backlog do Challenge Ford (Desafio 01 - Inteligencia Competitiva Automotiva)
para importacao no Azure DevOps (processo Scrum).

Saidas:
  backlog_azure_devops.csv  -> Boards > Work items > Import from CSV
  PLANO_DO_PROJETO.md       -> documento com todo o plano (backlog, release plan, sprint atual)

Uso: python gerar_backlog.py ["Nome do Projeto no Azure"]
"""
import csv
import sys

PROJECT = sys.argv[1] if len(sys.argv) > 1 else "Ford Challenge"

SPRINTS = {
    1: ("Sprint 1", "16/02/2026", "12/04/2026", "Fundação, catálogo de atributos e entrada da pesquisa"),
    2: ("Sprint 2", "13/04/2026", "07/06/2026", "Autenticação, coleta de fontes e extração com IA"),
    3: ("Sprint 3", "03/08/2026", "27/09/2026", "Saída padronizada, validação Ranger Raptor, APK e segurança"),
    4: ("Sprint 4", "28/09/2026", "11/10/2026", "Comparação, exportação, observabilidade e vídeo pitch"),
    0: ("Backlog futuro", "-", "-", "Itens opcionais não planejados nesta release"),
}
SPRINT_ATUAL = 3

BV = {"Must": 100, "Should": 50, "Could": 20}
PRIORIDADE_TXT = {
    "Must": "Obrigatório (Must have) — requisito do desafio Ford, sem ele a solução não é aceita",
    "Should": "Necessário (Should have) — agrega valor relevante ao negócio, mas não bloqueia a aceitação",
    "Could": "Opcional (Could have) — melhoria desejável, entra se houver capacidade",
}

DOD_PADRAO = ("Código revisado via Pull Request; testes automatizados passando no pipeline; "
              "sem vulnerabilidades críticas/altas no SAST/SCA; critérios de aceite BDD validados pelo PO; "
              "documentação (Swagger/README) atualizada; deploy no ambiente de homologação.")

# ---------------------------------------------------------------------------
# EPICOS
# ---------------------------------------------------------------------------
EPICS = [
    dict(code="EP-01", title="Fundação da Plataforma e Catálogo de Atributos",
         desc="Estabelecer a arquitetura (camadas: App Mobile, API Gateway/Backend, Serviço de Coleta, Motor de Extração IA, Banco de Dados), "
              "o ambiente de desenvolvimento, o pipeline CI e o catálogo padrão de atributos técnicos que garante que toda saída tenha o mesmo formato.",
         ac="Arquitetura documentada (diagrama de componentes alinhado ao modelo ArchiMate da sprint anterior); pipeline CI executando em todo PR; "
            "catálogo com ao menos 40 atributos técnicos padronizados com unidade e categoria."),
    dict(code="EP-02", title="Segurança e Gestão de Acesso",
         desc="Garantir que apenas usuários autenticados e autorizados utilizem a ferramenta, com perfis distintos, API protegida e segurança integrada ao pipeline (DevSecOps).",
         ac="Autenticação JWT com expiração; perfis Analista, Gestor e Administrador; endpoints públicos e protegidos; pipeline com SAST, SCA e secret scanning."),
    dict(code="EP-03", title="Pesquisa de Veículos Concorrentes (Entrada)",
         desc="Permitir que o analista informe, a partir de uma entrada simples, Marca, Modelo e Versão do veículo e defina livremente a lista de equipamentos/atributos técnicos que deseja pesquisar.",
         ac="Usuário consegue iniciar uma pesquisa informando Marca, Modelo, Versão e uma lista livre de atributos; entradas inválidas são rejeitadas com mensagem clara."),
    dict(code="EP-04", title="Coleta e Extração Inteligente de Dados Técnicos",
         desc="Coletar dados técnicos da concorrência em fontes oficiais e secundárias e extrair as especificações com um motor híbrido (IA/LLM + regras), normalizando unidades.",
         ac="Para um veículo válido, o motor retorna os atributos solicitados com valor, unidade normalizada e fonte (URL e data de coleta)."),
    dict(code="EP-05", title="Saída Padronizada de Especificações Técnicas",
         desc="Gerar uma lista de especificações técnicas sempre no mesmo formato, independente do veículo, com campos claros, organizados e comparáveis, explicitando dados inexistentes.",
         ac="Saída segue um schema único e versionado; atributos sem informação aparecem como 'Não disponível'; é possível comparar e exportar resultados."),
    dict(code="EP-06", title="Aplicativo Mobile",
         desc="Aplicativo React Native (Expo) com identidade visual consistente, que permite pesquisar, visualizar e comparar especificações, publicado como APK.",
         ac="APK instala e executa em dispositivo físico/emulador; todos os fluxos (login, pesquisa, resultado, comparação) funcionam sem erros."),
    dict(code="EP-07", title="Qualidade, Validação e Observabilidade",
         desc="Assegurar que a solução está operando corretamente, usando a Ford Ranger Raptor como caso de validação oficial, testes automatizados e monitoramento.",
         ac="100% das especificações do slide da Ranger Raptor entregues corretamente pelo teste de aceitação automatizado; logs estruturados e dashboard de monitoramento ativos."),
    dict(code="EP-08", title="Entrega Final e Pitch",
         desc="Consolidar documentação e apresentar a solução final à Ford e à FIAP em vídeo pitch/técnico de até 6 minutos.",
         ac="README e Swagger completos; vídeo com pitch + parte técnica, até 6 minutos, entregue em todas as disciplinas."),
]

# ---------------------------------------------------------------------------
# FEATURES
# ---------------------------------------------------------------------------
FEATURES = [
    dict(code="FT-01", epic="EP-01", title="Arquitetura e Ambiente de Desenvolvimento",
         story="Como equipe de desenvolvimento, quero uma arquitetura definida e um ambiente com CI, para construir a solução de forma organizada e segura.",
         ac="Dado o repositório do projeto, quando um PR é aberto, então o pipeline compila, executa testes e reporta o resultado."),
    dict(code="FT-02", epic="EP-01", title="Catálogo Padrão de Atributos Técnicos",
         story="Como analista de inteligência competitiva, quero um catálogo padrão de atributos técnicos, para que todas as pesquisas sejam comparáveis entre si.",
         ac="Dado o catálogo, quando consulto um atributo, então vejo nome padrão, categoria, unidade e sinônimos."),
    dict(code="FT-03", epic="EP-02", title="Autenticação e Perfis de Acesso",
         story="Como administrador, quero controlar quem acessa a ferramenta e com qual perfil, para proteger dados estratégicos da Ford.",
         ac="Dado um usuário sem token, quando acessa um recurso protegido, então recebe 401; dado um perfil sem permissão, então recebe 403."),
    dict(code="FT-04", epic="EP-02", title="Proteção da API e DevSecOps",
         story="Como responsável por segurança, quero a API protegida contra abuso e o código verificado automaticamente, para reduzir riscos antes do deploy.",
         ac="Dado um volume de requisições acima do limite, então a API responde 429; dado um PR com segredo exposto, então o pipeline falha."),
    dict(code="FT-05", epic="EP-03", title="Identificação do Veículo",
         story="Como analista, quero informar Marca, Modelo e Versão de forma simples, para identificar exatamente o veículo concorrente.",
         ac="Dado que informo Marca, Modelo e Versão válidos, quando confirmo, então a pesquisa é criada com status 'Em processamento'."),
    dict(code="FT-06", epic="EP-03", title="Lista Livre de Atributos",
         story="Como analista, quero definir livremente a lista de equipamentos/atributos que desejo pesquisar, para focar no que importa para cada análise.",
         ac="Dado que adiciono atributos do catálogo ou texto livre, quando envio a pesquisa, então todos os atributos informados aparecem no resultado."),
    dict(code="FT-07", epic="EP-04", title="Coleta de Fontes de Dados",
         story="Como analista, quero que a ferramenta busque dados em fontes confiáveis, para não precisar pesquisar manualmente em vários sites.",
         ac="Dado um veículo válido, quando a coleta é executada, então o conteúdo das fontes é armazenado com URL e data de coleta."),
    dict(code="FT-08", epic="EP-04", title="Extração de Especificações com IA",
         story="Como analista, quero que a IA extraia e normalize as especificações das fontes, para receber dados precisos e organizados.",
         ac="Dado o conteúdo coletado, quando o motor processa, então cada atributo solicitado recebe valor, unidade padrão, fonte e grau de confiança."),
    dict(code="FT-09", epic="EP-05", title="Lista Padronizada de Especificações",
         story="Como gestor de produto, quero receber as especificações sempre no mesmo formato, para comparar veículos rapidamente.",
         ac="Dadas duas pesquisas de veículos diferentes, quando visualizo os resultados, então ambos têm exatamente os mesmos campos na mesma ordem."),
    dict(code="FT-10", epic="EP-05", title="Comparação, Exportação e Histórico",
         story="Como gestor de produto, quero comparar veículos lado a lado e exportar os dados, para apoiar decisões de preço e pacote de equipamentos.",
         ac="Dado dois ou mais resultados, quando comparo, então vejo uma tabela única com as diferenças destacadas e posso exportá-la."),
    dict(code="FT-11", epic="EP-06", title="Telas do Aplicativo",
         story="Como usuário mobile, quero telas consistentes e intuitivas, para pesquisar e consultar especificações em qualquer lugar.",
         ac="Dado o app instalado, quando navego pelas telas, então cores, tipografia e componentes seguem o design system."),
    dict(code="FT-12", epic="EP-06", title="Publicação do Aplicativo",
         story="Como avaliador, quero instalar o app via APK, para testar a solução em um dispositivo real.",
         ac="Dado o APK gerado pelo EAS Build, quando instalo em um Android, então o app abre e executa todos os fluxos sem erros."),
    dict(code="FT-13", epic="EP-07", title="Validação com Ford Ranger Raptor",
         story="Como Ford (cliente do desafio), quero validar a solução com a Ranger Raptor, para confirmar que ela opera corretamente.",
         ac="Dado o gabarito da Ranger Raptor, quando a pesquisa é executada, então todas as especificações do slide são entregues corretamente."),
    dict(code="FT-14", epic="EP-07", title="Testes Automatizados e Observabilidade",
         story="Como equipe, quero testes automatizados e monitoramento, para detectar falhas rapidamente e garantir qualidade contínua.",
         ac="Dado um deploy, quando os testes rodam, então o relatório é publicado no pipeline; dado um erro em produção, então ele aparece no dashboard."),
    dict(code="FT-15", epic="EP-08", title="Documentação e Apresentação Final",
         story="Como professores e Ford, queremos documentação clara e um pitch objetivo, para entender e avaliar a solução.",
         ac="Dado o repositório, quando sigo o README, então consigo executar a solução; o vídeo tem no máximo 6 minutos."),
]

# ---------------------------------------------------------------------------
# PRODUCT BACKLOG ITEMS  (ordem da lista = ordem de implementacao no backlog)
# pri: Must/Should/Could | eff: Planning Poker (Fibonacci) | sprint: 1..4 (0 = futuro)
# ---------------------------------------------------------------------------
PBIS = [
    # ------------------------------- SPRINT 1 -------------------------------
    dict(code="PBI-01", ft="FT-01", sprint=1, pri="Must", eff=3, deps=[], tag="Arquitetura",
         title="Definir arquitetura da solução e diagrama de componentes",
         story="Como equipe, quero a arquitetura documentada com componentes e responsabilidades, para orientar o desenvolvimento.",
         gherkin=[("Diagrama publicado", "que a arquitetura foi modelada no ArchiMate", "a equipe consulta a Wiki do projeto",
                   "encontra o diagrama com App Mobile, API, Serviço de Coleta, Motor IA e Banco de Dados e o fluxo de autenticação")],
         dod="Diagrama e descrição de responsabilidades publicados na Wiki do Azure DevOps."),
    dict(code="PBI-02", ft="FT-01", sprint=1, pri="Must", eff=5, deps=["PBI-01"], tag="DevOps",
         title="Configurar repositório, estratégia de branches e pipeline CI",
         story="Como desenvolvedor, quero um pipeline que valide cada Pull Request, para evitar que código quebrado chegue à main.",
         gherkin=[("PR válido", "um Pull Request com código compilável e testes passando", "o pipeline é executado", "o PR fica apto para merge"),
                  ("PR com falha", "um Pull Request com teste falhando", "o pipeline é executado", "o merge é bloqueado pela branch policy")],
         dod="Branch policy ativa na main exigindo build verde e 1 revisor."),
    dict(code="PBI-03", ft="FT-01", sprint=1, pri="Must", eff=5, deps=["PBI-01"], tag="Dados",
         title="Modelar banco de dados (veículos, atributos, pesquisas, especificações, fontes)",
         story="Como desenvolvedor, quero um modelo de dados normalizado, para armazenar pesquisas e especificações de forma consistente.",
         gherkin=[("Migração aplicada", "o script de migração do banco", "é executado em um ambiente limpo",
                   "as tabelas Veiculo, Atributo, Pesquisa, Especificacao e Fonte são criadas com suas chaves e relacionamentos")],
         dod="Diagrama ER publicado e migrações versionadas no repositório."),
    dict(code="PBI-04", ft="FT-02", sprint=1, pri="Must", eff=5, deps=["PBI-03"], tag="Dados",
         title="Cadastrar catálogo padrão de atributos técnicos com unidade e categoria",
         story="Como analista, quero um catálogo com atributos padrão (motor, potência, torque, transmissão, tração, dimensões, capacidades, segurança, conforto), para padronizar a saída.",
         gherkin=[("Consulta ao catálogo", "que o catálogo foi carregado", "consulto GET /atributos",
                   "recebo ao menos 40 atributos, cada um com nome padrão, categoria e unidade"),
                  ("Atributo duplicado", "que o atributo 'Potência máxima' já existe", "um administrador tenta cadastrá-lo novamente", "recebo 409 Conflict")],
         dod="Seed do catálogo versionado e coberto por teste."),
    dict(code="PBI-05", ft="FT-02", sprint=1, pri="Should", eff=3, deps=["PBI-04"], tag="Dados",
         title="Mapear sinônimos de atributos (ex.: 'cv', 'potência', 'hp')",
         story="Como analista, quero que termos diferentes para o mesmo atributo sejam reconhecidos, para não perder dados por variação de nomenclatura.",
         gherkin=[("Sinônimo reconhecido", "que 'hp' é sinônimo de 'Potência máxima'", "informo o atributo 'hp' na pesquisa",
                   "o resultado apresenta o campo padrão 'Potência máxima'")],
         dod="Tabela de sinônimos com ao menos 3 variações para os 20 atributos mais usados."),
    dict(code="PBI-06", ft="FT-05", sprint=1, pri="Must", eff=5, deps=["PBI-03"], tag="API",
         title="Informar Marca, Modelo e Versão para iniciar a pesquisa",
         story="Como analista, quero informar Marca, Modelo e Versão, para identificar o veículo concorrente a ser pesquisado.",
         gherkin=[("Entrada válida", "que estou autenticado", "envio POST /pesquisas com marca 'Ford', modelo 'Ranger' e versão 'Raptor'",
                   "recebo 201 Created com o id da pesquisa e status 'EM_PROCESSAMENTO'"),
                  ("Campo obrigatório ausente", "que estou autenticado", "envio a pesquisa sem a versão",
                   "recebo 400 Bad Request informando que 'versao' é obrigatória")],
         dod="Endpoint documentado no Swagger com exemplos."),
    dict(code="PBI-07", ft="FT-05", sprint=1, pri="Should", eff=3, deps=["PBI-06"], tag="API",
         title="Sugerir (autocompletar) marcas, modelos e versões",
         story="Como analista, quero sugestões enquanto digito, para evitar erros de digitação na identificação do veículo.",
         gherkin=[("Sugestão de modelo", "que selecionei a marca 'Toyota'", "digito 'Hil'", "vejo a sugestão 'Hilux'")],
         dod="Resposta de sugestões em menos de 500 ms (p95)."),
    dict(code="PBI-08", ft="FT-06", sprint=1, pri="Must", eff=5, deps=["PBI-04", "PBI-06"], tag="API",
         title="Definir livremente a lista de atributos a pesquisar",
         story="Como analista, quero escolher atributos do catálogo ou digitar atributos livres, para montar a pesquisa conforme minha necessidade.",
         gherkin=[("Atributos do catálogo e livres", "que informei o veículo", "adiciono 'Torque máximo' do catálogo e o texto livre 'Snorkel'",
                   "a pesquisa é registrada com os 2 atributos"),
                  ("Lista vazia", "que informei o veículo", "envio a pesquisa sem nenhum atributo", "recebo 400 com a mensagem 'Informe ao menos um atributo'")],
         dod="Limite máximo de 100 atributos por pesquisa validado."),
    dict(code="PBI-09", ft="FT-11", sprint=1, pri="Must", eff=3, deps=[], tag="Mobile",
         title="Criar design system do app (cores, tipografia, componentes)",
         story="Como usuário, quero uma identidade visual consistente, para ter uma experiência profissional em todas as telas.",
         gherkin=[("Componentes reutilizáveis", "a biblioteca de componentes do app", "uma nova tela é criada",
                   "ela usa apenas tokens de cor, tipografia e componentes do design system")],
         dod="Design system documentado no Figma e implementado como tema no app."),
    dict(code="PBI-10", ft="FT-13", sprint=1, pri="Must", eff=3, deps=["PBI-04"], tag="QA",
         title="Criar gabarito de referência (massa de teste) da Ford Ranger Raptor",
         story="Como QA, quero o gabarito oficial das especificações da Ranger Raptor, para validar automaticamente a saída da solução.",
         gherkin=[("Gabarito completo", "o slide de especificações da Ranger Raptor fornecido pela Ford", "o gabarito JSON é criado",
                   "contém todos os atributos do slide com valor e unidade padronizados")],
         dod="Gabarito revisado por 2 membros e versionado em /tests/fixtures."),
    # ------------------------------- SPRINT 2 -------------------------------
    dict(code="PBI-11", ft="FT-03", sprint=2, pri="Must", eff=8, deps=["PBI-02", "PBI-03"], tag="Segurança",
         title="Cadastro e login com geração e validação de JWT",
         story="Como usuário, quero me autenticar com e-mail e senha, para acessar a ferramenta de forma segura.",
         gherkin=[("Login válido", "um usuário cadastrado", "envio POST /auth/login com credenciais corretas", "recebo 200 com um JWT que expira em 1 hora"),
                  ("Credenciais inválidas", "um usuário cadastrado", "envio senha incorreta", "recebo 401 sem indicar qual campo está errado"),
                  ("Token expirado", "um JWT expirado", "acesso GET /pesquisas", "recebo 401 'Token expirado'")],
         dod="Senhas com hash BCrypt; segredo JWT em variável de ambiente/cofre."),
    dict(code="PBI-12", ft="FT-03", sprint=2, pri="Must", eff=5, deps=["PBI-11"], tag="Segurança",
         title="Controle de acesso por perfil (Analista, Gestor, Administrador)",
         story="Como administrador, quero atribuir perfis aos usuários, para que cada um acesse apenas o que lhe é permitido.",
         gherkin=[("Analista cria pesquisa", "um usuário com perfil Analista", "cria uma pesquisa", "recebe 201"),
                  ("Analista tenta gerenciar catálogo", "um usuário com perfil Analista", "envia POST /atributos", "recebe 403 Forbidden"),
                  ("Admin gerencia usuários", "um usuário com perfil Administrador", "altera o perfil de outro usuário", "recebe 200")],
         dod="Matriz de permissões publicada na Wiki."),
    dict(code="PBI-13", ft="FT-07", sprint=2, pri="Must", eff=8, deps=["PBI-03", "PBI-06"], tag="Coleta",
         title="Conector de coleta em fichas técnicas oficiais das montadoras",
         story="Como analista, quero que a ferramenta colete a ficha técnica no site oficial da montadora, para ter dados de fonte primária.",
         gherkin=[("Coleta com sucesso", "uma pesquisa da 'Ford Ranger Raptor'", "o conector é executado", "o conteúdo da ficha técnica é salvo com URL e data de coleta"),
                  ("Fonte indisponível", "que o site da montadora está fora do ar", "o conector é executado", "a falha é registrada e a pesquisa segue para fontes alternativas")],
         dod="Respeita robots.txt e timeout de 15 s por fonte."),
    dict(code="PBI-14", ft="FT-07", sprint=2, pri="Should", eff=3, deps=["PBI-13"], tag="Coleta",
         title="Cache de fontes coletadas com data e URL",
         story="Como analista, quero reaproveitar coletas recentes, para obter respostas mais rápidas e reduzir custo.",
         gherkin=[("Cache válido", "uma coleta do mesmo veículo feita há menos de 7 dias", "faço nova pesquisa", "o conteúdo em cache é utilizado"),
                  ("Cache expirado", "uma coleta com mais de 7 dias", "faço nova pesquisa", "uma nova coleta é realizada")],
         dod="TTL configurável por variável de ambiente."),
    dict(code="PBI-15", ft="FT-08", sprint=2, pri="Must", eff=13, deps=["PBI-04", "PBI-13"], tag="IA",
         title="Extrair especificações do conteúdo coletado com motor híbrido (LLM + regras)",
         story="Como analista, quero que a IA identifique no texto das fontes os valores dos atributos solicitados, para não ter que ler fichas técnicas manualmente.",
         gherkin=[("Extração de atributo existente", "o conteúdo coletado da Ranger Raptor", "o motor extrai 'Potência máxima'", "retorna o valor e a unidade encontrados na fonte"),
                  ("Atributo não encontrado", "um atributo que não consta em nenhuma fonte", "o motor processa", "retorna o atributo sem valor, sem inventar dados")],
         dod="Precisão ≥ 90% no gabarito da Ranger Raptor; prompt e regras versionados."),
    dict(code="PBI-16", ft="FT-11", sprint=2, pri="Must", eff=3, deps=["PBI-09", "PBI-11"], tag="Mobile",
         title="Telas de login e cadastro no app",
         story="Como usuário mobile, quero entrar no app com minhas credenciais, para acessar minhas pesquisas.",
         gherkin=[("Login no app", "que estou na tela de login", "informo credenciais válidas", "sou direcionado à tela inicial e o token fica em armazenamento seguro"),
                  ("Erro de login", "que estou na tela de login", "informo senha errada", "vejo a mensagem 'E-mail ou senha inválidos'")],
         dod="Token armazenado com expo-secure-store."),
    dict(code="PBI-17", ft="FT-11", sprint=2, pri="Must", eff=5, deps=["PBI-06", "PBI-08", "PBI-09"], tag="Mobile",
         title="Tela de nova pesquisa (veículo + lista de atributos)",
         story="Como analista mobile, quero informar o veículo e os atributos em uma única tela, para iniciar a pesquisa rapidamente.",
         gherkin=[("Pesquisa enviada", "que preenchi Marca, Modelo, Versão e 3 atributos", "toco em 'Pesquisar'", "vejo a confirmação e o status 'Em processamento'"),
                  ("Campos obrigatórios", "que não preenchi a Versão", "toco em 'Pesquisar'", "o campo Versão é destacado com mensagem de obrigatoriedade")],
         dod="Tela validada em Android físico e emulador."),
    # ------------------------------- SPRINT 3 -------------------------------
    dict(code="PBI-18", ft="FT-08", sprint=3, pri="Must", eff=5, deps=["PBI-15"], tag="IA",
         title="Normalizar unidades e formatos das especificações",
         story="Como gestor, quero que valores venham em unidades padrão (cv, kgfm, mm, L, kg), para comparar veículos sem conversões manuais.",
         gherkin=[("Conversão de unidade", "que a fonte informa '292 kW'", "o normalizador processa o atributo 'Potência máxima'", "o valor exibido é '397 cv'"),
                  ("Valor já padronizado", "que a fonte informa '397 cv'", "o normalizador processa", "o valor permanece '397 cv'")],
         dod="Cobertura de testes unitários ≥ 90% no módulo normalizador."),
    dict(code="PBI-19", ft="FT-09", sprint=3, pri="Must", eff=8, deps=["PBI-08", "PBI-18"], tag="API",
         title="Gerar lista de especificações em formato único (schema padronizado)",
         story="Como gestor de produto, quero que a lista de especificações tenha sempre os mesmos campos e ordem, para comparar qualquer veículo.",
         gherkin=[("Formato único", "pesquisas concluídas da 'Ford Ranger Raptor' e da 'Toyota Hilux GR-S'", "consulto GET /pesquisas/{id}/especificacoes de cada uma",
                   "ambas as respostas seguem o mesmo schema: categoria, atributo, valor, unidade, fonte, dataColeta, confianca"),
                  ("Pesquisa inexistente", "um id de pesquisa que não existe", "consulto as especificações", "recebo 404 no formato padrão de erro")],
         dod="Schema JSON versionado (v1) e teste de contrato no pipeline."),
    dict(code="PBI-20", ft="FT-09", sprint=3, pri="Must", eff=2, deps=["PBI-19"], tag="API",
         title="Explicitar 'Não disponível' quando a informação não existir",
         story="Como analista, quero ver claramente quando um dado não foi encontrado, para não confundir ausência de informação com erro.",
         gherkin=[("Dado inexistente", "que o atributo 'Snorkel' não foi encontrado em nenhuma fonte", "consulto o resultado",
                   "o atributo aparece com valor 'Não disponível' e motivo 'Não encontrado nas fontes consultadas'")],
         dod="Nenhum campo do schema retorna nulo ou vazio sem o status explícito."),
    dict(code="PBI-21", ft="FT-04", sprint=3, pri="Must", eff=3, deps=["PBI-11"], tag="Segurança",
         title="Hardening da API: rate limit, validação de entrada e padronização de erros",
         story="Como responsável por segurança, quero limitar abusos e validar entradas, para proteger a API contra ataques e dados maliciosos.",
         gherkin=[("Rate limit", "um usuário que fez 60 requisições no último minuto", "faz a 61ª requisição", "recebe 429 Too Many Requests"),
                  ("Entrada maliciosa", "um campo 'modelo' com script '<script>'", "envio a pesquisa", "recebo 400 com erro no formato padrão (RFC 7807)")],
         dod="Erros padronizados em todos os endpoints."),
    dict(code="PBI-22", ft="FT-04", sprint=3, pri="Should", eff=5, deps=["PBI-02"], tag="Segurança",
         title="Pipeline DevSecOps (SAST, SCA, secret scanning e container scan)",
         story="Como equipe, quero verificações de segurança automáticas no pipeline, para detectar vulnerabilidades antes do deploy.",
         gherkin=[("Segredo exposto", "um commit contendo uma chave de API", "o pipeline executa o Gitleaks", "o build falha e aponta o arquivo"),
                  ("Dependência vulnerável", "uma dependência com CVE crítica", "o pipeline executa o SCA", "o build falha com o relatório da vulnerabilidade")],
         dod="Relatórios de SAST/SCA/Trivy publicados como artefatos do pipeline."),
    dict(code="PBI-23", ft="FT-14", sprint=3, pri="Must", eff=5, deps=["PBI-12", "PBI-19"], tag="QA",
         title="Testes automatizados da API (sucesso, erro e acesso não autorizado)",
         story="Como QA, quero testes automatizados dos principais comportamentos da API, para garantir que regressões sejam detectadas.",
         gherkin=[("Suíte executada no pipeline", "a suíte de testes de API", "o pipeline é executado",
                   "os cenários de sucesso, erro (400/404) e não autorizado (401/403) são executados e o relatório é publicado")],
         dod="Cobertura de linhas ≥ 70% na API; relatório JUnit publicado na aba Tests do pipeline."),
    dict(code="PBI-24", ft="FT-13", sprint=3, pri="Must", eff=5, deps=["PBI-10", "PBI-20"], tag="QA",
         title="Teste de aceitação automatizado com a Ford Ranger Raptor",
         story="Como Ford, quero que a solução seja validada automaticamente com a Ranger Raptor, para confirmar que opera corretamente.",
         gherkin=[("Validação oficial", "o gabarito da Ford Ranger Raptor", "executo a pesquisa com todos os atributos do slide",
                   "100% das especificações retornadas conferem com o gabarito em valor e unidade"),
                  ("Formato consistente", "o resultado da Ranger Raptor", "valido contra o schema v1", "a validação passa sem erros")],
         dod="Cenário BDD executando no pipeline e relatório de aderência campo a campo anexado."),
    dict(code="PBI-25", ft="FT-11", sprint=3, pri="Must", eff=5, deps=["PBI-17", "PBI-19"], tag="Mobile",
         title="Tela de resultado com a lista padronizada de especificações",
         story="Como analista mobile, quero visualizar as especificações agrupadas por categoria, para consultar os dados de forma clara.",
         gherkin=[("Resultado exibido", "uma pesquisa concluída", "abro a tela de resultado", "vejo os atributos agrupados por categoria com valor, unidade e fonte"),
                  ("Dado indisponível", "um atributo sem informação", "abro a tela de resultado", "vejo o selo 'Não disponível' em cinza")],
         dod="Estados de carregando, vazio e erro implementados."),
    dict(code="PBI-26", ft="FT-12", sprint=3, pri="Must", eff=3, deps=["PBI-25"], tag="Mobile",
         title="Gerar build APK via Expo EAS Build",
         story="Como avaliador, quero um APK instalável, para testar o app em um dispositivo Android.",
         gherkin=[("APK instalável", "o perfil 'preview' configurado no eas.json", "executo o EAS Build", "o APK é gerado, instala e abre sem erros em dispositivo físico")],
         dod="Link do APK e evidências (prints) no README."),
    dict(code="PBI-27", ft="FT-15", sprint=3, pri="Must", eff=3, deps=["PBI-19", "PBI-21"], tag="Documentação",
         title="Documentação da API (OpenAPI/Swagger) e README de execução",
         story="Como desenvolvedor e avaliador, quero a API documentada e instruções de execução, para usar e avaliar a solução.",
         gherkin=[("Swagger disponível", "a API em execução", "acesso /swagger-ui", "vejo todos os endpoints com exemplos, códigos de status e esquema de autenticação"),
                  ("README executável", "um ambiente limpo", "sigo o README", "consigo subir API e app localmente")],
         dod="README revisado por um membro que não participou da escrita."),
    # ------------------------------- SPRINT 4 -------------------------------
    dict(code="PBI-28", ft="FT-07", sprint=4, pri="Should", eff=5, deps=["PBI-13"], tag="Coleta",
         title="Conector para fontes secundárias (portais automotivos especializados)",
         story="Como analista, quero complementar a ficha oficial com portais especializados, para reduzir campos 'Não disponível'.",
         gherkin=[("Complemento de dados", "um atributo ausente na ficha oficial", "o conector secundário encontra o valor", "o atributo é preenchido com a fonte secundária identificada")],
         dod="Fonte primária sempre tem precedência sobre a secundária."),
    dict(code="PBI-29", ft="FT-08", sprint=4, pri="Should", eff=5, deps=["PBI-15"], tag="IA",
         title="Indicador de confiança e rastreabilidade de fonte por atributo",
         story="Como gestor, quero saber a confiança e a origem de cada dado, para decidir se posso usá-lo em análises estratégicas.",
         gherkin=[("Fontes divergentes", "duas fontes com valores diferentes para 'Torque máximo'", "o motor consolida o resultado", "o atributo exibe confiança 'Média' e as duas fontes")],
         dod="Regra de cálculo da confiança documentada."),
    dict(code="PBI-30", ft="FT-10", sprint=4, pri="Should", eff=8, deps=["PBI-19"], tag="API",
         title="Comparar dois ou mais veículos lado a lado",
         story="Como gestor de produto, quero comparar veículos concorrentes lado a lado, para entender o posicionamento em pacotes de equipamentos.",
         gherkin=[("Comparação", "as pesquisas da Ranger Raptor e da Hilux GR-S", "solicito a comparação", "vejo uma tabela com os mesmos atributos e as diferenças destacadas")],
         dod="Comparação de até 4 veículos."),
    dict(code="PBI-31", ft="FT-11", sprint=4, pri="Should", eff=5, deps=["PBI-25", "PBI-30"], tag="Mobile",
         title="Tela de comparação de veículos no app",
         story="Como analista mobile, quero comparar veículos no app, para apoiar reuniões de negócio.",
         gherkin=[("Comparar no app", "que selecionei 2 pesquisas concluídas", "toco em 'Comparar'", "vejo a tabela comparativa com rolagem horizontal")],
         dod="Validada em telas de 5\" a 6,7\"."),
    dict(code="PBI-32", ft="FT-10", sprint=4, pri="Should", eff=5, deps=["PBI-19"], tag="API",
         title="Exportar especificações em CSV, XLSX e PDF",
         story="Como gestor, quero exportar os resultados, para compartilhar com outras áreas da Ford.",
         gherkin=[("Exportação CSV", "uma pesquisa concluída", "solicito exportação em CSV", "recebo um arquivo com os mesmos campos do schema padrão")],
         dod="Arquivos exportados preservam 'Não disponível'."),
    dict(code="PBI-33", ft="FT-10", sprint=4, pri="Could", eff=3, deps=["PBI-12", "PBI-19"], tag="API",
         title="Histórico de pesquisas do usuário",
         story="Como analista, quero consultar minhas pesquisas anteriores, para reutilizar resultados sem refazer a coleta.",
         gherkin=[("Histórico", "que realizei 5 pesquisas", "acesso o histórico", "vejo as 5 pesquisas ordenadas da mais recente para a mais antiga")],
         dod="Paginação implementada."),
    dict(code="PBI-34", ft="FT-14", sprint=4, pri="Should", eff=5, deps=["PBI-11"], tag="Observabilidade",
         title="Logs estruturados, métricas e dashboard de monitoramento",
         story="Como equipe de operação, quero logs e dashboards, para detectar e responder a incidentes rapidamente.",
         gherkin=[("Falha de login registrada", "5 tentativas de login falhas em 1 minuto", "consulto o dashboard", "vejo o alerta de possível força bruta com usuário e IP")],
         dod="Dashboard no Grafana/Azure Monitor com latência, erros e taxa de sucesso da extração."),
    dict(code="PBI-35", ft="FT-15", sprint=4, pri="Must", eff=5, deps=["PBI-24", "PBI-26"], tag="Pitch",
         title="Produzir vídeo pitch/técnico da solução final (até 6 min)",
         story="Como equipe, queremos apresentar o problema, a solução e a parte técnica em vídeo, para a avaliação final da Ford e FIAP.",
         gherkin=[("Vídeo entregue", "o roteiro aprovado pela equipe", "o vídeo é finalizado", "tem até 6 minutos, contém pitch e demonstração técnica e o link é entregue em todas as disciplinas")],
         dod="Link do vídeo publicado no Teams de todas as disciplinas."),
    # ------------------------------ FUTURO ----------------------------------
    dict(code="PBI-36", ft="FT-06", sprint=0, pri="Could", eff=3, deps=["PBI-08"], tag="API",
         title="Salvar modelos (templates) de listas de atributos",
         story="Como analista, quero salvar listas de atributos usadas com frequência, para agilizar novas pesquisas.",
         gherkin=[("Template salvo", "uma lista com 10 atributos", "salvo como 'Picapes médias'", "consigo reutilizá-la em uma nova pesquisa")],
         dod="Templates privados por usuário."),
    dict(code="PBI-37", ft="FT-14", sprint=0, pri="Could", eff=3, deps=["PBI-15", "PBI-34"], tag="Observabilidade",
         title="Monitorar custo e latência das chamadas ao modelo de IA",
         story="Como gestor técnico, quero acompanhar custo e tempo do modelo de IA, para controlar o orçamento da solução.",
         gherkin=[("Custo monitorado", "chamadas ao LLM durante o dia", "consulto o dashboard", "vejo tokens consumidos, custo estimado e latência p95")],
         dod="Alerta quando o custo diário ultrapassar o limite configurado."),
]

# ---------------------------------------------------------------------------
# TAREFAS DA SPRINT ATUAL (Sprint 3)  - esforco em horas (Remaining Work)
# ---------------------------------------------------------------------------
TASKS = [
    dict(code="T-01", pbi="PBI-18", h=4, act="Development", deps=[], title="Criar tabela de conversão de unidades (kW→cv, Nm→kgfm, pol→mm)"),
    dict(code="T-02", pbi="PBI-18", h=6, act="Development", deps=["T-01"], title="Implementar serviço normalizador de valores e unidades"),
    dict(code="T-03", pbi="PBI-18", h=3, act="Testing", deps=["T-02"], title="Testes unitários do normalizador (casos de borda e unidades desconhecidas)"),
    dict(code="T-04", pbi="PBI-19", h=3, act="Design", deps=[], title="Definir schema JSON v1 da lista de especificações"),
    dict(code="T-05", pbi="PBI-19", h=6, act="Development", deps=["T-04", "T-02"], title="Implementar endpoint GET /pesquisas/{id}/especificacoes"),
    dict(code="T-06", pbi="PBI-19", h=3, act="Development", deps=["T-05"], title="Agrupar e ordenar atributos por categoria do catálogo"),
    dict(code="T-07", pbi="PBI-19", h=3, act="Testing", deps=["T-05"], title="Teste de contrato do schema v1 no pipeline"),
    dict(code="T-08", pbi="PBI-20", h=2, act="Development", deps=["T-05"], title="Regra de preenchimento 'Não disponível' com motivo"),
    dict(code="T-09", pbi="PBI-20", h=2, act="Testing", deps=["T-08"], title="Testes de atributos inexistentes e texto livre não reconhecido"),
    dict(code="T-10", pbi="PBI-21", h=3, act="Development", deps=[], title="Implementar rate limit por usuário/IP (60 req/min)"),
    dict(code="T-11", pbi="PBI-21", h=3, act="Development", deps=[], title="Validação e sanitização de entrada em todos os DTOs"),
    dict(code="T-12", pbi="PBI-21", h=2, act="Development", deps=["T-11"], title="Padronizar respostas de erro (RFC 7807 Problem Details)"),
    dict(code="T-13", pbi="PBI-22", h=3, act="Deployment", deps=[], title="Adicionar SAST (Semgrep/SonarCloud) ao pipeline"),
    dict(code="T-14", pbi="PBI-22", h=2, act="Deployment", deps=[], title="Habilitar SCA (Dependabot/Snyk) nas dependências da API e do app"),
    dict(code="T-15", pbi="PBI-22", h=2, act="Deployment", deps=[], title="Adicionar secret scanning (Gitleaks) ao pipeline"),
    dict(code="T-16", pbi="PBI-22", h=2, act="Deployment", deps=["T-13"], title="Adicionar scan de imagem Docker (Trivy)"),
    dict(code="T-17", pbi="PBI-23", h=4, act="Testing", deps=["T-12"], title="Testes de autenticação e perfis (401/403)"),
    dict(code="T-18", pbi="PBI-23", h=4, act="Testing", deps=["T-05", "T-12"], title="Testes de pesquisa: sucesso, 400 e 404"),
    dict(code="T-19", pbi="PBI-23", h=2, act="Deployment", deps=["T-17", "T-18"], title="Publicar relatório de testes e cobertura no pipeline"),
    dict(code="T-20", pbi="PBI-24", h=5, act="Testing", deps=["T-05", "T-08"], title="Automatizar cenário BDD da Ranger Raptor (Gherkin + step definitions)"),
    dict(code="T-21", pbi="PBI-24", h=3, act="Testing", deps=["T-20"], title="Gerar relatório de aderência campo a campo vs. gabarito"),
    dict(code="T-22", pbi="PBI-25", h=4, act="Design", deps=[], title="Layout da tela de resultado agrupada por categoria"),
    dict(code="T-23", pbi="PBI-25", h=4, act="Development", deps=["T-05", "T-22"], title="Integrar tela de resultado ao endpoint de especificações"),
    dict(code="T-24", pbi="PBI-25", h=2, act="Development", deps=["T-23"], title="Estados de carregando, vazio, erro e selo 'Não disponível'"),
    dict(code="T-25", pbi="PBI-26", h=2, act="Deployment", deps=[], title="Configurar eas.json (perfil preview) e variáveis de ambiente"),
    dict(code="T-26", pbi="PBI-26", h=3, act="Deployment", deps=["T-24", "T-25"], title="Gerar APK e testar instalação em dispositivo físico e emulador"),
    dict(code="T-27", pbi="PBI-27", h=3, act="Documentation", deps=["T-05", "T-12"], title="Documentar endpoints no OpenAPI/Swagger com exemplos"),
    dict(code="T-28", pbi="PBI-27", h=2, act="Documentation", deps=["T-26"], title="Escrever README (execução, prints das telas, link do APK)"),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
pbi_by = {p["code"]: p for p in PBIS}
task_by = {t["code"]: t for t in TASKS}


def sprint_path(n):
    return f"{PROJECT}\\{SPRINTS[n][0]}" if n else PROJECT


def label(code):
    if code in pbi_by:
        return f"{code} {pbi_by[code]['title']}"
    if code in task_by:
        return f"{code} {task_by[code]['title']}"
    return code


def successors(code):
    return [p["code"] for p in PBIS if code in p["deps"]]


def gherkin_html(p):
    out = [f"<b>Funcionalidade:</b> {p['title']}"]
    for nome, dado, quando, entao in p["gherkin"]:
        out.append(f"<br><br><b>Cenário:</b> {nome}<br><b>Dado</b> {dado}<br><b>Quando</b> {quando}<br><b>Então</b> {entao}")
    out.append(f"<br><br><b>Critério de pronto (DoD):</b> {DOD_PADRAO} <b>Específico:</b> {p['dod']}")
    return "".join(out)


def gherkin_md(p):
    lines = [f"Funcionalidade: {p['title']}"]
    for nome, dado, quando, entao in p["gherkin"]:
        lines += ["", f"  Cenário: {nome}", f"    Dado {dado}", f"    Quando {quando}", f"    Então {entao}"]
    return "\n".join(lines)


def pbi_desc_html(p):
    deps = ", ".join(label(d) for d in p["deps"]) or "Nenhuma"
    suc = ", ".join(successors(p["code"])) or "Nenhum"
    return (f"<b>História de usuário:</b> {p['story']}<br><br>"
            f"<b>Prioridade:</b> {PRIORIDADE_TXT[p['pri']]}<br>"
            f"<b>Esforço (Planning Poker):</b> {p['eff']} pontos<br>"
            f"<b>Depende de (predecessores):</b> {deps}<br>"
            f"<b>Bloqueia (sucessores):</b> {suc}<br>"
            f"<b>Release:</b> {SPRINTS[p['sprint']][0]}")


def main():
    # ---------------------------------------------------------------------------
    # CSV
    # ---------------------------------------------------------------------------
    HEADER = ["ID", "Work Item Type", "Title 1", "Title 2", "Title 3", "Title 4", "Description",
              "Acceptance Criteria", "Business Value", "Effort", "Remaining Work", "Activity",
              "Iteration Path", "Tags"]


    def row(**kw):
        return [kw.get(h, "") for h in HEADER]


    rows = []
    for ep in EPICS:
        rows.append(row(**{"Work Item Type": "Epic", "Title 1": f"[{ep['code']}] {ep['title']}",
                           "Description": ep["desc"], "Acceptance Criteria": ep["ac"],
                           "Iteration Path": PROJECT, "Tags": "Épico"}))
        for ft in [f for f in FEATURES if f["epic"] == ep["code"]]:
            pbis = [p for p in PBIS if p["ft"] == ft["code"]]
            pri = "Must" if any(p["pri"] == "Must" for p in pbis) else "Should"
            rows.append(row(**{"Work Item Type": "Feature", "Title 2": f"[{ft['code']}] {ft['title']}",
                               "Description": f"<b>História:</b> {ft['story']}<br><b>Prioridade:</b> {PRIORIDADE_TXT[pri]}<br><b>Esforço total:</b> {sum(p['eff'] for p in pbis)} pontos",
                               "Acceptance Criteria": ft["ac"], "Business Value": BV[pri],
                               "Effort": sum(p["eff"] for p in pbis), "Iteration Path": PROJECT, "Tags": pri}))
            for p in pbis:
                rows.append(row(**{"Work Item Type": "Product Backlog Item", "Title 3": f"[{p['code']}] {p['title']}",
                                   "Description": pbi_desc_html(p), "Acceptance Criteria": gherkin_html(p),
                                   "Business Value": BV[p["pri"]], "Effort": p["eff"],
                                   "Iteration Path": sprint_path(p["sprint"]), "Tags": f"{p['pri']}; {p['tag']}"}))
                for t in [t for t in TASKS if t["pbi"] == p["code"]]:
                    tdeps = ", ".join(label(d) for d in t["deps"]) or "Nenhuma"
                    rows.append(row(**{"Work Item Type": "Task", "Title 4": f"[{t['code']}] {t['title']}",
                                       "Description": f"<b>Esforço estimado:</b> {t['h']} h<br><b>Depende de:</b> {tdeps}<br><b>PBI:</b> {label(p['code'])}",
                                       "Remaining Work": t["h"], "Activity": t["act"],
                                       "Iteration Path": sprint_path(SPRINT_ATUAL), "Tags": f"Sprint3; {p['tag']}"}))

    with open("backlog_azure_devops.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        w.writerow(HEADER)
        w.writerows(rows)

    # ---------------------------------------------------------------------------
    # MARKDOWN
    # ---------------------------------------------------------------------------
    md = []
    A = md.append
    A("# Plano do Projeto — Ford Challenge 2026 · Desafio 01: Inteligência Competitiva Automotiva")
    A("")
    A("**Disciplina:** Testing, Compliance and Quality Assurance — Sprint 3  ")
    A("**Ferramenta:** Azure DevOps (processo Scrum)  ")
    A(f"**Projeto no Azure:** `{PROJECT}`")
    A("")
    A("## 1. Visão do produto")
    A("")
    A("Ferramenta que recebe **Marca, Modelo, Versão** e uma **lista livre de atributos técnicos** e devolve uma "
      "**lista padronizada de especificações** (sempre no mesmo formato, com campos comparáveis e 'Não disponível' "
      "explícito quando o dado não existir). A validação oficial é feita com a **Ford Ranger Raptor**.")
    A("")
    A("**Arquitetura (resumo, alinhada ao modelo ArchiMate):** App Mobile (React Native/Expo) → API REST (JWT, perfis) → "
      "Serviço de Coleta (fontes oficiais e secundárias, cache) → Motor de Extração IA (LLM + regras + normalizador) → "
      "Banco de Dados (catálogo de atributos, pesquisas, especificações, fontes). Pipeline DevSecOps e observabilidade transversais.")
    A("")
    A("**Personas:** Analista de Inteligência Competitiva · Gestor de Produto · Administrador.")
    A("")
    A("## 2. Critérios de priorização e estimativa")
    A("")
    A("| Prioridade | Significado | Business Value |")
    A("|---|---|---|")
    for k in ["Must", "Should", "Could"]:
        A(f"| **{k}** | {PRIORIDADE_TXT[k]} | {BV[k]} |")
    A("")
    A("**Esforço:** Planning Poker com sequência de Fibonacci (1, 2, 3, 5, 8, 13). Referência: 3 pontos = endpoint CRUD simples com testes.")
    A("")
    A("**Definition of Ready (DoR):** história no formato *Como/Quero/Para*, critérios BDD escritos, dependências identificadas, estimada pelo time.  ")
    A(f"**Definition of Done (DoD) padrão:** {DOD_PADRAO}")
    A("")
    A("## 3. Backlog do produto (Épicos → Features → PBIs)")
    A("")
    for ep in EPICS:
        A(f"### {ep['code']} — {ep['title']}")
        A("")
        A(f"{ep['desc']}  ")
        A(f"**Critério de aceite do épico:** {ep['ac']}")
        A("")
        for ft in [f for f in FEATURES if f["epic"] == ep["code"]]:
            A(f"#### {ft['code']} — {ft['title']}")
            A("")
            A(f"*{ft['story']}*  ")
            A(f"**Critério de aceite:** {ft['ac']}")
            A("")
            for p in [p for p in PBIS if p["ft"] == ft["code"]]:
                deps = ", ".join(p["deps"]) or "—"
                A(f"**{p['code']} — {p['title']}**  ")
                A(f"{p['story']}  ")
                A(f"Prioridade: **{p['pri']}** · Esforço: **{p['eff']} pts** · Depende de: {deps} · Release: **{SPRINTS[p['sprint']][0]}**")
                A("")
                A("```gherkin")
                A(gherkin_md(p))
                A("```")
                A(f"Pronto quando: DoD padrão + {p['dod']}")
                A("")

    A("## 4. Backlog ordenado (sequência de implementação)")
    A("")
    A("| # | PBI | Título | Prioridade | Esforço | Depende de | Sprint |")
    A("|---|---|---|---|---|---|---|")
    for i, p in enumerate(PBIS, 1):
        A(f"| {i} | {p['code']} | {p['title']} | {p['pri']} | {p['eff']} | {', '.join(p['deps']) or '—'} | {SPRINTS[p['sprint']][0]} |")
    A("")

    A("## 5. Release plan (roadmap de entregas)")
    A("")
    A("| Sprint | Período | Objetivo | PBIs | Pontos |")
    A("|---|---|---|---|---|")
    for n in [1, 2, 3, 4, 0]:
        items = [p for p in PBIS if p["sprint"] == n]
        A(f"| **{SPRINTS[n][0]}** | {SPRINTS[n][1]} – {SPRINTS[n][2]} | {SPRINTS[n][3]} | {', '.join(p['code'] for p in items)} | **{sum(p['eff'] for p in items)}** |")
    total = sum(p["eff"] for p in PBIS if p["sprint"])
    A("")
    A(f"Total planejado: **{total} pontos** em 4 sprints (média de **{total/4:.0f} pontos/sprint**, variação máxima de ±5 pontos). "
      "Itens *Could* sem capacidade ficam no Backlog futuro.")
    A("")

    A("## 6. Sprint atual — Sprint 3 (03/08/2026 – 27/09/2026)")
    A("")
    A("**Meta da sprint:** entregar a lista padronizada de especificações validada com a Ford Ranger Raptor, o APK do app e a API protegida com pipeline DevSecOps.")
    A("")
    sp3 = [p for p in PBIS if p["sprint"] == 3]
    A(f"**Capacidade comprometida:** {sum(p['eff'] for p in sp3)} pontos · {sum(t['h'] for t in TASKS)} horas de tarefas.")
    A("")
    A("| Tarefa | PBI | Descrição | Atividade | Esforço (h) | Depende de |")
    A("|---|---|---|---|---|---|")
    for t in TASKS:
        A(f"| {t['code']} | {t['pbi']} | {t['title']} | {t['act']} | {t['h']} | {', '.join(t['deps']) or '—'} |")
    A("")
    A("**Caminho crítico:** T-01 → T-02 → T-05 → T-08 → T-20 → T-21 (validação Ranger Raptor) e T-05 → T-23 → T-24 → T-26 → T-28 (APK + README).")
    A("")

    with open("PLANO_DO_PROJETO.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print(f"CSV: {len(rows)} work items  |  pontos planejados: {total}")
    for n in [1, 2, 3, 4, 0]:
        print(SPRINTS[n][0], sum(p["eff"] for p in PBIS if p["sprint"] == n))


if __name__ == "__main__":
    main()
