import os, tempfile, requests
from .common import singleton

@singleton
class TaboolaApi:
    _CLIENT_ID = os.getenv("CLIENT_ID")
    _CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    _ACCOUNT_ID = os.getenv("ACCOUNT_ID")

   

    def __init__(self) -> None:
        print(self._CLIENT_SECRET, self._CLIENT_ID)
        self.token = None
        self.msg = ""

        pass

    def get_token(self):
        # path = os.path.join(os.getcwd(), "backend/app/utils/token.txt")
        # with open(path, "r", encoding="utf-8") as f:
        #     self.token = f.read()
        #     return
        if self.token != None:
            return
        url = "https://backstage.taboola.com/backstage/oauth/token"

        payload = {
            "client_id": self._CLIENT_ID,
            "client_secret": self._CLIENT_SECRET,
            "grant_type": "client_credentials",
        }
        headers = {"content-type": "application/x-www-form-urlencoded"}

        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            self.token = result.get("access_token")
        print(response.text)

    def post_update_campaign(self, campaign_id, item_id, active=True):
        if not campaign_id:
            raise Exception(detail="capaign_id is null")
        url = f"https://backstage.taboola.com/backstage/api/1.0/{self._ACCOUNT_ID}/campaigns/{campaign_id}/items/{item_id}/"

        payload = {"is_active": active}
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        try:
            response = requests.post(url, json=payload, headers=headers)

            # print(response.text)
            if response.status_code == 200:
                self.msg = "修改成功！"
                return True
        except:
            self.msg = "修改失败"
            return False

    def taboola_update_campaign(self, site, operation):
        if not site:
            raise Exception(detail="capaign_id is null")

        url = f"https://backstage.taboola.com/backstage/api/1.0/{self._ACCOUNT_ID}/block-publisher"

        payload = {"sites": [site], "patch_operation": operation}
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        try:
            response = requests.patch(url, json=payload, headers=headers)

            # print(response.text)
            if response.status_code == 200:
                self.msg = "修改成功！"
                return True
        except:
            self.msg = "修改失败"
            return False


if __name__ == "__main__":
    t = TaboolaApi()
    t.get_token()
    t.update_campaign("27592812", "3731640592")
