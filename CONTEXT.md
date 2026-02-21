# Contexto do projeto - ORMs Erros Comuns

## O que foi feito

### Estrutura do projeto
- **Backend**: Django + DRF com endpoint GET `/api/hello/`
- **Frontend**: React + Vite em `frontend/` (criado com `npm create vite@latest`, deps instaladas)
- **Slides**: MARP em `slides/slides.md` (8 slides sobre erros comuns com ORMs)
- **Testes**: `tests/test_api.py` com teste do endpoint DRF
- **Python**: 3.14, gerenciado com `uv`, deps em `pyproject.toml`
- **JS**: npm para o frontend

### GitHub
- **Repo público**: https://github.com/rodbv/orms-erros-comuns
- **GitHub Pages habilitado** (source: GitHub Actions)
- **Slides publicados**: https://rodbv.github.io/orms-erros-comuns/

### GitHub Actions (ambas passando)
1. `.github/workflows/tests.yml` — roda `uv run pytest` em push/PR
2. `.github/workflows/slides.yml` — converte `slides/slides.md` para HTML com `@marp-team/marp-cli` e faz deploy para GitHub Pages (push na main)

### Ferramentas
- `uv` para Python (deps, venv, rodar testes)
- `npm` para JS/frontend
- `gh` CLI para GitHub
- MARP para slides (extensão "Marp for VS Code" para preview local)

### Comandos úteis
- Backend: `uv run python manage.py runserver`
- Frontend: `cd frontend && npm run dev`
- Testes: `uv run pytest`
- Slides: abrir `slides/slides.md` no VS Code com extensão Marp

## Pergunta pendente
O usuário perguntou como o MARP gera os slides (se usa JS). Resposta: o marp-cli converte o .md para um HTML standalone com CSS e JS embutidos inline. É um único arquivo HTML auto-contido.

## Migração recente
- FastAPI removido
- Backend migrado para Django + DRF
- Rota principal de API agora é `/api/hello/`
