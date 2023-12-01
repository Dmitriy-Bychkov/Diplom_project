from django.contrib import admin

from exams.models import Answer, QuestionAnswer, Question, ExamQuestion, Exam


class QuestionAnswerInlineAdmin(admin.TabularInline):
    """ Представление инлайн ответов """

    fields = ('question', 'answer', 'is_correct')
    extra = 1
    model = QuestionAnswer


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """ Представление ответов на тесты в админке """

    list_display = ('text',)
    search_fields = ('text',)
    inlines = [QuestionAnswerInlineAdmin]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """ Представление ответов на тесты в админке """

    list_display = ('text',)
    search_fields = ('text',)

    inlines = [QuestionAnswerInlineAdmin]


class ExamQuestionInlineAdmin(admin.TabularInline):
    """ Представление ответов на тесты в админке """

    fields = ('test', 'question')
    extra = 1
    model = ExamQuestion


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    """ Представление ответов на тесты в админке """

    list_display = ('name', 'material')
    search_fields = ('name',)

    inlines = [ExamQuestionInlineAdmin]
