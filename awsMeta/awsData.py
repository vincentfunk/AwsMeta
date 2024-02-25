import requests


class AwsData:
    """links a value with a sublist of children values"""
    skip_list = ['pkcs7', 'signature', 'openssh-key']
    skipper = True

    def __init__(self, val, address, parent=None, skp=''):
        if skp in ['-a', 'a', 'aggro', 'all']:
            AwsData.skipper = False
        self.address = address
        self.value = val
        self.parent = parent
        self.children = self.get_next()

    def get_next(self):
        if AwsData.skipper and self.parent and self.parent.value in AwsData.skip_list:
            return []
        url = self.address + "/" + self.value
        response = requests.get(url)
        if response.status_code == 200:
            return [AwsData(data, url, self) for data in response.text.replace('/', '').split('\n') if data != '']
        else:
            return []

    def display(self, depth=0):
        print("-" * depth + self.value)
        for child in self.children:
            child.display(depth + 1)
