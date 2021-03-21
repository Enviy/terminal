import os
import re
import random
import requests
import logging


wnik_log = logging.getLogger(__name__)

class Client():
    def __init__(self):
        key = os.environ.get('WORDNIK')
        if key == '' or key == None:
            wnik_log.error('[!] Failed to load credentials!.')
            return None
        self.url = "https://api.wordnik.com/v4{0}&api_key=" + key

    def _handle_errors(self, r):
        # r : request response body
        if r.status_code == 200:
            return (None, '')
        try:
            resp = r.json()
        except:
            wnik_log.error('[!] Failed to load response into json:\n{0}'.format(r.text))
            return ('Error', r)

        if resp.get('statusCode') == 404 and resp.get('error') == 'Not Found':
            wnik_log.error('[!] Requested API resource not found')
            return ('Error', r)
        elif resp.get('statusCode') == 503 and resp.get('error') == 'Service Unavailable':
            echo = requests.get(r.url)
            if echo.status_code == 200:
                return (echo, '')
            elif echo.status_code == 503 and 'Service Unavailable' in echo.text:
                wnik_log.error('[!] Requested API resource not found')
                return ('Error', echo)
        r.raise_for_status()

    def _rand_indexes(self, r):
        # r : iterator (typically list or dict)
        rand_indexes = []
        while len(rand_indexes) < 3 and len(r) > 3:
            r_index = random.randrange(0, len(r))
            if r_index not in rand_indexes:
                rand_indexes.append(r_index)
        if len(r) <= 3:
            for i in range(len(r)):
                rand_indexes.append(i)
        return rand_indexes

    def _handle_definitions(self, r):
        # r : response iterator
        definitions = []
        to_remove = ['<spn>',
                     '</spn>',
                     '<er>',
                     '</er>',
                     '<xref>',
                     '</xref>',
                     '<xref urlencoded="',
                    '<em>',
                    '</em>',
                    '<internalXref urlencoded="',
                    '">',
                    '</internalXref>',
                    '(',
                    ')',
                    '<ex>',
                    '</ex>',
                    '%20',
                    '<stype>',
                    '</stype>']
        for i in r:
            if i.get('text'):
                d = i['text']
                for item in to_remove:
                    d = d.replace(item, '')
                definitions.append(d)
        output = []
        for i in self._rand_indexes(definitions):
            output.append(definitions[i])
        return output

    def _handle_examples(self, r):
        # r : response json body
        examples = []
        # this should build a list of unique strings
        for i in r['examples']:
            if i.get('text') and i['text'].replace('-', '').strip() not in examples:
                examples.append(i['text'].replace('-', '').strip())
        output = []
        # this should build a list based on random indexes
        for i in self._rand_indexes(examples):
            output.append(examples[i])
        return output

    def _handle_related(self, r):
        # r : response json body
        # for related words, this is a list of dict
        relationship = ['cross-reference',
                        'same-context',
                        'synonym']
        related = []
        for i in r:
            if i.get('relationshipType') in relationship:
                for word in i['words']:
                    if word not in related:
                        related.append(word)
        return related

    def _handle_phrases(self, r):
        # r : response json body
        # build list of short phrases
        phrases = []
        for i in r:
            phrases.append(i['gram1'] + ' ' + i['gram2'])
        return phrases

    def _handle_etymology(self, r):
        # r : response json body
        # for etymology, this is a single index list
        # cleans etymology string
        regex = r"(\[\w(.*?)\])"
        rawline = re.search(regex, r[0]).group()
        etymology = rawline.replace('[', '').replace('<ets>','').replace('</ets>','').replace(']','').replace('<er>','').replace('</er>','').strip()
        return etymology

    def GetWord(self, word, opt):
        # word : string of term to query
        # opt : string type of query
        opts = ['audio',
                'definitions',
                'etymologies',
                'examples',
                'frequency',
                'hyphenation',
                'phrases',
                'pronunciations',
                'relatedWords',
                'scrabbleScore',
                'topExample']
        if opt in opts:
            arg = '/word.json/{word}/{opt}?'.format(word=word, opt=opt)
        else:
            wnik_log.error('[!] Failed; Select opt from list: {0}'.format(opts))
            return None
        r = requests.get(self.url.format(arg))
        e = self._handle_errors(r)
        if e[0] != None and e[0] != 'Error':
            resp = e[0].json()
        elif e[0] == 'Error':
            return {'Error': e[1].json()}
        elif e[0] == None:
            resp = r.json()
        if opt == 'definitions':
            return self._handle_definitions(resp)
        elif opt == 'examples':
            return self._handle_examples(resp)
        elif opt == 'relatedWords':
            return self._handle_related(resp)
        elif opt == 'phrases':
            return self._handle_phrases(resp)
        elif opt == 'etymologies':
            return self._handle_etymology(resp)
        return resp

    def RandWord(self, part=None):
        # part : string 'noun, adjective, verb' etc
        parts = ['noun',
                 'adjective',
                 'verb',
                 'adverb',
                 'pronoun',
                 'preposition',
                 'interjection',
                 'abbreviation',
                 'affix',
                 'article',
                 'auxiliary-verb',
                 'conjuction',
                 'definite-article',
                 'family-name',
                 'given-name',
                 'idiom',
                 'imperative',
                 'noun-plural',
                 'past-participle',
                 'phrasal-prefix',
                 'proper-noun',
                 'proper-noun-plural',
                 'proper-noun-posessive',
                 'suffix',
                 'verb-intransitive',
                 'verb-transitive']
        arg = "/words.json/randomWord?hasDictionaryDef=true{0}&maxCorpusCount=-1&minDictionaryCount=1&maxDictionaryCount=-1&minLength=5&maxLength=-1"
        if part in parts:
            arg = arg.format('&includePartOfSpeech=' + part)
        elif part not in parts and part != None:
            wnik_log.warning('[!] part not in parts, disregarding.')
            arg = arg.format('')
        else:
            arg = arg.format('')
        r = requests.get(self.url.format(arg))
        e = self._handle_errors(r)
        if e[0] != None and e[0] != 'Error':
            resp = e[0].json()
        elif e[0] == 'Error':
            return {'Error': e[1].json()}
        elif e[0] == None:
            resp = r.json()
        return resp['word']

