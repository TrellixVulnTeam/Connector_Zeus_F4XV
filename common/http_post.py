import requests
import json
import datetime

headers = {}
class POST:
    def __init__(self, params='', ip='', port='',
                 user='', passw='', channel=''):
        self.params = params
        self.ip = ip
        self.user = user
        self.passw = passw
        self.channel = channel
        self.port = port




    def URLs(self,info=''):

        self.info = info
        URL = {

            'login': 'https://' + self.ip + ':' + self.port + '/cgi-bin/api/v1/system/login',
            'clients': 'https://' + self.ip + ':' + self.port + '/cgi-bin/api/v1/interface/wireless/1/clients',
            'version': 'https://' + self.ip + ':' + self.port + '/cgi-bin/api/v1/system/device',
            'noise': 'https://' + self.ip + ':' + self.port + '/cgi-bin/api/v1/interface/wireless/1/survey',
            'statusWireless': 'https://' + self.ip + ':' + self.port + '/cgi-bin/api/v1/interface/wireless/1/status',
            'statusSystem': 'https://' + self.ip + ':' + self.port + '/cgi-bin/api/v1/system/device/status'

        }

        if self.info == "login":
            return URL['login']
        if self.info == "clients":
            return URL['clients']
        if self.info == "version":
            return URL['version']
        if self.info == "noise":
            return URL['noise']
        if self.info == "statusWireless":
            return URL['statusWireless']
        if self.info == "statusSystem":
            return URL['statusSystem']

        return URL
    def login(self):
        payload = self.params
        post = requests.post(POST.URLs(self, 'login'), data=json.dumps(payload), verify=False, headers=headers)

        if post.status_code == 200:
            token = json.loads(post.content.decode('utf-8'))['data']['Token']
            headers['Authorization'] = 'Bauer ' + token

        return True

    def GetClients(self):

        post = requests.get(str(POST.URLs(self, 'clients')),verify=False, headers=headers)
        response = json.loads(post.content.decode('utf-8'))
        return response

    def GetVersion(self):

        post = requests.get(str(POST.URLs(self, 'version')), verify=False, headers=headers)
        response = json.loads(post.content.decode('utf-8'))
        return response

    def GetNoise(self):
        post = requests.get(str(POST.URLs(self, 'noise')), verify=False, headers=headers)
        response = json.loads(post.content.decode('utf-8'))
        size = len(response["data"])
        sum=0
        for i in range(size):
            signal = response["data"][i]["signal"]
            sum = sum - signal

        average = sum/size
        return round(average,2)

    def GetNoise_channelCount(self):
        post = requests.get(str(POST.URLs(self, 'noise')), verify=False, headers=headers)
        response = json.loads(post.content.decode('utf-8'))
        size = len(response["data"])
        return size

    def Getchannel(self):
        post = requests.get(str(POST.URLs(self, 'statusWireless')), verify=False, headers=headers)
        response = json.loads(post.content.decode('utf-8'))
        return int(response['data']['channel'])

    def GetNoise_ownChannel(self):

        Own_Channel = POST.Getchannel(self)
        post = requests.get(str(POST.URLs(self, 'noise')), verify=False, headers=headers)
        response = json.loads(post.content.decode('utf-8'))
        size = len(response["data"])
        sum = 0
        count = 0
        average = 0

        for i in range(size):
            get = response["data"][i]["signal"], response["data"][i]["channel"] == Own_Channel
            if (get[1] == True):
                signal = get[0]
                count = count + int(1)
                sum = sum - signal
        if count >= 1:
            average = sum / count
        return round(average,2)



    def GetNoise_byChannel(self):
        post = requests.get(str(POST.URLs(self, 'noise')), verify=False, headers=headers)
        response = json.loads(post.content.decode('utf-8'))
        size = len(response["data"])
        sum = 0
        count=0
        average=0
        for i in range(size):
            get = response["data"][i]["signal"], response["data"][i]["channel"] == int(self.channel)
            if (get[1] == True):
                #print(get[0])
                signal = get[0]
                count = count + int(1)
                sum = sum - signal
        if count >=1:
            average = sum / count
        return round(average,2)

    def GetUptime(self):
        post = requests.get(str(POST.URLs(self, 'statusSystem')), verify=False, headers=headers)
        response = json.loads(post.content.decode('utf-8'))
        time = str(datetime.timedelta(seconds=(response["data"]["uptime"])))
        return time





