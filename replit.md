# Agenda Escolar — Django 5.2

## Objetivo
Sistema de acompanhamento de eventos escolares. Faz scraping da plataforma Bernoulli com Playwright, armazena eventos em SQLite, e envia notificações WhatsApp via Evolution API.

## Stack
- **Backend**: Django 5.2 + SQLite
- **Scraping**: Playwright (async)
- **WhatsApp**: Evolution API (desativado temporariamente)
- **Frontend**: Bootstrap 5 + Bootstrap Icons
- **Deploy**: gunicorn (produção), manage.py runserver (dev)

## Estrutura de Apps
- `agenda/` — app principal: modelos, views, serviços, admin
- `evolution/` — integração com Evolution API para WhatsApp
- `core/` — configurações Django e urls raiz

## Modelos
- `Escola` — escolas cadastradas
- `Turma` — turmas vinculadas à escola
- `Aluno` — alunos com telefone/email
- `ConexaoAgenda` — credenciais Bernoulli por turma (campo `ativo`)
- `AgendaEvento` — eventos scraped (título, data, tipo, hash único)
- `TarefaCompleta` — aluno + evento, marca se concluído (unique_together)
- `WhatsAppEnvio` — controle de envios por turma+hash

## URLs principais
- `/` — home (requer login para ver painel)
- `/login/` — login customizado
- `/logout/` — logout
- `/register/` — cadastro
- `/tarefas/<aluno_id>/` — lista de tarefas do aluno com botão AJAX
- `/tarefa/concluir/` — endpoint AJAX para marcar/desmarcar tarefa
- `/admin/` — Django Admin com todos os modelos registrados

## Serviços
- `agenda/services/sync_agenda.py` — sincroniza eventos via scraping
- `agenda/services/envio_service.py` — agrupa e envia mensagens WhatsApp por turma
- `agenda/services/salvar_eventos_service.py` — salva eventos no banco
- `agenda/agenda_robot.py` — Playwright scraper do Bernoulli

## Configuração
- `ALLOWED_HOSTS = ['*']`
- `CSRF_TRUSTED_ORIGINS` configurado para Replit
- `django.contrib.humanize` em INSTALLED_APPS
- Workflow: `python manage.py runserver 0.0.0.0:5000`

## WhatsApp
- Envio temporariamente desativado em `sync_agenda.py` (comentado)
- Evolution API configurada via env vars `EVOLUTION_API_URL`, `EVOLUTION_API_KEY`, `EVOLUTION_INSTANCE`

## Migrations aplicadas
- 0001_initial
- 0002_conexaoagenda_ativo
- 0003_update_whatsappenvio
- 0004_tarefacompleta
