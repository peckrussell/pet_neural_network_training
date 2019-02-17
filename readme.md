### Pet Neural Network Training

This is a script for use on a **Raspberry Pi** to take photos with the the **Raspberry Pi Camera Module V2** to take photos on a timer and upload
them to a google drive account.

Once enough photos have been uploaded for training Google Collaboratory can be used to train the neural network utilizing the free GPU/TPUs
on the platform.

### Script Use : camera_test.py
-----------------------------------------------------------------------------------------------------
#### ex) python3 camera_test.py -t 2 -f 10 -l 'milo'
* -t Length in minutes to take photos
* -f frequency in seconds to take photos
* -l List of names of individuals in photo (i.e. 'milo', 'milo_alex')
