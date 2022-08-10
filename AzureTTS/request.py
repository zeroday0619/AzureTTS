import aiohttp

from io import BytesIO


class RequestException(Exception):
    def __init__(self, status_code: int, message: str) -> None:
        """API Request Exception

        :param status_code: The HTTP status code
        :param message: The error message
        :rtype: object
        """
        self._message = message
        self._status_code = status_code

    def __str__(self) -> str:
        return f"{self._status_code}, {self._message}"


class MicrosoftTTS:
    def __init__(self, api_key: str) -> None:
        """simple aiohttp module

        :param api_key: Microsoft Azure subscription key
        """
        self._api_key = api_key
        self._api_url = "https://koreacentral.tts.speech.microsoft.com/cognitiveservices"

    async def get_voice_list(self) -> list[dict]:
        async with aiohttp.ClientSession(
                headers={
                    "Ocp-Apim-Subscription-Key": self._api_key
                }
        ) as req:
            async with req.get(
                    url=self._api_url + "/voices/list"
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                elif resp.status == 400:
                    raise RequestException(
                        status_code=resp.status,
                        message="A required parameter is missing, empty, or null. Or, the value passed to either a "
                                "required or optional parameter is invalid. A common reason is a header that's too "
                                "long. "
                    )
                elif resp.status == 401:
                    raise RequestException(
                        status_code=resp.status,
                        message="The request is not authorized. Make sure your subscription key or token is valid and "
                                "in the correct region. "
                    )
                elif resp.status == 429:
                    raise RequestException(
                        status_code=resp.status,
                        message="You have exceeded the quota or rate of requests allowed for your subscription."
                    )
                elif resp.status == 502:
                    raise RequestException(
                        status_code=resp.status,
                        message="There's a network or server-side problem. This status might also indicate invalid "
                                "headers. "
                    )
                else:
                    raise RequestException(
                        status_code=resp.status,
                        message="Unknown error occurred."
                    )

    @staticmethod
    def create_ssml(text: str, lang: str, gender: str) -> str:
        return f"""<speak version='1.0' xml:lang='{lang}'><voice xml:lang='{lang}' xml:gender='{gender}'
                name='en-US-ChristopherNeural'>{text}</voice></speak>"""

    async def write_to_fp(self, ssml_text: str, _io: BytesIO):
        _content_length = len(ssml_text)
        async with aiohttp.ClientSession(
                headers={
                    "Content-Type": "application/ssml+xml",
                    "Content-Length": _content_length,
                    "X-Microsoft-OutputFormat": "audio-24khz-16bit-24kbps-mono-opus"
                }
        ) as req:
            async with req.post(
                    url=self._api_url + "/v1",
                    data=ssml_text
            ) as resp:
                if resp.status == 200:
                    async for chunk in resp.content.iter_chunked(n=1024):
                        _io.write(chunk)
                elif resp.status == 400:
                    raise RequestException(
                        status_code=resp.status,
                        message="A required parameter is missing, empty, or null. Or, the value passed to either a "
                                "required or optional parameter is invalid. A common reason is a header that's too "
                                "long. "
                    )
                elif resp.status == 401:
                    raise RequestException(
                        status_code=resp.status,
                        message="The request is not authorized. Make sure your subscription key or token is valid and "
                                "in the correct region."
                    )
                elif resp.status == 415:
                    raise RequestException(
                        status_code=resp.status,
                        message="It's possible that the wrong Content-Type value was provided. Content-Type should be "
                                "set to application/ssml+xml."
                    )
                elif resp.status == 429:
                    raise RequestException(
                        status_code=resp.status,
                        message="You have exceeded the quota or rate of requests allowed for your subscription."
                    )
                elif resp.status == 502:
                    raise RequestException(
                        status_code=resp.status,
                        message="There's a network or server-side problem. This status might also indicate invalid "
                                "headers."
                    )
                else:
                    raise RequestException(
                        status_code=resp.status,
                        message="Unknown error occurred."
                    )
