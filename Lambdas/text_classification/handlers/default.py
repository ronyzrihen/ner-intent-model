from .BaseHandler import BaseHandler


class DefaultHandler(BaseHandler):
    def handle(self):
        return {
            "statusCode": 200,
            "body": "Sorry, I didn't understand your question."
        }
