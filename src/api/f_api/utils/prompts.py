from langchain_core.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.prompts.prompt import PromptTemplate


def build_chatbot_prompt() -> ChatPromptTemplate:
    rag_prompt=PromptTemplate(
        input_variables=["context", "question"],
        template="""
            Answer the following question making use of the given context.
            If you don't know the answer, just say you don't know.

            -----------------
            Question:
            {question}

            -----------------
            Context:
            {context}
        """
    )

    prompt = rag_prompt
    input_variables=["context", "question"]

    return ChatPromptTemplate(
        input_variables=input_variables,
        messages=[HumanMessagePromptTemplate(prompt=prompt)]
    )
