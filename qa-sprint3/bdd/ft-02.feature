# language: pt
@EP-01
Funcionalidade: FT-02 Catálogo Padrão de Atributos Técnicos
  Como analista de inteligência competitiva, quero um catálogo padrão de atributos técnicos, para que todas as pesquisas sejam comparáveis entre si.

  @PBI-04 @Must
  Cenário: Consulta ao catálogo
    Dado que o catálogo foi carregado
    Quando consulto GET /atributos
    Então recebo ao menos 40 atributos, cada um com nome padrão, categoria e unidade

  @PBI-04 @Must
  Cenário: Atributo duplicado
    Dado que o atributo 'Potência máxima' já existe
    Quando um administrador tenta cadastrá-lo novamente
    Então recebo 409 Conflict

  @PBI-05 @Should
  Cenário: Sinônimo reconhecido
    Dado que 'hp' é sinônimo de 'Potência máxima'
    Quando informo o atributo 'hp' na pesquisa
    Então o resultado apresenta o campo padrão 'Potência máxima'
