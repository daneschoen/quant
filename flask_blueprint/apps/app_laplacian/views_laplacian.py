import sys, os
import json, datetime, calendar  # from datetime import timedelta, timezone
import pytz  # from pytz import utc, timezone
import string, re
from pprint import pprint

import copy
import html.parser   # python 3.0
from operator import itemgetter

from flask import render_template, request, redirect, url_for, g, \
    abort, session, flash, logging, make_response, Response, jsonify

from flask_login import login_user, logout_user, current_user, login_required, \
    confirm_login, fresh_login_required

from flask_restful import reqparse, abort, Resource, Api, fields   #, marshal_with

import requests
#import urllib.parse
#from bson.objectid import ObjectId

from apps import app
from apps import cache, redis_db, PLOT_ROUTES

from . import app_laplacian

# from apps.app_util import mongodb

from apps.settings.constants import *

from . import stock_covariance as pd_utils
from .nlp_frequency_words import analyze_frequency_words, get_uploaded_file


"""
import sys, os
import json

from django.shortcuts import render, render_to_response, get_object_or_404

#from qna.models import Question, Answer

from django.http import Http404, HttpResponse, HttpResponseRedirect
#from django.template import Context, loader   #not needed since using render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from laplacian.models import Document
from laplacian.forms import DocumentForm

# -------------
# DJANGO views
# -------------
#
# http://127.0.0.1:8000/laplacian/
#
def index_method(request):
    # Test
    # return HttpResponse("Hello, world. You're at the poll index.")

    #latest_question_list = Question.objects.all().order_by('-pub_date')[:5]

    # Heuristic
    #output = ' > '.join([q.question_text for q in latest_question_list])
    #return HttpResponse(output)

    # 1) long way
    # Load the template "polls/index.html" and passes it a context. The context is a dictionary mapping template variable names to Python objects.
    # template = loader.get_template('polls/index.html')
    # c = Context({
    #     'latest_poll_list': latest_poll_list,
    # })
    # return HttpResponse(template.render(c))

    # 2) shorter
    # context = {'latest_poll_list': latest_poll_list}
    # return render_to_response('polls/index.html', {'latest_poll_list': latest_poll_list})

    # 3)
    return render(request, 'laplacian/index.html')
"""

@app_laplacian.route("/")
def index():
    #return render_template('index_laplacian.html')
    return render_template('index_geo.html')

@app_laplacian.route("aboutme")
def aboutme():
    #return render_template('index_laplacian.html')
    return render_template('aboutme.html')


@app_laplacian.route('pitch_private')
def pitch_private():
    return render_template('pitch_private.html')

#@app_quant.route('whitepaper')
#def whitepaper():
#    return render_template('quant_fintech_whitepaper.html')


@app_laplacian.route('presentation_finance_platform')
def presentation_finance_platform():
    return render_template('quantcypher_finance_platform.html')


@app_laplacian.route('presentation_datascience')
def presentation_datascience():
    return render_template('quantcypher_datascience.html')


# ---------------------------------------

@app_laplacian.route("ml_zemletryaseniye")
def ml_zemletryaseniye():
    return render_template('aboutme.html')

@app_laplacian.route("ml_health")
def ml_health():
    return render_template('aboutme.html')

@app_laplacian.route("correlation_rolling")
def correlation_rolling():
    return render_template('aboutme.html')

@app_laplacian.route("correlation_matrix")
def correlation_matrix():
    return render_template('aboutme.html')

@app_laplacian.route("distributions")
def distributions():
    return render_template('plot_distributions.html')

@app_laplacian.route("quant_quantlib")
def quant_quantlib():
    return render_template('aboutme.html')


@app_laplacian.route("tradeapp")
def tradeapp():
    return render_template('tradeapp.html')


# ------------------   REACTIVE GRAPHS: 2D, 3D   -------------------------------

@app_laplacian.route(PLOT_ROUTES['scatter_histogram'])
def scatter_histogram():
    return render_template('scatter_histogram.html')

@app_laplacian.route(PLOT_ROUTES['threed'])
def threed():
    return render_template('threed_.html')

@app_laplacian.route(PLOT_ROUTES['stream_wind'])
def stream_wind():
    return render_template('stream_wind_.html')

@app_laplacian.route(PLOT_ROUTES['stream_model_training'])
def stream_model_training():
    return render_template('stream_model_training_.html')


@app_laplacian.route("scatter_dynamic")
def d3_scatter_dynamic():
    return render_template('splom.html')


@app_laplacian.route("threed_cube")
def threed_cube():
    return render_template('threed_cube.html')

@app_laplacian.route("threed_cube_webgl_d3")
def threed_cube_webgl_d3():
    return render_template('threed_cube_webgl_d3.html')

@app_laplacian.route("threed_animation")
def threed_animation():
    return render_template('threed_animation_visjs.html')



@app_laplacian.route("gis_rainfall")
def gis_rainfall():
    return render_template('aboutme.html')

@app_laplacian.route("gis_openlayers_esri")
def gis_openlayers_esri():
    return render_template('aboutme.html')

@app_laplacian.route("gis_typhoon_tracking")
def gis_typhoon_tracking():
    return render_template('aboutme.html')

@app_laplacian.route("gis_openlayers_kml_earthquake")
def gis_openlayers_kml_earthquake():
    return render_template('aboutme.html')

@app_laplacian.route("gis_river")
def gis_river():
    return render_template('aboutme.html')

@app_laplacian.route("d3_geo_sat_land")
def d3_geo_sat_land():
    return render_template('aboutme.html')

@app_laplacian.route("d3_geo_sat_tiles")
def d3_geo_sat_tiles():
    return render_template('aboutme.html')

@app_laplacian.route("d3_geo_projection_earth_torus")
def d3_geo_projection_earth_torus():
    return render_template('aboutme.html')

@app_laplacian.route("d3_geo_projection_earth_mollweide")
def d3_geo_projection_earth_mollweide():
    return render_template('aboutme.html')


@app_laplacian.route("d3_line_histogram_dynamic")
def d3_line_histogram_dynamic():
    return render_template('line_zoom2_grid.html')


"""
def contact_me(request):

  return render(request, 'laplacian/contact_me.html', {'foo': ['just','testing']})


#
# http://127.0.0.1:8000/app_name/foo
#
def correlation_rolling(request):
  #p = get_object_or_404(Question, pk=question_id)

  if request.method == 'GET':
      pass
      #form1 = Form1()
      #form2 = Form2()
      #form3 = Form3()
  elif (request.POST):
      #return HttpResponse(request.POST['tickerb'])  # debug

      #form1 = Form1(request.POST)
      #form2 = Form2(request.POST)
      #form3 = Form3(request.POST)
      #if form1.is_valid() and form2.is_valid() and form3.is_valid():
      #    form1.save()
      #    form2.save()
      #    form3.save()


      instr_lst = []
      instr_lst.append(request.POST['ticker1'])
      instr_lst.append(request.POST['ticker2'])
      corr_days = int(request.POST['corr_days'])

      user_entered = {}
      user_entered['ticker1'] = instr_lst[0]
      user_entered['ticker2'] = instr_lst[1]
      user_entered['corr_days'] = corr_days

      try:
        df_matrix = pd_utils.fetch_data_matrix(instr_lst, save=True)
      except:
        e = sys.exc_info()[0]
        return render_to_response('laplacian/correlation_rolling.html', {
            'user_entered': user_entered,
            'error_message': "Unable to retrieve ticker symbol(s)",  #e,
        }, context_instance=RequestContext(request))
      else:
        pd_utils.correlation_rolling(df_matrix, corr_days)
        #return render_to_response('my_page.html',
        #  {'form1' : form1, 'form2' : form2, 'form3' : form3})
        return render(request, 'laplacian/correlation_rolling.html', {'success': 1, 'user_entered': user_entered})

  return render(request, 'laplacian/correlation_rolling.html', {'foo': ['just','testing']})




def correlation_matrix(request):
  #p = get_object_or_404(Question, pk=question_id)

  if (request.POST):
      instr_lst = []
      instr_lst.append(request.POST['ticker1'])
      instr_lst.append(request.POST['ticker2'])
      instr_lst.append(request.POST['ticker3'])
      instr_lst.append(request.POST['ticker4'])
      instr_lst.append(request.POST['ticker5'])

      #corr_days = int(request.POST['corr_days'])

      user_entered = {}
      user_entered['ticker1'] = instr_lst[0]
      user_entered['ticker2'] = instr_lst[1]
      user_entered['ticker3'] = instr_lst[2]
      user_entered['ticker4'] = instr_lst[3]
      user_entered['ticker5'] = instr_lst[4]
      #user_entered['corr_days'] = corr_days

      try:
        df_matrix = pd_utils.fetch_data_matrix(instr_lst, save=True)
      except:
        e = sys.exc_info()[0]
        return render_to_response('laplacian/correlation_matrix.html', {
            'user_entered': user_entered,
            'error_message': "Unable to retrieve ticker symbol(s)",  #e,
        }, context_instance=RequestContext(request))
      else:
        corr_matrix = pd_utils.correlation_matrix(df_matrix)
        pd_utils.correlation_matrix_heat(corr_matrix)
        return render(request, 'laplacian/correlation_matrix.html', {'success': 1, 'user_entered': user_entered})

  return render(request, 'laplacian/correlation_matrix.html', {'foo': ['just','testing']})


def quantlib(request):

  return render(request, 'laplacian/comingSoon_split2.html')


# ==============================================================================
# NLP stuff
# ==============================================================================

def list(request):
    # Handle file upload
    if request.method == 'POST':
        try:
          form = DocumentForm(request.POST, request.FILES)
          if form.is_valid():
              newdoc = Document(docfile = request.FILES['docfile'])
              newdoc.save()

        except:
          pass

        else:
          # Redirect to the document list after POST
          return HttpResponseRedirect(reverse('laplacian.views.list'))

    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'laplacian/list.html',
        {'form': form, 'documents': documents},
        context_instance=RequestContext(request)
    )


def handle_uploaded_file_chunk(f):
    # Looping over UploadedFile.chunks() instead of using read() ensures that large files don’t overwhelm your system’s memory.
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def handle_uploaded_file_line(filename):
    doc_text=""
    with open('/opt/www/holivue_home/holivue_project/media/documents/'+filename, 'rb') as f:
        for line in f:
            doc_text += line
    return doc_text

def handle_uploaded_file(filename):
    doc_text=""
    with open('/opt/www/holivue_home/holivue_project/media/documents/'+filename, 'rb') as f:
        #doc_text = f.read()
        doc_text = unicode(f.read(), "UTF-8")
    return doc_text.strip()


def nlp_resume(request):

    # Handle file upload
    doc_name=""
    freq_sorted_json=[]
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
              # Upload doc and save
              newdoc = Document(docfile = request.FILES['docfile'])
              newdoc.save()
              doc_name = newdoc.filename()

              # Read doc AND clean up immediately
              file_path_name = '/opt/www/holivue_home/holivue_project/media/documents/'+doc_name
              #doc_text = handle_uploaded_file(doc_name)
              doc_text = get_uploaded_file(file_path_name)
              os.remove(file_path_name)

              # Analyze text
              if doc_text and len(doc_text) > 1:
                  freq_sorted_json = analyze_frequency_words(doc_text)
                  freq_sorted_json = json.dumps(freq_sorted_json)
              else:
                  pass
                  #freq_sorted_json = ["alpha","beta",{"i":"5", "j":"8"}]
                  #freq_sorted_json = json.dumps(freq_sorted_json)
            except:
              pass

    else:
        form = DocumentForm() # A empty, unbound form

    #freq_sorted_json = ["alpha","beta",{"i":"5", "j":"8"}]
    #freq_sorted_json = json.dumps(freq_sorted_json)

    return render(request, 'laplacian/nlp_resume.html',
      {'form': form, 'doc_name': doc_name, 'freq_sorted_json': freq_sorted_json},
    )



def nlp_facebook(request):

    return render(request, 'laplacian/nlp_facebook.html')


def nlp_article_blog(request):

    return render(request, 'laplacian/nlp_article_blog.html')


def nlp_twitter(request):

    return render(request, 'laplacian/nlp_twitter.html')



# ==============================================================
# GIS and D3 charts
# ==============================================================
def gis_river(request):
    return render(request, 'laplacian/geo_line_point.html')

def gis_rainfall(request):
    return render(request, 'laplacian/dual_rainfall.html')

def gis_openlayers_esri(request):
    return render(request, 'laplacian/gis_openlayers_esri.html')

def gis_typhoon_tracking(request):
    return render(request, 'laplacian/gis_typhoon_tracking.html')

def gis_openlayers_kml_earthquake(request):
    return render(request, 'laplacian/gis_openlayers_kml_earthquake.html')


def d3_scatter_dynamic(request):
    return render(request, 'laplacian/splom2.html')


def d3_geo_sat_land(request):
    return render(request, 'laplacian/geo_sat_land.html')

def d3_geo_sat_tiles(request):
    return render(request, 'laplacian/geo_sat_tiles.html')

def d3_geo_projection_earth_torus(request):
    return render(request, 'laplacian/geo_projection_hammer_retroazimuthal.html')

def d3_geo_projection_earth_mollweide(request):
    return render(request, 'laplacian/geo_projection_earth_mollweide.html')

def d3_geo_earth_gnomic(request):
    return render(request, 'laplacian/geo_earth_gnomic.html')


def d3_line_histogram_dynamic(request):
    return render(request, 'laplacian/line_zoom2_grid.html')

"""
