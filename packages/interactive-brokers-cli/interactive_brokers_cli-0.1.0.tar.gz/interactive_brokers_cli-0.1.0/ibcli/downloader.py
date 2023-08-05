'''
    Downloader
'''

class Downloader:
    ''' Flex Query downloader '''
    def __init__(self):
        super().__init__()

    def get(self, id: int, token: str) -> str:
        ''' Downloads the Flex Query by id '''
        assert token is not None
        assert token != ''

        # Validation
        if id is None:
            raise ValueError(f"Flex Query id {id} is invalid.")

        # config = Config()
        # token = config.token

        # request
        parameters = self.get_ref_code(token, id)
        url = parameters[0]
        ref_code = parameters[1]

        # todo fetch the query results
        # https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService.GetStatement
        result_url = f"{url}?q={ref_code}&t={token}&v=3"

        content = self.__download(result_url)
        return content

    def get_ref_code(self, token, id):
        '''
        Creates a request. 
        Returns (url, ref_code)
        '''
        from ibcli.ib_response_parser import ResponseParser

        # send request
        request_url = f"https://gdcdyn.interactivebrokers.com/Universal/servlet/FlexStatementService.SendRequest?t={token}&q={id}&v=3"
        response = self.__download(request_url)

        # Parse response
        res_par = ResponseParser()
        resp = res_par.parse(response)
        status = resp.findtext("Status")
        if status != "Success":
            error_msg = f"Error downloading the reference code: {resp.text}"
            raise ValueError(error_msg)
        ref_code = resp.findtext("ReferenceCode")
        url = resp.findtext("Url")

        return (url, ref_code)

    def __download(self, url: str) -> str:
        import requests

        request = requests.get(url)
        #request.ok, status_code
        content = request.text
        return content
