from rest_framework.permissions import BasePermission

class AdminOuLeitura(BasePermission):

    def has_permission(self, request, view):
        # Se a view não for um ViewSet (ex: APIView simples),
        # ela pode não ter o atributo 'action'
        action = getattr(view, "action", None)

        #  Todo mundo pode listar ou ver detalhes de um item específico
        if action in ["list", "retrieve"]:
            return True

        # criar (create)
        # atualizar (update/partial_update) 
        # deletar (destroy) exigem Admin autenticado
        return (
            request.user.is_authenticated
            and request.user.is_staff
        )
    
class AdminOuCria(BasePermission):

    def has_permission(self, request, view):
        action = getattr(view, "action", None)

        #  Qualquer usuário (mesmo anônimo) pode enviar/criar uma solicitação
        if action == "create":
            return True

        # Ver listas, ver detalhes, editar ou deletar exige ser Admin
        return (
            request.user.is_authenticated
            and request.user.is_staff
        )