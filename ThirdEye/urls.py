"""ThirdEye URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from system import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_views),
    path('index/',views.login_views_submit),
    path('register/',views.register_view),
    path('register/register_submit/',views.register_view_submit),
    path('grading',views.grading,name='grading'),
    path('pat_case',views.pat_case_view,name='pat_case'),
    # path('index/grading/',views.grading),
    path('docList/',views.doc_list_view,name='docList'),
    path('doc_register/',views.doc_register, name='doc_register'),
    path('doc_dealcase/<str:id>', views.doc_dealcase, name='doc_dealcase'),
    path('doc_patlist/', views.doc_patlist, name='doc_patlist'),
    path('doc_patlist_name/', views.findpatname, name='doc_patlist_name'),
    # path('doc_app',)
    path('docAppointment/<int:id>/',views.doc_appointment,name='docAppointment'),

path('set_session/', views.set_session, name='set_session'),
    path('get_session/', views.get_session, name='get_session'),
    path('clear_session/', views.clear_session, name='clear_session')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                        document_root=settings.MEDIA_ROOT)