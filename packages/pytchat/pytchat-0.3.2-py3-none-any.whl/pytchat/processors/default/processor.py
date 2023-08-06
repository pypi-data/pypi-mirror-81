import asyncio
import time
from .renderer.textmessage import LiveChatTextMessageRenderer
from .renderer.paidmessage import LiveChatPaidMessageRenderer
from .renderer.paidsticker import LiveChatPaidStickerRenderer
from .renderer.legacypaid import LiveChatLegacyPaidMessageRenderer
from .renderer.membership import LiveChatMembershipItemRenderer
from .. chat_processor import ChatProcessor
from ... import config

logger = config.logger(__name__)


class Chatdata:
    def __init__(self, chatlist: list, timeout: float):
        self.items = chatlist
        self.interval = timeout

    def tick(self):
        if self.interval == 0:
            time.sleep(1)
            return
        time.sleep(self.interval / len(self.items))

    async def tick_async(self):
        if self.interval == 0:
            await asyncio.sleep(1)
            return
        await asyncio.sleep(self.interval / len(self.items))


class DefaultProcessor(ChatProcessor):
    def process(self, chat_components: list):

        chatlist = []
        timeout = 0

        if chat_components:
            for component in chat_components:
                timeout += component.get('timeout', 0)
                chatdata = component.get('chatdata')
                if chatdata is None:
                    continue
                for action in chatdata:
                    if action is None:
                        continue
                    if action.get('addChatItemAction') is None:
                        continue
                    if action['addChatItemAction'].get('item') is None:
                        continue

                    chat = self._parse(action)
                    if chat:
                        chatlist.append(chat)
        return Chatdata(chatlist, float(timeout))

    def _parse(self, sitem):
        action = sitem.get("addChatItemAction")
        if action:
            item = action.get("item")
        if item is None:
            return None
        try:
            renderer = self._get_renderer(item)
            if renderer is None:
                return None

            renderer.get_snippet()
            renderer.get_authordetails()
        except (KeyError, TypeError) as e:
            logger.error(f"{str(type(e))}-{str(e)} sitem:{str(sitem)}")
            return None
        return renderer

    def _get_renderer(self, item):
        if item.get("liveChatTextMessageRenderer"):
            renderer = LiveChatTextMessageRenderer(item)
        elif item.get("liveChatPaidMessageRenderer"):
            renderer = LiveChatPaidMessageRenderer(item)
        elif item.get("liveChatPaidStickerRenderer"):
            renderer = LiveChatPaidStickerRenderer(item)
        elif item.get("liveChatLegacyPaidMessageRenderer"):
            renderer = LiveChatLegacyPaidMessageRenderer(item)
        elif item.get("liveChatMembershipItemRenderer"):
            renderer = LiveChatMembershipItemRenderer(item)
        else:
            renderer = None
        return renderer
