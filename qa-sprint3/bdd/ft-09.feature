# language: pt
@EP-05
Funcionalidade: FT-09 Lista Padronizada de Especificações
  Como gestor de produto, quero receber as especificações sempre no mesmo formato, para comparar veículos rapidamente.

  @PBI-19 @Must
  Cenário: Formato único
    Dado pesquisas concluídas da 'Ford Ranger Raptor' e da 'Toyota Hilux GR-S'
    Quando consulto GET /pesquisas/{id}/especificacoes de cada uma
    Então ambas as respostas seguem o mesmo schema: categoria, atributo, valor, unidade, fonte, dataColeta, confianca

  @PBI-19 @Must
  Cenário: Pesquisa inexistente
    Dado um id de pesquisa que não existe
    Quando consulto as especificações
    Então recebo 404 no formato padrão de erro

  @PBI-20 @Must
  Cenário: Dado inexistente
    Dado que o atributo 'Snorkel' não foi encontrado em nenhuma fonte
    Quando consulto o resultado
    Então o atributo aparece com valor 'Não disponível' e motivo 'Não encontrado nas fontes consultadas'
