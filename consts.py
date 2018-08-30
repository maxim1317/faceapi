##################################################
################### API CONSTS ###################
##################################################

subscription_key = 'd83931a50c3c444da8deae372468f55f'
uri_base = 'https://northeurope.api.cognitive.microsoft.com/face/v1.0'

groupID = '1534'

wait_time = 5

##################################################
################## LOCAL CONSTS ##################
##################################################

pics_needed = 6
threshold = 0.6
       
pic_dir = 'pics/frame/' # I save last frame here for cropping and stuff

##################################################
################## FRONT CONSTS ##################
##################################################

front_url = "http://localhost:9000/rest/userdata"

front_headers = {
    'Content-Type': 'application/json',
}
front_payload = {
    'userData' : None, 
    'inHelmet' : False,
}

#################################################



            

