from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from django.contrib import admin

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	# url(r'^', include('home.urls'))
    url(r'^home/', include('qalearn.home.urls')),
    url(r'^$', RedirectView.as_view(url='/home/', permanent=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
