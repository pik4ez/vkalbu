# pip3 install vk
# https://github.com/dimka665/vk
import vkapicall


class VkApi():
    def __init__(self, token, sleep_interval=1, request_timeout=3,
            api_version='5.35'):
        self.token = token
        self.sleep_interval = sleep_interval
        self.request_timeout = request_timeout
        self.api_version=api_version
        self.api = None


    """Returns VkApiCall passing requested vk api method. """
    def __getattr__(self, method_name):
        api_call = vkapicall.VkApiCall(
                vkapi=self,
                method_name=method_name
                )
        return api_call
