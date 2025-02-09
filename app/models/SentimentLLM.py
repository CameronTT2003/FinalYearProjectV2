import json
import sys
import threading
import time
import itertools
import asyncio

# Third-party imports
from openai import OpenAI

# Initialize LM Studio client
client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")
MODEL = "llama-3.2-1b-instruct"

async def send_prompt_with_texts(initialText: str, texts: list):    
    prompt = "Look at all these comments and give me a paragraph. This is what the user posted: " + initialText
    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistant that processes user-provided comments. "
                "Respond to the prompt and summerise the list of comments provided focussing on sentiment."
                "You are to only give a paragraph and no statistical data."
            ),
        },
        {"role": "user", "content": f"{prompt}\n\nTexts: {json.dumps(texts)}"},
    ]

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True,
        )

        print("\nSentiment Assistant:", end=" ", flush=True)
        collected_content = ""
        for chunk in response:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                collected_content += content
        return collected_content

    except Exception as e:
        print(
            f"\nError communicating with LM Studio!\n\n"
            f"Please ensure:\n"
            f"1. LM Studio server is running at 127.0.0.1:1234 (hostname:port)\n"
            f"2. Model '{MODEL}' is downloaded\n"
            f"3. Model '{MODEL}' is loaded, or that just-in-time model loading is enabled\n\n"
            f"Error details: {str(e)}\n"
            "See https://lmstudio.ai/docs/basics/server for more information"
        )
        exit(1)


if __name__ == "__main__":
    # Example usage
    initialText = "This is a nice mushroom."
    texts = ['Anna the assistant 🍄🍄\u200d🟫', 'Awesome daddy!👍', 'Well that’s certainly an interesting mushroom. I never would have thought!', '>:(( \n\nIt is a nice one, though.\n\n:)', 'Hell yeah! So cute!', 'Hm, I’d never considered the biological lens cap holder option 🤣', '', 'Nice!', 'Nom nom nom nom', 'Hmmmm that is an interesting mushroom!', 'Love this so so SO much!', 'Adorable!! 🥰 Thank you for sharing!', 'luv the way she held the lens cap, awesome', "Do you ever see mushrooms that aren't so nice? Maybe a little grumpy, or mean?", 'I love that you get your kid involved. Making memories and teaching her so much about nature ❤️', 'YOU GOING TO EAT IT?', 'You have the cutest assistant ever!', 'Hell yeah!', "That's a nice daughter", 'Enjoy your mushroom postings…but I still prefer when you say, “Here are some nice mushrooms”. Something classy about it; makes my day! Thanks!', 'It 100% looks like the tree swallowed an orbital sander', 'What mushrooms are poisonous? (Asking for a friend) 😉', 'Nice', "Ya find LOTTA mushrooms where ev'a ya go don' ya?🤔.", 'Wow 🤗', 'What a big beautiful specimen!', 'Oak bracket??', 'Here’s some nice mushrooms I found a while back', 'Don’t wanna hear about no bushwhack baby, mind your six', "Dude, IT'S NOT A MUSHROOM!!  Wake up!", 'Adorable!!!\nI wish everyone raised their kids to appreciate the natural world!', 'Now you’ve got me looking closely at mushrooms. I found some very beautiful ones attached to emerged tree roots in my front yard. Thank you for expanding my mind and sense of beauty. 💙', 'Soft or squishy?', "Ahh, it's a baby. Thought it was a critter in the backpack.", "That's not a mushroom.", 'Love this! ❤️', 'Mushroom cliff 🙂', 'This one is a mood.', 'Your tiny assistant holds the lens cap 😭🥰', 'Horse hoof?', "It's so good having a helper!", '🤗', 'I found a lovely mushroom today and took a photo, you wanna see?', 'Hell yeah', 'Elephant ear?', 'Nice', "The mushroom, perhaps, found y'all.  🍄", "Looks like it's from a scifi movie. 😁", 'Love your sidekick!',  'Through all the noise, these intermittent pics of shrooms and fungi remind me of what life really is.', 'That little primate-grip on the lens cover.', 'We used to call these “conks” or “artist conk.”  The bottom is soft and white and you can draw on it with a sharp object and it turns dark. Spray a little clear finish on it and it’ll last for years.', 'One cool dad!! 👍😆', 'Yeah Anna!!! Way to make it happen!', 'I admire your helper. ✨', 'Sorry. That’s a lost walrus. Can you redirect him home?', 'So, you have your own little mushroom on your back, thanks, you just made my day :)', 'I love this so much! This is what I do with my granddaughter, Scarlet! Get them out there in the snow, get them out there and mother nature for the win-win!!!', "reminds me of an elephant's foot.", 'Sweet assistant!🥰', 'I think I found one like yours at Latourell Falls, OR', 'These mushrooms are fantastic. Thank you for sharing', 'Thank god for your posts… and I love the way that competent little hand comes up to take whatever it is that you’re handing her.🙏🏻🥰', 'The tree would care to differ.', 'It looks like an elephant foot bottom! 🐘', 'You, sir, are way too nice. 😂', 'Ribbit ribbit', 'That looks like an elephant foot 🤨🙃', 'thats a really cute mushroom', "This is so wholesome I can't handle it. 😍", 'I rename this mushroom to ashy knee', 'And the Lil one! \n\nVery Nice', '', "Your choice of course - this being the big bad world of social media an' all - but I was hoping for a proper glimpse of your little cutie.", 'Very cool!', "You'll need to translate what wee one is saying 🥰", 'Mushroom info - tinder conk: wikipedia.org/wiki/Fomes_fomentarius\n\nMore videos on my Patreon! Some free ones, even 🫶 Patreon.com/luke_venechukk', "it almost looks like a frog's mouth!!! hehe!!!", 'So sweet\nThanks for sharing with us ❤️❤️', 'nice', 'This is precious. Hell yeah! \n👶🏻🧔🏻\u200d♂️🤳🏻🍄\u200d🟫', 'It’s a facade. He’s not nice at all. Beware, he will betray confidences!', '', 'That brings back memories from 50 years  s ago. I think all 4 of our kids accompanied me doing lots of things while on my back like that. Great learning experience for the little ones while you accomplish things.', '', 'Hey Luke! You have a baby girl?!  \nIs that mushroom growing upside down?', "That one is very cool. What is it called. Here's one of my shroom shots", "You've trained your minion well, Anna! 😊😍", 'Enjoy it why you can strap them to your back and force them to do your silly man hobbies with you. \n\nThey will remember and by the time they are 9 you will be forever known as the terrorist who forced them to freeze to death when they would rather be watching Spongebob or Bluey.', 'That is a very nice mushroom', 'I am not a mushroom scientist, but I used to go for mushroom walks with my son when he was little. I love seeing the baby accompanying you!', 'Feed me, Seymour!', '🥰', 'Lovely day.', 'Wow! Fascinating facts!\n\nglowhub.com/blogs/news/1...', 'Sweet! Such a great little hiking buddy!', 'It’s the little hand grabbing the lens cap for me. 🥰', 'That looks like a horse hoof coming out of the tree.', "I also have found some just yesterday. I'd love to see some frogs just chilling on them lol.", 'Beauty!', '😀 @greenpeaceus.bsky.social', 'We love mushrooms. We just inoculated a bunch.', 'Awww. How sweet! 🍄\u200d🟫', 'Not really snowy.', "I admire your hobby!\nVery intrepid! As every collector knows, it's not just the joy of finding your prize, but the joy of the hunt. The anticipation of discovery, mellowed by the knowledge that you might just catch a cold instead. \nExcelsior!", 'Ahhhh!!! Love this!!! Ty for sharing!!! Have a mushroomie day!!🍄\u200d🟫🍄🍄\u200d🟫🍄🍄\u200d🟫🍄🍄\u200d🟫🍄🍄\u200d🟫', 'How great to share nature with the younger generation 👧🏼😊💕', 'Thank you mushroom.', 'This one is edible brother?\nIt looks just like a clam...', 'Phellinus', 'Do you have a small apprentice on your back?', 'Anna is a very good helper!', 'You did!', 'What an interesting shroom.', 'In this very mad world I love your pictures of mushrooms', 'This is new variant of fungi mushroom 🍄💜✨', 'Just read your second post. I should think and read on before I reply!', "Oh lukeluke! I hope you're right on that. I'm no expert but I don't think that particular fungus has the tree's best interest....", 'Looks like an elephant foot', 'Nice work papa. I just thought those little hands were for making cookies disappear, I didn’t know they doubled as a lens cap holder.', 'These conks have saved many a struggling fire from going out in my little cabin. Thanks for sharing such a great video - your personal assistant is adorable 😂']
    asyncio.run(send_prompt_with_texts(initialText, texts))
