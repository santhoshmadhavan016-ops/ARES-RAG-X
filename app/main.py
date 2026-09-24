import sys
import os

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(PROJECT_ROOT)
sys.path.append(
    os.path.join(PROJECT_ROOT, "src")
)
sys.path.append(
    os.path.join(PROJECT_ROOT, "agents")
)

from coordinator import AgentCoordinator


def main():

    coordinator = AgentCoordinator()

    print("\n")
    print("=" * 70)
    print("ARES-RAG X")
    print("MULTI-AGENT ENTERPRISE AI SYSTEM")
    print("=" * 70)

    print("\nSystem ready.")
    print("Type 'exit' to stop.")

    while True:

        query = input("\nEnter your question: ")

        if query.lower().strip() in [
            "exit",
            "quit"
        ]:

            print("\nExiting ARES-RAG X.")
            break

        answer = coordinator.run(query)

        print("\n")
        print("=" * 70)
        print("FINAL ANSWER")
        print("=" * 70)

        print(answer)


if __name__ == "__main__":
    main()
    