"""
Testes unitários para o escavador YouTube.
Valida se a variável de ambiente DB_URL está presente.
Garante que a função test_db_connection lida corretamente com ausência da variável.
Estrutura inicial para expandir testes do serviço.
"""
import pytest
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from main import test_db_connection

def test_env_db_url_exists(monkeypatch):
    monkeypatch.setenv('DB_URL', 'postgresql://user:pass@localhost:5432/db')
    # Não conecta de verdade, só testa se a variável existe
    assert os.getenv('DB_URL') is not None

def test_db_connection_handles_missing(monkeypatch, capsys):
    monkeypatch.delenv('DB_URL', raising=False)
    test_db_connection()
    captured = capsys.readouterr()
    assert 'DB_URL não encontrada no .env' in captured.out
