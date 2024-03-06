from django.apps import AppConfig
class GraderConfig(AppConfig):
    name = 'grader'

    def ready(self):
        import grader.signal
