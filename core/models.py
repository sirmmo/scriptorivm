from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry

import json

# Create your models here.

class Tag(models.Model):
	name = models.TextField()
	class Meta:
		abstract=True

class PaperTag(Tag):
	pass
class GeoTag(Tag):
	pass


class Phase(models.Model):
	name = models.CharField(max_length=300)
	description = models.TextField(blank=True, null=True)
	year_from = models.IntegerField()
	year_to = models.IntegerField()

	def __str__(self):
		return self.name


class Geom(models.Model):
	name = models.TextField()
	description = models.TextField(blank=True, null=True)
	geometry = models.GeometryField()
	tags = models.ManyToManyField(GeoTag)
	objects = models.GeoManager()

	def __str__(self):
		return self.name

	def as_feature(self):
		r = {
			"type":"Feature",
			"properties":self.as_json(),
			"geometry": json.loads(GEOSGeometry(self.geometry).json)
		}
		return r

	def as_json(self, flat=False):
		r = {
			"name": self.name,
			"papers": [a.id for a in self.researches.all()],
			"tags": [a.name for a in self.tags.all()]
		}
		if flat:
			r["geometry"] = json.loads(GEOSGeometry(self.geometry).json)
		return r


class Paper(models.Model):
	owner = models.ForeignKey(User)

	uri = models.URLField()
	title = models.TextField()
	abstract = models.TextField()

	refers_to_period = models.ForeignKey(Phase)
	refers_to_geometry = models.ManyToManyField(Geom, related_name='researches')

	publication_date = models.DateField()
	tags = models.ManyToManyField(PaperTag)


	def as_timeline(self, mode="REF"):
		att = "refers_to_phase" if mode == "REF" else "publication_date"
		r = {
			"startDate": getattr(self, att),
			"headline": self.title,
			"text": self.abstract,
			"asset": {
				"media": "http://maps.google.com/maps?q=chicago&hl=en&sll=41.874961,-87.619054&sspn=0.159263,0.351906&t=t&hnear=Chicago,+Cook,+Illinois&z=11",
				"credit": "",
				"caption": ""
			}
		}
		return r
		

	def as_json(self):
		r = {
			"title":self.title,
			"uri":self.uri,
			#"refers_to_phase":self.refers_to_phase,
			"refers_to_geometry":self.refers_to_geometry.to_feature(),
			"publication_date":self.publication_date,
			"tags": [a.name for a in self.tags.all()]
		}
		return r
