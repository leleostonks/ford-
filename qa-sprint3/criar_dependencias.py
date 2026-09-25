# -*- coding: utf-8 -*-
"""
Depois que o CSV foi importado no Azure DevOps:
  - cria os links de dependencia (Predecessor/Successor) entre PBIs e entre Tasks;
  - ordena o backlog na sequencia de implementacao (Backlog Priority);
  - ajusta o estado dos PBIs (Sprints 1-2 Done, Sprint 3 Committed, Sprint 4 Approved).

Pre-requisitos:
  pip install requests
  Personal Access Token (PAT) com escopo "Work Items: Read & Write"

Uso (PowerShell):
  $env:AZDO_ORG = "minha-organizacao"         # dev.azure.com/<isto>
  $env:AZDO_PROJECT = "Ford Challenge"
  $env:AZDO_PAT = "xxxxxxxx"
  python criar_dependencias.py
"""
import base64
import os
import re
import sys

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gerar_backlog import PBIS, TASKS  # noqa: E402  (reaproveita os mesmos dados)

ORG = os.environ["AZDO_ORG"]
PROJECT = os.environ.get("AZDO_PROJECT", "Ford Challenge")
PAT = os.environ["AZDO_PAT"]

BASE = f"https://dev.azure.com/{ORG}/{PROJECT}/_apis/wit"
AUTH = {"Authorization": "Basic " + base64.b64encode(f":{PAT}".encode()).decode()}

# 1) Mapeia codigo ([PBI-19], [T-05]) -> ID do work item
wiql = {"query": "SELECT [System.Id] FROM WorkItems WHERE [System.TeamProject] = @project "
                 "AND ([System.Title] CONTAINS '[PBI-' OR [System.Title] CONTAINS '[T-')"}
r = requests.post(f"{BASE}/wiql?api-version=7.1", json=wiql, headers=AUTH)
r.raise_for_status()
ids = [w["id"] for w in r.json()["workItems"]]

code_to_id = {}
for i in range(0, len(ids), 200):
    chunk = ",".join(map(str, ids[i:i + 200]))
    r = requests.get(f"{BASE}/workitems?ids={chunk}&fields=System.Title&api-version=7.1", headers=AUTH)
    r.raise_for_status()
    for w in r.json()["value"]:
        m = re.match(r"\[((?:PBI|T)-\d+)\]", w["fields"]["System.Title"])
        if m:
            code_to_id[m.group(1)] = w["id"]

print(f"{len(code_to_id)} itens encontrados")

# 2) Cria link "Predecessor" em cada item apontando para suas dependencias
pares = [(p["code"], d) for p in PBIS for d in p["deps"]] + [(t["code"], d) for t in TASKS for d in t["deps"]]
for item, dep in pares:
    if item not in code_to_id or dep not in code_to_id:
        print(f"  ! ignorado {item} -> {dep} (não encontrado)")
        continue
    patch = [{"op": "add", "path": "/relations/-", "value": {
        "rel": "System.LinkTypes.Dependency-Reverse",  # Predecessor
        "url": f"https://dev.azure.com/{ORG}/_apis/wit/workItems/{code_to_id[dep]}",
        "attributes": {"comment": f"{item} depende de {dep}"}}}]
    r = requests.patch(f"{BASE}/workitems/{code_to_id[item]}?api-version=7.1", json=patch,
                       headers={**AUTH, "Content-Type": "application/json-patch+json"})
    if r.ok:
        print(f"  ok {item} <- predecessor {dep}")
    elif "already exists" in r.text or "Relation already exists" in r.text:
        print(f"  = {item} -> {dep} já existia")
    else:
        print(f"  ERRO {item} -> {dep}: {r.status_code} {r.text[:200]}")

# 3) Ordena o backlog na sequencia de implementacao e ajusta o estado conforme a sprint
ESTADO = {1: "Done", 2: "Done", 3: "Committed", 4: "Approved", 0: "New"}
for ordem, p in enumerate(PBIS, 1):
    if p["code"] not in code_to_id:
        continue
    patch = [{"op": "add", "path": "/fields/Microsoft.VSTS.Common.BacklogPriority", "value": ordem * 1000},
             {"op": "add", "path": "/fields/System.State", "value": ESTADO[p["sprint"]]}]
    r = requests.patch(f"{BASE}/workitems/{code_to_id[p['code']]}?api-version=7.1", json=patch,
                       headers={**AUTH, "Content-Type": "application/json-patch+json"})
    print(f"  {'ok' if r.ok else 'ERRO'} {p['code']} ordem {ordem} estado {ESTADO[p['sprint']]}"
          + ("" if r.ok else f": {r.text[:200]}"))
