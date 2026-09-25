# Ford Challenge 2026: Plano no Azure DevOps (Sprint 3, QA)

Desafio 01, Inteligência Competitiva Automotiva. Este passo a passo cria o plano completo no Azure Boards: Épicos, Features, PBIs, BDD, prioridade, esforço, dependências, release plan e as tarefas da Sprint 3.

## Arquivos

| Arquivo | O que é |
|---|---|
| `backlog_azure_devops.csv` | 8 Épicos, 15 Features, 37 PBIs e 28 Tasks, com hierarquia, descrição, critérios BDD, Business Value, Effort, Sprint e Tags |
| `criar_dependencias.py` | Cria os links Predecessor/Successor, ordena o backlog e define o estado dos PBIs |
| `PLANO_DO_PROJETO.md` | O plano inteiro em texto, para colar na Wiki do projeto |
| `gerar_backlog.py` | Fonte única dos dados. Edite aqui e rode de novo para gerar o CSV e o .md |

## Passo a passo (cerca de 15 min)

1. **Criar o projeto.** Em dev.azure.com, crie um projeto chamado **`Ford Challenge`** com o processo **Scrum** (Advanced › Work item process › Scrum).
   Se usar outro nome, rode `python gerar_backlog.py "Nome Do Projeto"` para gerar o CSV de novo.
2. **Criar as sprints.** Vá em Project settings › Boards › Project configuration › Iterations e crie as sprints abaixo com estas datas:
   - Sprint 1: 16/02/2026 a 12/04/2026
   - Sprint 2: 13/04/2026 a 07/06/2026
   - Sprint 3: 03/08/2026 a 27/09/2026
   - Sprint 4: 28/09/2026 a 11/10/2026

   Depois, em Team configuration › Iterations, selecione as 4 sprints para o time.
3. **Importar o CSV.** Vá em Boards › Work items › **Import Work Items** › selecione `backlog_azure_devops.csv` › Import › **Save items**.
4. **Criar as dependências e a ordem do backlog.** Crie um PAT em User settings › Personal access tokens com o escopo *Work Items: Read & Write*. Depois rode:
   ```powershell
   pip install requests
   $env:AZDO_ORG = "sua-organizacao"
   $env:AZDO_PROJECT = "Ford Challenge"
   $env:AZDO_PAT = "seu-pat"
   python criar_dependencias.py
   ```
5. **Criar a Wiki.** Vá em Overview › Wiki › Create project wiki e cole o conteúdo de `PLANO_DO_PROJETO.md`. Anexe também o diagrama ArchiMate da sprint anterior.
6. **Dar acesso ao professor:**
   - Em Organization settings › Users › Add users, adicione o e-mail do professor com access level **Basic**.
   - Em Project settings › Permissions › **Project Administrators** › Add, adicione o professor.
7. **Entregar o link.** O link é `https://dev.azure.com/<organizacao>/Ford%20Challenge`. Envie pelo Teams.

## Onde o professor vê cada critério

| Critério (20% cada) | Onde está no Azure |
|---|---|
| Backlog Épicos › Features › PBIs | Boards › Backlogs (nível Epics e Features, com "Parents: Show") |
| Descrição, aceite BDD e DoD | Em cada item: *Description* (história Como/Quero/Para) e *Acceptance Criteria* (Gherkin e DoD) |
| Prioridade, esforço e dependências, backlog ordenado | Tags Must/Should/Could, *Business Value*, *Effort* (Fibonacci), aba Links (Predecessor/Successor) e ordem do Backlog |
| Release plan | Boards › Backlogs › painel **Planning** (arrastar entre sprints) e Delivery Plans (opcional) |
| Sprint atual | Boards › Sprints › Sprint 3 › Taskboard (28 tarefas com horas, atividade e dependências) |

## Observação

A arquitetura usada no backlog tem estes componentes: App Mobile (Expo), API REST com JWT, Serviço de Coleta, Motor de Extração IA (LLM + regras) e Banco de Dados. Se os nomes no ArchiMate do grupo forem outros, ajuste os títulos em `gerar_backlog.py` e gere os arquivos de novo.
