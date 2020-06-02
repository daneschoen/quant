import os, sys
import argparse

import random

from bson.objectid import ObjectId

import markdown
import codecs


class Article_insertupdate:


    HTML_DEST_DIR = '/home/admin/projects/kiklearn/flask_blueprint/apps/app_blog_tribal/templates/'
    JSN_ARTICLE_REL_DIR = 'article'
    JSN_ARTICLE_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), JSN_ARTICLE_REL_DIR))

    def __init__(self):
        #self.canvas_created = False
        #self.pth = os.path.dirname( os.path.realpath(__file__))
        pass


    def json_mongo(self, article_json, mongocol):
        mdstr = article_meta_md['body']
        html = markdown.markdown(mdstr)

        article = {
            "cnty": article_meta_md['cnty'],
            "title": article_meta_md['title'],
            "author": article_meta_md.get('author', "Daniel Schoe"),
            "tags":  article_meta_md['tags'],
            "lead":  article_meta_md['lead'],
            "body":  mdstr,
            "article_photo": article_meta_md['article_photo'],
            "date": article_meta_md.get('date', datetime.datetime.utcnow()),
            "slug":  article_meta_md['slug'],
            "vote":  article_meta_md.get('vote', random.randint(100, 1000))
        }

        result = mongocol.update(
            { "id": ObjectId(article_meta['id']) },
            article,
            upsert=False
        )


    def filejson_mongo(self, src):
        try:
          """
          input_file = codecs.open(src, mode="r", encoding="utf-8")
          mdstr = input_file.read()
          """


          ###mdstr_mongo(mdstr)
        except IOError as err:
          print("IO error: {0}".format(err))
        except:
          print("Unexpected error:", sys.exc_info()[0])
        finally:
          if input_file:
              input_file.close()


    def filemd_html(self, src, dest):
        try:
          input_file = codecs.open(src, mode="r", encoding="utf-8")
          text = input_file.read()
          # html = markdown.markdown(text)
          html = markdown.markdown(text, extensions=['markdown.extensions.nl2br'])
          output_file = codecs.open(dest, "w",
                                    encoding="utf-8",
                                    errors="xmlcharrefreplace"
                                   )
          output_file.write(html)

        except IOError as err:
          print("IO error: {0}".format(err))
        except:
          print("Unexpected error:", sys.exc_info()[0])
        finally:
          if input_file:
              input_file.close()
          if output_file:
              output_file.close()


    @classmethod
    def checkfile(self, inpathfile):
        if os.path.isfile(inpathfile):
            return True
        return False



if __name__ == "__main__":
    """ Usage:

    # -------------------
    # jsn file => mongodb
    # -------------------

    # -------------------
    # md file => mongodb
    # -------------------
    $ cd ~/projects/kiklearn/flask_blueprint/apps/app_blog_tribal
    $ python3 util_markdown.py _.md

    # -------------------
    # md file => html
    # -------------------
    $ python3 -m markdown markdown_.md > markdown_.html
    $ echo "Some **Markdown** text." | python -m markdown > output.html

    $ python3 -m markdown -x codehilite some_markdown.md > body.html
    $ pygmentize -S default -f html > codehilite.css

    # -----------------------------------------------------

    $ python3 util_markdown.py _.md -dest ./article123.html
    $ python3 util_markdown.py _.md -dest ./templates/article123.html

    $ python3 util_markdown.py ./templates/markdown.md -dest ./templates/article123.html

    $ python3 util_markdown.py _.md -dest ./templates/article123.html

    DEFAULT IF RUNNING MANUALLY IS MD => MONGO

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('src')
    #parser.add_argument('-mongo','--mongo', action='store_true')
    #parser.add_argument('-dest', '--dest', default=None)
    parser.add_argument('-log','--log', action='store_true')  #, default=os.getcwd())
    # parser.add_argument('log', nargs='?')  #, default=os.getcwd())
    parser.add_argument('-dest')

    args = parser.parse_args()

    if not Article_insertupdate.checkfile(args.src):
        print('Input file ' + args.src + ' not found')
        sys.exit()

    article_insertupdate = Article_insertupdate()
    #article_insertupdate.INFILENAME = args.src

    if not args.dest:
        #article_insertupdate.filejsn_mongo(args.src)
        pass
    else:
        article_insertupdate.filemd_html(args.src, args.dest)
