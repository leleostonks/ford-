# language: pt
@EP-03
Funcionalidade: FT-05 Identificação do Veículo
  Como analista, quero informar Marca, Modelo e Versão de forma simples, para identificar exatamente o veículo concorrente.

  @PBI-06 @Must
  Cenário: Entrada válida
    Dado que estou autenticado
    Quando envio POST /pesquisas com marca 'Ford', modelo 'Ranger' e versão 'Raptor'
    Então recebo 201 Created com o id da pesquisa e status 'EM_PROCESSAMENTO'

  @PBI-06 @Must
  Cenário: Campo obrigatório ausente
    Dado que estou autenticado
    Quando envio a pesquisa sem a versão
    Então recebo 400 Bad Request informando que 'versao' é obrigatória

  @PBI-07 @Should
  Cenário: Sugestão de modelo
    Dado que selecionei a marca 'Toyota'
    Quando digito 'Hil'
    Então vejo a sugestão 'Hilux'
