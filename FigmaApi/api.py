import requests

class FigmaApi:
    _BASE_URL = "https://api.figma.com"
    _HEADERS = {}

    def __init__( self, apiToken:str) :
        self._HEADERS["X-Figma-Token"] = apiToken
        pass

    def getFileHistory(self, key):
        url = self._BASE_URL + f"/v1/files/{key}/versions"
        return self._requestGet(url)

    def getFilesInfo(self, projectId):
        url = self._BASE_URL + f"/v1/projects/{projectId}/files"
        return self._requestGet(url)


    def getProjectsByTeamId(self, teamId):
        url = self._BASE_URL + f"/v1/teams/{teamId}/projects"
        return self._requestGet(url)

    def getMyUser(self):
        url = self._BASE_URL + "/v1/me"
        return self._requestGet(url)
    
    def _requestGet(self, url):
        headers = self._HEADERS
        data = requests.get(url, headers=headers)
        return data.json()