import requests
import json

HOST = 'http://3.67.196.232/'
class CRUD:

    def get_all_todo(self, url):
        response = requests.get(url + 'todo/all')
        if response.status_code == 200:
            return json.loads(response.text)
        elif response.status_code == 404:
            raise Exception('Нет такой записи')
        raise Exception('Непредвиденная ошибка')

    def create_todo(self, url, data: dict):
        response = requests.post(url + 'todo/create', data=json.dumps(data))
        if response.status_code == 200:
            return 1
        return 0

    def update_todo(self,url, id_: int):
        response = requests.put(url + f'todo/{id_}/update')
        if response.status_code == 200:
            return json.loads(response.text)

    def delete_todo(self, url, id_: int):
        response = requests.delete(url + f'todo/{id_}/delete')
        if response.status_code == 200:
            return json.loads(response.text)
