import os

from groq import Groq
from exa_py import Exa

import os

def get_info(drug):

    exa = Exa('key')


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
    api_key="key",
)

def groqs(prompt, drug):

    result = get_info(drug)
    content = f"[non-verbose] Answer the question {prompt}, considering {drug} return ONLY a quick answer, responsibly, just the string and nothing more." #only the json structure: {{'quick-answer': string, 'explanation': string}}"
    #print(content)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model="llama3-8b-8192",
    )

    final = chat_completion.choices[0].message.content

    return final


#print(groqs("Can I take this while drunk?", "{'name': 'Duloxetine', 'manufacturer_name': 'Asclemed USA, Inc.', 'active_ingredients': [{'name': 'DULOXETINE HYDROCHLORIDE', 'strength': '30 mg/1'}]}"))
