from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, phone_number,first_name, last_name, password):
        if not email:
            raise ValueError('user must have email')
        
        if not phone_number:
            raise ValueError('user must have phone number')
        
        user = self.model(email=self.normalize_email(email), phone_number=phone_number, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.is_worker = False
        user.save(using=self._db)
        return user
    
    def create_workeruser(self, email, phone_number, first_name, last_name, gender, workerID, password):
        if not email:
            raise ValueError('user must have email')
        
        if not phone_number:
            raise ValueError('user must have phone number')
        
        if not workerID:
            raise ValueError('user must have worker id')
        
        user = self.model(email=self.normalize_email(email), phone_number=phone_number, first_name=first_name, last_name=last_name, gender=gender, workerID=workerID)
        user.set_password(password)
        user.is_worker = True
        user.save(using=self._db)
        return user
    

    def create_customeruser(self, email, phone_number, first_name, last_name, gender, password):
        if not email:
            raise ValueError('user must have email')
        
        if not phone_number:
            raise ValueError('user must have phone number')
        
        user = self.model(email=self.normalize_email(email), phone_number=phone_number, first_name=first_name, last_name=last_name, gender=gender)
        user.set_password(password)
        user.is_worker = False
        user.save(using=self._db)
        return user
    

    def create_superuser(self, email, phone_number, password):
        user = self.create_user(email, phone_number, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user