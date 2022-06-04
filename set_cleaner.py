import sys
import spacy
from spacy_langdetect import LanguageDetector
from csv import DictReader, DictWriter

USAGE = '''
USAGE: ./set_cleaner.py input_csv output_csv text_column
    input_csv - path to input file
    output_csv - path to output file
    text_column - name of the text column
'''


@spacy.language.Language.factory("language_detector")
def create_lang_detector(nlp, name):
    return LanguageDetector(language_detection_function=None)


nlp = spacy.load('ru_core_news_md')
nlp.add_pipe('language_detector')


def is_lang(text: str, lang: str) -> bool:
    text_lang = nlp(text)._.language
    return text_lang['language'] == 'ru' and text_lang['score'] >= 0.6


def clean(input_csv: str, output_csv: str, text_col: str) -> None:
    with (open(input_csv, 'r') as input_fd,
          open(output_csv, 'w') as output_fd):
        reader = DictReader(input_fd)
        writer = DictWriter(output_fd, fieldnames=reader.fieldnames)
        writer.writeheader()

        texts = set()

        for row in reader:
            text = row[text_col]
            # 1 Remove duplicates
            # 2 Remove anything not in Russian language
            if text not in texts and is_lang(text, 'ru'):
                texts.add(text)
                writer.writerow(row)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(USAGE, file=sys.stderr)
        exit(1)

    input_csv = sys.argv[1]
    output_csv = sys.argv[2]
    text_col = sys.argv[3]

    clean(input_csv, output_csv, text_col)
