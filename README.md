# README #

Projeto para gestão dos dados coletados pelo IFAG

## Requisitos de sistema ###

* Debian 8.5 ou compativel
* Postgres 9.4 ou compativel
* Python 3.6

## Instalação ###

### Configuração do crontab
```
# IFAG Calculo de média dos indicadores
*/5 * * * * /var/www/dados.ifag.org.br/venv/bin/python /var/www/dados.ifag.org.br/manage.py calculateavg --settings project.settings.dados
```

@TODO