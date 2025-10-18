# Estratégia de Versionamento de Código

## Padrão Adotado: Git Flow

### Visão Geral
O Git Flow é uma estratégia de ramificação (branching) que organiza o desenvolvimento em diferentes tipos de branches, facilitando releases, hotfixes e colaboração em equipe.

### Branches Principais
- **main**: Contém sempre o código de produção estável.
- **develop**: Integração de novas features e correções antes de irem para produção.

### Branches de Suporte
- **feature/**: Para desenvolvimento de novas funcionalidades. Ex: `feature/api-auth`
- **release/**: Preparação de uma nova versão para produção. Ex: `release/1.2.0`
- **hotfix/**: Correções urgentes em produção. Ex: `hotfix/1.2.1`
- **bugfix/**: Correções de bugs identificados durante o desenvolvimento.

### Fluxo de Trabalho
1. Crie uma branch `feature/` a partir de `develop` para cada nova funcionalidade.
2. Ao finalizar, faça merge da feature em `develop` via pull request.
3. Para releases, crie uma branch `release/` a partir de `develop`. Após testes, faça merge em `main` e `develop`.
4. Para hotfixes, crie uma branch `hotfix/` a partir de `main`. Após correção, faça merge em `main` e `develop`.

### Boas Práticas
- Commits pequenos, claros e frequentes.
- Pull requests obrigatórios e revisão de código.
- Tags semânticas para releases (ex: v1.2.0).
- Automatizar testes e builds no CI para cada merge.
- Documentar mudanças relevantes no CHANGELOG.md.

### Alternativa: Trunk-Based Development
- Para times menores ou projetos de alta frequência de deploy, pode-se adotar trunk-based (apenas branch principal, deploy contínuo, feature flags).

---

Esta estratégia pode ser adaptada conforme o time e o projeto evoluírem. Recomenda-se revisitar periodicamente para garantir eficiência e qualidade.