from base62 import Base62Source
import exceptions as ex

class InMemoryStore:
    # static declared an in-memory dictionary for storing all the entries
    imdictionary = {}

    # static variable for keying the incoming entries into the dictonary
    key = 0

    # class method for creating an entry into the look-up mapping
    @classmethod
    def create_entry(cls, long_url):
        # checking for empty long url
        if long_url is None or not long_url.strip():
            raise ex.EmptyLongUrlException("Provided long url is empty. Please try with a valid url")

        # checking for duplicate entry
        longurl_entry_exists =  cls.long_url_entry_exists(long_url)
        if longurl_entry_exists:
            return longurl_entry_exists

        # proceeds to creating a new entry for lookup mapping
        cls.key = cls.key + 1
        short_code = Base62Source.base62encode(cls.key)
        cls.imdictionary[cls.key] = {
            "short_code" : short_code,
            "long_url" : long_url
        }
        return short_code

    # class method to check if long_url already exists
    @classmethod
    def long_url_entry_exists(cls, long_url):
        for key, value in cls.imdictionary.items():
            if value['long_url'] == long_url:
                return value['short_code']
        return None

    # class method for checking if there is a corresponding entry for the key
    @classmethod
    def entry_exists(cls, dict_id):
        return dict_id in cls.imdictionary and cls.imdictionary[dict_id] is not None

    # class method to retrieve the long_url
    @classmethod
    def get_long_url(cls, shortcode):
        if shortcode is None:
            raise ex.EmptyShortCodeException("The short url has no characters to uniquely identify a long url. Please try with a valid url")
        dict_id = Base62Source.base62decode(shortcode)
        if not cls.entry_exists(dict_id):
            raise ex.EntryDoesNotExistException("There is no entry for the corresponding short_url. Please try again with a valid url")
        return cls.imdictionary[dict_id]['long_url']
