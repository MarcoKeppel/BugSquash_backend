from django.http import HttpResponse
import requests
from django.views.decorators.csrf import csrf_exempt
from proxy.views import proxy_view
from . import controller as c
from BugSquash.models import Interaction, Routine
import json
import time


@csrf_exempt
def index(request):
    # requests.get('https://hackathon.bz.it/')
    # response = HttpResponse(requests.get('https://hackathon.bz.it/'))
    # response['Access-Control-Allow-Origin'] = '*'
    # extra_requests_args = {'Access-Control-Allow-Origin': '*'}
    # return proxy_view(request, 'http://website.twisty.cool')

    URL = "https://hackathon.bz.it/secure/login"

    return HttpResponse("SUP")


def add_routine(request):
    url = request.GET['target'].replace('"', '')
    name = request.GET['name'].replace('"', '')
    result = request.GET['result'].replace('"', '')
    interactions = json.loads(request.GET['interactions'])

    r = Routine()
    r.url = url
    r.name = name
    r.result = result
    r.save()

    counter = 0
    for interaction in interactions:
        i = Interaction()
        i.interaction_type = interaction['interaction_type']
        if i.interaction_type != 'click' and i.interaction_type != 'submit':
            i.content = interaction['content']
        i.element_id = interaction['id']
        i.fk_routine = r
        i.pos = counter
        i.save()
        counter += 1

    response = HttpResponse(json.dumps(True))
    response['Access-Control-Allow-Origin'] = '*'
    return response


# def proxy():
#     return proxy_view(request, 'http://website.twisty.cool')

def start_routine(request):
    name = request.GET['target'].replace('"', '')
    r = Routine.objects.get(name=name)
    interactions = Interaction.objects.filter(fk_routine=r)
    if len(interactions) == 0:
        return HttpResponse("Routine has no interaction")
    interactions = sorted(interactions, key=lambda x: x.pos, reverse=False)
    bug_squash = c.BugSquash(r.url)
    for interaction in interactions:
        if interaction.interaction_type == 'click':
            bug_squash.click_by_id(interaction.element_id)
        elif interaction.interaction_type == 'fill':
            bug_squash.fill_input_by_id(interaction.element_id, interaction.content)
        elif interaction.interaction_type == 'submit':
            bug_squash.get_first_form().submit()
    # time.sleep(1000)
    rtn = {'result': bug_squash.check_url(r.result), 'vitals': bug_squash.get_web_vitals()}
    response = HttpResponse(json.dumps(rtn))
    response['Access-Control-Allow-Origin'] = '*'
    return response


def debug(request):
    url = request.GET['target'].replace('"', '')
    if url is None:
        return HttpResponse("No url given")
    bug_squash = c.BugSquash(url)

    bug_squash.fill_input_by_id("_username", "hello")
    bug_squash.fill_input_by_id("_password", "hello")
    bug_squash.click_by_id("_submit")

    response = HttpResponse(url)
    response['Access-Control-Allow-Origin'] = '*'
    return response
