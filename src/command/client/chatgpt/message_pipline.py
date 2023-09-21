"""
    Currently, this module has a lot of parts which
    should be pushed in different single python programs.
    It's just a possible prototype of how logic of global message
    handler could be organised and concrete realization of
    how ChatGPT flow could be organised and integrated in global logic.
    Other flows are expected to be equal to ChatGPT flow.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, TypeVar, Generic, Dict, Any

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from script.main import BotApp
from src.common.global_fallback.unknown_command import ignored_texts_re

# TODO: It is need to think about how we are going to test such stuff,

# engine
_SelectHandlerRequest = TypeVar("_SelectHandlerRequest")


class Handler(Generic[_SelectHandlerRequest], ABC):
    class ProcessRequest:
        pass

    def __init__(self):
        pass

    @abstractmethod
    async def process(self, request: ProcessRequest):
        pass

    @abstractmethod
    def if_appropriate(self, request: _SelectHandlerRequest) -> bool:
        pass


HandlerType = TypeVar("HandlerType", bound=Handler)


class Factory(Generic[HandlerType, _SelectHandlerRequest], ABC):
    def __init__(self):
        self._handlers: List[HandlerType] = []

    def get(self, request: _SelectHandlerRequest) -> HandlerType:
        for handler in self._handlers:
            if handler.if_appropriate(request):
                return handler
        raise ValueError("There is not appropriate handler.")


""" messages handling pipline (for different flows) """


@dataclass()
class SelectMessageHandlerRequest:
    update: Update
    context: ContextTypes.DEFAULT_TYPE


class MessageHadler(Handler[SelectMessageHandlerRequest], ABC):
    @dataclass()
    class ProcessMessageRequest(Handler.ProcessRequest):
        update: Update
        context: ContextTypes.DEFAULT_TYPE

    def __init__(self):
        super().__init__()


# ChatGPT message handling pipline
class ChatGPTMessageHandler(MessageHadler):
    def if_appropriate(self, request: SelectMessageHandlerRequest):
        return request.context.user_data.get("GPT_active", False)

    async def process(self, request):
        # check for premium
        ...

        # check for tokens limit
        ...

        # go through embedding filters
        ...


# Chooser of active flow message handling pipline
class GlobalMessageHandler(Factory[MessageHadler]):
    def __init__(self):
        super().__init__()
        self._handlers = [ChatGPTMessageHandler()]

    async def process(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # choose active flow
        select_request = SelectMessageHandlerRequest(update, context)
        message_handler = self.get(select_request)

        # process message with active flow
        process_request = MessageHandler.ProcessMessageRequest(update, context)
        message_handler.process(process_request)


""" engine part for flow handlers """


# I think that each flow should be inherited from
# base class because they all should have common method
# get_handlers to register them in telegram application
class FlowHandler(ABC):
    @abstractmethod
    def get_handlers(self) -> Dict[int, Any]:
        pass


""" New handler that is not connected with specific flow """


# I think that logic of request message handling
# should be separated from single callback handler realization (for instance: ChatGptCallbackHandler)
# according to our diagram in Miro, because when new flow will be implemented
# it will be impossible to distinguish handling methods of different flows
# so as they have equal event when telegram should call them
class CommonHandler(FlowHandler):
    def __init__(self):
        self._request_handler = MessageHandler(
            filters.TEXT & ~(filters.Regex(ignored_texts_re) | filters.COMMAND),
            GlobalMessageHandler().process,
        )

    def get_handlers(self) -> Dict[int, Any]:
        pass


# usage example
if __name__ == "__main__":
    # just to show use case
    # (one of the reason to encapsulate app application realization instead of
    # just consequent command in the main, it will be usefull for different test)
    class TestBot(BotApp):
        def __init__(self):
            super().__init__()
            self._application.add_handlers(CommonHandler().get_handlers())
