from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.gis.geos import GEOSGeometry, Point
# Create your views here.

from core.models import *

import json
import requests

def index(request):
	return render(request, "map.html")

def timeline(request):
	return render(request, "timeline.html")


#visualize data
def get_filter(request):
	filter = {}
	bbox = request.REQUEST.get("bb")
	ref_ts = request.REQUEST.get("ref_ts")
	pub_ts = request.REQUEST.get("pub_ts")

	if bbox:
		filter["geom__crosses"] = bbox

	if ref_ts:
		filter["ref_ts"] = ref_ts

	if pub_ts:
		filter["pub_ts"] = pub_ts

	return filter

def get_tags(keys_only=True):
	op_tags = []
	op_intensity = {}
	r = requests.get("https://api.zotero.org/groups/360979/tags?start=0&limit=100&v=3").json()
	for tag in r:
		if "op:" in tag.get("tag"):
			if "." in tag.get("tag"):
					op_tags.append(tag.get("tag").split(":")[1])
					op_intensity[tag.get("tag")] = tag.get("meta").get("numItems")
					
			elif tag.get("tag").split(":")[1] in ["I","II","III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]:
					op_tags.append(tag.get("tag").split(":")[1])
					op_intensity[tag.get("tag")] = tag.get("meta").get("numItems")

			else:
					op_tags.append(tag.get("tag"))
					op_intensity[tag.get("tag")] = tag.get("meta").get("numItems")

	if keys_only:
		return op_tags
	else:
		return op_intensity

def geojson(request):
	filter = get_filter(request)

	ret = {"features":[], "type":"FeatureCollection"}

	op_tags = get_tags()


	filter["name__in"]=op_tags

	#fix bbox
	for geom in Geom.objects.filter(**filter):
		ret["features"].append(geom.as_feature())

	return HttpResponse(json.dumps(ret))

def the_timeline(request, mode="REF"):
	#filter = get_filter(request)
	#
	#ret = {
	#	"timeline": {
	#	"headline": "Research Timeline",
	#	"type": "default",
	#	"text": "",
	#	"date":[]
	#	}
	#}
#
	#order = "refers_to_date" if mode=="REF" else "publication_date"
#
	#first = True
	#for paper in Paper.objects.filter(**filter).order_by(order):
	#	if first:
	#		ret["startDate"] = getattr(paper, order)
	#		first = False
	#	ret["date"].append(paper.as_timeline(mode))
#
	#return HttpResponse(json.dumps(ret))
	ret = []

	tags = get_tags(False)
	for phase in Phase.objects.all():
		ret.append({
			"name":phase.name,
			"from":phase.year_from,
			"to":phase.year_to,
			"amount":tags.get(phase.symbol, 0),
			"filter":phase.symbol
		})
	return HttpResponse(json.dumps(ret))

def get_timeilne_items(request):
	phase = request.GET.get("phase")
	phases = {}
	phases[phase] = [phase]

	return get_filtered_items(phases)



def get_items(request):
	lon = float(request.GET.get("lon", "0.0"))
	lat = float(request.GET.get("lat", "0.0"))

	filter_prefix = "op:"

	#period = json.loads(request.GET.get("phase", "[]"))

	p = Point(lon, lat, srid="4326")

	gs = Geom.objects.filter(geometry__contains=p)
	names={}
	for g in gs:
		names["op:"+g.name]=[t.name for t in g.tags.all()]

	return get_filtered_items(names)

def get_filtered_items(names):

	ret = {}
	base_url = """https://api.zotero.org/groups/360979/items?start=0&limit=100&v=3&tag={}"""

	for name in names:
		if base_url != "":
				r = requests.get(base_url.format(name)).json()
		else:
				r = {}

		ret[name] = {"tags":names[name], "researches":r}

	return HttpResponse(json.dumps(ret))
