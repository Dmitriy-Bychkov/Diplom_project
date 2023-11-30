from django.contrib import admin

from exams.models import Answer, QuestionAnswer, Question, ExamQuestion, Exam


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """ Представление ответов на тесты в админке """

    list_display = ('text',)
    search_fields = ('text',)


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    """ Представление ответов на тесты в админке """

    list_display = ('question', 'answer', 'is_correct')
    search_fields = ('is_correct',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """ Представление ответов на тесты в админке """

    list_display = ('text',)
    search_fields = ('text',)


@admin.register(ExamQuestion)
class ExamQuestionAdmin(admin.ModelAdmin):
    """ Представление ответов на тесты в админке """

    list_display = ('test', 'question')
    search_fields = ('test',)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    """ Представление ответов на тесты в админке """

    list_display = ('name', 'material')
    search_fields = ('name',)
