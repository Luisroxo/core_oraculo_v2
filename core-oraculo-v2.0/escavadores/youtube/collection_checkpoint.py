"""
Sistema de Checkpoint para Coleta Cronológica Inteligente
=========================================================

Gerencia o estado de coleta por canal, evitando reprocessamento
e garantindo cobertura histórica completa.
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, Optional

class CollectionCheckpoint:
    def __init__(self, checkpoint_file='coleta_checkpoint.json'):
        self.checkpoint_file = checkpoint_file
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        """Carrega estado dos checkpoints ou cria novo"""
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        # Estado inicial vazio
        return {}
    
    def _save_state(self):
        """Salva estado atual dos checkpoints"""
        with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)
    
    def get_checkpoint(self, channel_id: str) -> Optional[str]:
        """
        Obtém o timestamp do último vídeo coletado para um canal
        
        Args:
            channel_id: ID do canal do YouTube
            
        Returns:
            Timestamp ISO do último vídeo coletado ou None se primeiro run
        """
        channel_state = self.state.get(channel_id, {})
        return channel_state.get('ultimo_video_timestamp')
    
    def get_channel_info(self, channel_id: str) -> Dict:
        """Obtém informações completas do canal"""
        return self.state.get(channel_id, {
            'ultimo_video_timestamp': None,
            'ultimo_video_id': None,
            'total_coletados': 0,
            'primeira_execucao': datetime.now(timezone.utc).isoformat(),
            'ultima_execucao': None,
            'status': 'novo'
        })
    
    def update_checkpoint(self, channel_id: str, video_timestamp: str, video_id: str):
        channel_state = self.state.setdefault(channel_id, self.get_channel_info(channel_id))
        channel_state['ultimo_video_timestamp'] = video_timestamp
        channel_state['ultimo_video_id'] = video_id
        channel_state['ultima_execucao'] = datetime.now(timezone.utc).isoformat()
        channel_state['status'] = 'atualizado'
        self._save_state()
