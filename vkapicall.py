# pip3 install vk
# https://github.com/dimka665/vk
import vk
from time import sleep


class VkApiCall():
    def __init__(self, vkapi, method_name):
        self.vkapi = vkapi
        self.method_name = method_name


    """Returns new VkApiCall with appended method_name attr.

    Required for nested attrs like audio.search.
    """
    def __getattr__(self, method_name):
        return VkApiCall(
                vkapi=self.vkapi,
                method_name=self.method_name + '.' + method_name)


    """Passes call to vk api backend.

    Additionally manages request timeouts.
    """
    def __call__(self, **kwargs):
        # Initialize vk api backend.
        if not self.vkapi.api:
            print('init api')
            self.vkapi.api = vk.API(
                    access_token=self.vkapi.token,
                    api_version=self.vkapi.api_version,
                    timeout=self.vkapi.request_timeout,
                    )

        # As self.method_name can be nested, e.g. "audio.get", we should
        # get api.audio, then api.audio.get, and then call it with kwargs.
        api_method = self.multi_getattr(self.vkapi.api, self.method_name)
        result = api_method(**kwargs)
        # TODO store last request time, check it and sleep BEFORE api call
        sleep(self.vkapi.sleep_interval)

        return result


    """Returns nested attributes.

    Allows to get nested attributes, for example obj.nested.attr.
    Takes obj and attributes as a dot delimited string: 'nested.attr'.
    """
    def multi_getattr(self, obj, attr):
        attributes = attr.split('.')
        for a in attributes:
            obj = getattr(obj, a)
        return obj
