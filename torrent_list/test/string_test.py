__author__ = 'Konstantin'

import unittest, re


str = 'Мачо и ботан 2 / 22 Jump Street 2001 (1800) (4000) (2017) (2014) (2012)BDRip [H.264/1080p-LQ]'

class RETestCase(unittest.TestCase):
    def test_get_year(self):
        # self.assertEqual(True, False)
        from datetime import date
        year, fill_name = '', ''

        p = re.compile("\(\d{4}\)")
        matches = p.findall(str)
        for m in matches:
            token = int(m[1 : -1])
            if (token > 1900) and (token < date.today().year + 1):
                year = token
                fill_name = str[:str.index(m)].strip()
                break
        print(year)
        print(fill_name)
        self.assertTrue(year)
        self.assertTrue(fill_name)


    def test_russian(self):
        from torrent_list.scraping.nnm_scraping import is_russian
        str = ('test sting', 'тесто', 'teфффtt')

        for token in str:
            if is_russian(token):
                print('Russian: %s' % token)
            else:
                print('English: %s' % token)


    def test_get_names(self):
        from torrent_list.scraping.nnm_scraping import get_names
        names = (str,
                    'прив/second / third/fourth / fifth',
                    'прив/second/third/fourth/fifth',
                    'прив/два/third/fourth/fifth',
                    'first/second / third/fourth / fifth')

        for token in names:
            name_rus, name_eng = get_names(token)
            print('\nRussian: %s' % name_rus)
            print('English: %s' % name_eng)


    def test_re_digit(self):
        # self.assertEqual(True, False)
        from datetime import date
        test_str = ('123', 't123', '123t',' 012 ', '987')

        p = re.compile("^[0-9]+$")
        for s in test_str:
            if p.match(s):
                print(s)

    def test_split_url(self):
        # self.assertEqual(True, False)
        from torrent_list.utils import split_url
        test_url = 'http://nnm-club.me/forum/viewtopic.php?t=852125'

        print(split_url(test_url))


if __name__ == '__main__':
    unittest.main()

