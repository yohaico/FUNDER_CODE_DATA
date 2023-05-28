import openai
import time
import logger as logger

openai.api_key = ""


def get_response(text):
    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "assistant", "content": text},

                ]
            )
            # res = response.choices[0].text
            out_res = response["choices"][0]["message"]["content"]
            return out_res
        except Exception as e:
            logger.print_msg(str(e))
            time.sleep(1)
            continue
