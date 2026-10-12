#!/usr/bin/env python3
"""Autorização única: liga o app do TikTok à conta da Juliana e gera o TIKTOK_REFRESH_TOKEN.

Passo 1:  python3 src/autorizar_tiktok.py link
          Abra o link, entre na conta @ferreira.bolos e autorize. A página de retorno
          (site/autorizar.html no GitHub Pages) mostra um código.
Passo 2:  python3 src/autorizar_tiktok.py codigo <CODIGO>
          Imprime o refresh_token. Salve como segredo TIKTOK_REFRESH_TOKEN no GitHub.

Precisa das variáveis TIKTOK_CLIENT_KEY, TIKTOK_CLIENT_SECRET e TIKTOK_REDIRECT_URI
(a mesma URL cadastrada no app, ex: https://<usuario>.github.io/juliana-tiktok/site/autorizar.html)."""
import os, sys, urllib.parse
import requests

key, secret, redirect = (os.environ[k] for k in ("TIKTOK_CLIENT_KEY", "TIKTOK_CLIENT_SECRET", "TIKTOK_REDIRECT_URI"))

if sys.argv[1] == "link":
    q = urllib.parse.urlencode({"client_key": key, "scope": "user.info.basic,video.upload",
                                "response_type": "code", "redirect_uri": redirect, "state": "juliana"})
    print(f"https://www.tiktok.com/v2/auth/authorize/?{q}")
else:
    r = requests.post("https://open.tiktokapis.com/v2/oauth/token/", timeout=60, data={
        "client_key": key, "client_secret": secret, "code": urllib.parse.unquote(sys.argv[2]),
        "grant_type": "authorization_code", "redirect_uri": redirect})
    d = r.json()
    print("refresh_token:", d.get("refresh_token") or d)
    print("expira em (dias):", int(d.get("refresh_expires_in", 0)) // 86400)
