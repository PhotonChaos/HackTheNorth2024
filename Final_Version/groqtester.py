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

def groqs(prompt, drug):

    #result = get_info(drug)
    content = f"[non-verbose] Answer the question {prompt}, considering {drug}. Return ONLY a quick answer in string format."
    #print(content)

    try:
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
    
    except Exception as e:
        # Return error message
        return f"Error: {str(e)}"


#print(groqs("Can I take this while drunk?", "{'name': 'Duloxetine', 'manufacturer_name': 'Asclemed USA, Inc.', 'active_ingredients': [{'name': 'DULOXETINE HYDROCHLORIDE', 'strength': '30 mg/1'}]}"))
