# language: pt
@EP-08
Funcionalidade: FT-15 Documentação e Apresentação Final
  Como professores e Ford, queremos documentação clara e um pitch objetivo, para entender e avaliar a solução.

  @PBI-27 @Must
  Cenário: Swagger disponível
    Dado a API em execução
    Quando acesso /swagger-ui
    Então vejo todos os endpoints com exemplos, códigos de status e esquema de autenticação

  @PBI-27 @Must
  Cenário: README executável
    Dado um ambiente limpo
    Quando sigo o README
    Então consigo subir API e app localmente

  @PBI-35 @Must
  Cenário: Vídeo entregue
    Dado o roteiro aprovado pela equipe
    Quando o vídeo é finalizado
    Então tem até 6 minutos, contém pitch e demonstração técnica e o link é entregue em todas as disciplinas
