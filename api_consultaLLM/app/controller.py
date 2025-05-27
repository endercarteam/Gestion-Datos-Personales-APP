from app.llm_service import GeminiService

class LLMController:
    def __init__(self):
        self.gemini_service = GeminiService()

    def process_query(self, query):
        """
        Procesa una consulta del usuario utilizando el servicio LLM
        """
        return self.gemini_service.process_query(query)
