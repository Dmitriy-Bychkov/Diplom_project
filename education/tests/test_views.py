from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from education.models import Section, Material
from exams.models import Exam

User = get_user_model()


class IndexViewTests(TestCase):
    """ Тесты для контроллера IndexView """

    def setUp(self):
        """ Создаем тестовую базу данных """

        self.student = User.objects.create(
            email='test@test.com',
            password='testpassword',
            first_name='Dmitriy',
            is_staff=False,
            is_student=True
        )
        self.section = Section.objects.create(section_name="Новый раздел")
        self.material = Material.objects.create(
            material_name='Test Material',
            section=self.section
        )
        self.exam = Exam.objects.create(
            material=self.material,
            name='Exam_name'
        )
        self.url = reverse("education:index")

    def test_for_anonymous_users(self):
        """
        Проверка редиректа на страницу логина,
        для неавторизованных пользователей
        """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        expected_text = \
            'Для дальнейшей работы необходима регистрация в нашем сервисе.'

        self.assertContains(response, expected_text)

    def test_response_for_authorized_users(self):
        """
        Проверка успешного открытия главной страницы
        для авторизованного пользователя
        и наличия контента для него
        """

        self.client.force_login(self.student)
        response = self.client.get(self.url)
        expected_text = f'Приветствуем тебя, {self.student.first_name}!'

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, expected_text)

    def test_context(self):
        """ Проверка контекста главной страницы """

        url = reverse('education:index')
        response = self.client.get(url)
        context = response.context

        # Проверка заголовка страницы
        self.assertEqual(context['title'], 'Главная страница')

        # Проверка количества образовательных разделов
        self.assertEqual(context['total_sections'], 1)

        # Проверка количества всех загруженных материалов
        self.assertEqual(context['total_materials'], 1)

        # Проверка количества зарегистрированных студентов
        self.assertEqual(context['registered_students'], 1)

        # Проверка количества всех загруженных тестов
        self.assertEqual(context['total_exams'], 1)


class SectionListViewTests(TestCase):
    """ Тесты для контроллера SectionListView """

    def setUp(self):
        """ Создаем тестовую базу данных """

        self.student = User.objects.create(
            email='test@test.com',
            password='testpassword',
            is_staff=False,
            is_student=True
        )
        self.section = Section.objects.create(section_name="Новый раздел")
        self.url = reverse("education:sections_list")

    def test_redirect_to_login(self):
        """
        Проверка редиректа на страницу логина,
        для неавторизованных пользователей
        """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

        expected_url = reverse("users:login") + "?next=" + self.url
        self.assertEqual(response.url, expected_url)

    def test_response_success(self):
        """
        Проверка успешного открытия страницы разделов
        для авторизованного пользователя
        """

        self.client.force_login(self.student)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_page_content(self):
        """ Проверка наличия контента на странице разделов """

        self.client.force_login(self.student)
        response = self.client.get(self.url)

        self.assertContains(response, self.section.section_name)


class MaterialListViewTestCase(TestCase):
    """ Тесты для списка материалов """

    def setUp(self):
        """ Создаем тестовую базу данных """

        self.student = User.objects.create(
            email='test@test.com',
            password='testpassword',
            is_staff=False,
            is_student=True
        )
        self.section = Section.objects.create(section_name="Новый раздел")
        self.material1 = Material.objects.create(
            material_name='Test Material 1',
            section=self.section
        )
        self.material2 = Material.objects.create(
            material_name='Test Material 2',
            section=self.section
        )
        self.url = reverse('education:materials_list')

    def test_redirect_to_login(self):
        """
        Проверка редиректа на страницу логина,
        для неавторизованных пользователей
        """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

        expected_url = reverse("users:login") + "?next=" + self.url
        self.assertEqual(response.url, expected_url)

    def test_materials_list_from_index_page(self):
        """
        Проверка успешного открытия страницы материалов
        для авторизованного пользователя
        из главной страницы и наличия контента для него
        """

        self.client.force_login(self.student)
        response = self.client.get(self.url)
        expected_text1 = 'Все доступные материалы'
        expected_text2 = f'{self.material1.material_name}'

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, expected_text1)
        self.assertContains(response, expected_text2)

    def test_material_list_from_section_page(self):
        """
        Проверка успешного открытия страницы материалов
        для авторизованного пользователя
        из страницы разделов и наличия контента для него
        """

        self.client.force_login(self.student)
        url = reverse(
            'education:materials_list_by_section',
            kwargs={'section_id': self.section.id}
        )
        response = self.client.get(url)
        context = response.context['material_list']
        expected_text1 = \
            (f'Материалы из раздела '
             f'<u>{self.section.section_name}</u>'
             )
        expected_text2 = f'{self.material2.material_name}'

        # Проверка статуса ответа
        self.assertEqual(response.status_code, 200)

        # Проверка шаблона
        self.assertTemplateUsed(response, 'education/material_list.html')

        # Проверка количества созданных материалов
        self.assertEqual(len(context), 2)

        # Проверка контекста
        self.assertIn(self.material1, context)
        self.assertIn(self.material2, context)
        self.assertContains(response, expected_text1)
        self.assertContains(response, expected_text2)

    def test_material_list_from_section_page_invalid_id(self):
        """
        Проверка списка материалов из страницы разделов
        с недопустимым идентификатором раздела
        """

        self.client.force_login(self.student)
        invalid_section_id = 999
        url = reverse(
            'education:materials_list_by_section',
            kwargs={'section_id': invalid_section_id}
        )
        response = self.client.get(url)

        # Проверка статуса ответа
        self.assertEqual(response.status_code, 404)


class MaterialDetailViewTests(TestCase):
    """
    Тесты для контроллера MaterialDetailView -
    подробного просмотра материала
    """

    def setUp(self):
        """ Создаем тестовую базу данных """

        self.student = User.objects.create(
            email='test@test.com',
            password='testpassword',
            is_staff=False,
            is_student=True
        )
        self.section = Section.objects.create(section_name="Новый раздел")
        self.material = Material.objects.create(
            material_name='Test Material',
            section=self.section
        )
        self.url = reverse(
            "education:view_material",
            kwargs={'pk': self.material.pk}
        )

    def test_redirect_to_login(self):
        """
        Проверка редиректа на страницу логина,
        для неавторизованных пользователей
        """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

        expected_url = reverse("users:login") + "?next=" + self.url
        self.assertEqual(response.url, expected_url)

    def test_response_success(self):
        """
        Проверка успешного открытия страницы просмотра
        материала для авторизованного пользователя
        """

        self.client.force_login(self.student)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_page_content(self):
        """ Проверка наличия контента на странице просмотра материала """

        self.client.force_login(self.student)
        response = self.client.get(self.url)

        self.assertContains(response, self.material.section.section_name)
        self.assertContains(response, self.material.material_name)
