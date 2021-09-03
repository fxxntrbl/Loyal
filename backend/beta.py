from typing import Literal
from .request import LoyalRequest

GDMF_APPLE = "https://gdmf.apple.com/v2/assets"

ASSET_TYPE = {
    "SoftwareUpdate": "com.apple.MobileAsset.SoftwareUpdate",
    "MacSoftwareUpdate": "com.apple.MobileAsset.MacSoftwareUpdate",
    "SFRSoftwareUpdate": "com.apple.MobileAsset.SFRSoftwareUpdate",
}

AUDIENCE_IOS = {
    "release": "01c1d682-6e8f-4908-b724-5501fe3f5e5c",
    "internal": "ce9c2203-903b-4fb3-9f03-040dc2202694",
    "11": {"beta": "b7580fda-59d3-43ae-9488-a81b825e3c73"},
    "12": {"beta": "ef473147-b8e7-4004-988e-0ae20e2532ef"},
    "13": {"beta": "d8ab8a45-ee39-4229-891e-9d3ca78a87ca"},
    "14": {
        "developerbeta": "dbbb0481-d521-4cdf-a2a4-5358affc224b",
        "publicbeta": "84da8706-e267-4554-8207-865ae0c3a120",
    },
    "15": {
        "developerbeta": "ce48f60c-f590-4157-a96f-41179ca08278",
        "publicbeta": "9e12a7a5-36ac-4583-b4fb-484736c739a8",
    },
}

AUDIENCE_TVOS = {
    "release": "356d9da0-eee4-4c6c-bbe5-99b60eadddf0",
    "11": {"beta": "ebd90ea1-6216-4a7c-920e-666faccb2d50"},
    "12": {"beta": "5b220c65-fe50-460b-bac5-b6774b2ff475"},
    "13": {"beta": "975af5cb-019b-42db-9543-20327280f1b2"},
    "14": {"beta": "65254ac3-f331-4c19-8559-cbe22f5bc1a6"},
    "15": {"beta": "4d0dcdf7-12f2-4ebf-9672-ac4a4459a8bc"},
}

AUDIENCE_WATCHOS = {
    "release": "b82fcf9c-c284-41c9-8eb2-e69bf5a5269f",
    "4": {"beta": "f659e06d-86a2-4bab-bcbb-61b7c60969ce"},
    "5": {"beta": "e841259b-ad2e-4046-b80f-ca96bc2e17f3"},
    "6": {"beta": "d08cfd47-4a4a-4825-91b5-3353dfff194f"},
    "7": {"beta": "ff6df985-3cbe-4d54-ba5f-50d02428d2a3"},
    "8": {"beta": "b407c130-d8af-42fc-ad7a-171efea5a3d0"},
}

AUDIENCE_AUDIOOS = {
    "release": "0322d49d-d558-4ddf-bdff-c0443d0e6fac",
    "14": {"beta": "b05ddb59-b26d-4c89-9d09-5fda15e99207"},
    "15": {"beta": "58ff8d56-1d77-4473-ba88-ee1690475e40"},
}

AUDIENCE_MACOS = {
    "release": "60b55e25-a8ed-4f45-826c-c1495a4ccc65",
    "11": {
        "developerbeta": "ca60afc6-5954-46fd-8cb9-60dde6ac39fd",
        "publicbeta": "902eb66c-8e37-451f-b0f2-ffb3e878560b",
        "customerbeta": "215447a0-bb03-4e18-8598-7b6b6e7d34fd",
    },
    "12": {
        "developerbeta": "298e518d-b45e-4d36-94be-34a63d6777ec",
        "publicbeta": "9f86c787-7c59-45a7-a79a-9c164b00f866",
        "customerbeta": "a3799e8a-246d-4dee-b418-76b4519a15a2",
    },
}


class BetaHandler:
    def __init__(self) -> None:
        self.HTTP = LoyalRequest()
        super().__init__()

    def __parse_audience(
        self,
        device_type: Literal["iOS", "tvOS", "watchOS", "audioOS", "macOS"],
        version: str,
        beta_channel: str,
    ) -> str:
        if device_type == "iOS":
            if isinstance(AUDIENCE_IOS[version], str):
                return AUDIENCE_IOS[version]

            return AUDIENCE_IOS[version][beta_channel]

        if device_type == "tvOS":
            if isinstance(AUDIENCE_TVOS[version], str):
                return AUDIENCE_TVOS[version]

            return AUDIENCE_TVOS[version][beta_channel]

        if device_type == "watchOS":
            if isinstance(AUDIENCE_WATCHOS[version], str):
                return AUDIENCE_WATCHOS[version]

            return AUDIENCE_WATCHOS[version][beta_channel]

        if device_type == "audioOS":
            if isinstance(AUDIENCE_AUDIOOS[version], str):
                return AUDIENCE_AUDIOOS[version]

            return AUDIENCE_AUDIOOS[version][beta_channel]

        if device_type == "macOS":
            if isinstance(AUDIENCE_MACOS[version], str):
                return AUDIENCE_MACOS[version]

            return AUDIENCE_MACOS[version][beta_channel]

    async def get_asset(
        self,
        asset_type: str,
        device_type: str,
        version: str,
        channel: str,
        device: str,
        codename: str,
    ):
        post_data = {
            "ClientVersion": "2",
            "AssetType": ASSET_TYPE[asset_type],
            "AssetAudience": self.__parse_audience(device_type, version, channel),
            "ProductType": device,
            "HWModelStr": codename,
            "ProductVersion": "0",
            "BuildVersion": "0",
        }

        header = {"Content-Type": "application/json"}

        response = await self.HTTP.post(GDMF_APPLE, data=post_data)
