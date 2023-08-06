# coding: utf-8
from otrs_somconnexio.otrs_models.abstract_article import AbstractArticle


class MMSuccessArticle(AbstractArticle):
    """
    Creates an article with the MM account code that identifies the account where
    MM processed the ticket request"
    """

    def __init__(self, body):
        self.subject = "Petició d'alta a MM entrada correctament"
        self.body = body
