import configparser
import re

def get_submodules() -> list[dict[str,str]]:
    config = configparser.ConfigParser()
    config.read(".gitmodules")

    submodules = []
    for section in config.sections():
        name = section.split('"')[1]
        url = config[section]['url']
        submodules.append({'name': name, 'url': url})

    return submodules

def format_submodules_text(submodules: list[dict[str,str]]) -> str:
    formattedtxt: str = ""

    for module in submodules:
        formattedtxt +=f"- [*{module['name']}:*]({module['url']})\n"

    return formattedtxt

def update_readme(formatedtxt: str) -> None:
    with open("README.md", 'r') as file:
        content = file.read()

        new_content = re.sub(
            r'<!-- SUBMODULES_START -->(.*?)<!-- SUBMODULES_END -->',
            f'<!-- SUBMODULES_START -->\n{formatedtxt}\n<!-- SUBMODULES_END -->',
            content,
            flags=re.DOTALL
        )

    with open('README.md', 'w') as file:
        file.write(new_content)


def main():
    submodules = get_submodules()
    formattedtxt = format_submodules_text(submodules)
    update_readme(formattedtxt)
    print("✅ README updated with submodule info.")

if __name__ == '__main__':
    main()