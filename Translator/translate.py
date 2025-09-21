from tabulate import tabulate
from deep_translator import GoogleTranslator

class TranslateClass:
    def __init__(self, text, dest_lang="ar"):
        self.text = text
        self.dest_lang = dest_lang

    def translate(self) -> str:
        return GoogleTranslator(source="auto", target=self.dest_lang).translate(self.text)

    def as_table(self) -> str:
        translated = self.translate()
        data = [
            ["Language", "Sentence"],
            ["English", self.text],
            ["Hindi", translated],
        ]
        return tabulate(data, headers="firstrow", tablefmt="grid")

    def __str__(self):
        return self.as_table()

if __name__ == "__main__":
    sentence = input("Enter Sentence: ")
    print(TranslateClass(sentence, "ar"))