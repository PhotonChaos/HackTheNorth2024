import os

from groq import Groq
from exa_py import Exa

import os

def get_info(drug):

    exa = Exa('54f5502b-e7ac-450c-a021-cf7b139dfba5')


    result = exa.search_and_contents(
      f"R{drug}",
      type="neural",
      use_autoprompt=True,
      num_results=1,
      text=True,
    )
    #print(result)
    return result


client = Groq(
    api_key="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",
)

def groqs(drug):

    result = get_info(drug)
    content = f"Explain {drug}, here is some context {result}"
    print(content)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content

print(groqs("RANITIDINE HYDROCHLORIDE"))
