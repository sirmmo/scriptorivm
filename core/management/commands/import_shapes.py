from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.gdal import SpatialReference, CoordTransform

from core.models import *

class Command(BaseCommand):
	def handle(self, *args, **options):
		Geom.objects.all().delete()

		ds_regiones = DataSource('/srv/scriptorium/scriptorium/shp/regiones.shp')
		tag_regio, c = GeoTag.objects.get_or_create(name="Regio")

		source = SpatialReference("32633")
		target = SpatialReference("4326")
		
		for l in ds_regiones:
			print l.fields
			for f in l:
				trans = CoordTransform(source, target)
				g = Geom()
				g.geometry = f.geom.geos
				g.geometry.transform(trans)
				g.name = f.get("Regio")
				g.description = ""
				g.save()
				g.tags.add(tag_regio)

		ds_insulae = DataSource('/srv/scriptorium/scriptorium/shp/insulae.shp')
		tag_insula, c = GeoTag.objects.get_or_create(name="Insula")

		source = SpatialReference("3857")

		for l in ds_insulae:      
			print l.fields
			for f in l:
				trans = CoordTransform(source, target)
				g = Geom()
				g.geometry = f.geom.geos
				g.geometry.transform(trans)
				g.name  = f.get("name")
				g.description = ""
				g.save()
				g.tags.add(tag_insula)


		ds_domi = DataSource('/srv/scriptorium/scriptorium/shp/domi.shp')
		tag_insula, c = GeoTag.objects.get_or_create(name="Domus")

		source = SpatialReference("32633")

		for l in ds_domi:      
			print l.fields
			for f in l:
				trans = CoordTransform(source, target)
				g = Geom()
				g.geometry = f.geom.geos
				g.geometry.transform(trans)
				g.name  = f.get("N2")
				g.description = f.get("N9")
				g.save()
				g.tags.add(tag_insula)


