from picamera import PiCamera
from time import time, localtime, strftime, sleep
import os
import argparse
import logging
import google_drive_upload as gdu

parser = argparse.ArgumentParser(description = 'Arguments for taking and labeling Raspberry Pi photos')
parser.add_argument('-t', action = 'store', dest = 'run_time', type = float, help = 'Length in minutes to take photos')
parser.add_argument('-f', action = 'store', dest = 'pic_freq', type = int, help = 'Frequency in seconds to take photos')
parser.add_argument('-l', action = 'store', dest = 'labels', type = str, help = 'List of names of individuals in photo, separated by _')
parser.add_argument('-c', action = 'store', dest = 'photo_count', type = int, help = 'Total number of photos to take, if this flag is included -t will be ignored')
args = parser.parse_args()
 
def make_photo_directory(labels):
   # return script dir to allow for client_secrets.json to be located   
   current_dir = os.getcwd()
   photos_dir = current_dir + '/' + 'piphotos_' + labels
   if not os.path.isdir(photos_dir):
      os.mkdir(photos_dir)
      print(photos_dir, 'Folder Created')
   return photos_dir, current_dir

def take_picture(camera, photo_folder, photo_freq, photo_time, labels):
   os.chdir(photo_folder + '/')
   logging.basicConfig(format = '%(asctime)s %(message)s', filename = 'photos.log', level = logging.DEBUG)
   t_end = time() + 60 * photo_time
   pic_count = 1
   t_wait = photo_freq - 3
   session_time = strftime('%Y%m%d_%H%M%S', localtime())

   while time() < t_end:
      for i in range(3,0,-1):
         print('Taking Photo in :', i, end = '\r')
         sleep(1)
      print('Taking Photo in : !', end = '\r')
      file_out = photo_folder + '/pipic_'+ labels + '_' + session_time + '_' + str(pic_count) + '.jpg'
      pic_count += 1
      try:
         camera.capture(file_out)
         logging.info('%s photo taken', file_out)
      except:
         logging.error('%s photo not added to folder, likely issue with PiCamera module', file_out)
      print('Waiting', t_wait, 'Seconds', end = '\r')
      sleep(t_wait)

   return pic_count, session_time

def folder_photo_deduplicate():
   import hashlib
   import imghdr
   from PIL import Image

   hash_dict = {}
   formats = ['jpeg', 'png']

   for i in os.listdir():
      if imghdr.what(i) in formats:
         with Image.open(i) as img:
            hash_val = hashlib.md5(img.tobytes()).hexdigest()
         if hash_val in hash_dict.keys():
            os.remove(i)
            hash_dict[hash_val] += 1
         else:
            hash_dict[hash_val] = 1
   return hash_dict


def move_to_s3():
   print('test')

def move_to_main_machine(my_ip=''):
   print('test')

def main():
  
   camera = PiCamera()
   photo_path, script_dir = make_photo_directory(args.labels)

   # take pics
   camera.start_preview()
   total_pics, photo_time = take_picture(camera, photo_path, args.pic_freq, args.run_time, args.labels)
   print('Pictures Taken :', total_pics)
   camera.stop_preview()

   # upload photos to google drive
   photo_folder_name = photo_path.split('/')[-1]
   os.chdir(script_dir + '/google_drive_upload')
   gdu.upload_folder(photo_path, photo_folder_name, photo_time)



main()
