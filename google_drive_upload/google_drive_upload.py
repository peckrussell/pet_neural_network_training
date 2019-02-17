import os
import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google_drive_config import drive_folder_id

def json_in_out(fold_id_dict = None, direction = 'in'):
	if direction == 'in':
		with open('folder_id_dict.json', 'w') as write_file:
			json.dump(fold_id_dict, write_file)
	elif direction == 'out':
		# read out folder_id_dict if exists, otherwise make dict
		try:
			with open('folder_id_dict.json', 'r') as read_file:
				data = json.load(read_file)
		except:
			data = dict()
		return data
			
def authorization():
	gauth = GoogleAuth()
	# Try to load saved client credentials
	gauth.LoadCredentialsFile("mycreds.txt")
	if gauth.credentials is None:
	    # Authenticate if they're not there
	    gauth.LocalWebserverAuth()
	elif gauth.access_token_expired:
	    # Refresh them if expired
	    gauth.Refresh()
	else:
	    # Initialize the saved creds
	    gauth.Authorize()
	# Save the current credentials to a file
	gauth.SaveCredentialsFile("mycreds.txt")
	drive = GoogleDrive(gauth)
	
	return drive

def upload_folder(folder_path, photo_folder_name, photo_time):
	drive = authorization()

	# create new folder for images
	folder_id_dict = json_in_out(direction = 'out')
	folder_id = folder_id_dict.get(photo_folder_name)
	if folder_id == None:
		new_folder = drive.CreateFile({'title':photo_folder_name,
						'parents':[{'id':drive_folder_id}], 
						'mimeType':'application/vnd.google-apps.folder'
						})
		new_folder.Upload()
		folder_id = new_folder['id']
		#update folder id dictionary 
		folder_id_dict[photo_folder_name] = folder_id
		json_in_out(folder_id_dict, direction = 'in')
		print(photo_folder_name, 'Successfully Created in Google Drive')
	
	# upload content to Google Drive
	for photo in os.listdir(folder_path):
		if photo[-3:] == 'jpg' and photo_time in photo:
			new_file = drive.CreateFile({'parents':[{'kind':'drive#fileLink', 'id':folder_id}]})
			photo_path = folder_path + '/' + photo
			new_file.SetContentFile(photo_path)
			new_file.Upload()
	print('Photos Successfully Uploaded to Google Drive Folder:', photo_folder_name)


