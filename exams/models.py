from django.db import models
from education.models import Material, NULLABLE


class Answer(models.Model):
    """ Модель ответа """

    text = models.CharField(
        max_length=255,
        verbose_name='ответ'
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'


class QuestionAnswer(models.Model):
    """ Модель связей вопросов и ответов """

    question = models.ForeignKey(
        'exams.Question',
        on_delete=models.CASCADE,
        verbose_name='вопрос'
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        verbose_name='ответ'
    )
    is_correct = models.BooleanField(
        verbose_name='правильный ответ'
    )

    def __str__(self):
        return f'{self.question} - {self.answer}, {self.is_correct}'

    class Meta:
        unique_together = ('answer', 'question')
        verbose_name = 'вопрос-ответ'
        verbose_name_plural = 'вопросы-ответы'


class Question(models.Model):
    """ Модель вопроса """

    text = models.CharField(
        max_length=255,
        verbose_name='вопрос'
    )
    answers = models.ManyToManyField(
        Answer,
        through=QuestionAnswer,
        related_name='questions',
        verbose_name='ответы'
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'


class ExamQuestion(models.Model):
    """ Модель связей тестов и вопросов """

    test = models.ForeignKey(
        'exams.Exam',
        on_delete=models.CASCADE,
        verbose_name='тест'
    )
    question = models.ForeignKey(
        'exams.Question',
        on_delete=models.CASCADE,
        verbose_name='вопрос'
    )

    def __str__(self):
        return f'{self.test} - {self.question}'

    class Meta:
        unique_together = ('test', 'question')
        verbose_name = 'тест-вопрос'
        verbose_name_plural = 'тесты-вопросы'


class Exam(models.Model):
    """ Модель теста """

    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name='материал'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='название теста'
    )
    questions = models.ManyToManyField(
        Question,
        through=ExamQuestion,
        related_name='exams',
        verbose_name='тесты'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'тест'
        verbose_name_plural = 'тесты'
