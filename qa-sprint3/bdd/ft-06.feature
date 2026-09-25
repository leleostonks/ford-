# language: pt
@EP-03
Funcionalidade: FT-06 Lista Livre de Atributos
  Como analista, quero definir livremente a lista de equipamentos/atributos que desejo pesquisar, para focar no que importa para cada análise.

  @PBI-08 @Must
  Cenário: Atributos do catálogo e livres
    Dado que informei o veículo
    Quando adiciono 'Torque máximo' do catálogo e o texto livre 'Snorkel'
    Então a pesquisa é registrada com os 2 atributos

  @PBI-08 @Must
  Cenário: Lista vazia
    Dado que informei o veículo
    Quando envio a pesquisa sem nenhum atributo
    Então recebo 400 com a mensagem 'Informe ao menos um atributo'

  @PBI-36 @Could
  Cenário: Template salvo
    Dado uma lista com 10 atributos
    Quando salvo como 'Picapes médias'
    Então consigo reutilizá-la em uma nova pesquisa
