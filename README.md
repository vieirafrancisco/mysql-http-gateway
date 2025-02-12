# mysql-http-gateway
Serviço HTTP para acesso e gerenciamento de dados em um banco de dados MySQL privado hospedado no Render

## Exemplo de uso:
```bash
curl -X POST -F "file=@/caminho/do/arquivo.sql" http://localhost:5000/execute_sql_file
```

## Em casos de erro:
Ajustar .sql conforme sugerido na mensagem de erro
