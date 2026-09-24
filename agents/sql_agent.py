import sys
import os

# Add project root
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(PROJECT_ROOT)
sys.path.append(
    os.path.join(PROJECT_ROOT, "src")
)

from text2sql import Text2SQL
from answer_generator import AnswerGenerator


class SQLAgent:

    def __init__(self):

        self.text2sql = Text2SQL()
        self.answer_generator = AnswerGenerator()

    def run(self, query):

        print("\n" + "=" * 70)
        print("SQL AGENT")
        print("=" * 70)

        print("Question:")
        print(query)

        # Convert natural language to SQL
        sql = self.text2sql.generate_sql(query)

        print("\nGenerated SQL:")
        print(sql)

        if not sql:
            return "I could not generate an SQL query for this question."

        # Execute SQL
        sql_result = self.text2sql.execute_query(sql)

        # Generate final answer
        answer = self.answer_generator.generate_sql_answer(
            query,
            sql_result
        )

        return answer


# ==========================================================
# TEST SQL AGENT
# ==========================================================

if __name__ == "__main__":

    agent = SQLAgent()

    question = input(
        "\nEnter a database question: "
    )

    answer = agent.run(question)

    print("\n")
    print("=" * 70)
    print("SQL AGENT ANSWER")
    print("=" * 70)

    print(answer)
    