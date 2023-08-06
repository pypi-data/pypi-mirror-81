import re
import os
import time
import sys
import pickle
import hashlib
import shutil
from urllib.parse import parse_qs, urlparse, urlunparse

import requests
from requests import ConnectionError, HTTPError


def cache_directory():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'requests_cache')


CACHE_ENABLED = False
def enable_requests_cache():
    global CACHE_ENABLED
    CACHE_ENABLED = True


def clean_cache():
    shutil.rmtree(cache_directory(), ignore_errors=True)


def download(url, retry=5):
    """
    Proxy function to be used with `enable_requests_cache()`
    to have the requests cached

    >>> import timeit
    >>> clean_cache()
    >>> enable_requests_cache()
    >>> url = "https://regardscitoyens.org/"
    >>> timeit.timeit(lambda: download(url), number=1) < 0.01
    False
    >>> timeit.timeit(lambda: download(url), number=1) < 0.01
    True
    """
    try:
        if CACHE_ENABLED:
            file = os.path.join(cache_directory(), hashlib.sha224(url.encode('utf-8')).hexdigest())
            if os.path.exists(file):
                try:
                    with open(file, 'rb') as f:
                        resp = pickle.load(f)
                        if '--debug' in sys.argv:
                            print('[download]', url, '[#cached]', file=sys.stderr)
                        return resp
                except Exception:
                    if '--debug' in sys.argv:
                        print('[download]', url, '[#failed-to-retrieve]', file=sys.stderr)

        LEGIFRANCE_PROXY = None
        if "legifrance.gouv.fr" in url:
            LEGIFRANCE_PROXY = os.getenv("LEGIFRANCE_PROXY")
            if not LEGIFRANCE_PROXY:
                raise Exception("You must configure a legifrance-proxy instance to be able to requests Légifrance, see lawfactory_utils README")
            url = LEGIFRANCE_PROXY + url.split('legifrance.gouv.fr')[1]

        if '--debug' in sys.argv:
            print('[download]', url, file=sys.stderr)

        resp = requests.get(url, headers={
            'User-Agent': 'https://github.com/regardscitoyens/the-law-factory-parser (Compat: Mozilla)'
        })

        if LEGIFRANCE_PROXY and LEGIFRANCE_PROXY in url:
            resp.url = resp.url.replace(LEGIFRANCE_PROXY, "https://www.legifrance.gouv.fr")

        if 500 <= resp.status_code < 600:
            raise HTTPError('%s Server Error for url: %s' % (resp.status_code, url), response=resp)

        if CACHE_ENABLED:
            if not os.path.exists(cache_directory()):
                os.makedirs(cache_directory())
            with open(file, 'wb') as f:
                pickle.dump(resp, f)
        return resp
    except (ConnectionError, HTTPError) as e:
        if retry:
            time.sleep(1)
            return download(url, retry=retry-1)
        raise e


def pre_clean_url(url):
    if url.startswith('www'):
        url = "http://" + url
    if url.startswith('/leg/http'):
        url = url[5:]
    return url


def get_redirected_url(url):
    """Returns redirected URL"""
    return download(url).url


def validate_link_CC_decision(url):
    if not url:
        return False
    url = url.lower().replace('http://', 'https://')
    if not url.startswith('https://www.conseil-constitutionnel.fr/decision/'):
        return False
    if url.count('/') != 5:
        return False
    if not url.endswith('dc.htm'):
        return False
    return True


def find_stable_link_for_CC_decision(url):
    if url == 'http://www.conseil-constitutionnel.fr/decision.50309.html':
        url = 'https://www.conseil-constitutionnel.fr/decision/2010/2010615dc.htm'
    resp = download(url)

    if resp.status_code is not 200:
        # try to fix "acces-par-date" urls
        if 'acces-par-date' in url:
            year, num = url.split('decision-n-')[1].split('-dc-')[0].split('-')
            stable_format = "https://www.conseil-constitutionnel.fr/decision/{year}/{year}{num}DC.htm"
            new_url = stable_format.format(year=year, num=num)
            new_resp = download(new_url)
            if new_resp.status_code is 200:
                return new_resp.url
        # TODO: use log_error
        print('[WARNING] INVALID CC URL - ', url, resp.status_code, file=sys.stderr)

    return resp.url # redirected url


def find_jo_link(url):
    resp = download(url)
    m = re.search(r'(https://www\.legifrance\.gouv\.fr/affichTexte.do\?cidTexte=[\w\d]+)&amp;dateTexte=\d+', resp.text)
    if m:
        return m.group(0) + '&categorieLien=id'
    else:
        # TODO: use log_error
        print('[WARNING] INVALID JO URL - ', url, file=sys.stderr)
        return url


AN_NEW_URL_TEMPLATE = "http://www.assemblee-nationale.fr/dyn/{legislature}/dossiers/{slug}"
AN_OLD_URL_TEMPLATE = "http://www.assemblee-nationale.fr/{legislature}/dossiers/{slug}.asp"


re_clean_ending_digits = re.compile(r"(\d+\.asp)[\dl]+$")
def clean_url(url):
    """
    Normalize the url and clean it

    >>> clean_url("http://www.assemblee-nationale.fr/15/dossiers/le_nouveau_dossier.asp#deuxieme_partie")
    'http://www.assemblee-nationale.fr/dyn/15/dossiers/deuxieme_partie'
    >>> clean_url("http://www.conseil-constitutionnel.fr/conseil-constitutionnel/francais/les-decisions/acces-par-date/decisions-depuis-1959/2013/2013-681-dc/decision-n-2013-681-dc-du-5-decembre-2013.138900.html")
    'https://www.conseil-constitutionnel.fr/decision/2013/2013681DC.htm'
    >>> clean_url('https://www.legifrance.gouv.fr/eli/loi/2017/9/15/JUSC1715752L/jo/texte')
    'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000035567936'
    >>> clean_url('https://www.legifrance.gouv.fr/UnTexteDeJorf.do?numjo=SSAX2011914L')
    'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000042219373'
    """
    url = url.strip()

    # fix urls like 'pjl09-518.htmlhttp://www.assemblee-nationale.fr/13/ta/ta051`8.asp'
    if url.find('https://') > 0:
        url = 'https://' + url.split('https://')[1]
    if url.find('http://') > 0:
        url = 'http://' + url.split('http://')[1]

    scheme, netloc, path, params, query, fragment = urlparse(url)

    path = path.replace('//', '/')

    if 'xtor' in fragment:
        fragment = ''

    # fix url like http://www.senat.fr/dossier-legislatif/www.conseil-constitutionnel.fr/decision/2012/2012646dc.htm
    if 'www.conseil-' in url:
        url = urlunparse((scheme, netloc, path, params, query, fragment))
        url = 'http://www.conseil-' + url.split('www.conseil-')[1]
        return find_stable_link_for_CC_decision(url)

    if 'legifrance.gouv.fr' in url:
        params = ''
        url_jo_params = parse_qs(query)

        if 'UnTexteDeJorf' in path:
            url = url.replace("UnTexteDeJorf.do", "WAspad/UnTexteDeJorf.do")
            newurl = get_redirected_url(url)
            if url != newurl:
                return clean_url(newurl)

        if 'WAspad' in path or 'affichTexte.do' in path:
            newurl = get_redirected_url(url)
            if url != newurl:
                return clean_url(newurl)

        if 'cidTexte' in url_jo_params:
            query = 'cidTexte=' + url_jo_params['cidTexte'][0]
        elif path.endswith('/jo/texte'):
            newurl = get_redirected_url(url)
            if url != newurl:
                return clean_url(newurl)

        if netloc == 'legifrance.gouv.fr':
            netloc = 'www.legifrance.gouv.fr'
        if 'jo_pdf.do' in path and 'id' in url_jo_params:
            path = 'affichTexte.do'
            query = 'cidTexte=' + url_jo_params['id'][0]

        # new legifrance wants to add an useless r=XXXXX variable
        if query.startswith('r='):
            query = ""

        # ensure to link initial version of the text and not furtherly modified ones
        if query.startswith('cidTexte'):
            query += '&categorieLien=id'

        path = path.replace('./affichTexte.do', 'affichTexte.do')

        # ensure it links to the initial version for the new legifrance links
        if 'loda/id/JORFTEXT' in path:
            path_parts = [part for part in path.split('/') if part]
            if not path_parts[-1].startswith("JORFTEXT") and path_parts[-2].startswith("JORFTEXT"):
                path_parts = path_parts[:-1]
                path = '/'.join(path_parts)
                path = path.replace('loda/id', 'jorf/id')

    if 'senat.fr' in netloc:
        path = path.replace('leg/../', '/')
        path = path.replace('dossierleg/', 'dossier-legislatif/')

        # normalize dosleg url by removing extra url parameters
        if 'dossier-legislatif/' in path:
            query = ''
            fragment = ''

    if netloc == 'webdim':
        netloc = 'www.assemblee-nationale.fr'

    # force https
    if 'assemblee-nationale.fr' not in netloc and 'conseil-constitutionnel.fr' not in netloc:
        scheme = 'https'

    # url like http://www.assemblee-nationale.fr/13/projets/pl2727.asp2727
    if 'assemblee-nationale.fr' in url:
        path = re_clean_ending_digits.sub(r"\1", path)
        if '/dossiers/' in path:
            url = urlunparse((scheme, netloc, path, params, query, fragment))
            legislature, slug = parse_national_assembly_url(url)
            if legislature and slug:
                template = AN_OLD_URL_TEMPLATE
                if legislature > 14:
                    template = AN_NEW_URL_TEMPLATE
                return template.format(legislature=legislature, slug=slug)

    return urlunparse((scheme, netloc, path, params, query, fragment))


def parse_national_assembly_url(url_an):
    """Returns the slug and the legislature of an AN url

    >>> # old format
    >>> parse_national_assembly_url("http://www.assemblee-nationale.fr/14/dossiers/devoir_vigilance_entreprises_donneuses_ordre.asp")
    (14, 'devoir_vigilance_entreprises_donneuses_ordre')
    >>> # new format
    >>> parse_national_assembly_url("http://www.assemblee-nationale.fr/dyn/15/dossiers/retablissement_confiance_action_publique")
    (15, 'retablissement_confiance_action_publique')
    >>> # sometimes there's a linked subsection, it's the real dosleg ID, we only use it if we are in the 15th legislature
    >>> parse_national_assembly_url("http://www.assemblee-nationale.fr/14/dossiers/le_dossier.asp#deuxieme_partie")
    (14, 'le_dossier')
    >>> parse_national_assembly_url("http://www.assemblee-nationale.fr/15/dossiers/le_nouveau_dossier.asp#deuxieme_partie")
    (15, 'deuxieme_partie')
    >>> # some dossier-like urls are not actual dossiers
    >>> parse_national_assembly_url("http://www.assemblee-nationale.fr/14/dossiers/motion_referendaire_2097.pdf")
    (14, None)

    """
    legislature_match = re.search(r"\.fr/(dyn/)?(\d+)/", url_an)
    if legislature_match:
        legislature = int(legislature_match.group(2))
    else:
        legislature = None

    slug = None
    slug_match = re.search(r"/([\w_\-]*)(?:\.asp)?(?:#([\w_\-]*))?$", url_an)
    if slug_match:
        if legislature and legislature > 14:
            slug = slug_match.group(2) or slug_match.group(1)
        else:
            slug = slug_match.group(1)

    return legislature, slug


if __name__ == "__main__":
    import doctest
    doctest.testmod()
