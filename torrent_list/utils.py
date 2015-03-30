__author__ = 'Konstantin'


def split_url(url):
    spl = url.split('/')
    last = spl[-1]
    base_url = '/'.join(spl[0: -1]) + '/'

    return base_url, last

if __name__ == '__main__':
    test_url = 'http://nnm-club.me/forum/viewtopic.php?t=852125'

    print(split_url(test_url))