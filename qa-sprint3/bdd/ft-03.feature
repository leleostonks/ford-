# language: pt
@EP-02
Funcionalidade: FT-03 Autenticação e Perfis de Acesso
  Como administrador, quero controlar quem acessa a ferramenta e com qual perfil, para proteger dados estratégicos da Ford.

  @PBI-11 @Must
  Cenário: Login válido
    Dado um usuário cadastrado
    Quando envio POST /auth/login com credenciais corretas
    Então recebo 200 com um JWT que expira em 1 hora

  @PBI-11 @Must
  Cenário: Credenciais inválidas
    Dado um usuário cadastrado
    Quando envio senha incorreta
    Então recebo 401 sem indicar qual campo está errado

  @PBI-11 @Must
  Cenário: Token expirado
    Dado um JWT expirado
    Quando acesso GET /pesquisas
    Então recebo 401 'Token expirado'

  @PBI-12 @Must
  Cenário: Analista cria pesquisa
    Dado um usuário com perfil Analista
    Quando cria uma pesquisa
    Então recebe 201

  @PBI-12 @Must
  Cenário: Analista tenta gerenciar catálogo
    Dado um usuário com perfil Analista
    Quando envia POST /atributos
    Então recebe 403 Forbidden

  @PBI-12 @Must
  Cenário: Admin gerencia usuários
    Dado um usuário com perfil Administrador
    Quando altera o perfil de outro usuário
    Então recebe 200
