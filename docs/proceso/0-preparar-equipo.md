# 0 · Preparar tu equipo

## Una sola vez por computadora

**Requisitos previos:** WSL con Ubuntu, Python 3.11 o más nuevo.

| Paso | Comando | Qué hace |
|---|---|---|
| 1 | `git config --global user.name "Tu Nombre"` | Nombre que aparece en tus commits. |
| 2 | `git config --global user.email "tu@correo"` | Correo de tus commits; usa el mismo de GitHub. |
| 3 | `sudo apt install gh` | Instala `gh`, la herramienta de GitHub para la terminal. |
| 4 | `gh auth login` | Conecta `gh` (y `git push`) con tu cuenta. Elige GitHub.com → HTTPS → navegador. |
| 5 | `mkdir -p ~/proyectos && cd ~/proyectos` | Carpeta de trabajo dentro de Linux (más rápida que `/mnt/d/...`). |
| 6 | `gh repo clone Sierra-034/especificaciones-escolares` | Baja el estándar. |
| 7 | `gh repo clone Sierra-034/plataforma-escolar -- --recurse-submodules` | Baja la implementación **con** `estandar/` adentro. |
| 8 | `cd especificaciones-escolares && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt` | Ambiente para el verificador y el sitio. |

**Cómo saber que salió bien:** `gh auth status` dice «Logged in»; `ls ~/proyectos` muestra los dos repos;
`ls ~/proyectos/plataforma-escolar/estandar` no está vacío.

**Si algo falla:** si `estandar/` está vacío, corre `git submodule update --init` dentro de `plataforma-escolar`.

## Antes de cada sesión

**Requisitos previos:** lo anterior.

| Paso | Comando | Qué hace |
|---|---|---|
| 1 | `cd ~/proyectos/especificaciones-escolares` | Entra al repo. |
| 2 | `git status` | Debe decir *nothing to commit, working tree clean*. Si no, termina o descarta lo pendiente antes de empezar algo nuevo. |
| 3 | `git switch main && git pull` | Te pone en `main` y baja lo que se unió en GitHub (por ejemplo, tus propios *squash*). |
| 4 | `source .venv/bin/activate` | Activa el ambiente de Python. |

En `plataforma-escolar` es igual, más `git submodule update` después del `pull`, para que `estandar/`
quede en la versión que `main` tiene fijada.
