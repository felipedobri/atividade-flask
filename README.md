
## Atualizar o sistema e instalar dependências

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-venv python3-pip git
```

### Clonar o repositório

```bash
cd ~
git clone https://github.com/felipedobri/atividade-flask.git
cd atividade-flask
```

### Criar e ativar o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### Instalar as dependências

```bash
pip install -r requirements.txt
```

### Testar manualmente

```bash
python app.py
```

### Criar o serviço systemd

```bash
sudo nano /etc/systemd/system/flask-app.service
```

Colar:

```ini
[Unit]
Description=Flask Atividade 3
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/atividade-flask
ExecStart=/home/ubuntu/atividade-flask/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Habilitar e iniciar o serviço

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now flask-app
```