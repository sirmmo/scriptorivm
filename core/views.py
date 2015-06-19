from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.gis.geos import GEOSGeometry, Point
# Create your views here.

from core.models import *

import json

def index(request):
	return render(request, "map.html")

#CRUD OPS
@login_required
def upsert_paper(request, id=None):
	if request.method == "GET":
		return render(request, "form.html")
	else:
		pass

@login_required
def delete_paper(request, id):
	if request.method == "DELETE":
		pass
	else:
		pass


@login_required
def upsert_geometry(request, id=None):
	if request.method == "GET":
		return render("form.html", request)
	else:
		pass

@login_required
def delete_geometry(request, id):
	if request.method == "DELETE":
		pass
	else:
		pass

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

def geojson(request):
	filter = get_filter(request)

	ret = {"features":[], "type":"FeatureCollection"}

	#fix bbox
	for geom in Geom.objects.filter(**filter):
		ret["features"].append(geom.as_feature())

	return HttpResponse(json.dumps(ret))

def timeline(request, mode="REF"):
	filter = get_filter(request)
	
	ret = {
		"timeline": {
		"headline": "Research Timeline",
		"type": "default",
		"text": "",
		"date":[]
		}
	}

	order = "refers_to_date" if mode=="REF" else "publication_date"

	first = True
	for paper in Paper.objects.filter(**filter).order_by(order):
		if first:
			ret["startDate"] = getattr(paper, order)
			first = False
		ret["date"].append(paper.as_timeline(mode))

	return HttpResponse(json.dumps(ret))


def get_items(request):
	lon = float(request.GET.get("lon", "0.0"))
	lat = float(request.GET.get("lat", "0.0"))

	#period = json.loads(request.GET.get("phase", "[]"))

	p = Point(lon, lat, srid="4326")

	gs = Geom.objects.filter(geometry__contains=p)
	names=[]
	for g in gs:
		names.append("op:"+g.name)



	return HttpResponse(json.dumps(names))
