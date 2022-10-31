#!/bin/python3

from sys import argv

def usage(query):
    if query == []:
        print("""Usage:
    ./main.py [OPTION] [PARAMS]

Options:""")
        for k, v in params.items():
            print(f"    {k}\t{v['name']}\t{v['desc']}")
        print("""
For additional info on an option, run ./main.py h [OPTION]
""")
    else:
        query = filter(lambda q: q in params, query)
        if query != []:
            print(f"""Usage:
    ./main.py [{'|'.join(query)}] [PARAMS]

Description:""")
        for q in query:
            print(params[q]['details'])

params = {
    "h": {"func": usage, "name": "help", "desc": "gives additional info on an option or shows this description if no command specified",
        "details": f"""    (h)elp
        {'\n        '.join(n + '\t' + f"show the help for the '{p['name']}' option" for n, p in params.items())}
"""
    }

    # Define modes here (access to the AI, training of a new AI, testing of AI, modelization, scrapping, generating databases)
}

if __name__ == '__main__':
    if len(argv) == 0:
        usage([])
    else:
        mode, *args = argv
        params[mode]['func'](args)
