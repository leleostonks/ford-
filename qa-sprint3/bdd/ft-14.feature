# language: pt
@EP-07
Funcionalidade: FT-14 Testes Automatizados e Observabilidade
  Como equipe, quero testes automatizados e monitoramento, para detectar falhas rapidamente e garantir qualidade contínua.

  @PBI-23 @Must
  Cenário: Suíte executada no pipeline
    Dado a suíte de testes de API
    Quando o pipeline é executado
    Então os cenários de sucesso, erro (400/404) e não autorizado (401/403) são executados e o relatório é publicado

  @PBI-34 @Should
  Cenário: Falha de login registrada
    Dado 5 tentativas de login falhas em 1 minuto
    Quando consulto o dashboard
    Então vejo o alerta de possível força bruta com usuário e IP

  @PBI-37 @Could
  Cenário: Custo monitorado
    Dado chamadas ao LLM durante o dia
    Quando consulto o dashboard
    Então vejo tokens consumidos, custo estimado e latência p95
