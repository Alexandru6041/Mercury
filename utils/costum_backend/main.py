from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class MyBackend(BaseBackend):
    
    def authenticate(request, username = None, password = None):
        try:
            user = User.objects.get(email = username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username = username)
            except User.DoesNotExist:
                return None
        
        if user.check_password(password):
            return user
        
        return None
    
    
    def validate_password(password, user = None):
        error_messages = []
        
        try:
            validate_password(password, user)
        except ValidationError as e:
            for i in range(len(e.messages)):
                error_messages.append(e.messages[i])
        
        return error_messages