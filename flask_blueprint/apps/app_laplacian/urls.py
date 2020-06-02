
#from django.conf.urls.defaults import patterns, include, url
from django.conf.urls import patterns, url, include
from django.conf import settings
from django.conf.urls.static import static
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from laplacian import views

#from api import QuestionAnswer_Resource, UserResource

# generic views ListView and DetailView - abstract the concepts of "display a list of objects"
# and "display a detail page for a particular type of object."
#urlpatterns = patterns('laplacian.views',
urlpatterns = patterns('',
    #/laplacian
    url(r'^$', views.index_method, name='index_url_name'),

    # /laplacian/rollingcorrelation/pitch/
    url(r'^rollingcorrelation/$', views.correlation_rolling, name='correlation_rolling'),
    url(r'^correlationmatrix/$', views.correlation_matrix, name='correlation_matrix'),
    url(r'^quantlib/$', views.quantlib, name='quantlib'),

    url(r'^list/$', views.list, name='list'),

    url(r'^nlp-resume/$', views.nlp_resume, name='nlp_resume'),
    url(r'^nlp-facebook/$', views.nlp_facebook, name='nlp_facebook'),
    url(r'^nlp-article-blog/$', views.nlp_article_blog, name='nlp_article_blog'),
    url(r'^nlp-twitter/$', views.nlp_twitter, name='nlp_twitter'),

    url(r'^gis-river/$', views.gis_river, name='gis_river'),
    url(r'^gis-rainfall/$', views.gis_rainfall, name='gis_rainfall'),
    url(r'^gis-openlayers-esri/$', views.gis_openlayers_esri, name='gis_openlayers_esri'),
    url(r'^gis-typhoon-tracking/$', views.gis_typhoon_tracking, name='gis_typhoon_tracking'),
    url(r'^gis-openlayers-kml-earthquake/$', views.gis_openlayers_kml_earthquake, name='gis_openlayers_kml_earthquake'),

    url(r'^d3-scatter-dynamic/$', views.d3_scatter_dynamic, name='d3_scatter_dynamic'),
    url(r'^d3-line-histogram-dynamic/$', views.d3_line_histogram_dynamic, name='d3_line_histogram_dynamic'),
    url(r'^d3-geo-satellite-land/$', views.d3_geo_sat_land, name='d3_geo_sat_land'),
    url(r'^d3-geo-satellite-tiles/$', views.d3_geo_sat_tiles, name='d3_geo_sat_tiles'),
    url(r'^d3-geo-projection-earth-torus/$', views.d3_geo_projection_earth_torus, name='d3_geo_projection_earth_torus'),
    url(r'^d3-geo-projection-earth-mollweide/$', views.d3_geo_projection_earth_mollweide, name='d3_geo_projection_earth_mollweide'),

    url(r'^contactme/$', views.contact_me, name='contact_me'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
