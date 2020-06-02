
"""
RAKE + NLTK

The Rapid Automatic Keyword Extraction (RAKE) algorithm extracts keywords from text, by identifying runs of non-stopwords and then scoring these phrases across the document. It requires no training, the only input is a list of stop words for a given language, and a tokenizer that splits the text into sentences and sentences into words.


I started looking for something along these lines because I needed to parse a block of text
before vectorizing it and using the resulting features as input to a predictive model.
Vectorizing text is quite easy with Scikit-Learn as shown in its Text Processing Tutorial.
What I was trying to do was to cut down the noise by extracting keywords from the
input text and passing a concatenation of the keywords into the vectorizer. It didn't
improve results by much in my cross-validation tests, however, so I ended up not using it.
But keyword extraction can have other uses, so I decided to explore it a bit more.

"""

# Adapted from: github.com/aneesha/RAKE/rake.py
from __future__ import division
import operator
import nltk
import string

def isPunct(word):
  return len(word) == 1 and word in string.punctuation

def isNumeric(word):
  try:
    float(word) if '.' in word else int(word)
    return True
  except ValueError:
    return False

class RakeKeywordExtractor:

  def __init__(self):
    self.stopwords = set(nltk.corpus.stopwords.words())
    self.top_fraction = 1 # consider top third candidate keywords by score

  def _generate_candidate_keywords(self, sentences):
    phrase_list = []
    for sentence in sentences:
      words = map(lambda x: "|" if x in self.stopwords else x,
        nltk.word_tokenize(sentence.lower()))
      phrase = []
      for word in words:
        if word == "|" or isPunct(word):
          if len(phrase) > 0:
            phrase_list.append(phrase)
            phrase = []
        else:
          phrase.append(word)
    return phrase_list

  def _calculate_word_scores(self, phrase_list):
    word_freq = nltk.FreqDist()
    word_degree = nltk.FreqDist()
    for phrase in phrase_list:
      degree = len(filter(lambda x: not isNumeric(x), phrase)) - 1
      for word in phrase:
        word_freq.inc(word)
        word_degree.inc(word, degree) # other words
    for word in word_freq.keys():
      word_degree[word] = word_degree[word] + word_freq[word] # itself
    # word score = deg(w) / freq(w)
    word_scores = {}
    for word in word_freq.keys():
      word_scores[word] = word_degree[word] / word_freq[word]
    return word_scores

  def _calculate_phrase_scores(self, phrase_list, word_scores):
    phrase_scores = {}
    for phrase in phrase_list:
      phrase_score = 0
      for word in phrase:
        phrase_score += word_scores[word]
      phrase_scores[" ".join(phrase)] = phrase_score
    return phrase_scores

  def extract(self, text, incl_scores=False):
    sentences = nltk.sent_tokenize(text)
    phrase_list = self._generate_candidate_keywords(sentences)
    word_scores = self._calculate_word_scores(phrase_list)
    phrase_scores = self._calculate_phrase_scores(
      phrase_list, word_scores)
    sorted_phrase_scores = sorted(phrase_scores.iteritems(),
      key=operator.itemgetter(1), reverse=True)
    n_phrases = len(sorted_phrase_scores)
    if incl_scores:
      return sorted_phrase_scores[0:int(n_phrases/self.top_fraction)]
    else:
      return map(lambda x: x[0],
        sorted_phrase_scores[0:int(n_phrases/self.top_fraction)])

def test():
  rake = RakeKeywordExtractor()
  keywords = rake.extract("""
Compatibility of systems of linear constraints over the set of natural
numbers. Criteria of compatibility of a system of linear Diophantine
equations, strict inequations, and nonstrict inequations are considered.
Upper bounds for components of a minimal set of solutions and algorithms
of construction of minimal generating sets of solutions for all types of
systems are given. These criteria and the corresponding algorithms for
constructing a minimal supporting set of solutions can be used in solving
all the considered types of systems and systems of mixed types.
  """, incl_scores=True)
  print keywords

if __name__ == "__main__":
  test()

"""
The results are nearly identical, and I hope you will agree that the code is much more readable (if you are familiar with the NLTK API, of course). Here is the results from the original RAKE implementation, compared to my NLTK based implementation.

sujit@cyclone:src$ python rake.py
[('minimal generating sets', 8.6666666666666661),
 ('linear diophantine equations', 8.5),
 ('minimal supporting set', 7.6666666666666661),
 ('minimal set', 4.6666666666666661),
 ('linear constraints', 4.5),
 ('upper bounds', 4.0),
 ('natural numbers', 4.0),
 ('nonstrict inequations', 4.0)]
sujit@cyclone:src$ python rake_nltk.py
[('minimal generating sets', 8.6666666666666661),
 ('linear diophantine equations', 8.5),
 ('minimal supporting set', 7.6666666666666661),
 ('minimal set', 4.6666666666666661),
 ('linear constraints', 4.5),
 ('upper bounds', 4.0),
 ('natural numbers', 4.0),
 ('nonstrict inequations', 4.0),
 ('strict inequations', 4.0)]

As you can see, the NLTK based version returns one more candidate keyword. This is because it finds 27 candidate keywords instead of 24 keywords. I believe its related to the way the original version handles punctuation (ie as part of the preceding word) compared to NLTK's approach (as a separate token). In any case, I am not convinced its a bug because one of extra keywords returned was "corresponding algorithms" with score 3.5, which seems reasonable.

An optimization on top of this is to find candidate keywords that span a stopword. So the next step would involve storing the text into a Lucene index and hitting it with n2 SpanQuery calls where n is the number of extracted keywords, something along these lines.




I recently needed to build a Named Entity Recognizer (NER) for our proprietary concept mapping/indexing platform to recognize and extract age group data from our document corpus. The approach I envisioned was to match specific age related patterns in the data and map them into specific age brackets.

I have also been reading the NLTK Book (free online version available here) lately, and came across a concept called concordance, which is basically a list of occurrences of a particular keyword with the context in the document corpus. It occurred to me that running a concordance on the document corpus for selected keywords would help me extract the patterns I needed.

Thinking through this some more, I remembered reading Accessing words around a positional match in Lucene by Grant Ingersoll, where he demonstrates the use of Span Queries to find collocated terms.

Since I already had an index whose body was indexed with term vectors, positions and offsets, I figured it would be easier to adapt Grant's code than set up NLTK to find the concordances for a few key terms. So this is what I did - the JUnit test below shows my version, which generates output very similar to that generated by NLTK's concordance() method


/ Source: src/test/java/com/mycompany/tgni/utils/ConcordanceGeneratorTest.java
package com.mycompany.tgni.utils;

import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;

import org.apache.commons.lang.StringUtils;
import org.apache.commons.lang.math.IntRange;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.Term;
import org.apache.lucene.index.TermVectorMapper;
import org.apache.lucene.index.TermVectorOffsetInfo;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.spans.SpanTermQuery;
import org.apache.lucene.search.spans.Spans;
import org.apache.lucene.store.FSDirectory;
import org.junit.Test;

public class ConcordanceGeneratorTest {

  private static final int NUM_CONTEXT_CHARS = 25;
  private static final String[] AGE_TERMS = new String[] {
    "aged", "age", "year"
  };

  @Test
  public void testGenerateConcordance() throws Exception {
    IndexSearcher searcher = new IndexSearcher(FSDirectory.open(
      new File("/path/to/my/index")));
    IndexReader reader = searcher.getIndexReader();
    PrintWriter writer = new PrintWriter(new FileWriter(
      new File("/tmp/concordance.txt")), true);
    for (String ageTerm : AGE_TERMS) {
      writer.println("==== concordance for term='" + ageTerm + "' ====");
      SpanTermQuery spt = new SpanTermQuery(new Term("body", ageTerm));
      Spans spans = spt.getSpans(reader);
      OffsetTermVectorMapper tvm = new OffsetTermVectorMapper();
      while (spans.next()) {
        Document doc = reader.document(spans.doc());
        String body = doc.get("body");
        tvm.start = spans.start();
        tvm.end = spans.end();
        reader.getTermFreqVector(spans.doc(), "body", tvm);
        String conc = StringUtils.substring(body,
          tvm.range.getMinimumInteger() - NUM_CONTEXT_CHARS,
          tvm.range.getMaximumInteger() + NUM_CONTEXT_CHARS);
        if (StringUtils.isNotEmpty(conc)) {
          writer.println(StringUtils.join(new String[] {
            "...", conc, "..."
          }));
        }
      }
    }
    searcher.close();
    writer.flush();
    writer.close();
  }

  private class OffsetTermVectorMapper extends TermVectorMapper {

    public int start;
    public int end;
    public IntRange range;

    @Override
    public void map(String term, int frequency, TermVectorOffsetInfo[] offsets,
        int[] positions) {
      for (int i = 0; i < positions.length; i++) {
        if (positions[i] >= start && positions[i] < end) {
          TermVectorOffsetInfo offset = offsets[i];
          range = new IntRange(offset.getStartOffset(), offset.getEndOffset());
        }
      }
    }

    @Override
    public void setExpectations(String field, int numTerms,
        boolean storeOffsets, boolean storePositions) {
      // NOOP
    }
  }
}
The code scans the index for spans containing the keywords "age", "aged" and "year", finds the character offsets of these spans, then returns substrings consisting of 25 character snippets on either side for context. Here is some sample output (truncated to 20 top results for brevity).

==== concordance for term='aged' ====
...y feel trapped within an aged body. Grief, a sense of ...
...ated deaths among people aged 65 years or older and ar...
...tal falls involve people aged 75 years or older-only 4...
...population. Among people aged 65 to 69 years, 1 of eve...
...racture, and among those aged 85 years or older, 1 fal...
...g Medicare beneficiaries aged &gt; or = 65 yearsUnite...
...or, ME) at 68 weeks and aged in our colony room at Ru...
...nalyzed with Age (middle-aged and young)  Treatment (...
...ntly a disease of middle-aged white males, with a medi...
..., but also occurs in the aged. It was the first human ...
...es. Among the population aged five years and above, HI...
... 121 consecutive adults (aged &gt;16 years) who underw...
...c abnormality. In middle-aged and older adults, in who...
...es more common in middle-aged patients withchronic act...
...ctures are mostly middle-aged and actively employed. I...
...d 426 non-twin siblings, aged 12-18 years, was recruit...
...y much involved. Edwina, aged 77, is a young mother an...
...eening for 94% of people aged 55 years and over....
... criteria (), were those aged 18 or older (male or fem...
...g 301 toddlers (children aged 1 to 2 years) with upper...
...
==== concordance for term='age' ====
...ric Depression Scale Old age isn't so bad when you co...
...n individual 65 years of age or older. Among such ind...
... social integration. The age range of this rapidly gr...
...er of people 65 years of age or older is projected to...
...llion people 65 years of age and older. This group wi...
...n older than 85 years of age represents the fastest-g...
...e older than 65 years of age. These statistics are ex...
... individuals 95 years of age and older. African Ameri...
...but only 8% of the older age groups. In 1986, most ol...
...n older than 65 years of age continue to work; 25% ar...
...ans will be 100 years of age or older by the year 205...
...y 2 million will be that age by the year 2080. Falls ...
... individuals 65 years of age and older. Two thirds of...
... in patients 85 years of age and older are caused by ...
...s older than 65 years of age have this fear. Structur...
...rises progressively with age, whereas diastolic press...
...d to half by 75 years of age. Vascular changes may al...
...he case in the geriatric age group. It is well docume...
...s older than 70 years of age do not have chest pain w...
...s older than 65 years of age use about 25% of all pre...
...
==== concordance for term='year' ====
...ntegrity, for at least 1 year after nerve injury. Irre...
... often has occurred by 2 years. Sensory cross-reinnerva...
...ed state for a period of years. Thus, even late reinner...
..., on the order of 2 to 3 years, may be able to restore ...
...ocols were used over the years the data was gathered. E...
...ient is an individual 65 years of age or older. Among s...
...ation spans more than 40 years. The world's geriatric p...
...ng at a rate of 2.5% per yearsignificantly faster tha...
... Americans older than 65 years increased from a little ...
... the number of people 65 years of age or older is proje...
...re 146 million people 65 years of age and older. This g...
...se to 232 million by the year 2020. A decreasing rate ...
...population older than 85 years of age represents the fa...
...cted to continue. By the year 2020, one fifth of the p...
...on will be older than 65 years of age. These statistics...
...3:1 among individuals 95 years of age and older. Africa...
...population older than 65 years. Approximately 12% of th...
...population older than 65 years of age continue to work;...
...on Americans will be 100 years of age or older by the y...
...s of age or older by the year 2050 and that nearly 2 m...
...

As you can see, this list is a good way to find common patterns that need to be extracted from the corpus. All you need is a bit of imagination to think of some good representative terms that cover most patterns you are likely to encounter in the corpus. You also need to scan the list manually to weed it out. It is now relatively simple to craft a number of regular expressions that capture the lower and upper bound (where available) of the date ranges and assign these to predefined age group blocks.

Of course, the downside is that it kind of puts the cart before the horse. The Age-Group NER is part of the indexing pipeline, but we need an index to be built without this filter first in order to get data to build this filter. The right way would probably be to generate the concordance data with something like NLTK. But it is relatively cheap resource-wise to build a plain old Lucene index from your corpus, so perhaps its not quite so bad.


 """
