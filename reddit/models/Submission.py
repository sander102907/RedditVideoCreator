import praw
import markdown
from bs4 import BeautifulSoup
from nltk import tokenize

import nltk
nltk.download('punkt')

class Submission:
    def __init__(self, title: str, author: praw.models.Redditor, comments: list[praw.models.comment_forest] = None) -> None:
        self.title = title
        self.author = author
        self.comments = [] if comments is None else comments

    def add_comment(self, comment: praw.models.comment_forest):
        self.comments.append(comment)

    def get_tts_texts(self) -> list[str]:
        texts = []
        for comment in self.comments:
            comment_text = self.__md_to_text(comment.body)
            comment_texts = tokenize.sent_tokenize(comment_text)
            texts.append({'text': comment_texts, 'profile_img_url': comment.author.icon_img})
        return texts

    def get_full_tts_text(self) -> str:
        text = self.title + '\n'
        for comment in self.comments:
            comment_text = self.__md_to_text(comment.body)
            text += comment_text + '\n'
        return text

    def __md_to_text(self, md):
        html = markdown.markdown(md)
        soup = BeautifulSoup(html, features='html.parser')
        
        return soup.get_text().replace("’", "'")