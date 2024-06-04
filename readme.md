## Install virtual Venv Linux##
     apt install virtual venv 

## Criar Ambiente Virtual ##
     python3 -m venv clone_twitter 

## Ativar o Ambiente Virtual clone_twitter ##
     source clone_twitter/bin/activate

## Visualizar Bibliotecas Instaladas no Ambiente Virtual do Venv e adiciona a um arquivo requirements.txt##
     clone_twitter/bin/pip3 freeze 
     clone_twitter/bin/pip3 freeze > requirements.txt

## Instalar dependencias a partir do requirements.txt ##
     clone_twitter/bin/pip3 install -r requirements.txt

## Criar Repositorio das migraçoes
     flask db init
     flask db migrate -m "Initial migration."

## Aplica mudanças descritas pelo script de migração
     flask db update