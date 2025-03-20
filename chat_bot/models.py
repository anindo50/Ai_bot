from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.utils import timezone

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_input = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # auto_now_add ensures the timestamp is set
    title = models.CharField(max_length=255, blank=True, null=True)  # Auto-generated title

    def save(self, *args, **kwargs):
        # Check if title is not set
        if not self.title:
            # Ensure timestamp is set before generating the title
            if self.timestamp is None:
                self.timestamp = timezone.now()  # Set it to the current time if it's not set

            # Generate a default title based on the timestamp
            self.title = f"Conversation {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        
        super().save(*args, **kwargs)

