# language: pt
@EP-07
Funcionalidade: FT-13 Validação com Ford Ranger Raptor
  Como Ford (cliente do desafio), quero validar a solução com a Ranger Raptor, para confirmar que ela opera corretamente.

  @PBI-10 @Must
  Cenário: Gabarito completo
    Dado o slide de especificações da Ranger Raptor fornecido pela Ford
    Quando o gabarito JSON é criado
    Então contém todos os atributos do slide com valor e unidade padronizados

  @PBI-24 @Must
  Cenário: Validação oficial
    Dado o gabarito da Ford Ranger Raptor
    Quando executo a pesquisa com todos os atributos do slide
    Então 100% das especificações retornadas conferem com o gabarito em valor e unidade

  @PBI-24 @Must
  Cenário: Formato consistente
    Dado o resultado da Ranger Raptor
    Quando valido contra o schema v1
    Então a validação passa sem erros
