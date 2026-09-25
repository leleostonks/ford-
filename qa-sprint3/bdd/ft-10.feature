# language: pt
@EP-05
Funcionalidade: FT-10 Comparação, Exportação e Histórico
  Como gestor de produto, quero comparar veículos lado a lado e exportar os dados, para apoiar decisões de preço e pacote de equipamentos.

  @PBI-30 @Should
  Cenário: Comparação
    Dado as pesquisas da Ranger Raptor e da Hilux GR-S
    Quando solicito a comparação
    Então vejo uma tabela com os mesmos atributos e as diferenças destacadas

  @PBI-32 @Should
  Cenário: Exportação CSV
    Dado uma pesquisa concluída
    Quando solicito exportação em CSV
    Então recebo um arquivo com os mesmos campos do schema padrão

  @PBI-33 @Could
  Cenário: Histórico
    Dado que realizei 5 pesquisas
    Quando acesso o histórico
    Então vejo as 5 pesquisas ordenadas da mais recente para a mais antiga
