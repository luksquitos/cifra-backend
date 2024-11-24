# from rest_framework.permissions import BasePermission

# class HasAtLeastOneSchool(BasePermission):
#     def _is_authenticated(self, request):
#         return bool(request.user and request.user.is_authenticated)
        
#     def has_permission(self, request, view):
#         if not self._is_authenticated(request):
#             return False
        
#         user = request.user
#         user_schools = len(user.schools.all())

#         return user_schools > 0
