import os

#################################################
################# MS API CONSTS #################
#################################################

subscription_key = 'd83931a50c3c444da8deae372468f55f'
uri_base = 'https://northeurope.api.cognitive.microsoft.com/face/v1.0'

groupID = '1535'

wait_time = 5

#################################################

pics_needed = 6
treshold = 0.6

# socket_port = 8086

#################################################

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

