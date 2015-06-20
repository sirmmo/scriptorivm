from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.gdal import SpatialReference, CoordTransform

from core.models import *
import csv

class Command(BaseCommand):
	for 