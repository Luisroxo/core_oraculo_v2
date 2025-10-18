import sys
import re
import subprocess
import os
from pathlib import Path

ROADMAP_PATH = Path(__file__).parent / "core-oraculo-v2.0" / "ROADMAP.md"

def marcar_subtarefa_concluida(subtarefa):
    # Validação automática: só permite marcar como concluída se existir código do serviço
    # Mapeamento simples: subtarefa -> pasta esperada
    subtarefa_map = {
        "Implementar API Gateway (FastAPI)": "core-oraculo-v2.0/api-gateway/main.py",
        "Implementar API Gateway": "core-oraculo-v2.0/api-gateway/main.py",
        "YouTube": "core-oraculo-v2.0/escavadores/youtube/main.py",
        "Blog": "core-oraculo-v2.0/escavadores/blog/main.py",
        "Telegram": "core-oraculo-v2.0/escavadores/telegram/main.py",
        "Instagram": "core-oraculo-v2.0/escavadores/instagram/main.py",
        "Licitações": "core-oraculo-v2.0/escavadores/licitacoes/main.py",
        "Relatórios": "core-oraculo-v2.0/executadores/relatorios/main.py",
        "Conteúdo (IA)": "core-oraculo-v2.0/executadores/conteudo-ia/main.py",
        "Automações": "core-oraculo-v2.0/executadores/automacoes/main.py",
        "ERP/CRM": "core-oraculo-v2.0/executadores/erp-crm/Main.java",
        "Mídias Sociais": "core-oraculo-v2.0/executadores/midias-sociais/index.js",
    }
    for chave, caminho in subtarefa_map.items():
        if chave in subtarefa:
            full_path = os.path.join(os.path.dirname(__file__), caminho)
            if not os.path.exists(full_path):
                print(f"[ERRO] Não existe código implementado para '{chave}'. Crie o arquivo '{caminho}' antes de marcar como concluído.")
                return False, None
    with open(ROADMAP_PATH, "r", encoding="utf-8") as f:
        conteudo = f.readlines()

    nova_lista = []
    subtarefa_encontrada = False
    tarefa_inicio = None
    tarefa_fim = None
    tarefa_concluida = False
    tarefa_titulo = None
    tarefa_principal_nome = None

    # Marcar subtarefa como concluída
    for i, linha in enumerate(conteudo):
        if subtarefa in linha and linha.strip().startswith("- "):
            if "[ ]" in linha:
                linha = linha.replace("- ", "- [x] ", 1)
            subtarefa_encontrada = True
        nova_lista.append(linha)

    if not subtarefa_encontrada:
        print(f"Subtarefa '{subtarefa}' não encontrada.")
        return False, False

    # Verificar se todas as subtarefas da tarefa principal estão concluídas
    for i, linha in enumerate(nova_lista):
        if linha.strip().startswith("- [ ] **") or linha.strip().startswith("- [x] **"):
            tarefa_inicio = i
            tarefa_titulo = linha.strip()
            tarefa_principal_nome = linha.strip().replace("- [x] ", "").replace("- [ ] ", "").replace("**", "").strip()
            # Procurar fim da tarefa (próxima tarefa ou fim do arquivo)
            for j in range(i+1, len(nova_lista)):
                if nova_lista[j].strip().startswith("- [ ] **") or nova_lista[j].strip().startswith("- [x] **"):
                    tarefa_fim = j
                    break
            else:
                tarefa_fim = len(nova_lista)
            # Checar se a subtarefa está dentro deste bloco
            bloco = nova_lista[tarefa_inicio:tarefa_fim]
            if any(subtarefa in l for l in bloco):
                # Se todas as subtarefas estão marcadas, marcar tarefa principal
                if all(l.strip().startswith("- [x]") or l.strip().startswith("- [x] **") or not l.strip().startswith("- ") for l in bloco[1:]):
                    if "[ ]" in nova_lista[tarefa_inicio]:
                        nova_lista[tarefa_inicio] = nova_lista[tarefa_inicio].replace("[ ]", "[x]", 1)
                        tarefa_concluida = True
                break

    with open(ROADMAP_PATH, "w", encoding="utf-8") as f:
        f.writelines(nova_lista)
    return True, tarefa_principal_nome if tarefa_concluida else None

def git_commit_push(msg):
    subprocess.run(["git", "add", str(ROADMAP_PATH)], check=True)
    subprocess.run(["git", "commit", "-m", msg], check=True)
    subprocess.run(["git", "push"], check=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python atualizar_roadmap.py \"Subtarefa exata\"")
        sys.exit(1)
    subtarefa = sys.argv[1]
    marcada, tarefa_principal_concluida = marcar_subtarefa_concluida(subtarefa)
    if marcada:
        print(f"Subtarefa '{subtarefa}' marcada como concluída.")
        if tarefa_principal_concluida:
            print(f"Todas as subtarefas da tarefa principal '{tarefa_principal_concluida}' foram concluídas! Realizando commit e push...")
            git_commit_push(f"Tarefa principal concluída: {tarefa_principal_concluida}")
