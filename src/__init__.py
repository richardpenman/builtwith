import json
import os
import re
import sys
import urllib.request


def builtwith(url, headers=None, html=None, user_agent="builtwith"):
    """Detect the technology used to build a website"""
    techs = {}

    # check URL
    for app_name, app_spec in data["apps"].items():
        if "url" in app_spec:
            if contains(url, app_spec["url"]):
                add_app(techs, app_name, app_spec)

    # download content
    if None in (headers, html):
        try:
            request = urllib.request.Request(url, None, {"User-Agent": user_agent})
            if html:
                # already have HTML so just need to make HEAD request for headers
                request.get_method = lambda: "HEAD"
            response = urllib.request.urlopen(request)
            if headers is None:
                headers = response.headers
            if html is None:
                html = response.read()
        except Exception as e:
            print("Error:", e)

    # check headers
    if headers:
        for app_name, app_spec in data["apps"].items():
            if "headers" in app_spec:
                if contains_dict(headers, app_spec["headers"]):
                    add_app(techs, app_name, app_spec)

    # check html
    if html:
        for app_name, app_spec in data["apps"].items():
            for key in "html", "script":
                snippets = app_spec.get(key, [])
                if not isinstance(snippets, list):
                    snippets = [snippets]
                for snippet in snippets:
                    if contains(html, snippet):
                        add_app(techs, app_name, app_spec)
                        break

        # check meta
        # XXX add proper meta data parsing
        if isinstance(html, bytes):
            html = html.decode()
        regex = re.compile(
            "<meta[^>]*?name=['\"]([^>]*?)['\"][^>]*?content=['\"]([^>]*?)['\"][^>]*?>",
            re.IGNORECASE
        )
        metas = dict(regex.findall(html))
        for app_name, app_spec in data["apps"].items():
            for name, content in app_spec.get("meta", {}).items():
                if name in metas:
                    if contains(metas[name], content):
                        add_app(techs, app_name, app_spec)
                        break

    return techs


parse = builtwith


def add_app(techs, app_name, app_spec):
    """Add this app to technology"""
    for category in get_categories(app_spec):
        if category not in techs:
            techs[category] = []
        if app_name not in techs[category]:
            techs[category].append(app_name)
            implies = app_spec.get("implies", [])
            if not isinstance(implies, list):
                implies = [implies]
            for app_name in implies:
                add_app(techs, app_name, data["apps"][app_name])


def get_categories(app_spec):
    """Return category names for this app_spec"""
    return [data["categories"][str(c_id)] for c_id in app_spec["cats"]]


def contains(v, regex):
    """Removes meta data from regex then checks for a regex match"""
    if isinstance(v, bytes):
        v = v.decode()
    return re.compile(regex.split("\\;")[0], flags=re.IGNORECASE).search(v)


def contains_dict(d1, d2):
    """Takes 2 dictionaries

    Returns True if d1 contains all items in d2"""
    for k2, v2 in d2.items():
        v1 = d1.get(k2)
        if v1:
            if not contains(v1, v2):
                return False
        else:
            return False
    return True


def load_apps(filename="apps.json"):
    """Load apps from Wappalyzer JSON (https://github.com/ElbertF/Wappalyzer)"""
    # get the path of this filename relative to the current script
    # XXX add support to download update
    filename = os.path.join(os.getcwd(), os.path.dirname(__file__), filename)
    return json.load(open(filename))


data = load_apps()


if __name__ == "__main__":
    urls = sys.argv[1:]
    if urls:
        for url in urls:
            results = builtwith(url)
            for result in sorted(results.items()):
                print("%s: %s" % result)
    else:
        print("Usage: %s url1 [url2 url3 ...]" % sys.argv[0])
