import os
from zipfile import ZipFile

from WhatappToJson import WhatappToJson

class WhatsappFileReader(object):

    def convert_to_json(self, chat_path:str, device: str):
        return WhatappToJson.formatFile(source=chat_path, device=device,group_dates=True)

    def get_iphone_chat(self, file_name:str, path: str):
        files_to_extract: list
        complete_path = os.path.join(path, file_name)
        with ZipFile(complete_path,'r') as myzip:
            files_to_extract =  myzip.namelist()
            for zipped in files_to_extract:
                myzip.extract(zipped,path=path)
        
        chat_path = os.path.join(path,'_chat.txt')
        return chat_path, files_to_extract

    def get_android_chat(self, file_name:str, path: str):
        return os.path.join(path, file_name)

    def process_files(self):
        PENDING_FILE_PATH = 'data/pending'

        files = {}
        
        iphone_path = os.path.join(PENDING_FILE_PATH, 'iphone')
        files['iphone'] = [i for i in os.listdir(iphone_path) if i.endswith('.zip')]
        android_path = os.path.join(PENDING_FILE_PATH, 'android')
        files['android'] = [i for i in os.listdir(android_path) if i.startswith('WhatsApp Chat with ') and i.endswith('.txt')]
        
        print(f"iphone chats{len(files['iphone'])}\n Android {len(files['android'])}")

        for data in files['iphone']:
            chat, files_extracted  = self.get_iphone_chat(data, iphone_path)            
            chat_json = self.convert_to_json(chat, 'iphone')

            title = data.replace('WhatsApp Chat - ','').replace('.zip','')
            
            yield {'title': title,
                    'json': chat_json,
                    'file_to_move': [data],
                    'file_to_delete': files_extracted,
                    'path': iphone_path,
                    'device': 'iphone'
            }
        
        for data in files['android']:
            chat = self.get_android_chat(data, android_path)
            chat_json = self.convert_to_json(chat, 'android')
            title = data.replace('WhatsApp Chat with ','').replace('.txt','')
            
            yield {'title': title,
                    'json': chat_json,
                    'file_to_move': [data],
                    'file_to_delete': [],
                    'path': android_path,
                    'device': 'android'
            }