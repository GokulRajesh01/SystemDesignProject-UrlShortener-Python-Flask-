import exceptions as ex

class Base62Source:
    # string for base 62 scope creation
    base62scope = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    # static method for encoding using base62
    @staticmethod 
    def base62encode(id):
        base62shortcode = []
        while id != 0:
            base62shortcode.append(Base62Source.base62scope[id % 62])
            id = id // 62
        base62shortcode.reverse()
        return "".join(base62shortcode)

    # static method for decoding using base62
    @staticmethod
    def base62decode(short_code):
        id = 0
        shortcode_list = list(short_code)
        shortcode_list.reverse()
        for index, char in enumerate(shortcode_list):
            try:
                id = id + Base62Source.base62scope.index(char) * (62 ** index)
            except ValueError:
                raise ex.InvalidCharacterInShortCode("Unrecognized characters in Base62 Scope found in short code")
        return id