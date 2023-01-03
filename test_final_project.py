from final_project import get_gif, get_gif_params, get_tweet, get_random_tweet, bearer_oauth
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


def test_get_tweets():

    tweets = get_tweet(bearer_oauth)
    assert type(tweets) == dict
    assert type(tweets['data']) == list
    assert len(tweets['data']) == 10


def test_random_tweet():
    tweet = get_random_tweet(get_tweet(bearer_oauth))
    assert type(tweet) == str
    assert 'twitter.com' in tweet
    assert re.match(
        r"^https:\/\/fxtwitter.com\/twitter\/status\/\d+$", tweet)
