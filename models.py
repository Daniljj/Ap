from django.contrib.auth.models import User
from django.db import models

# cd mysite
# python manage.py makemigrations - найти новые миграции
# python manage.py showmigrations - показать найденные миграции
# python manage.py migrate myauth - произвести миграцию для отдельного приложения
# python manage.py migrate shopapp 0002 - откат к необходимой миграции (можно и вперед и назад)


def profile_preview_directory_path(insctace: "Profile", filename: str) -> str:
    return "profiles/profile_{pk}/avatar/{filename}".format(
        pk=insctace.pk,
        filename=filename,
    )


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accapted = models.BooleanField(default=False)
    avatar = models.ImageField(
        null=True, blank=True, upload_to=profile_preview_directory_path
    )

    def __str__(self):
        return self.user.username  # Возвращает имя пользователя

    def get_username(self):
        """Возвращает имя пользователя."""
        return self.user.username
