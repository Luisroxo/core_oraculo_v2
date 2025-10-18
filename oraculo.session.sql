SELECT video_id, LENGTH(transcricao) AS tamanho
FROM transcricoes
WHERE video_id IN ('abc', 'def', 'ghi', ... , 'xyz')
  AND transcricao IS NOT NULL AND transcricao != '';