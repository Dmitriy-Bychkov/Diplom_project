from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from education.models import Material, Section
from exams.models import Exam, Question, Answer

User = get_user_model()


class ExamViewTestCase(TestCase):
    """ Тесты для отображения страницы с экзаменом """

    def setUp(self):
        """ Создаем тестовую базу данных """

        # Создание пользователя
        self.student = User.objects.create(
            email='test@test.com',
            password='testpassword',
            is_staff=False,
            is_student=True
        )

        # Создание раздела
        self.section = Section.objects.create(section_name="New_section")

        # Создание материала
        self.material = Material.objects.create(
            material_name='Material_name',
            section=self.section
        )

        # Создание ответа
        self.answer = Answer.objects.create(text="Test_answer")

        # Создание вопроса
        self.question1 = Question.objects.create(
            text='Test_question_text_1',
            answers=self.answer,
        )
        self.question2 = Question.objects.create(
            text='Test_question_text_2',
            answers=self.answer
        )
        self.exam1 = Exam.objects.create(
            name='New_exam_1',
            material=self.material
        )
        self.exam2 = Exam.objects.create(
            name='New_exam_2',
            material=self.material
        )

        self.url = reverse('exams:exam', kwargs={'exam_id': self.exam1.pk})

    # def test_exam_view_with_valid_exam_id(self):
    #     """
    #     Проверка успешного открытия страницы экзамена с действительным идентификатором экзамена.
    #     """
    #
    #     self.client.force_login(self.student)
    #     response = self.client.get(self.url)

    # Проверка статуса ответа
    # self.assertEqual(response.status_code, 200)

    # # Проверка наличия информации об экзамене на странице
    # self.assertContains(response, self.exam1.exam_name)
    # self.assertContains(response, self.exam1.exam_description)
    #
    # # Проверка наличия вопросов на странице
    # self.assertContains(response, self.question1.question_text)
    # self.assertContains(response, self.question2.question_text)

    # def test_exam_view_with_invalid_exam_id(self):
    #     """
    #     Проверка отображения страницы 404 при использовании недействительного идентификатора экзамена.
    #     """
    #
    #     invalid_exam_id = 1000
    #     url = reverse('exams:exam', kwargs={'exam_id': invalid_exam_id})
    #
    #     self.client.force_login(self.student)
    #     response = self.client.get(url)
    #
    #     # Проверка статуса ответа
    #     self.assertEqual(response.status_code, 404)
    #
    # def test_exam_view_with_unauthenticated_user(self):
    #     """
    #     Проверка перенаправления на страницу входа при попытке доступа к странице экзамена без авторизации.
    #     """
    #
    #     response = self.client.get(self.url)
    #
    #     # Проверка статуса ответа
    #     self.assertEqual(response.status_code, 302)
    #
    #     # Проверка перенаправления на страницу входа
    #     login_url = reverse('login')
    #     self.assertIn(login_url, response.url)
