#!/usr/bin/env python3

import openai
import config  # contains OPENAI_API_KEY

def main():
    # Set your OpenAI API key from config
    openai.api_key = config.OPENAI_API_KEY
    
    # Fetch and list all models your account can access
    models = openai.Model.list()
    for m in models["data"]:
        print(m["id"])

if __name__ == "__main__":
    main()
