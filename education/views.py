from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import TemplateView, ListView, DetailView
from education.models import Section, Material
from exams.models import Exam
from users.models import User


class IndexView(TemplateView):
    """ Контроллер для отображения главной страницы сервиса """

    template_name = 'education/index.html'

    def get_context_data(self, **kwargs):
        """
        Переопределение метода get_context_data для получения
        дополнительных переменных контекста при использовании их в шаблоне
        """

        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'

        # Получение количества образовательных разделов
        total_sections = Section.objects.count()
        context['total_sections'] = total_sections

        # Получение количества всех загруженных материалов
        total_materials = Material.objects.count()
        context['total_materials'] = total_materials

        # Получение количества зарегистрированных студентов
        registered_students = User.objects.filter(is_staff=False).count()
        context['registered_students'] = registered_students

        # Получение количества всех загруженных тестов
        total_exams = Exam.objects.count()
        context['total_exams'] = total_exams

        return context


class SectionListView(LoginRequiredMixin, ListView):
    """ Контроллер для просмотра списка разделов """

    model = Section


class MaterialListView(LoginRequiredMixin, ListView):
    """ Контроллер для просмотра списка материалов """

    model = Material
    template_name = 'education/materials_list.html'
    context_object_name = 'material_list'

    def get_context_data(self, **kwargs):
        """
        Переопределение метода get_context_data для получения
        дополнительных переменных контекста при использовании их в шаблоне
        """

        context = super().get_context_data(**kwargs)
        section_id = self.kwargs.get('section_id')
        if section_id:
            try:
                section = Section.objects.get(id=section_id)
            except Section.DoesNotExist:
                raise Http404()

            context['section'] = section
        return context

    def get_queryset(self):
        """
        Переопределение метода get_queryset для фильтрации
        материалов, принадлежащих определенному разделу
        """

        queryset = super().get_queryset()

        # Получаем идентификатор раздела из URL
        section_id = self.kwargs.get('section_id')
        if section_id:
            # Фильтруем материалы по идентификатору раздела
            queryset = queryset.filter(section__id=section_id)
        return queryset


class MaterialDetailView(LoginRequiredMixin, DetailView):
    """ Контроллер для детального просмотра материала """

    model = Material
