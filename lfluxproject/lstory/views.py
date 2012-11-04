from django.shortcuts import get_object_or_404, redirect
from django.views.generic.simple import direct_to_template
from django.template import RequestContext
from django.template.loader import render_to_string
from datetime import datetime
from models import Story
from tumblelog.models import Post
from django.core.paginator import Paginator



# from http://dwiel.net/blog/python-parsing-the-output-of-datetime-isoformat/
def _parse_iso_datetime(s):
    # parse a datetime generated by datetime.isoformat()
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        try:
            return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            return datetime.strptime(s, "%Y-%m-%d")


def index(request, template='lstory/index.html'):
    stories = Story.objects.filter(published__isnull=False)
    return direct_to_template(request, template, {
        'stories': stories,
    })

def version(request, slug, date, template='lstory/highlight.html'):
    obj = Story.objects.get(slug=slug)
    date = _parse_iso_datetime(date)
    version = obj.versions.for_date(date)
    tumblepage = Paginator(Post.objects.for_parent(obj).public().filter(published_at__lte=date),10).page(request.GET.get('page', 1))

    return direct_to_template(request, template, {
        'current': version,
        'date': date,
        'mode': 'version',
        'tumbleposts': tumblepage,
    })


def diff(request, slug, model, template='lstory/highlight.html'):
    obj = get_object_or_404(model, slug=slug)

    if request.GET.get('date'):
        return redirect(obj.versions.for_date(_parse_iso_datetime(request.GET['date'])).get_version_url())

    cookie_lastread = request.session.get('last_read', {}).get(slug, None)

    fromdate = request.GET.get('since', None) or cookie_lastread or unicode(datetime.now().isoformat()) 
    fromdate = _parse_iso_datetime(fromdate) if fromdate else None

    todate = _parse_iso_datetime(request.GET['until']) if request.GET.get('until') else datetime.now()

    current = obj.versions.for_date(todate)
    previous = obj.versions.for_date(fromdate)

    tumblepage = Paginator(Post.objects.for_parent(obj).public(),10).page(request.GET.get('page', 1))


    may_track = not request.COOKIES.get('do_not_track')
    from_specified = 'since' in request.GET
    cookie_exists = cookie_lastread


    allow_mark_as_read = not request.GET.get('until') and not (may_track and cookie_exists and from_specified) # prevent popup only when specifying from_date while a cookie is already set

    embed_code = render_to_string('lstory/embedcode.html', {'story': current}, context_instance=RequestContext(request))


    response = direct_to_template(request, template, {
        'current': current,
        'previous': previous,
        'field_diff': current.diff_to_older(previous),
        'fromdate': fromdate,
        'todate': todate,
        'mode': 'highlight',
        'allow_mark_as_read': allow_mark_as_read,
        'tumbleposts': tumblepage,
        'embed_code': embed_code,
    })

    response.set_cookie('test', fromdate.isoformat(), httponly=False)
    return response


def summary(request, slug, date_end, template='lstory/highlight.html'):
    story = get_object_or_404(Story, slug=slug)
    summary = story.storysummary_set.get(timeframe_end=_parse_iso_datetime(date_end))
    previous, current = summary.storyversions()
    diff = current.diff_to_older(previous)
    return direct_to_template(request, template, {
        'story': story,
        'summary': summary,
        'field_diff': diff,
        'current': current,
        'previous': previous,
    })


def toggle_tracking(request, set_track=False):
    # fake the correct value for the context processor
    if not set_track:
        request.COOKIES['do_not_track'] = 'yup'
    else:
        if 'do_not_track' in request.COOKIES:
            del request.COOKIES['do_not_track']

    response = direct_to_template(request, 'lstory/mark_as_read_popup.inc', {})

    # actually change the cookie values
    if set_track:
        response.delete_cookie('do_not_track')
    else:
        response.set_cookie('do_not_track', 'yup')
        request.session.clear()
    return response


def mark_as_read(request, slug):
    value = request.GET.get('to_value', datetime.now().isoformat())
    x = request.session.get('last_read') or {}
    previous_value = x.get(slug, None)
    x[slug] = value
    request.session['last_read'] = x
    request.session.modified = True

    s = Story.objects.get(slug=slug)

    return direct_to_template(request, 'lstory/marked_as_read.inc', {
        'previous_value': previous_value,
        'current': s,
    })
