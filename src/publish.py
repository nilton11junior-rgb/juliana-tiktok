#!/usr/bin/env python3
"""Envia carrosséis para o rascunho (caixa de entrada) do TikTok da Juliana quando chega 'publicar_em'.

Usa a Content Posting API do TikTok, modo MEDIA_UPLOAD: o carrossel chega no app como
notificação; a Juliana abre, escolhe um som em alta e posta. Esse modo não exige auditoria do app.

Variáveis de ambiente (segredos do GitHub):
  TIKTOK_CLIENT_KEY, TIKTOK_CLIENT_SECRET   do app em developers.tiktok.com
  TIKTOK_REFRESH_TOKEN                     gravado pelo workflow autorizar-tiktok (vale 365 dias)
  GH_PAT                                   chave do GitHub (só este repositório, permissão Secrets) para renovar o token
  PUBLIC_BASE_URL                          URL pública de criativos/gerados (GitHub Pages, prefixo verificado no TikTok)

Uso:
  python3 src/publish.py conteudo/calendario/semana-2026-10-12.json             # envia o que venceu
  python3 src/publish.py conteudo/calendario/semana-2026-10-12.json --dry-run   # só mostra
  --dry-run --ignore-time  simula também os que ainda não venceram
Estado: estado/published.json (não envia o mesmo post duas vezes)."""
import json, os, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "estado" / "published.json"
API = "https://open.tiktokapis.com/v2"


def access_token():
    r = requests.post(f"{API}/oauth/token/", timeout=60, data={
        "client_key": os.environ["TIKTOK_CLIENT_KEY"],
        "client_secret": os.environ["TIKTOK_CLIENT_SECRET"],
        "grant_type": "refresh_token",
        "refresh_token": os.environ["TIKTOK_REFRESH_TOKEN"],
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})
    d = r.json()
    if "access_token" not in d:
        raise RuntimeError(f"token: {r.status_code} {d.get('error')} {d.get('error_description')}")
    novo = d.get("refresh_token")
    if novo and novo != os.environ["TIKTOK_REFRESH_TOKEN"]:
        guardar_refresh_token(novo)
    return d["access_token"]


def guardar_refresh_token(token):
    """Grava o refresh token novo direto nos segredos do repositório (precisa do segredo GH_PAT).
    O valor vai por stdin para o gh e nunca é impresso nem salvo em arquivo."""
    if not os.environ.get("GH_PAT"):
        print("AVISO: refresh token novo, mas sem GH_PAT para atualizar o segredo")
        return
    print(f"::add-mask::{token}")
    subprocess.run(["gh", "secret", "set", "TIKTOK_REFRESH_TOKEN", "--repo", os.environ.get("GITHUB_REPOSITORY", "")],
                   input=token.encode(), check=True, env={**os.environ, "GH_TOKEN": os.environ["GH_PAT"]},
                   capture_output=True)
    os.environ["TIKTOK_REFRESH_TOKEN"] = token
    print("segredo TIKTOK_REFRESH_TOKEN atualizado")


def api(token, path, body):
    r = requests.post(f"{API}/{path}", json=body, timeout=60,
                      headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=UTF-8"})
    d = r.json()
    if d.get("error", {}).get("code", "ok") != "ok":
        raise RuntimeError(f"{path}: {r.status_code} {d['error']}")
    return d.get("data", {})


def slides_do_post(post_id):
    gerados = ROOT / "criativos" / "gerados"
    pastas = [p for p in gerados.rglob(post_id) if p.is_dir()]
    if not pastas:
        raise FileNotFoundError(f"sem slides para {post_id} (rode src/render.py)")
    jpgs = sorted(pastas[0].glob("slide-*.jpg"))
    if not 2 <= len(jpgs) <= 35:
        raise ValueError(f"{post_id}: precisa de 2 a 35 JPEG, achei {len(jpgs)}")
    return pastas[0].relative_to(gerados).as_posix(), jpgs


def enviar(post, base):
    rel, jpgs = slides_do_post(post["id"])
    token = access_token()
    data = api(token, "post/publish/content/init/", {
        "media_type": "PHOTO",
        "post_mode": "MEDIA_UPLOAD",
        "post_info": {"title": post["titulo"][:90], "description": post["legenda"]},
        "source_info": {"source": "PULL_FROM_URL", "photo_cover_index": 0,
                        "photo_images": [f"{base}/{rel}/{j.name}" for j in jpgs]},
    })
    pid = data["publish_id"]
    for _ in range(40):  # o TikTok baixa as fotos e manda para a caixa de entrada
        st = api(token, "post/publish/status/fetch/", {"publish_id": pid})
        status = st.get("status")
        if status in ("SEND_TO_USER_INBOX", "PUBLISH_COMPLETE"):
            return pid, status
        if status == "FAILED":
            raise RuntimeError(f"falhou: {st.get('fail_reason')}")
        time.sleep(6)
    raise TimeoutError(f"{post['id']}: TikTok não terminou de processar ({pid})")


def salvar_estado_no_git():
    if not os.environ.get("GITHUB_ACTIONS"):
        return
    try:
        run = lambda *a: subprocess.run(a, cwd=ROOT, check=True, capture_output=True)
        run("git", "config", "user.name", "juliana-bot")
        run("git", "config", "user.email", "bot@users.noreply.github.com")
        run("git", "add", "estado/published.json")
        run("git", "commit", "-m", "estado: carrossel enviado ao TikTok")
        run("git", "pull", "--rebase")
        run("git", "push")
    except Exception as e:
        print(f"aviso: não consegui salvar o estado no git agora: {e}")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    ignore_time = dry and "--ignore-time" in sys.argv
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    now = datetime.now(timezone.utc)
    base = os.environ.get("PUBLIC_BASE_URL", "").rstrip("/")
    data = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    if not dry and not os.environ.get("TIKTOK_CLIENT_KEY"):
        print("app do TikTok ainda não configurado (sem TIKTOK_CLIENT_KEY): nada enviado")
        return
    falhas = []
    for post in data["posts"]:
        if post["id"] in state:
            continue
        if not post.get("aprovado", False):
            print(f"sem aprovação do Nilton, não envia: {post['id']}")
            continue
        if post.get("agendado_no_studio"):
            print(f"já agendado no TikTok Studio, robô não envia: {post['id']}")
            continue
        if datetime.fromisoformat(post["publicar_em"]) > now and not ignore_time:
            print(f"aguardando {post['id']} ({post['publicar_em']})")
            continue
        if dry:
            rel, jpgs = slides_do_post(post["id"])
            print(f"[dry-run] enviaria {post['id']}: {len(jpgs)} slides, título {len(post['titulo'])}/90, "
                  f"legenda {len(post['legenda'])} caracteres")
            continue
        try:
            pid, status = enviar(post, base)
        except Exception as e:
            print(f"ERRO ao enviar {post['id']}: {e}")
            falhas.append(post["id"])
            continue
        state[post["id"]] = {"publish_id": pid, "status": status, "em": now.isoformat()}
        STATE.write_text(json.dumps(state, indent=2))
        salvar_estado_no_git()
        print(f"enviado {post['id']} -> {status} ({pid})")
    if falhas:
        sys.exit(1)


if __name__ == "__main__":
    main()
