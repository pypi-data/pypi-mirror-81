def isOpenApiv2(document):
    return type(document) is dict and 'swagger' in document and document["swagger"] == 2


def isOpenApiv3(document):
    return type(document) is dict and 'openapi' in document and document["openapi"] == 3


def isOpenApiv3_1(document):
    return type(document) is dict and 'openapi' in document and document["openapi"] == 3.1
