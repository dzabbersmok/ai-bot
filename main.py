import os
import sys
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_prompt
from call_function import available_functions, call_function
from config import MAX_ITERS

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("environment variable wasn't found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    if args.verbose:
        print("User prompt:", args.user_prompt)

    for _ in range(MAX_ITERS):
        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print("Final response")
                print(final_response)
                return
        except Exception as e:
            print(f"Error in generate_content: {e}")

    print(f"Maximum iterations ({MAX_ITERS}) reached")
    sys.exit(1)


def generate_content(client: OpenAI, messages: list, verbose: bool) -> None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
        temperature=0,
    )


    if not response.usage:
        raise RuntimeError("failed API request")


    if verbose:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")


    message = response.choices[0].message
    if not message.tool_calls:
        print("Response:")
        print(message.content)
        return

    messages.append(message)

    if not message.tool_calls:
        return message.content

    for tool_call in message.tool_calls:
        if tool_call.type != "function":
            continue

        function_args = json.loads(tool_call.function.arguments or "{}")
        print(f"Calling function: {tool_call.function.name}({function_args})")


        result_message = call_function(tool_call)
        if not result_message.get("content"):
            raise RuntimeError(f"Empty function response for {tool_call.function.name}")
        if verbose:
            print(f"-> {result_message['content']}")

        messages.append(result_message)

    return None

if __name__ == "__main__":
    main()
