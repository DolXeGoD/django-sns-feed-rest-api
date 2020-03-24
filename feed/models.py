from django.db import models

# Create your models here.
class Feed(models.Model):
    feed_id = models.AutoField(primary_key=True)
    feed_md_image = models.ImageField(blank=True, null=True)
    feed_md_name = models.CharField(max_length=100)
    feed_content = models.TextField()
    feed_upload_dttm = models.DateTimeField(auto_now_add=True)

    def get_comment_count(self):
        return self.comment_set.count()

    def get_like_count(self):
        return self.like_set.count()

    def get_share_count(self):
        return self.share_set.count()

    class Meta:
        db_table = 'tb_feed'

class Like(models.Model):
    feed_id = models.ForeignKey('Feed', on_delete=models.CASCADE)
    user_id = models.IntegerField()

    class Meta:
        unique_together = ("feed_id", "user_id")
        db_table = 'tb_feed_like'

class Comment(models.Model):
    feed_id = models.ForeignKey('Feed', on_delete=models.CASCADE)
    user_id = models.IntegerField()
    comment = models.CharField(max_length=100)
    upload_dttm = models.DateTimeField(auto_now_add=True)
    update_dttm = models.DateTimeField(auto_now=True)

    def get_user_id(self):
        return self.user_id

    class Meta:
        unique_together = ("feed_id", "user_id")
        db_table = 'tb_feed_comment'

class Share(models.Model):
    feed_id = models.ForeignKey('Feed', on_delete=models.CASCADE)
    share_count = models.IntegerField()

    def get_share_count(self):
        return self.share_count

    class Meta:
        db_table = 'tb_feed_share'