# mysql-http-gateway
Serviço HTTP para acesso e gerenciamento de dados em um banco de dados MySQL privado hospedado no Render

## Exemplo de uso:
```bash
curl -X POST -F "file=@/caminho/do/arquivo.txt" http://localhost:5000/load_mysql_data
```

## Em casos de erro:
Ajustar .sql conforme sugerido na mensagem de erro
