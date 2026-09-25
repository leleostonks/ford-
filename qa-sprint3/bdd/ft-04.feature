# language: pt
@EP-02
Funcionalidade: FT-04 Proteção da API e DevSecOps
  Como responsável por segurança, quero a API protegida contra abuso e o código verificado automaticamente, para reduzir riscos antes do deploy.

  @PBI-21 @Must
  Cenário: Rate limit
    Dado um usuário que fez 60 requisições no último minuto
    Quando faz a 61ª requisição
    Então recebe 429 Too Many Requests

  @PBI-21 @Must
  Cenário: Entrada maliciosa
    Dado um campo 'modelo' com script '<script>'
    Quando envio a pesquisa
    Então recebo 400 com erro no formato padrão (RFC 7807)

  @PBI-22 @Should
  Cenário: Segredo exposto
    Dado um commit contendo uma chave de API
    Quando o pipeline executa o Gitleaks
    Então o build falha e aponta o arquivo

  @PBI-22 @Should
  Cenário: Dependência vulnerável
    Dado uma dependência com CVE crítica
    Quando o pipeline executa o SCA
    Então o build falha com o relatório da vulnerabilidade
