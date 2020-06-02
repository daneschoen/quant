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

import stock_covariance as pd_utils
from nlp_frequency_words import analyze_frequency_words, get_uploaded_file
"""

"""
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


# ==============================================================
# NLP stuff
# ==============================================================

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

def d3_line_histogram_dynamic(request):
    return render(request, 'laplacian/line_zoom2_grid.html')


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

"""
