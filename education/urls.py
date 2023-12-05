from django.urls import path
from education.apps import EducationConfig
from education.views import (IndexView, SectionListView,
                             MaterialListView, MaterialDetailView)

app_name = EducationConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('sections_list/', SectionListView.as_view(), name='sections_list'),
    path('materials_list/', MaterialListView.as_view(),
         name='materials_list'
         ),
    path('materials_list/<int:section_id>/', MaterialListView.as_view(),
         name='materials_list_by_section'
         ),
    path('view_material/<int:pk>/', MaterialDetailView.as_view(),
         name='view_material'
         ),
]
