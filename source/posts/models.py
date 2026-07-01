from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    image = models.ImageField(
        upload_to='posts',
        null=False,
        blank=False,
        verbose_name='Изображение'
    )
    caption = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    likes_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Лайки'
    )
    comments_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Комментарии'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    def __str__(self):
        return f'Пост {self.author.username} от {self.created_at.strftime("%d.m.%Y")}'

    class Meta:
        db_table = 'post'
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-created_at']


class Like(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Пользователь'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Публикация'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата лайка'
    )

    class Meta:
        db_table = 'like'
        unique_together = ['user', 'post']
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class Comment(models.Model):
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация'
    )
    text = models.TextField(
        null=False,
        blank=False,
        verbose_name='Текст'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата'
    )

    def __str__(self):
        return f'Комментарий {self.author.username}'

    class Meta:
        db_table = 'comment'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']