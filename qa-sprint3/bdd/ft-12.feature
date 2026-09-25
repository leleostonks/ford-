# language: pt
@EP-06
Funcionalidade: FT-12 Publicação do Aplicativo
  Como avaliador, quero instalar o app via APK, para testar a solução em um dispositivo real.

  @PBI-26 @Must
  Cenário: APK instalável
    Dado o perfil 'preview' configurado no eas.json
    Quando executo o EAS Build
    Então o APK é gerado, instala e abre sem erros em dispositivo físico
