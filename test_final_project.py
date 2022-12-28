from final_project import get_quote, get_gif, get_gif_params
import re
import pytest
from dotenv import load_dotenv
import os


@pytest.mark.asyncio
async def test_gif():
    load_dotenv()
    TENOR_API = os.getenv('TENOR_API_KEY')
    TENOR_CLIENT = os.getenv('TENOR_API_CLIENT')
    gif = await get_gif(TENOR_API, TENOR_CLIENT)
    assert type(gif) == str
    assert gif.endswith('.gif') == True


def test_gif_params():
    assert type(get_gif_params()) == str
    assert re.match(r"^simpsons .+$", get_gif_params())


def test_quote():
    assert type(get_quote()) == str
    assert '-' in get_quote()
    assert re.match(r"^.+ - .+$", get_quote())
