from django.http import JsonResponse, HttpResponse
from rest_framework import status, authentication
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django.shortcuts import render, redirect
import requests
from io import BytesIO
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
import piexif
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from fractions import Fraction
from bs4 import BeautifulSoup
import tempfile
import random, os
from zipfile import *
from image_optimizer.models import *
import json

def to_deg(value, loc):
	"""convert decimal coordinates into degrees, munutes and seconds tuple
	Keyword arguments: value is float gps-value, loc is direction list ["S", "N"] or ["W", "E"]
	return: tuple like (25, 13, 48.343 ,'N')
	"""
	if value < 0:
		loc_value = loc[0]
	elif value > 0:
		loc_value = loc[1]
	else:
		loc_value = ""
	abs_value = abs(value)
	deg =  int(abs_value)
	t1 = (abs_value-deg)*60
	min = int(t1)
	sec = round((t1 - min)* 60, 5)
	return (deg, min, sec, loc_value)


def to_degrees(value):
	degrees = value[0][0] / value[0][1]
	minutes = value[1][0] / value[1][1] / 60
	seconds = value[2][0] / value[2][1] / 3600
	return degrees + minutes + seconds


def change_to_rational(number):
	"""convert a number to rantional
	Keyword arguments: number
	return: tuple like (1, 2), (numerator, denominator)
	"""
	f = Fraction(str(number))
	return (f.numerator, f.denominator)

def download_images2(request, url, entities, gps_lat, gps_long):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	images = [img["src"] for img in soup.find_all("img")]
	entity_list = entities.split(",")
	title = soup.title.string.strip().replace(" ", "_").lower().replace("|", "").replace(":", "")

	check_img = ImageOptimizer.objects.filter(url=url, entities=entities)
	if not check_img:
		print('not exist..')
		image = ImageOptimizer(
			url = url,
			entities = entities,
			user_id = request.user.id,
			gps_lat = gps_lat,
			gps_long = gps_long
		)
		image.save()
	else:
		print('exist..')

	with tempfile.TemporaryDirectory() as temp_dir:
		for i, image_url in enumerate(images):
			if '.jpg' in image_url:
				new_url = ".".join(image_url.split(".jpg")[:1]) + ".jpg"
				response = requests.get(new_url)
				print('response', response)

				# Add EXIF data to the image
				img = Image.open(BytesIO(response.content))
				print('this is img', img)
				print(GPSTAGS)

				# Get the EXIF data
				exif_data = img._getexif()
				for tag_id in exif_data:
					tag = TAGS.get(tag_id, tag_id)
					data = exif_data.get(tag_id)
					if isinstance(data, bytes):
						data = data.decode()
					print(f"this is sss {tag:25}: {data}")

				lat = 50
				lng = -3
				altitude = 1
				lat_deg = to_deg(lat, ["S", "N"])
				lng_deg = to_deg(lng, ["W", "E"])

				exiv_lat = (change_to_rational(lat_deg[0]), change_to_rational(lat_deg[1]), change_to_rational(lat_deg[2]))
				exiv_lng = (change_to_rational(lng_deg[0]), change_to_rational(lng_deg[1]), change_to_rational(lng_deg[2]))
				print('exiv_lat and exiv_lng', exiv_lat, exiv_lng)

				gps_ifd = {
					piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
					piexif.GPSIFD.GPSAltitudeRef: 1,
					piexif.GPSIFD.GPSAltitude: change_to_rational(round(altitude)),
					piexif.GPSIFD.GPSLatitudeRef: lat_deg[3],
					piexif.GPSIFD.GPSLatitude: exiv_lat,
					piexif.GPSIFD.GPSLongitudeRef: lng_deg[3],
					piexif.GPSIFD.GPSLongitude: exiv_lng,
				}
				print('gps_ifd', gps_ifd)

				zeroth_ifd = {piexif.ImageIFD.Make: u"Canon",
							piexif.ImageIFD.XResolution: (96, 1),
							piexif.ImageIFD.YResolution: (96, 1),
							piexif.ImageIFD.Software: u"Canon"
							}
				print('zeroth_ifd', zeroth_ifd)

				first_ifd = {piexif.ImageIFD.Make: u"Canon",
							piexif.ImageIFD.XResolution: (40, 1),
							piexif.ImageIFD.YResolution: (40, 1),
							piexif.ImageIFD.Software: u"Canon"
							}
				print('first_ifd', first_ifd)

				exif_com = {piexif.ExifIFD.UserComment: 'my message'.encode()}
				exif_dict = {"0th":zeroth_ifd,"GPS": gps_ifd,"1st":first_ifd,"Exif": exif_com,}
				exif_bytes = piexif.dump(exif_dict)

				print('exif_bytes', exif_dict)
				random_entity = random.choice(entity_list).strip().replace(" ", "_")
				
				check = ImageOptimizerFile.objects.filter(image_filename = f"{title}_{random_entity}_{i+1}.jpg")
				if not check:
					print('not exist..')
					image_file = ImageOptimizerFile(
						img_op_id = image.id,
						gps = "{} , {}".format(gps_lat, gps_long),
						exif_data = exif_data,
						image_filename = f"{title}_{random_entity}_{i+1}.jpg"
					)
					image_file.save()

				img.save(os.path.join(temp_dir, f"{title}_{random_entity}_{i+1}.jpg"), "JPEG", exif=exif_bytes)

		# Create a zip file of the downloaded images
		zip_file = BytesIO()
		with ZipFile(zip_file, 'w') as zip:
			for file in os.listdir(temp_dir):
				zip.write(os.path.join(temp_dir, file), file)

		# Return the zip file to the user as a download
		response = HttpResponse(zip_file.getvalue(), content_type='application/force-download')
		response['Content-Disposition'] = f'attachment; filename="{title}.zip"'
		print('response ', response)
		return response


@login_required
def user_image_optimizer(request):
	if request.method == 'POST':
		url = request.POST.get('url')
		entities = request.POST.get('entities')
		gps_lat = request.POST.get('latitude')
		gps_long = request.POST.get('longitude')
		response = download_images2(request, url, entities, gps_lat, gps_long)
		return response
	context = {
		'active_tab': 'image_optimizer',
	}
	return render(request, 'indexer-user/user-image-optimizer.html', context)



# DOWNLOAD AGAIN
def download_images2_again(request, pk, url, entities, gps_lat, gps_long):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	images = [img["src"] for img in soup.find_all("img")]
	entity_list = entities.split(",")
	title = soup.title.string.strip().replace(" ", "_").lower().replace("|", "").replace(":", "")

	image_op = ImageOptimizer.objects.filter(id = pk).first()
	image_op.url = url
	image_op.entities = entities
	image_op.save()

	with tempfile.TemporaryDirectory() as temp_dir:
		for i, image_url in enumerate(images):
			if '.jpg' in image_url:
				new_url = ".".join(image_url.split(".jpg")[:1]) + ".jpg"
				response = requests.get(new_url)
				print('response', response)

				# Add EXIF data to the image
				img = Image.open(BytesIO(response.content))
				print('this is img', img)
				print(GPSTAGS)

				# Get the EXIF data
				exif_data = img._getexif()
				for tag_id in exif_data:
					tag = TAGS.get(tag_id, tag_id)
					data = exif_data.get(tag_id)
					if isinstance(data, bytes):
						data = data.decode()
					print(f"this is sss {tag:25}: {data}")

				lat = 50
				lng = -3
				altitude = 1
				lat_deg = to_deg(lat, ["S", "N"])
				lng_deg = to_deg(lng, ["W", "E"])

				exiv_lat = (change_to_rational(lat_deg[0]), change_to_rational(lat_deg[1]), change_to_rational(lat_deg[2]))
				exiv_lng = (change_to_rational(lng_deg[0]), change_to_rational(lng_deg[1]), change_to_rational(lng_deg[2]))
				print('exiv_lat and exiv_lng', exiv_lat, exiv_lng)

				gps_ifd = {
					piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
					piexif.GPSIFD.GPSAltitudeRef: 1,
					piexif.GPSIFD.GPSAltitude: change_to_rational(round(altitude)),
					piexif.GPSIFD.GPSLatitudeRef: lat_deg[3],
					piexif.GPSIFD.GPSLatitude: exiv_lat,
					piexif.GPSIFD.GPSLongitudeRef: lng_deg[3],
					piexif.GPSIFD.GPSLongitude: exiv_lng,
				}
				print('gps_ifd', gps_ifd)

				zeroth_ifd = {piexif.ImageIFD.Make: u"Canon",
							piexif.ImageIFD.XResolution: (96, 1),
							piexif.ImageIFD.YResolution: (96, 1),
							piexif.ImageIFD.Software: u"Canon"
							}
				print('zeroth_ifd', zeroth_ifd)

				first_ifd = {piexif.ImageIFD.Make: u"Canon",
							piexif.ImageIFD.XResolution: (40, 1),
							piexif.ImageIFD.YResolution: (40, 1),
							piexif.ImageIFD.Software: u"Canon"
							}
				print('first_ifd', first_ifd)

				exif_com = {piexif.ExifIFD.UserComment: 'my message'.encode()}
				exif_dict = {"0th":zeroth_ifd,"GPS": gps_ifd,"1st":first_ifd,"Exif": exif_com,}
				exif_bytes = piexif.dump(exif_dict)

				print('exif_bytes', exif_dict)
				random_entity = random.choice(entity_list).strip().replace(" ", "_")
				
				print('this is img_id', image_op.id)
				check = ImageOptimizerFile.objects.filter(img_op_id = image_op.id, image_filename = f"{title}_{random_entity}_{i+1}.jpg")
				if not check:
					print('not exist..')
					image_file = ImageOptimizerFile(
						img_op_id = image_op.id,
						gps = "{} , {}".format(gps_lat, gps_long),
						exif_data = exif_data,
						image_filename = f"{title}_{random_entity}_{i+1}.jpg"
					)
					image_file.save()
				else:
					ImageOptimizerFile.objects.filter(img_op_id = image_op.id, image_filename = f"{title}_{random_entity}_{i+1}.jpg").update(
						gps = gps_ifd,
						exif_data = exif_data,
						image_filename = f"{title}_{random_entity}_{i+1}.jpg"
					)
					print('exist..')

				img.save(os.path.join(temp_dir, f"{title}_{random_entity}_{i+1}.jpg"), "JPEG", exif=exif_bytes)

		# Create a zip file of the downloaded images
		zip_file = BytesIO()
		with ZipFile(zip_file, 'w') as zip:
			for file in os.listdir(temp_dir):
				zip.write(os.path.join(temp_dir, file), file)

		# Return the zip file to the user as a download
		response = HttpResponse(zip_file.getvalue(), content_type='application/force-download')
		response['Content-Disposition'] = f'attachment; filename="{title}.zip"'
		print('response ', response)
		return response

@login_required
def download_image_again(request, pk):
	img = ImageOptimizer.objects.filter(id = pk).first()
	if request.method == 'POST':
		response = download_images2_again(request, pk, request.POST.get('up_url'), request.POST.get('up_entities') ,
			request.POST.get('up_latitude'), 
			request.POST.get('up_longitude'))
		return response
	context = {
		'img': img,
		'pk': pk
	}
	return render(request, 'indexer-user/user-image-optimizer-update.html', context)




