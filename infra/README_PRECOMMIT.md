# Pré-commit hooks — ORÁCULO v2.0

Este projeto utiliza o [pre-commit](https://pre-commit.com/) para garantir qualidade, formatação e segurança do código antes de cada commit.

## Como instalar

1. Instale o pre-commit globalmente:
   ```bash
   pip install pre-commit
   ```
2. Instale os hooks no repositório:
   ```bash
   pre-commit install
   ```

## Hooks configurados
- **black**: formatação automática de código Python
- **flake8**: análise estática de código Python
- **bandit**: análise de segurança para Python
- **prettier**: formatação de arquivos JS, TS, JSON, Markdown
- **lint-staged**: lint e format para arquivos JS/TS

## Dicas
- Para rodar manualmente: `pre-commit run --all-files`
- Para Node, instale também `eslint` e `prettier` no projeto.
- Os hooks são executados automaticamente antes de cada commit.

---
Dúvidas? Consulte este arquivo ou o time de DevOps.