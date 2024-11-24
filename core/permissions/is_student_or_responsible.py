# from rest_framework.permissions import BasePermission
# from features.student.models import Student, StudentResponsible


# class IsStudent(BasePermission):
#     allowed_methods = ["GET", "POST", "PATCH", "PUT", "DELETE"]

#     def is_authenticated(self, request):
#         return bool(request.user.is_authenticated)

#     def has_permission(self, request, view):
#         if request.method not in self.allowed_methods:
#             return False

#         if self.is_authenticated(request):
#             is_student = Student.objects.filter(user=request.user).exists()
            
#             if is_student:
#                 self.change_view(request, view)
            
#             return bool(is_student)
        
#         return False

#     def change_view(self, request, view):
#         view.student = Student.objects.get(user=request.user)
        

# class IsResponsible(BasePermission):
#     allowed_methods = ["GET", "POST", "PATCH", "PUT", "DELETE"]
    
#     def is_authenticated(self, request):
#         return bool(request.user.is_authenticated)

#     def has_permission(self, request, view):
#         if request.method not in self.allowed_methods:
#             return False
        
#         if self.is_authenticated(request):
#             is_responsible = StudentResponsible.objects.filter(user=request.user).exists()
            
#             if is_responsible:
#                 self.change_view(request, view)
            
#             return bool(is_responsible)
        
#         return False

#     def change_view(self, request, view):
#         responsible_student = StudentResponsible.objects.get(user=request.user)
#         view.students = responsible_student.students.all()