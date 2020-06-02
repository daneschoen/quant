import os
import datetime
import argparse
import re
from shutil import copy2   # copyfile,
from subprocess import check_output

# ==============================================================================

file_head_quant_lst = ['index_quant', 'index_head_dia', 'index_head_rak']    # css
file_tail_quant_lst = ['index_tail_dia', 'index_tail_rak']                   # js

file_head_blog_visuably_lst = ['index_head_dia_']   # css
file_tail_blog_visuably_lst = ['index_tail_dia_']   # js

file_index_def_blog_visuably_lst = ['index_land_visuably', 'index_finance']   # css + js
file_index_def_blog_datasciencery_lst = ['index_land_datasciencery']

file_index_def_lst_ = list(set(file_index_def_blog_visuably_lst).union(set(file_index_def_blog_datasciencery_lst)))

css_def_lst = ['app_lapas','app_visuably']
js_def_lst = ['app_quantcypher', 'app_visuably']  #! 'app_lapas',

file_ext = ".html"

PATH_QUANT = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'app_quant', 'templates'))
PATH_BLOG_VISUABLY = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'app_blog_visuably', 'templates'))
PATH_DATASCIENCERY = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'app_datasciencery', 'templates'))
PATH_BLOG_SCIENCEISMETA = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'app_blog_scienceismeta', 'templates'))
PATH_BLOG_SCIENCESTRANGE = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'app_blog_sciencestrange', 'templates'))
PATH_BLOG_MOLTENWARS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'app_blog_moltenwars', 'templates'))

# ==============================================================================

def mv_dev_prod_min(file_head_lst=file_head_blog_visuably_lst,
                    file_tail_lst=file_tail_blog_visuably_lst,
                    file_index_def_lst=file_index_def_lst_,
                    css_def_lst=css_def_lst,
                    js_def_lst=js_def_lst,
                    path_template=PATH_BLOG_VISUABLY,
                    tpl_lst=[],
                    css_lst=[],
                    js_lst=[]):
    '''
    index_         : index_dev.html => index_.html
    index_finance_ : index_finance_dev.html => index_finance.html

    new  tpl  new  js/css
    new  tpl  same js/css
    same tpl  new  js/css*
    same tpl  same js/css

    new or same tpl  new   js/css  =>
    new or same tpl  same  js/css  =>
    '''
    # file_head_lst.extend(tpl_lst)
    index_lst = []
    for tpl in tpl_lst:
        if tpl[:5] == 'index':  # eg 'index_finance_dev'
            index_lst.append(tpl)
            # file_head_lst.append(tpl)

    if len(css_lst) > 0 or len(js_lst) > 0:
        nw_dtimestamp = datetime.datetime.now().strftime("%y%m%d.%H%M%S")  # '051823.120538'

    # css : css_lst => q new
    #       if not in css_def_lst => q=123456.78912
    #       js_lst  => q new
    #       if not in js_def_lst => q=123456.78912
    # ------------------------------------------
    # index_head_dia index_tail_dia ... files
    # ------------------------------------------
    if css_lst:
        for file_base in file_head_lst:
            path_file_in  = os.path.abspath(os.path.join(path_template, file_base + 'dev' + file_ext))
            path_file_out = os.path.abspath(os.path.join(path_template, file_base + 'prod' + file_ext))

            #path_file_out_bak = os.path.abspath(os.path.join(path, file_base + bak + file_ext))
            #copy(path_file_out, path_file_out_bak)

            with open(path_file_in) as fin, open(path_file_out,"r+") as fout:
                """
                for line in file_in:
                    line = line.replace('app_quant.js','app_quant.min.js')
                    line = line.replace('lapas.js','lapas.min.js')
                    file_out.write(line)

                # ---------
                import re

                rep = {"condition1": "", "condition2": "text"} # define desired replacements here

                # use these three lines to do the replacement
                rep = dict((re.escape(k), v) for k, v in rep.iteritems())
                pattern = re.compile("|".join(rep.keys()))
                text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)

                >>> pattern.sub(lambda m: rep[re.escape(m.group(0))], "(condition1) and --condition2--")
                '() and --text--'
                """

                html_dev = fin.read()
                html_prod = fout.read()
                fout.seek(0)

                # html = html.replace('lapas.css','lapas.min.css')

                for css in css_lst:
                    # print(css + '.min.css?q=' + nw_dtimestamp)
                    # /static/css/lapas.css?q=051823.120538
                    #re.sub(r"lapas.min.css\?q=\d{6}\.\d{6}", "lapas.min.css?q="+nw_dtimestamp, html)
                    # html = re.sub(r"/static/css/" + css + "\.min\.css\?q=\d{6}\.\d{6}", "/static/css/lapas.min.css?q="+nw_dtimestamp, html)

                    # html = re.sub(r"/static/js/app_quantcypher\.min\.js\?q=\d{6}\.\d{6}", "/static/js/quantcypher.min.js?q="+nw_dtimestamp, html)
                    # html = re.sub(r"/static/js/app_visuably\.min\.js\?q=\d{6}\.\d{6}", "/static/js/visuably.min.js?q="+nw_dtimestamp, html)
                    # html = re.sub(r"/static/js/app_lapas\.min\.js\?q=\d{6}\.\d{6}", "/static/js/lapas.min.js?q="+nw_dtimestamp, html)

                    # html = html.replace('app_quantcypher.js','app_quantcypher.min.js')
                    # html = html.replace('app_visuably.js','app_visuably.min.js')
                    # html = html.replace('lapas.js','lapas.min.js')

                    html_dev = html_dev.replace(css+'.css', css+'.min.css?q='+nw_dtimestamp)
                    print('css_lst: ' + css + " q=" + nw_dtimestamp)

                # [x for x in item if x not in z]
                for css in list(set(css_def_lst) - set(css_lst)):
                    # Get q from prod to keep for non-modified js: lapas.min.css?q=123456.789012
                    idx_beg = html_prod.find(css+'.min.css?q=')
                    if idx_beg == -1:
                        continue
                    idx_beg = idx_beg + len(css) + 11
                    q = html_prod[idx_beg : idx_beg + 13]

                    html_dev = html_dev.replace(css+'.css', css+'.min.css?q=' + q)
                    print('css_def_lst: ' + css + "q=q " + q)

                #if os.path.basename(path_file_in) == 'index_quant_dev.html':
                # if 'index_' in os.path.basename(path_file_in):
                # if os.path.basename(path_file_in).startswith('index_'):
                #     # html = html.replace('app_quantcypher.js','app_quantcypher.min.js')
                #     # html = html.replace('app_visuably.js','app_visuably.min.js')
                #     # html = html.replace('lapas.js','lapas.min.js')
                #     # Get q from prod to keep for non-modified js: lapas.min.css?q=123456.789012
                #     idx_beg = html_prod.find(css)+len(css) + 10
                #     q = html_prod[idx_beg : idx_beg + 13]
                #     for js in js_lst:
                #         html_dev = html_dev.replace(css+'.css', css+'.min.css?q='+nw_dtimestamp)
                #     # [x for x in item if x not in z]
                #     for js in list(set(js_def_lst) - set(js_lst)):
                #         html_dev = html_dev.replace(css+'.css', css+'.min.css?q=123456.78912')

                fout.write(html_dev)
                fout.truncate()

                print("css: " + os.path.basename(path_file_in) + " => " + os.path.basename(path_file_out) + "\n")

    if js_lst:
        for file_base in file_tail_lst:
            path_file_in  = os.path.abspath(os.path.join(path_template, file_base + 'dev' + file_ext))
            path_file_out = os.path.abspath(os.path.join(path_template, file_base + 'prod' + file_ext))

            with open(path_file_in) as fin, open(path_file_out,"r+") as fout:
                html_dev = fin.read()
                html_prod = fout.read()
                fout.seek(0)

                for js in js_lst:
                    html_dev = html_dev.replace(js+'.js', js+'.min.js?q=' + nw_dtimestamp)
                    print('js: ' + js + "  " + nw_dtimestamp)

                for js in list(set(js_def_lst) - set(js_lst)):
                    # Get q from prod to keep for non-modified js: lapas.min.css?q=123456.789012
                    idx_beg = html_prod.find(js+'.min.js?q=')
                    if idx_beg == -1:
                        continue
                    idx_beg = idx_beg + len(js) + 10
                    q = html_prod[idx_beg : idx_beg + 13]

                    html_dev = html_dev.replace(js+'.js', js+'.min.js?q=' + q)
                    print('js_def: ' + js + " q=q " + q)

                fout.write(html_dev)
                fout.truncate()

                print("js: " + os.path.basename(path_file_in) + "  => " + os.path.basename(path_file_out) + "\n")

    # --------------------------
    # index*.html files
    # --------------------------
    #if os.path.basename(path_file_in).startswith('index_'):
    if css_lst or js_lst:
        index_lst = list(set(file_index_def_lst).union(set(index_lst)))
    for file_base in index_lst:

        path_template = get_path_template(file_base)

        # First make backups of DEST file being overwritten, ie dev => PROD => PROD_BAK
        file_path_tpl     = os.path.abspath(os.path.join(path_template, file_base + file_ext))
        file_path_tpl_bak = os.path.abspath(os.path.join(path_template, file_base + '_bak' + file_ext))
        print("================================")
        print(file_path_tpl)
        print(file_path_tpl_bak)
        copy2(file_path_tpl, file_path_tpl_bak)
        print(os.path.basename(file_path_tpl) + "  =>  " + os.path.basename(file_path_tpl_bak))

        path_file_in  = os.path.abspath(os.path.join(path_template, file_base + '_dev' + file_ext))
        path_file_out = os.path.abspath(os.path.join(path_template, file_base + file_ext))

        with open(path_file_in) as fin, open(path_file_out,"r+") as fout:
            html_dev = fin.read()
            html_prod = fout.read()
            fout.seek(0)

            for css in css_lst:
                html_dev = html_dev.replace(css+'.css', css+'.min.css?q='+nw_dtimestamp)
                print("css: " + css +"  " +nw_dtimestamp)

            for css in list(set(css_def_lst) - set(css_lst)):
                # Get q from prod to keep for non-modified css/js: lapas.min.css?q=123456.789012
                idx_beg = html_prod.find(css+'.min.css?q=')
                if idx_beg == -1:
                    continue
                idx_beg = idx_beg + len(css) + 11
                q = html_prod[idx_beg : idx_beg + 13]
                print("css: " + css +"  " +q)
                html_dev = html_dev.replace(css+'.css', css+'.min.css?q=' + q)

            for js in js_lst:
                html_dev = html_dev.replace(js+'.js', js+'.min.js?q='+nw_dtimestamp)

            for js in list(set(js_def_lst) - set(js_lst)):
                idx_beg = html_prod.find(js+'.min.js?q=')
                if idx_beg == -1:
                    continue
                idx_beg = idx_beg + len(js) + 10
                q = html_prod[idx_beg : idx_beg + 13]
                print("js: " + js+"  " +q)
                html_dev = html_dev.replace(js+'.js', js+'.min.js?q=' + q)

            fout.write(html_dev)
            fout.truncate()

            print(os.path.basename(path_file_in) + "  => " + os.path.basename(path_file_out) + "\n")


def cp_dev_prod(file_head_lst=file_head_blog_visuably_lst,
                file_tail_lst=file_tail_blog_visuably_lst,
                path_template=PATH_BLOG_VISUABLY,
                mode="prod",
                tpl_lst=[] ):

    # ['art_abc.html']
    #file_base_head_tail_lst = file_quant_head_lst[1:] + file_quant_tail_lst
    #for i in (1,len(file_quant_head_lst)-1):
    #    file_base = file_quant_head_lst[i]
    for file_base in tpl_lst:
        if file_base[:5] == 'index':
            continue
        #path_file_dev = os.path.abspath(os.path.join(path_template, file_base + dev + file_ext))
        #path_file_prod = os.path.abspath(os.path.join(path_template, file_base + file_ext))
        #path_file_ = os.path.abspath(os.path.join(path_template, file_base + '_' + file_ext))
        path_file_tpl = os.path.abspath(os.path.join(path_template, file_base + file_ext))

        # if mode == "dev":
        #     copy(path_file_dev, path_file_)
        #     print(os.path.basename(path_file_dev) + " => " + os.path.basename(path_file_))
        # elif mode == "prod":
        #     copy(path_file_prod, path_file_)
        #     print(os.path.basename(path_file_prod) + " => " + os.path.basename(path_file_))
        with open(path_file_tpl, "r+") as fin_out:
            html = fin_out.read()
            fin_out.seek(0)

            for file_head in file_head_lst:
                if mode == "prod":
                    html = html.replace(file_head + "dev.html", file_head + "prod.html")
                elif mode == "dev":
                    html = html.replace(file_head + "prod.html", file_head + "dev.html")

            for file_tail in file_tail_lst:
                if mode == "prod":
                    html = html.replace(file_tail + "dev.html", file_tail + "prod.html")
                elif mode == "dev":
                    html = html.replace(file_tail + "prod.html", file_tail + "dev.html")

            fin_out.write(html)
            fin_out.truncate()

            print(os.path.basename(path_file_tpl) + ": inside {% include 'index_head_dia_dev.html' %}, tail => index_head_dia_PROD.html, ...")

    # cp just first non-index tpl to _prod.html or _dev.html
    #if tpl_lst:
    for file_base in tpl_lst:

        if file_base[:5] == 'index':
            continue
        file_path_tpl = os.path.abspath(os.path.join(path_template, tpl_lst[0] + file_ext))
        file_path_test = os.path.abspath(os.path.join(path_template, '_' + mode + file_ext))
        copy2(file_path_tpl, file_path_test)

        print(os.path.basename(path_file_tpl) + "  =>  " + os.path.basename(file_path_test))
        break


def get_path_template(tpl_lst_str):
    path_template = PATH_BLOG_VISUABLY

    txt = ''
    if isinstance(tpl_lst_str, str):
    #if isinstance(o, (str, unicode)):
    #if type(tpl_lst) is str
        txt = tpl_lst_str
    elif len(tpl_lst_str) > 0:
        txt = tpl_lst[0]

    if 'datasciencery' in txt:
        path_template = PATH_DATASCIENCERY

    return path_template


def get_subprocess(dir):
    # ls -altr | tail -n 10
    stdout = check_output(["ls", "-altr", dir], encoding='UTF-8')
    res = stdout.split('\n')
    for l in res[-10:]:
        print(l)

def sanity_check():
    base_env_dir = os.getcwd().split('Agape')[0]
    base_proj_dir = base_env_dir + 'Agape/development/'
    print(get_subprocess(base_proj_dir + "projects/fintech/flask_blueprint/apps/static/js/"))
    print(get_subprocess(base_proj_dir + "projects/fintech/flask_blueprint/apps/static/css/"))
    print(get_subprocess(PATH_BLOG_VISUABLY))
    print(get_subprocess(PATH_DATASCIENCERY))


# ------------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--css', nargs='*')
    parser.add_argument('--js', nargs='*')
    parser.add_argument('--tpl', nargs='+')
    parser.add_argument('--mode', nargs='?', default='prod')
    args = parser.parse_args()

    """
    for _, value in parser.parse_args()._get_kwargs():
        if value is not None:
            print(value)
    print(args)
    print(args.tpl)
    print(args.css is None)
    print(args.mode)
    """

    css_lst = []
    js_lst = []
    tpl_lst=[]
    if args.css is not None:
        css_lst = args.css
    if args.js is not None:
        js_lst = args.js
    if args.tpl is not None:
        tpl_lst = args.tpl

    print()

    path_template = get_path_template(tpl_lst)

    mv_dev_prod_min(tpl_lst=tpl_lst,
                    path_template=path_template,
                    css_lst=css_lst,
                    js_lst=js_lst)

    cp_dev_prod(tpl_lst=tpl_lst, path_template=path_template, mode=args.mode)

    sanity_check()


    '''
    # --------------------------------------------------------------------------
    # UNITTEST
    # --------------------------------------------------------------------------
    - MUST BE IDEMPOTENT

    $ cp templates/index0.html templates/index.html
    $ cp templates/index_finance0.html templates/index_finance.html
    $ cp index_tail_dia_dev0.html index_tail_dia_dev.html
    $ cp index_tail_dia_prod0.html index_tail_dia_prod.html
    $ cp about_0.html about_.html

    $ p3 ../app_util/minify_.py
    $ p3 ../app_util/minify_.py --tpl index_land           # assert index0.html == index.html,  index_dev0.html == index_dev.html
    $ p3 ../app_util/minify_.py --tpl index_finance        # $ diff templates/index_dev.html templates/index.html
    $ p3 ../app_util/minify_.py --tpl index index_finance  # $ diff templates/index_finance0.html templates/index_finance.html
                                                           # $ diff templates/index_finance_dev.html templates/index_finance.html

    $ p3 ../app_util/minify_.py --css app_quantcypher                    # NOTHING
    $ p3 ../app_util/minify_.py --css lapas                              # new q: index*.html, index_head_dia
    $ p3 ../app_util/minify_.py --css app_quantcypher --tpl index_land   # new q: index.html, index_head_dia
    $ p3 ../app_util/minify_.py --css app_quantcypher --tpl index_land index_finance

    $ p3 ../app_util/minify_.py --js app_quantcypher
    $ p3 ../app_util/minify_.py --js app_quantcypher --tpl index

    $ p3 ../app_util/minify_.py --css lapas --js app_quantcypher
    $ p3 ../app_util/minify_.py --css lapas --js app_quantcypher --tpl index_finance

    $ p3 ../app_util/minify_.py --tpl about_                      #
    $ p3 ../app_util/minify_.py --tpl about_ --css foo            #
    $ p3 ../app_util/minify_.py --tpl about_ --css lapas
    $ p3 ../app_util/minify_.py --tpl about_ --css lapas --js app_quantcypher
    '''

# ==============================================================================
# ==============================================================================
# ==============================================================================
