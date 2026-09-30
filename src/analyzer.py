from src.llm import complete
from src.prompts import ANSWER_SYSTEM


def summarize(question, df):
    preview = df.head(50).to_markdown(index=False)
    user = f"Question : {question}\n\nRésultat SQL :\n{preview}"
    return complete(ANSWER_SYSTEM, user)
