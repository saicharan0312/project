from django.db import models


class Room(models.Model):
    """
    A room for people to chat in.
    """

    # Room title
    title = models.CharField(max_length=255)

    # If only "staff" users are allowed (is_staff on django's User)
    staff_only = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return "room-%s" % self.id


from register.models import User

class Message(models.Model):
    roomid =models.IntegerField()
    author= models.ForeignKey(User,related_name='author_messages',on_delete=models.CASCADE)
    timestamp= models.DateTimeField(auto_now_add=True)
    content =models.TextField()

    def __str__(self):
        return self.author.username

    def last_10_messsages(room):
        print("cool1!")
        o=Message.objects.filter(roomid=room).order_by('timestamp').all()[:10]
        return o