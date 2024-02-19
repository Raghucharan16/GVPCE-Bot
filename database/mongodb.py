from pymongo import MongoClient

class MongoDB:
    def __init__(self, uri: str, db_name: str, collection_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def find_question_paper(self, branch: str, year: int, subject: str):
        # Implement logic to query MongoDB based on branch, year, and subject
        query = {"branch": branch, "year": year, "subject": subject}
        question_paper = self.collection.find_one(query)
        return question_paper
