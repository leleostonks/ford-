# -*- coding: utf-8 -*-
"""Gera a documentacao de QA (Sprint 3) em Markdown + .feature a partir dos dados de gerar_backlog.py."""
import os
import sys

from gerar_backlog import (BV, DOD_PADRAO, EPICS, FEATURES, PBIS, PRIORIDADE_TXT, SPRINT_ATUAL, SPRINTS,
                           TASKS)

OUT = sys.argv[1] if len(sys.argv) > 1 else "qa-sprint3"
os.makedirs(os.path.join(OUT, "bdd"), exist_ok=True)

COMPONENTE = {
    "EP-01": "Banco de Dados · Pipeline CI",
    "EP-02": "API REST (Auth/JWT) · Pipeline DevSecOps",
    "EP-03": "API REST · App Mobile",
    "EP-04": "Serviço de Coleta · Motor de Extração IA",
    "EP-05": "API REST · Banco de Dados",
    "EP-06": "App Mobile",
    "EP-07": "Testes automatizados · Observabilidade",
    "EP-08": "Documentação · Entrega",
}
pbi_by = {p["code"]: p for p in PBIS}
ft_by = {f["code"]: f for f in FEATURES}
sname = lambda n: SPRINTS[n][0]
pts = lambda items: sum(p["eff"] for p in items)


def write(name, lines):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def nid(code):
    return code.replace("-", "")


# ------------------------------------------------------------------ 01 backlog
L = ["# 1. Backlog do Produto", "",
     "Backlog no padrão Scrum (Épico › Feature › Product Backlog Item), alinhado à arquitetura definida na sprint anterior (TOGAF/ArchiMate).", "",
     "## Arquitetura de referência", "",
     "```mermaid", "flowchart LR",
     "  U([Analista / Gestor / Admin]) --> APP[App Mobile<br/>React Native · Expo]",
     "  APP -->|HTTPS + JWT| API[API REST<br/>Auth · Pesquisas · Especificações]",
     "  API --> COL[Serviço de Coleta<br/>fontes oficiais e secundárias · cache]",
     "  COL --> IA[Motor de Extração IA<br/>LLM + regras + normalizador]",
     "  API --> DB[(Banco de Dados<br/>catálogo · pesquisas · specs · fontes)]",
     "  IA --> DB",
     "  CI[[Pipeline CI/CD DevSecOps]] -.-> API",
     "  CI -.-> APP",
     "  OBS[[Observabilidade<br/>logs · métricas · dashboard]] -.-> API",
     "```", "",
     "## Épicos × componentes da arquitetura", "",
     "| Épico | Componente(s) | Features | PBIs | Pontos |", "|---|---|---|---|---|"]
for ep in EPICS:
    fts = [f for f in FEATURES if f["epic"] == ep["code"]]
    ps = [p for p in PBIS if ft_by[p["ft"]]["epic"] == ep["code"]]
    L.append(f"| **{ep['code']}** {ep['title']} | {COMPONENTE[ep['code']]} | {len(fts)} | {len(ps)} | {pts(ps)} |")
L += ["", f"**Total:** {len(EPICS)} épicos · {len(FEATURES)} features · {len(PBIS)} PBIs · {pts(PBIS)} pontos", "",
      "## Estrutura hierárquica", ""]
for ep in EPICS:
    L += [f"### {ep['code']} · {ep['title']}", "", ep["desc"], ""]
    for ft in [f for f in FEATURES if f["epic"] == ep["code"]]:
        L.append(f"- **{ft['code']} · {ft['title']}**")
        for p in [p for p in PBIS if p["ft"] == ft["code"]]:
            L.append(f"  - {p['code']} · {p['title']} · `{p['pri']}` · {p['eff']} pts · {sname(p['sprint'])}")
    L.append("")
write("01-backlog.md", L)

# ------------------------------------------------------------------ 02 historias / BDD
L = ["# 2. Histórias de Usuário, Critérios de Aceite e Pronto (BDD)", "",
     "Histórias no formato **Como / Quero / Para**, com critérios de aceite em **Gherkin** (Dado / Quando / Então). "
     "Os cenários executáveis estão em [`bdd/`](bdd/).", "",
     "**Personas:** Analista de Inteligência Competitiva · Gestor de Produto · Administrador.", "",
     "## Definition of Ready (DoR)", "",
     "- História escrita no formato Como / Quero / Para",
     "- Critérios de aceite em Gherkin",
     "- Dependências identificadas",
     "- Estimada pelo time (Planning Poker)",
     "- Cabe em uma sprint", "",
     "## Definition of Done (DoD)", ""]
L += [f"- {x.strip().rstrip('.')}" for x in DOD_PADRAO.split(";")] + [""]
for ep in EPICS:
    L += ["---", "", f"## {ep['code']} · {ep['title']}", "", f"**Descrição:** {ep['desc']}", "",
          f"**Critério de aceite do épico:** {ep['ac']}", ""]
    for ft in [f for f in FEATURES if f["epic"] == ep["code"]]:
        L += [f"### {ft['code']} · {ft['title']}", "", f"> {ft['story']}", "", f"**Critério de aceite:** {ft['ac']}", ""]
        for p in [p for p in PBIS if p["ft"] == ft["code"]]:
            L += [f"#### {p['code']} · {p['title']}", "", f"> {p['story']}", "", "```gherkin"]
            for nome, dado, quando, entao in p["gherkin"]:
                L += [f"Cenário: {nome}", f"  Dado {dado}", f"  Quando {quando}", f"  Então {entao}", ""]
            L[-1:] = ["```", "", f"**Pronto quando:** DoD + {p['dod']}", ""]
write("02-historias-bdd.md", L)

for ft in FEATURES:
    F = ["# language: pt", f"@{ft['epic']}", f"Funcionalidade: {ft['code']} {ft['title']}", f"  {ft['story']}", ""]
    for p in [p for p in PBIS if p["ft"] == ft["code"]]:
        for nome, dado, quando, entao in p["gherkin"]:
            F += [f"  @{p['code']} @{p['pri']}", f"  Cenário: {nome}", f"    Dado {dado}",
                  f"    Quando {quando}", f"    Então {entao}", ""]
    with open(os.path.join(OUT, "bdd", f"{ft['code'].lower()}.feature"), "w", encoding="utf-8") as f:
        f.write("\n".join(F))

# ------------------------------------------------------------------ 03 prioridade / esforco / dependencias
L = ["# 3. Prioridade, Esforço e Dependências", "",
     "## Prioridade (MoSCoW)", "", "| Prioridade | Significado | Valor de negócio |", "|---|---|---|"]
L += [f"| **{k}** | {PRIORIDADE_TXT[k]} | {BV[k]} |" for k in ["Must", "Should", "Could"]]
L += ["", "## Esforço (Planning Poker)", "",
      "Escala de Fibonacci **1 · 2 · 3 · 5 · 8 · 13**. Referência: **3 pontos** = um endpoint simples com testes. "
      "Itens com 13 pontos são revisados para quebra antes de entrar na sprint.", "",
      "| Prioridade | PBIs | Pontos |", "|---|---|---|"]
for k in ["Must", "Should", "Could"]:
    ps = [p for p in PBIS if p["pri"] == k]
    L.append(f"| {k} | {len(ps)} | {pts(ps)} |")
L += ["", "## Backlog ordenado (sequência de implementação)", "",
      "| # | PBI | Título | Feature | Prioridade | Esforço | Predecessores | Sprint |", "|---|---|---|---|---|---|---|---|"]
for i, p in enumerate(PBIS, 1):
    L.append(f"| {i} | {p['code']} | {p['title']} | {p['ft']} | {p['pri']} | {p['eff']} | {', '.join(p['deps']) or '—'} | {sname(p['sprint'])} |")
L += ["", "## Mapa de dependências", "",
      "Links **pai › filho** (Épico › Feature › PBI) estão em [01-backlog.md](01-backlog.md). Abaixo, os links de **precedência** entre PBIs (A → B = B depende de A).", "",
      "```mermaid", "flowchart LR"]
for n in [1, 2, 3, 4, 0]:
    L.append(f"  subgraph S{n}[\"{sname(n)}\"]")
    L += [f"    {nid(p['code'])}[\"{p['code']}\"]" for p in PBIS if p["sprint"] == n]
    L.append("  end")
L += [f"  {nid(d)} --> {nid(p['code'])}" for p in PBIS for d in p["deps"]]
L += ["```", ""]
write("03-prioridade-esforco-dependencias.md", L)

# ------------------------------------------------------------------ 04 release plan
L = ["# 4. Release Plan", "", "| Sprint | Período | Objetivo | Pontos | Status |", "|---|---|---|---|---|"]
status = {1: "Concluída", 2: "Concluída", 3: "Em curso", 4: "Planejada", 0: "Não planejado"}
for n in [1, 2, 3, 4, 0]:
    L.append(f"| **{sname(n)}** | {SPRINTS[n][1]} – {SPRINTS[n][2]} | {SPRINTS[n][3]} | {pts([p for p in PBIS if p['sprint'] == n])} | {status[n]} |")
planned = [p for p in PBIS if p["sprint"]]
L += ["", f"Total planejado: **{pts(planned)} pontos** em 4 sprints, média de **{pts(planned)/4:.1f} pontos por sprint**. "
      "Itens opcionais (*Could*) que não couberam ficam no backlog futuro.", "",
      "## Roadmap", "", "```mermaid", "gantt", "  dateFormat DD/MM/YYYY", "  axisFormat %b"]
for n in [1, 2, 3, 4]:
    L += [f"  section {sname(n)}", f"  {SPRINTS[n][3]} :{'active, ' if n == SPRINT_ATUAL else ''}{SPRINTS[n][1]}, {SPRINTS[n][2]}"]
L += ["```", ""]
for n in [1, 2, 3, 4, 0]:
    items = [p for p in PBIS if p["sprint"] == n]
    L += [f"## {sname(n)} · {pts(items)} pontos", "", f"**Objetivo:** {SPRINTS[n][3]}", "",
          "| PBI | Título | Épico | Prioridade | Pontos |", "|---|---|---|---|---|"]
    L += [f"| {p['code']} | {p['title']} | {ft_by[p['ft']]['epic']} | {p['pri']} | {p['eff']} |" for p in items]
    L.append("")
write("04-release-plan.md", L)

# ------------------------------------------------------------------ 05 sprint atual
sp = [p for p in PBIS if p["sprint"] == SPRINT_ATUAL]
L = [f"# 5. Sprint Atual · {sname(SPRINT_ATUAL)} ({SPRINTS[SPRINT_ATUAL][1]} – {SPRINTS[SPRINT_ATUAL][2]})", "",
     "**Meta da sprint:** entregar a lista padronizada de especificações validada com a Ford Ranger Raptor, "
     "o APK do app e a API protegida com pipeline DevSecOps.", "",
     f"**Compromisso:** {len(sp)} PBIs · {pts(sp)} pontos · {len(TASKS)} tarefas · {sum(t['h'] for t in TASKS)} horas", "",
     "## PBIs da sprint", "", "| PBI | Título | Pontos | Tarefas | Horas |", "|---|---|---|---|---|"]
for p in sp:
    ts = [t for t in TASKS if t["pbi"] == p["code"]]
    L.append(f"| {p['code']} | {p['title']} | {p['eff']} | {', '.join(t['code'] for t in ts)} | {sum(t['h'] for t in ts)} |")
L += ["", "## Tarefas", ""]
for p in sp:
    L += [f"### {p['code']} · {p['title']}", "", "| Tarefa | Descrição | Atividade | Esforço (h) | Dependências técnicas |", "|---|---|---|---|---|"]
    L += [f"| {t['code']} | {t['title']} | {t['act']} | {t['h']} | {', '.join(t['deps']) or '—'} |" for t in TASKS if t["pbi"] == p["code"]]
    L.append("")
L += ["## Esforço por atividade", "", "| Atividade | Horas |", "|---|---|"]
acts = {}
for t in TASKS:
    acts[t["act"]] = acts.get(t["act"], 0) + t["h"]
L += [f"| {a} | {h} |" for a, h in sorted(acts.items(), key=lambda x: -x[1])]
L += ["", "## Dependências entre tarefas", "", "```mermaid", "flowchart LR"]
L += [f"  {nid(t['code'])}[\"{t['code']} ({t['h']}h)\"]" for t in TASKS]
L += [f"  {nid(d)} --> {nid(t['code'])}" for t in TASKS for d in t["deps"]]
L += ["  classDef crit fill:#ffd6d6,stroke:#c00", "  class T01,T02,T05,T08,T20,T21,T23,T24,T26,T28 crit", "```", "",
      "**Caminho crítico** (em vermelho):", "",
      "- Validação da Ranger Raptor: T-01 → T-02 → T-05 → T-08 → T-20 → T-21",
      "- APK: T-05 → T-23 → T-24 → T-26 → T-28", ""]
write("05-sprint-atual.md", L)

# ------------------------------------------------------------------ README
write("README.md", [
    "# QA: Sprint 3", "",
    "Plano do projeto do Desafio 01 (Inteligência Competitiva Automotiva).", "",
    "1. [Backlog do Produto](01-backlog.md): Épicos, Features e PBIs alinhados à arquitetura",
    "2. [Histórias e BDD](02-historias-bdd.md): descrição, critérios de aceite e pronto ([cenários .feature](bdd/))",
    "3. [Prioridade, Esforço e Dependências](03-prioridade-esforco-dependencias.md): backlog ordenado",
    "4. [Release Plan](04-release-plan.md): roadmap por sprint",
    "5. [Sprint Atual](05-sprint-atual.md): tarefas da Sprint 3", "",
    "Para gerar os documentos de novo: `python gerar_docs.py .` (ou dois cliques em `rodar.bat`). "
    "Os dados ficam em `gerar_backlog.py`.",
])
print("ok")
