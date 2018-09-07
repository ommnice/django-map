from django.shortcuts import render
from django.http import JsonResponse
from map.models import Cell

def map_view(request):	

	return render(request, 'map.html',{	
		'csvs' : check_import_csv_list(),	
	})	



def import_view(request):	
	return render(request, 'import_data.html',{	
			
	})	



def check_import_csv_list():

	import_csv_list = []
	cells = list(Cell.objects.all())
	for t in cells:
		if t.import_csv_name not in import_csv_list:
			import_csv_list.append(t.import_csv_name)

	print(import_csv_list)		
	return import_csv_list


def load_cell(request):

	data = {}
	data['display'] = []

	csv_name = request.GET.get('csv','')
	print('load cell from : %s' % csv_name)

	for c in list(Cell.objects.filter(import_csv_name=csv_name)):

	# for c in list(Cell.objects.all()):	
		print('%s-%s' % (c.import_csv_name, c.key))
		cell ={}
		cell['key'] = c.key
		cell['lng'] = c.longitude
		cell['lat'] = c.latitude
		cell['azimuth'] = c.azimuth
		cell['beamwidth'] = c.beamwidth

		data['display'].append(cell)


	data['response'] = 'success'	

	return JsonResponse(data)		

def upload_csv(request):

	print('start upload csv ...')

	data = {}

	uploaded_file 	= request.FILES['upload_csv']
	csv_name 		= request.FILES['upload_csv'].name
	file_data 		= uploaded_file.read().decode("utf-8")  
	lines 			= file_data.split('\n')
	isHeader		= True

	try:

		print('upload csv name: %s' % csv_name.replace('.csv',''))

		# remove old data
		for c in list(Cell.objects.filter(import_csv_name=csv_name.replace('.csv',''))):
			c.delete()

		for line in lines: 

			if isHeader:
				isHeader = False
				continue

			if ',' in line:	
				values = line.split(',')

				Cell.objects.create(
					import_csv_name=csv_name.replace('.csv',''), 
					tech=values[0], 
					key=values[1], 
					parent_id=values[2], 
					sub_parent_id=values[3], 
					cell_id=values[4], 
					antenna_id=values[5], 
					longitude=values[6], 
					latitude=values[7],
					azimuth=values[8],
					beamwidth=values[9])

		
		print('total imported cell count: %s' % len(Cell.objects.all()))
					
	except Exception as e:
		print(repr(e))
	

	data['result']  = 1
	data['display'] = 'Importing done.'
	
	print('upload csv done.')						
	return JsonResponse(data)		