#ALL OTHER MODELS 


from django.db import models
from patient.models import User

GROUP_TYPES = [
    ('One-to-One', 'One-to-One'),
    ('Many-to-Many', 'Many-to-Many')
]

class MessageGroup(models.Model):
    name = models.CharField(max_length=100)
    create_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    groupType = models.CharField(choices=GROUP_TYPES, max_length=10)

    def __str__(self,):
        return str(self.id)

class MessageUserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=None)
    group = models.ForeignKey(MessageGroup, on_delete=None)
    create_date = models.DateTimeField(auto_now_add=True)
    last_message_time = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} in group : {group}'.format(user=str(self.user),group=str(self.group))

    class Meta:
        unique_together = ('user', 'group')

MSG_TYPES = [
    ('TXT', 'TEXT'),
    ('DOC', 'DOCUMENT'),
    ('IMG', 'IMAGE'),
    ('AUD', 'AUDIO'),
    ('VID', 'VIDEO'),
]


class MessageRecipient(models.Model):
    """

    """
    id = models.UUIDField(primary_key=True)
    message = models.ForeignKey(Message, on_delete=None)
    recipient = models.ForeignKey(User, on_delete=None)
    sentAt = models.DateTimeField(auto_now_add=True)
    messageUserGroup = models.ForeignKey(MessageUserGroup, on_delete=None)
    isRead = models.BooleanField(default=False)
    readAt = models.DateTimeField(null=True)
    callbackUrl = models.URLField(null=True)


class Message(models.Model):
    """
    Will store all the messages sent for each campaign,
     relations will be found in MessageRecipient model.
    """
    _id = models.UUIDField(primary_key=True)
    sentAt = models.DateTimeField(auto_now=True)
    messageType = models.CharField(
        max_length=50, choices=MSG_TYPES, default='Unknown', null=False,
    )
    messageBody = models.TextField()
    parent = models.ForeignKey('self', models.SET_NULL, null=True)
    creator = models.ForeignKey(User, on_delete=None, null=True)
    thumbnailURL = models.URLField(null=True)
    attachmentDisplayName = models.CharField(max_length=100, null=True)
    attachmentName = models.CharField(max_length=100, null=True)
    size = models.CharField(max_length=25, null=True)  # bytes
    duration = models.FloatField(null=True)  # seconds
    mimeType = models.TextField(null=True)

    def __str__(self):
        return "%s : %s" % (self.messageType, self.messageBody)

