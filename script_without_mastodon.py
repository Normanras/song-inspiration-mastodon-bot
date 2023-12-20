from gpt4all import GPT4All
import requests
import random
import string
import asyncio


MODEL = GPT4All(
    model_name="gpt4all-falcon-q4_0.gguf",
    #    model_path=(Path.home() / ".cache" / "gpt4all"),
    allow_download=False,
)

TIME_SIGNATURES = ["2/4", "3/4", "4/4", "2/2", "6/8", "9/8", "12/8"]

# Need to decide between manually entering this list or using ascii_letters, below
KEYS = ["A", "B", "C", "D", "E", "F", "G"]
SIGN = ["b", "#"]
NONKEYS = ["B#", "Cb", "E#", "Fb"]
# Option 2
MINOR = string.ascii_letters[0:7]
MAJOR = string.ascii_letters[26:33]
# and then use this:
# output = random.choice(KEYS)+random.choice(SIGN)


async def gather_sig_bpm():
    time_signature = random.choice(TIME_SIGNATURES)
    bpm = random.randrange(50, 201)
    return time_signature, bpm


async def gather_key():
    key = random.choice(KEYS) + random.choice(SIGN)
    while key in NONKEYS:
        key = random.choice(KEYS) + random.choice(SIGN)
    else:
        return key
        # if key not in NONKEYS:
        #     return key
        #     break
        # elif key in NONKEYS:
        #     pass


async def gather_theme():
    random_word = str(requests.get("https://random-word-api.herokuapp.com/word").text)[
        2:-2
    ]
    theme = MODEL.generate(
        f"Give me a writing prompt about {random_word}.",
        temp=0.7,
        callback=stop_on_token_callback,
    )
    theme = theme.splitlines()
    if len(theme) > 1:
        for x, line in enumerate(theme):
            if line.startswith("Sure"):
                del theme[x]
            elif line.endswith("."):
                theme = line
                return theme
    else:
        return theme


async def main():
    res = await asyncio.gather(gather_sig_bpm(), gather_key(), gather_theme())
    print(res)


def stop_on_token_callback(token_id, token_string):
    """
    Function to limit return length of the
    gpt4all response. Period indicates a sentence.
    """
    if "." in token_string:
        return False
    return True


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main())
    loop.close()
