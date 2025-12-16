from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permissão personalizada:
    - Administrador: pode fazer tudo (GET, POST, PUT, DELETE)
    - Anónimo: apenas consultar (GET)
    """
    
    def has_permission(self, request, view):
        """
        Este método é chamado pelo DRF sempre que chega um pedido à API
        Aqui, vamos verificar se o utilizador pode fazer este tipo de operação ou não.
        """
        
        # 1º: Verifica se é um método seguro (GET, HEAD, OPTIONS) (apenas leitura)
        if request.method in permissions.SAFE_METHODS:
            # Qualquer um pode fazer GET (ler)
            # Retorna True = deixa passar
            return True
        
        # Para métodos que alteram os dados (POST, PUT, DELETE):
        # Apenas os utilizadores autenticados e com permissões de admin
        return request.user and request.user.is_authenticated and request.user.is_staff