# language: pt
@EP-04
Funcionalidade: FT-08 Extração de Especificações com IA
  Como analista, quero que a IA extraia e normalize as especificações das fontes, para receber dados precisos e organizados.

  @PBI-15 @Must
  Cenário: Extração de atributo existente
    Dado o conteúdo coletado da Ranger Raptor
    Quando o motor extrai 'Potência máxima'
    Então retorna o valor e a unidade encontrados na fonte

  @PBI-15 @Must
  Cenário: Atributo não encontrado
    Dado um atributo que não consta em nenhuma fonte
    Quando o motor processa
    Então retorna o atributo sem valor, sem inventar dados

  @PBI-18 @Must
  Cenário: Conversão de unidade
    Dado que a fonte informa '292 kW'
    Quando o normalizador processa o atributo 'Potência máxima'
    Então o valor exibido é '397 cv'

  @PBI-18 @Must
  Cenário: Valor já padronizado
    Dado que a fonte informa '397 cv'
    Quando o normalizador processa
    Então o valor permanece '397 cv'

  @PBI-29 @Should
  Cenário: Fontes divergentes
    Dado duas fontes com valores diferentes para 'Torque máximo'
    Quando o motor consolida o resultado
    Então o atributo exibe confiança 'Média' e as duas fontes
