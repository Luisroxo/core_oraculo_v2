import unittest
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import settings

class TestConfig(unittest.TestCase):
    def test_lote_tamanho(self):
        self.assertTrue(settings.LOTE_TAMANHO > 0)
    def test_pausa_entre_videos(self):
        self.assertTrue(settings.PAUSA_ENTRE_VIDEOS >= 0)
    def test_pausa_entre_lotes(self):
        self.assertTrue(settings.PAUSA_ENTRE_LOTES >= 0)
    def test_max_retries(self):
        self.assertTrue(settings.MAX_RETRIES > 0)

    def test_channel_ids_multiple(self):
        # Isola variáveis de ambiente e não carrega .env
        import os
        from config import Settings
        os.environ.pop('CHANNEL_ID', None)
        os.environ.pop('ESCAVADOS_CHANNEL_ID', None)
        os.environ['CHANNEL_IDS'] = 'UC123,UC456,UC789'
        settings_test = Settings(load_env=False)
        ids = settings_test.CHANNEL_IDS
        self.assertEqual(ids, ['UC123', 'UC456', 'UC789'])

if __name__ == "__main__":
    unittest.main()
