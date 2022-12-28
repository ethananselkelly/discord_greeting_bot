from final_project import get_quote, get_gif, get_gif_params
import re
import pytest
import asyncio
# from asynctest import CoroutineMock
from dotenv import load_dotenv


@pytest.mark.asyncio
async def test_gif():
    gif = await get_gif()
    # gif = asyncio.run(get_gif())
    print(gif)
    assert gif == None
#     assert gif == 'gif not found'
# async def test_gif():
#     assert type(get_gif()) == str
# @pytest.fixture
# def loop():
#     loop = asyncio.new_event_loop()
#     yield loop
#     loop.close()


# def test_coroutine2(loop: asyncio.AbstractEventLoop):
#     res = loop.run_until_complete(get_gif())
#     assert type(res) == str


# @pytest.mark.asyncio
# async def test_mock2():
#     with patch('example.long_computation', new=CoroutineMock()) as mocked_coro:
#         await launch_tasks(3)
#         mocked_coro.assert_has_calls(
#             [call(0), call(1), call(2)], any_order=True)

# def test_gif_params():
#     assert type(get_gif_params()) == str
#     assert re.match(r"^simpsons .+$", get_gif_params())


# def test_quote():
#     assert type(get_quote()) == str
#     assert '-' in get_quote()
#     assert re.match(r"^.+ - .+$", get_quote())
