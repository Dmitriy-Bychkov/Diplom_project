from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView
from exams.models import Exam
from exams.services import calculate_exam_results


class ExamView(View):
    """ Контроллер для отображения страницы с экзаменом """

    def get(self, request, exam_id):
        """
        Обработчик GET-запроса для отображения страницы с экзаменом.

        Args:
            request (HttpRequest): HTTP-запрос.
            exam_id (int): Идентификатор экзамена.

        Returns:
            HttpResponse: HTTP-ответ с отображением страницы экзамена.
        """

        exam = get_object_or_404(Exam, pk=exam_id)
        questions = exam.questions.all()

        return render(
            request,
            'exams/exam.html',
            {'exam': exam, 'questions': questions}
        )


class ExamResultsView(View):
    """ Контроллер для отображения результатов экзамена """

    def post(self, request, exam_id):
        """
        Обработчик POST-запроса для расчета и отображения результатов экзамена.

        Args:
            request (HttpRequest): HTTP-запрос.
            exam_id (int): Идентификатор экзамена.

        Returns:
            HttpResponse: HTTP-ответ с результатами экзамена.
        """

        exam = get_object_or_404(Exam, pk=exam_id)
        questions = exam.questions.all()

        # Вызов функции calculate_exam_results из services.py
        # для расчета результатов экзамена
        context = calculate_exam_results(request, questions, exam_id)

        return render(request, 'exams/exam_results.html', context)


class ExamListView(LoginRequiredMixin, ListView):
    """
    Контроллер для просмотра списка тестов
    для проверки знаний студентов
    """

    model = Exam
