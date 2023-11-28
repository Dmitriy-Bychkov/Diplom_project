from django.urls import path
from education.apps import EducationConfig
from education.views import IndexView, SectionListView, MaterialListView, MaterialDetailView

app_name = EducationConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('sections/sections_list/', SectionListView.as_view(), name='sections_list'),
    # path('clients/clients_list/', ClientListView.as_view(), name='clients_list'),
    # path('clients/view_client/<int:pk>/', ClientDetailView.as_view(), name='view_client'),
    # path('clients/edit_client/<int:pk>/', ClientUpdateView.as_view(), name='edit_client'),
    # path('clients/delete_client/<int:pk>/', ClientDelete.as_view(), name='delete_client'),
    #
    # path('messages/create_message/', MessageCreateView.as_view(), name='create_message'),
    path('materials/materials_list/', MaterialListView.as_view(), name='materials_list'),
    path('materials/materials_list/<int:section_id>/', MaterialListView.as_view(), name='materials_list_by_section'),
    path('materials/view_material/<int:pk>/', MaterialDetailView.as_view(), name='view_material'),
    # path('messages/edit_message/<int:pk>/', MessageUpdateView.as_view(), name='edit_message'),
    # path('messages/delete_message/<int:pk>/', MessageDelete.as_view(), name='delete_message'),
    #
    # path('mailings/create_mailing/', MailingCreateView.as_view(), name='create_mailing'),
    # path('mailings/mailing_list/', MailingListView.as_view(), name='mailing_list'),
    # path('mailings/view_mailing/<int:pk>/', MailingDetailView.as_view(), name='view_mailing'),
    # path('mailings/edit_mailing/<int:pk>/', MailingUpdateView.as_view(), name='edit_mailing'),
    # path('mailings/edit_mailing_manager/<int:pk>/', MailingUpdateManagerView.as_view(), name='edit_mailing_manager'),
    # path('mailings/delete_mailing/<int:pk>/', MailingDelete.as_view(), name='delete_mailing'),
    # path('mailings/send_mailing/<int:pk>/', MailingSendMessageView.as_view(), name='send_mailing'),
    #
    # path('log/log_list/', LogListView.as_view(), name='log_list'),
]