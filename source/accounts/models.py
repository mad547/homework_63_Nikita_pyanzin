from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другой'),
    ]

    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    avatar = models.ImageField(
        upload_to='avatars',
        null=True,
        blank=True,
        verbose_name='Аватар'
    )
    bio = models.TextField(
        null=True,
        blank=True,
        verbose_name='Информация о себе'
    )
    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='Телефон'
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
        verbose_name='Пол'
    )
    posts_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Публикации'
    )
    followers_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Подписчики'
    )
    following_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Подписки'
    )

    def __str__(self):
        return f'Профиль {self.user.username}'

    class Meta:
        db_table = 'profile'
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class Follow(models.Model):
    follower = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Подписан на'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата подписки'
    )

    class Meta:
        db_table = 'follow'
        unique_together = ['follower', 'following']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.follower.username} → {self.following.username}'