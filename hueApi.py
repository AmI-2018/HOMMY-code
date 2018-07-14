from requests import request, RequestException


def send(method='GET', url=None, data=None, headers={}):
    # the response dictionary, initially empty
    response_dict = dict()

    # check that the URL is not empty
    if url is not None:
        # try to call the URL
        result = None
        try:
            # get the result
            result = request(method, url, data=data, headers=headers)
        except RequestException as e:
            # print the error
            print(e)

        # check result
        if result is not None:
            # consider the response content as JSON and put it in the dictionary
            response_dict = result.json()

    return response_dict