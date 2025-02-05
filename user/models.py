from django.db import models
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    friends = models.ManyToManyField('self', blank=True, symmetrical=False)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    token_created_at = models.DateTimeField(blank=True, null=True)

    def accept_friend_request(self, from_user):
        
        
        try:
            from chat.models import FriendRequest
            request = FriendRequest.objects.get(from_user=from_user, to_user=self)
            request.accepted = True
            request.save()
            self.friends.add(from_user)  
            from_user.friends.add(self)  
        except FriendRequest.DoesNotExist:
            pass
    
    def remove_friend(self, friend):
        if friend in self.friends.all():
            self.friends.remove(friend)
            friend.friends.remove(self)  

    def __str__(self):
        return self.username