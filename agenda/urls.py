from django.urls import path
from .views import views_user
from .views import views_tarefas

app_name = 'cal'

urlpatterns = [
    path('', views_user.home, name='home'),
    path('contato/', views_user.contato, name='contato'),
    path('manual/', views_user.manual_publico, name='manual_publico'),

    # Tarefas
    path('tarefas/<int:aluno_id>/', views_tarefas.listar_tarefas, name='listar_tarefas'),
    path('tarefa/concluir/', views_tarefas.marcar_concluida, name='marcar_concluida'),
]
