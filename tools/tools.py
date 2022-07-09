import hashlib


class Hash:
    def __init__(self, data):
        self.data = data

    def get_hash(self):
        return int(hashlib.sha1(self.data.encode("utf-8")).hexdigest(), 16) % (10 ** 64)


if __name__ == '__main__':
    title = "簡単♫ほっこり優しい味✿鶏南蛮うどん✿"
    h = Hash(title)
    print(h.get_hash())

