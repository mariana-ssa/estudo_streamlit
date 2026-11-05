# estudo_streamlit

O App financeiro feito com [Streamlit](https://streamlit.io/) foi desenvolvido durante os estudos com o [Téo Me Why](https://www.youtube.com/watch?v=JLcEWe7woVk&list=PLvlkVRRKOYFRYA40hJ_V8e_iC5Lu6YPyn).

O app permite fazer upload de um CSV de controle financeiro e visualizar os dados por instituição, estatísticas mensais (diferenças absolutas/relativas e médias móveis) e um planejamento de metas com atualização pela taxa Selic (consultada na API do Banco Central).


## Formato do arquivo CSV

O app espera o arquivo csv que foi passado durante o curso: [arquivo](https://www.youtube.com/redirect?event=video_description&redir_token=QUlxb01IYmNsX3BtcTNfM0RZNDI5M0xPUUpPRHxBSTVJdTVzaTRicjdPMGVKam53QVh2MUw4dW5PQnc3WXFUaF9HWGhoZURfTEZXd3N1eUlhLWxIazc4YzRCTUNBcDdQdDBzQ1JNc1hpLUxvRzRwVDVvZzlrcFFTeUt5TWxNYzJk&q=https%3A%2F%2Fdocs.google.com%2Fspreadsheets%2Fd%2F1-t9KenqGfLNrd8UJ79xS7eaq42ed95E7jf0VnavGuoA%2Fedit%3Fgid%3D720500922%23gid%3D720500922&v=FbI03HzijoA)

## Como executar

### Opção 1: Local com Python

1. Crie e ative o ambiente virtual:

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Rode o app:

   ```bash
   streamlit run main.py
   ```

5. Acesse no navegador: http://localhost:8501

### Opção 2: Docker Compose

Com Docker e Docker Compose instalados, rode na raiz do projeto:

```bash
docker compose up --build
```

Depois acesse http://localhost:8501

O `main.py` é montado como volume, então alterações no arquivo são refletidas sem precisar reconstruir a imagem (basta recarregar a página do Streamlit).

Para parar:

```bash
docker compose down
```