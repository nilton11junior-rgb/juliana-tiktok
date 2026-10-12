#!/usr/bin/env python3
"""Imprime quantos segundos faltam para o próximo post aprovado e ainda não enviado (até 5h30).
Imprime 0 se já há post vencido ou nenhum próximo. O robô usa isso para esperar o horário exato."""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIMITE = 5.5 * 3600
estado_p = ROOT / "estado" / "published.json"
estado = json.loads(estado_p.read_text()) if estado_p.exists() else {}
agora = datetime.now(timezone.utc)
menor = None
for f in sorted((ROOT / "conteudo" / "calendario").glob("*.json")):
    for p in json.loads(f.read_text(encoding="utf-8"))["posts"]:
        if p["id"] in estado or not p.get("aprovado", False):
            continue
        falta = (datetime.fromisoformat(p["publicar_em"]) - agora).total_seconds()
        if falta <= 0:
            print(0); raise SystemExit
        if falta <= LIMITE and (menor is None or falta < menor):
            menor = falta
print(int(menor) + 20 if menor else 0)
