from types import SimpleNamespace

import pytest

from agents.billing_agent import UserIdInjector


class FakeToolRequest:
    def __init__(self, args, runtime_config):
        self.name = "query_user_orders"
        self.args = args
        self.runtime = SimpleNamespace(config=runtime_config)

    def override(self, *, args):
        return FakeToolRequest(args=args, runtime_config=self.runtime.config)


@pytest.mark.asyncio
async def test_user_id_injector_overwrites_forged_user_id():
    interceptor = UserIdInjector()
    request = FakeToolRequest(
        args={"user_id": "user_9999", "limit": 5},
        runtime_config={"configurable": {"user_id": "user_1001"}},
    )
    captured_args = {}

    async def handler(new_request):
        captured_args.update(new_request.args)
        return {"ok": True}

    result = await interceptor(request, handler)

    assert result == {"ok": True}
    assert captured_args["user_id"] == "user_1001"
    assert captured_args["limit"] == 5
