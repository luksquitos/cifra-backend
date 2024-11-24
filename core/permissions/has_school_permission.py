# from rest_framework.permissions import BasePermission

# class HasSchoolPermissions(BasePermission):
#     def _is_authenticated(self, request):
#         return bool(request.user and request.user.is_authenticated)
        
#     def _get_school(self, request, view):
#         if hasattr(view, 'get_school'):
#             return view.get_school(request)
#         return None
    
#     def has_permission(self, request, view):
#         if not self._is_authenticated(request):
#             return False
        
#         if request.method not in ['PATCH', 'PUT', 'POST', 'DELETE']:
#             return True
        
#         school = self._get_school(request, view)
#         if not school:
#             if request.method in ['PATCH']:
#                 return True
#             return False
        
#         user = request.user
#         user_school = user.schools.filter(pk=school.pk).first()
#         return bool(user_school)
