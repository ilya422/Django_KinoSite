from django.db import models
from django.urls import reverse


def film_photos_directory_path(instance, filename):
    return f"films/photos/{instance.film.id}/{filename}"


def staff_photos_directory_path(instance, filename):
    return f"staff/photos/{instance.staff.id}/{filename}"


# Create your models here.

class Countries(models.Model):
    """
    Модель стран
    """
    class Meta:
        verbose_name = 'Страны'
        verbose_name_plural = verbose_name
        ordering = ['name']

    name = models.CharField(max_length=255, unique=True, verbose_name="Название")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class FilmGenres(models.Model):
    """
    Модель жанров фильмов
    """
    class Meta:
        verbose_name = 'Жанры фильмов'
        verbose_name_plural = verbose_name
        ordering = ['name']

    name = models.CharField(max_length=255, unique=True, verbose_name="Название")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменено")

    def __str__(self):
        return self.name


class FilmPhotoTypes(models.Model):
    """
    Модель типов фото для фильмов
    """
    class Meta:
        verbose_name = 'Типы фото фильмов'
        verbose_name_plural = verbose_name
        ordering = ['name']

    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменено")

    def __str__(self):
        return self.name


class FilmStaff(models.Model):
    """
    Модель рабочих над фильмами
    """
    class Meta:
        verbose_name = 'Рабочие над фильмом'
        verbose_name_plural = verbose_name
        ordering = ['-created_at', 'full_name']

    full_name = models.CharField(max_length=255, verbose_name="Полное имя")
    birthday = models.DateField(verbose_name="Дата рождения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменено")

    def __str__(self):
        return self.full_name


class FilmStaffTypes(models.Model):
    """
    Модель типов рабочих над фильмами
    """
    class Meta:
        verbose_name = 'Типы рабочих над фильмом'
        verbose_name_plural = verbose_name
        ordering = ['name']


    name = models.CharField(max_length=255, unique=True, verbose_name="Название")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменено")

    def __str__(self):
        return self.name


class FilmStaffPhotos(models.Model):
    """
    Модель фото рабочих над фильмами
    """
    class Meta:
        verbose_name = 'Фотографии рабочих над фильмами'
        verbose_name_plural = verbose_name
        ordering = ['created_at']


    staff = models.ForeignKey(
        "FilmStaff",
        on_delete=models.CASCADE,
        verbose_name="Работник"
    )
    is_main = models.BooleanField(default=False, verbose_name="Главное фото")
    image = models.ImageField(upload_to=staff_photos_directory_path, verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменено")

    def __str__(self):
        return f"{self.staff.name}/{self.image.name}"


class FilmPhotos(models.Model):
    """
    Модель фото фильмов
    """
    class Meta:
        verbose_name = 'Фото фильмов'
        verbose_name_plural = verbose_name
        ordering = ['created_at']

    film = models.ForeignKey(
        "Films",
        on_delete=models.CASCADE,
        verbose_name="Фильм"
    )
    type = models.ForeignKey(
        "FilmPhotoTypes",
        on_delete=models.CASCADE,
        verbose_name="Тип фото"
    )
    is_main = models.BooleanField(default=False, verbose_name="Главное фото?")
    image = models.ImageField(upload_to=film_photos_directory_path, verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменено")

    def __str__(self):
        return f"{self.film.name}/{self.type.name}/{self.image.name}"


class Films(models.Model):
    """
    Модель фильмов
    """
    class Meta:
        verbose_name = 'Фильмы'
        verbose_name_plural = verbose_name
        ordering = ['released_at', 'name']


    name = models.CharField(max_length=255, verbose_name="Название")
    title = models.TextField(verbose_name="Описание")
    released_at = models.DateField(verbose_name="Дата выпуска")
    staff = models.ManyToManyField(
        FilmStaff,
        through="FilmStaffAssociations"
    )
    counties = models.ManyToManyField(
        Countries,
        through="FilmCountriesAssociations"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменено")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/'
        return reverse('film', kwargs={'film_id': self.pk})


# region Associations

class FilmStaffAssociations(models.Model):
    """
    Модель многие ко многим для фильмов и рабочих
    """
    class Meta:
        verbose_name = 'Связи фильмов и рабочих'
        verbose_name_plural = verbose_name
        ordering = ['created_at']

        constraints = [models.UniqueConstraint(fields=('staff', 'film', 'staff_type'), name='film_staff_unique_key')]

    staff = models.ForeignKey(
        "FilmStaff",
        on_delete=models.CASCADE,
        verbose_name="Работник"
    )
    film = models.ForeignKey(
        "Films",
        on_delete=models.CASCADE,
        verbose_name="Фильм"
    )
    staff_type = models.ForeignKey(
        "FilmStaffTypes",
        on_delete=models.CASCADE,
        verbose_name="Тип работника"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменено")

    def __str__(self):
        return f"{self.film.name} - {self.staff.full_name}"

class FilmCountriesAssociations(models.Model):
    """
    Модель многие ко многим для фильмов и стран
    """
    class Meta:
        verbose_name = 'Связи фильмов и стран'
        verbose_name_plural = verbose_name
        ordering = ['created_at']

        constraints = [models.UniqueConstraint(fields=('country', 'film'), name='film_country_unique_key')]

    country = models.ForeignKey(
        "Countries",
        on_delete=models.CASCADE,
        verbose_name="Страна"
    )
    film = models.ForeignKey(
        "Films",
        on_delete=models.CASCADE,
        verbose_name="Фильм"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменено")

    def __str__(self):
        return f"{self.film.name} - {self.country.name}"

class FilmGenresAssociations(models.Model):
    """
    Модель многие ко многим для фильмов и жанров
    """
    class Meta:
        verbose_name = 'Связи фильмов и жанров'
        verbose_name_plural = verbose_name
        ordering = ['created_at']

        constraints = [models.UniqueConstraint(fields=('genre', 'film'), name='film_genre_unique_key')]

    genre = models.ForeignKey(
        "FilmGenres",
        on_delete=models.CASCADE,
        verbose_name="Жанр"
    )
    film = models.ForeignKey(
        "Films",
        on_delete=models.CASCADE,
        verbose_name="Фильм"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменено")

    def __str__(self):
        return f"{self.film.name} - {self.genre.name}"

# endregion
