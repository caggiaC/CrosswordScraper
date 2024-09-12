import json
import re


# this function is not mine: see https://www.codingem.com/python-range-of-letters/
def range_char(start, stop):
    return (chr(n) for n in range(ord(start), ord(stop) + 1))


def make_letters():
    with open("words.json") as f:
        words = json.load(f)
        letters = {}
        for letter in range_char("A", "Z"):
            letters[letter] = {
                'first': 0,
                'last': 0,
                'total':0
            }
        for entry in words:
            first = entry['first-letter']
            last = entry['last-letter']
            letters[first]['first'] += 1
            letters[first]['total'] += 1
            letters[last]['last'] += 1
            letters[last]['total'] += 1
        with open('letters.json', 'w') as fp:
            json.dump(letters, fp)


def make_phones():
    with open("words.json") as f:
        words = json.load(f)
        phones = {}
        for entry in words:
            try:
                phone_string = entry['phonemes'][0]
                phonemes = re.split(' ', phone_string)
                for phone in phonemes:
                    if phones.get(phone) is None:
                        phones[phone] = 1
                    else:
                        phones[phone] += 1
            except IndexError:
                continue
    with open('phones.json', 'w') as fp:
        json.dump(phones, fp)


def main():
    # make_letters()
    make_phones()


if __name__ == "__main__":
    main()
