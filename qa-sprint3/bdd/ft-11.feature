# language: pt
@EP-06
Funcionalidade: FT-11 Telas do Aplicativo
  Como usuário mobile, quero telas consistentes e intuitivas, para pesquisar e consultar especificações em qualquer lugar.

  @PBI-09 @Must
  Cenário: Componentes reutilizáveis
    Dado a biblioteca de componentes do app
    Quando uma nova tela é criada
    Então ela usa apenas tokens de cor, tipografia e componentes do design system

  @PBI-16 @Must
  Cenário: Login no app
    Dado que estou na tela de login
    Quando informo credenciais válidas
    Então sou direcionado à tela inicial e o token fica em armazenamento seguro

  @PBI-16 @Must
  Cenário: Erro de login
    Dado que estou na tela de login
    Quando informo senha errada
    Então vejo a mensagem 'E-mail ou senha inválidos'

  @PBI-17 @Must
  Cenário: Pesquisa enviada
    Dado que preenchi Marca, Modelo, Versão e 3 atributos
    Quando toco em 'Pesquisar'
    Então vejo a confirmação e o status 'Em processamento'

  @PBI-17 @Must
  Cenário: Campos obrigatórios
    Dado que não preenchi a Versão
    Quando toco em 'Pesquisar'
    Então o campo Versão é destacado com mensagem de obrigatoriedade

  @PBI-25 @Must
  Cenário: Resultado exibido
    Dado uma pesquisa concluída
    Quando abro a tela de resultado
    Então vejo os atributos agrupados por categoria com valor, unidade e fonte

  @PBI-25 @Must
  Cenário: Dado indisponível
    Dado um atributo sem informação
    Quando abro a tela de resultado
    Então vejo o selo 'Não disponível' em cinza

  @PBI-31 @Should
  Cenário: Comparar no app
    Dado que selecionei 2 pesquisas concluídas
    Quando toco em 'Comparar'
    Então vejo a tabela comparativa com rolagem horizontal
