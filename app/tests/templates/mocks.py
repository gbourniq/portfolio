# File to mock some actual object:
# - Articles, Categories, SubCategories, > all details, comments, pictures


# from http import HTTPStatus

# from moltres.client.entities import (
#     DocumentClient,
#     DocumentTypeClient,
#     ProjectClient,
#     QuestionClient,
#     TagClient,
#     UserClient,
# )
# from moltres.data_objects import (
#     CheatSheet,
#     DocumentType,
#     Extraction,
#     Project,
#     Question,
#     Tag,
# )


# class BaseMock:
#     DEFAULT_RESPONSE_CODE = HTTPStatus.OK
#     NOT_FOUND_CODE = HTTPStatus.NOT_FOUND
#     CREATED = HTTPStatus.CREATED


# class MockDocumentTypeClient(BaseMock, DocumentTypeClient):
#     DEFAULT_ID = 1

#     def get(self, **kwargs):
#         return (
#             [MockDocumentTypeClient.default_document_type()],
#             BaseMock.DEFAULT_RESPONSE_CODE,
#         )

#     def analyse(self, document_type_id, analysis_id, question_ids):
#         return (
#             Extraction(MockDocumentTypeClient.default_extract_data()),
#             MockDocumentTypeClient.DEFAULT_RESPONSE_CODE,
#         )

#     @staticmethod
#     def default_document_type_data():
#         return {
#             "id": MockDocumentTypeClient.DEFAULT_ID,
#             "name": "project2",
#             "documents": ["http://localhost:8000/api/v1/document/3932"],
#             "questions": ["http://localhost:8000/api/v1/question/661"],
#             "project": "http://localhost:8000/api/v1/project/213",
#         }

#     @staticmethod
#     def default_document_type():
#         return DocumentType(MockDocumentTypeClient.default_document_type_data())

#     @staticmethod
#     def default_extract_data():
#         return {
#             "task_ids": ["task0", "task1", "task2"],
#             "document_task_ids": {"0": "task0", "1": "task1", "2": "task2"},
#         }


# class MockDocumentClient(BaseMock, DocumentClient):
#     def get(self, **kwargs):
#         return (
#             MockDocumentClient.default_documents(),
#             MockDocumentClient.DEFAULT_RESPONSE_CODE,
#         )

#     def download(self, document_id):
#         if MockDocumentClient.DEFAULT_RESPONSE_CODE < 400:
#             filename = MockDocumentClient.default_filename(document_id)
#         else:
#             filename = None

#         return (
#             {filename: MockDocumentClient.default_contents()},
#             MockDocumentClient.DEFAULT_RESPONSE_CODE,
#         )

#     def upload_from_path(self, document_type_id, path):
#         pass

#     @staticmethod
#     def default_documents():
#         return [{"id": 1}, {"id": 2}, {"id": 3}]

#     @staticmethod
#     def default_filename(document_id):
#         return f"mock_filename_{document_id}"

#     @staticmethod
#     def default_contents():
#         return b"mock_contents"


# class MockQuestionClient(BaseMock, QuestionClient):
#     DEFAULT_PREDICTOR_FNAME = "predictor.pkl"
#     DEFAULT_PREDICTOR_CONTENT = b"i am a gurken"
#     DEFAULT_QNUM = 1
#     DEFAULT_QTYPE = 1
#     DEFAULT_SEEDLING_ID = 1

#     def get(self, **kwargs):
#         return (
#             MockQuestionClient.default_questions(),
#             MockQuestionClient.DEFAULT_RESPONSE_CODE,
#         )

#     def pull_cheatsheet(self, question_id):
#         return (
#             MockQuestionClient.mock_cheatsheet(question_id),
#             MockQuestionClient.DEFAULT_RESPONSE_CODE,
#         )

#     def push_cheatsheet(self, question_id, cheatsheet):
#         return (
#             [MockQuestionClient.DEFAULT_SEEDLING_ID],
#             MockQuestionClient.DEFAULT_RESPONSE_CODE,
#         )

#     def pull_logic(self, question_id):
#         return {"logic": self.default_logic()}, MockQuestionClient.DEFAULT_RESPONSE_CODE

#     def push_logic(self, question_id, logic):
#         return {"logic": self.default_logic()}, MockQuestionClient.DEFAULT_RESPONSE_CODE

#     def pull_predictor(self, question_id):
#         return (
#             {
#                 MockQuestionClient.DEFAULT_PREDICTOR_FNAME: MockQuestionClient.DEFAULT_PREDICTOR_CONTENT
#             },
#             MockQuestionClient.DEFAULT_RESPONSE_CODE,
#         )

#     def push_predictor(self, question_id, predictor_bytes):
#         return (
#             MockQuestionClient.default_question(trained=True),
#             MockQuestionClient.DEFAULT_RESPONSE_CODE,
#         )

#     def train(self, question_id: int, seedling_id: int):
#         return (
#             {"task_id": f"mock-task-{question_id}"},
#             MockQuestionClient.DEFAULT_RESPONSE_CODE,
#         )

#     @staticmethod
#     def default_logic(dependent_qnums=["1"], prefix="Q"):
#         logic = {}
#         for idx, qnum in enumerate(dependent_qnums):
#             logic[f"if{idx}"] = {
#                 "if": {
#                     "big": {
#                         "nested": {"ast": {"question": {"value": f"{prefix}{qnum}"}}}
#                     }
#                 }
#             }
#         return logic

#     @staticmethod
#     def default_question_data(
#         _id=1, document_type=1, trained=False, logic=True, training_documents=[1, 2]
#     ):
#         if type(logic) == bool:
#             q_logic = MockQuestionClient.default_logic() if logic else {}
#         else:
#             q_logic = logic

#         return {
#             "id": _id,
#             "question_type": 0,
#             "document_type": document_type,
#             "text": f"question{_id}",
#             "qnum": _id,
#             "latest_seedling": None,
#             "trained": trained,
#             "training_documents": training_documents,
#             "logic": q_logic,
#         }

#     @staticmethod
#     def default_question(
#         _id=1, document_type=1, trained=False, logic=True, training_documents=[1, 2]
#     ):
#         return Question(
#             MockQuestionClient.default_question_data(
#                 _id, document_type, trained, logic, training_documents
#             )
#         )

#     @staticmethod
#     def default_questions(**kwargs):
#         return [
#             MockQuestionClient.default_question(1, **kwargs),
#             MockQuestionClient.default_question(2, **kwargs),
#             MockQuestionClient.default_question(3, **kwargs),
#         ]

#     @staticmethod
#     def default_cheatsheet_data(question_id, text="what is life?", labelled=True):
#         data = (
#             [
#                 {
#                     "document_name": "mock_doc",
#                     "document_answers": [
#                         {"end": 100, "text": "correct_answer", "start": 1}
#                     ],
#                 }
#             ]
#             if labelled
#             else []
#         )
#         return {
#             "question": {
#                 "q_type": MockQuestionClient.DEFAULT_QTYPE,
#                 "qnum": question_id,
#                 "text": text,
#                 "doc_type": "mock_doc_type",
#             },
#             "data": data,
#         }

#     @staticmethod
#     def mock_cheatsheet(question=1, text="what is life?", labelled=True):
#         return CheatSheet(
#             MockQuestionClient.default_cheatsheet_data(question, text, labelled)
#         )


# class MockProjectClient(BaseMock, ProjectClient):
#     NON_EXISTENT_PROJ_NAME = "I don't exist"

#     def create(self, name, description=""):
#         return (
#             MockProjectClient.default_project(name, description),
#             MockProjectClient.CREATED,
#         )

#     def get(self, **kwargs):
#         return (
#             MockProjectClient.default_projects(),
#             MockProjectClient.DEFAULT_RESPONSE_CODE,
#         )

#     def get_by_name(self, proj_name):
#         if proj_name == MockProjectClient.NON_EXISTENT_PROJ_NAME:
#             return None, MockProjectClient.NOT_FOUND_CODE
#         return (
#             MockProjectClient.default_project(proj_name),
#             MockProjectClient.DEFAULT_RESPONSE_CODE,
#         )

#     def get_permissions(self, proj_id):
#         return (
#             MockProjectClient.default_permissions(),
#             MockProjectClient.DEFAULT_RESPONSE_CODE,
#         )

#     @staticmethod
#     def default_project_data(name, description=""):
#         return {"id": 1, "name": name, "description": description}

#     @staticmethod
#     def default_project(name, description=""):
#         return Project(MockProjectClient.default_project_data(name, description))

#     @staticmethod
#     def default_projects():
#         return [
#             {"id": 1, "name": "mock_project_1"},
#             {"id": 2, "name": "mock_project_2"},
#             {"id": 3, "name": "mock_project_3"},
#         ]

#     @staticmethod
#     def default_permissions():
#         return [{"id": 1, "user": 1}, {"id": 2, "user": 2}]


# class MockTagClient(BaseMock, TagClient):
#     def get(self, **kwargs):
#         return [MockTagClient.default_tag()], MockTagClient.DEFAULT_RESPONSE_CODE

#     def create(self, name: str, document_type_id, questions, documents):
#         return MockTagClient.default_tag(), MockTagClient.CREATED

#     @staticmethod
#     def default_tag(name="mock_tag"):
#         return Tag(MockTagClient.default_tag_data(name))

#     @staticmethod
#     def default_tag_data(name):
#         return {"id": 1, "name": name, "analysis": 1}


# class MockUserClient(BaseMock, UserClient):
#     def get(self, user_id):
#         return MockUserClient.default_user()

#     @staticmethod
#     def default_user():
#         return [{"username": "test1", "email": "test1"}]
