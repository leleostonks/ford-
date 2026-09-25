# language: pt
@EP-04
Funcionalidade: FT-07 Coleta de Fontes de Dados
  Como analista, quero que a ferramenta busque dados em fontes confiáveis, para não precisar pesquisar manualmente em vários sites.

  @PBI-13 @Must
  Cenário: Coleta com sucesso
    Dado uma pesquisa da 'Ford Ranger Raptor'
    Quando o conector é executado
    Então o conteúdo da ficha técnica é salvo com URL e data de coleta

  @PBI-13 @Must
  Cenário: Fonte indisponível
    Dado que o site da montadora está fora do ar
    Quando o conector é executado
    Então a falha é registrada e a pesquisa segue para fontes alternativas

  @PBI-14 @Should
  Cenário: Cache válido
    Dado uma coleta do mesmo veículo feita há menos de 7 dias
    Quando faço nova pesquisa
    Então o conteúdo em cache é utilizado

  @PBI-14 @Should
  Cenário: Cache expirado
    Dado uma coleta com mais de 7 dias
    Quando faço nova pesquisa
    Então uma nova coleta é realizada

  @PBI-28 @Should
  Cenário: Complemento de dados
    Dado um atributo ausente na ficha oficial
    Quando o conector secundário encontra o valor
    Então o atributo é preenchido com a fonte secundária identificada
