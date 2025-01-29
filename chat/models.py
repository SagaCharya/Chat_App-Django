from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class CustomUser(AbstractUser):
    friends = models.ManyToManyField('self', blank=True, symmetrical=False)

    def send_friend_request(self, to_user):
        """Send a friend request if one doesn't already exist."""
        

    def accept_friend_request(self, from_user):
        """Accept a friend request and add to the friends list."""
        try:
            request = FriendRequest.objects.get(from_user=from_user, to_user=self)
            request.accepted = True
            request.save()
            self.friends.add(from_user)  # Add mutual friendship
            from_user.friends.add(self)  # Ensure both users are friends
        except FriendRequest.DoesNotExist:
            pass
    
    def remove_friend(self, friend):
        """Remove a friend from the friends list."""
        if friend in self.friends.all():
            self.friends.remove(friend)
            friend.friends.remove(self)  # Remove mutual friendship

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

    @receiver(post_save, sender=CustomUser)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    

class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='to_user', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')


class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)