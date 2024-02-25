import requests


class AwsData:
    """links a value with a sublist of children values"""
    skip_list = ['pkcs7', 'signature', 'openssh-key']
    skipper = True

    def __init__(self, val, address, parent=None, skp='', next_child=True):
        if skp in ['-a', '-aggro', '-all']:
            AwsData.skipper = False
        self.address = address
        self.value = val
        self.parent = parent
        self.children = self.get_next() if next_child else []

    def get_next(self):
        """queries current address + value to find and create next child list"""
        if AwsData.skipper and self.parent and self.parent.value in AwsData.skip_list:
            return []
        url = self.address + "/" + self.value
        response = requests.get(url)
        if response.status_code == 200:
            # filter json data
            if AwsData.skipper and len(response.text) >= 2:
                if response.text[0] in '{[' and response.text[-1] in '}]':
                    return [AwsData(data, url, self, next_child=False) for data in response.text.replace('/', '').split('\n') if data != '']
            # get next children
            return [AwsData(data, url, self) for data in response.text.replace('/', '').split('\n') if data != '']
        else:
            return []

    def display(self, depth=0):
        """output tree starting here"""
        print("-" * depth + self.value)
        for child in self.children:
            child.display(depth + 1)
