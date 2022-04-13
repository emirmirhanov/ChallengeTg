from django.db import models

# Create your models here.


class Members(models.Model):
	name = models.CharField(max_length=20, verbose_name="имя")
	lastname = models.CharField(max_length=20, verbose_name="фамилие")
	user_name = models.CharField(max_length=30, verbose_name="имя пользователя в телеграмме", unique=True)
	live = models.IntegerField(verbose_name="жизнь пользователя")

	def __str__(self):
		return f"{self.user_name}"

	class Meta:
		verbose_name = "Участника"
		verbose_name_plural = "Участники"


class Post(models.Model):
	content = models.TextField(verbose_name="пост")
	active = models.BooleanField(default=False, verbose_name="Состояние")

	class Meta:
		verbose_name = "пост"
		verbose_name_plural = "посты"


class Report(models.Model):
	member = models.ForeignKey(Members, on_delete=models.CASCADE, verbose_name="Имя пользователя")
	time = models.DateTimeField(auto_now_add=True, verbose_name="время добаления")
	type_challenge = models.CharField(max_length=50, verbose_name="тип задания")

	class Meta:
		verbose_name = "отчет"
		verbose_name_plural = "отчеты"

