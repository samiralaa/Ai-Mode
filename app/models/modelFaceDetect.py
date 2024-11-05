import requests


def verificationFaces(image):
    dictToSend = {'known': image }
    res = requests.post('https://finger-print-face-recognition.herokuapp.com/verify', files=dictToSend)

    return res.text
def detectFaces(image1,image2):
    dictToSend = {'known': image1 , 'unknown': image2}
    res = requests.post('https://finger-print-face-recognition.herokuapp.com/compare', files=dictToSend)
    print(res)

    return res.text