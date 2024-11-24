# from rest_framework.permissions import BasePermission
# from features.school.models import SchoolEmployee

# class IsSchoolEmployee(BasePermission):
#     positions = ["teacher", "coordinator", "food", "administrative"]
#     allowed_methods = ["GET", "POST", "PATCH", "PUT", "DELETE"]
    
#     def is_authenticated(self, request):
#         return bool(request.user.is_authenticated)
    
#     def has_permission(self, request, view):
#         if request.method not in self.allowed_methods:
#             return False

#         if self.is_authenticated(request):
#             is_employee = SchoolEmployee.objects.filter(
#                 user=request.user,
#                 position__in=self.positions
#             ).exists()
            
#             if is_employee: 
#                 self.change_view(request, view)

#             return bool(is_employee)
    
#         return False
    
#     def change_view(self, request, view):
#         """
#         This is going to be used if are necessary
#         to change the queryset or serializers 
#         methods in some view.
#         """
#         pass
        


# class IsAdministrative(IsSchoolEmployee):
#     positions = ["administrative"]

# class IsTeacher(IsSchoolEmployee):
#     positions = ["teacher"]
    
#     def change_view(self, request, view):
#         """
#         A lot of cases we need to know
#         who are acessing the endpoint.
#         Because teachers can't do
#         everything that a Admin can.
#         """
#         view.teacher = SchoolEmployee.objects.get(
#             user=request.user, 
#             position__in=self.positions
#         )

# class IsCoordinator(IsSchoolEmployee):
#     positions = ["coordinator"]

# class IsFood(IsSchoolEmployee):
#     positions = ["food"]
