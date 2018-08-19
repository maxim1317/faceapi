#################################################
################# MS API CONSTS #################
#################################################

subscription_key = 'd83931a50c3c444da8deae372468f55f'
uri_base = 'https://northeurope.api.cognitive.microsoft.com/face/v1.0'

################### DETECTION ################### 

detect_headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

detect_params = {
    'returnFaceId': 'true',
    'returnFaceAttributes': 'smile',
}

################ GROUPS CREATION ################

group_headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

group_params = {
    'personGroupId' : '1534'
}

group_body = {
    'name': '',
}