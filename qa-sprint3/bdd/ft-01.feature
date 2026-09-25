# language: pt
@EP-01
Funcionalidade: FT-01 Arquitetura e Ambiente de Desenvolvimento
  Como equipe de desenvolvimento, quero uma arquitetura definida e um ambiente com CI, para construir a solução de forma organizada e segura.

  @PBI-01 @Must
  Cenário: Diagrama publicado
    Dado que a arquitetura foi modelada no ArchiMate
    Quando a equipe consulta a Wiki do projeto
    Então encontra o diagrama com App Mobile, API, Serviço de Coleta, Motor IA e Banco de Dados e o fluxo de autenticação

  @PBI-02 @Must
  Cenário: PR válido
    Dado um Pull Request com código compilável e testes passando
    Quando o pipeline é executado
    Então o PR fica apto para merge

  @PBI-02 @Must
  Cenário: PR com falha
    Dado um Pull Request com teste falhando
    Quando o pipeline é executado
    Então o merge é bloqueado pela branch policy

  @PBI-03 @Must
  Cenário: Migração aplicada
    Dado o script de migração do banco
    Quando é executado em um ambiente limpo
    Então as tabelas Veiculo, Atributo, Pesquisa, Especificacao e Fonte são criadas com suas chaves e relacionamentos
