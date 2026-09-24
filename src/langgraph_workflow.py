import sys
import os

from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# ============================================================
# PROJECT PATH
# ============================================================

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


# ============================================================
# IMPORT COMPONENTS
# ============================================================

from query_router import QueryRouter
from rag_agent import RAGAgent
from sql_agent import SQLAgent
from hybrid_agent import HybridAgent
from guardrails import Guardrails
from semantic_cache import SemanticCache


# ============================================================
# STATE
# ============================================================

class ARESState(TypedDict):

    query: str

    route: str

    answer: str

    query_allowed: bool

    answer_allowed: bool

    guardrail_reason: str

    cache_hit: bool


# ============================================================
# INITIALIZE COMPONENTS
# ============================================================

router = QueryRouter()

rag_agent = RAGAgent()

sql_agent = SQLAgent()

hybrid_agent = HybridAgent()

guardrails = Guardrails()

semantic_cache = SemanticCache()


# ============================================================
# GUARDRAIL NODE
# ============================================================

def guardrail_node(state):

    query = state["query"]

    print("\n")
    print("=" * 70)
    print("GUARDRAIL CHECK")
    print("=" * 70)

    validation = guardrails.validate_query(query)

    print("\nQuery:")
    print(query)

    print("\nAllowed:")
    print(validation["allowed"])

    print("\nReason:")
    print(validation["reason"])

    return {
        "query_allowed": validation["allowed"],
        "guardrail_reason": validation["reason"]
    }


# ============================================================
# GUARDRAIL ROUTER
# ============================================================

def guardrail_router(state):

    if state["query_allowed"]:

        return "semantic_cache"

    return "blocked"


# ============================================================
# BLOCKED NODE
# ============================================================

def blocked_node(state):

    print("\n")
    print("=" * 70)
    print("REQUEST BLOCKED")
    print("=" * 70)

    answer = (
        "Request blocked by security guardrails. "
        + state["guardrail_reason"]
    )

    return {
        "answer": answer,
        "answer_allowed": False
    }


# ============================================================
# SEMANTIC CACHE NODE
# ============================================================

def semantic_cache_node(state):

    query = state["query"]

    print("\n")
    print("=" * 70)
    print("SEMANTIC CACHE")
    print("=" * 70)

    cached_result = semantic_cache.get(query)

    if cached_result:

        print("\nCACHE HIT")

        print(
            f"Similarity: "
            f"{cached_result.get('similarity', 0):.4f}"
        )

        return {
            "answer": cached_result["answer"],
            "cache_hit": True
        }

    print("\nCACHE MISS")

    return {
        "cache_hit": False
    }


# ============================================================
# CACHE ROUTER
# ============================================================

def cache_router(state):

    if state["cache_hit"]:

        return "cache_end"

    return "router"


# ============================================================
# QUERY ROUTER NODE
# ============================================================

def router_node(state):

    query = state["query"]

    print("\n")
    print("=" * 70)
    print("QUERY ROUTER")
    print("=" * 70)

    route = router.route(query)

    print("\nUser Question:")
    print(query)

    print("\nSelected Route:")
    print(route)

    return {
        "route": route
    }


# ============================================================
# ROUTE DECISION
# ============================================================

def agent_router(state):

    route = state["route"]

    if route == "document":

        return "rag"

    elif route == "sql":

        return "sql"

    elif route == "hybrid":

        return "hybrid"

    return "rag"


# ============================================================
# RAG NODE
# ============================================================

def rag_node(state):

    query = state["query"]

    print("\n")
    print("=" * 70)
    print("LANGGRAPH → RAG AGENT")
    print("=" * 70)

    answer = rag_agent.run(query)

    return {
        "answer": answer
    }


# ============================================================
# SQL NODE
# ============================================================

def sql_node(state):

    query = state["query"]

    print("\n")
    print("=" * 70)
    print("LANGGRAPH → SQL AGENT")
    print("=" * 70)

    answer = sql_agent.run(query)

    return {
        "answer": answer
    }


# ============================================================
# HYBRID NODE
# ============================================================

def hybrid_node(state):

    query = state["query"]

    print("\n")
    print("=" * 70)
    print("LANGGRAPH → HYBRID AGENT")
    print("=" * 70)

    answer = hybrid_agent.run(query)

    return {
        "answer": answer
    }


# ============================================================
# ANSWER GUARDRAIL
# ============================================================

def answer_guardrail_node(state):

    answer = state["answer"]

    print("\n")
    print("=" * 70)
    print("ANSWER GUARDRAIL")
    print("=" * 70)

    validation = guardrails.validate_answer(answer)

    print("\nAnswer:")
    print(answer)

    print("\nAllowed:")
    print(validation["allowed"])

    print("\nReason:")
    print(validation["reason"])

    return {
        "answer_allowed": validation["allowed"],
        "guardrail_reason": validation["reason"]
    }


# ============================================================
# ANSWER GUARDRAIL ROUTER
# ============================================================

def answer_guardrail_router(state):

    if state["answer_allowed"]:

        return "cache_store"

    return "blocked_answer"


# ============================================================
# BLOCKED ANSWER NODE
# ============================================================

def blocked_answer_node(state):

    print("\n")
    print("=" * 70)
    print("ANSWER BLOCKED")
    print("=" * 70)

    return {
        "answer": (
            "The generated answer was blocked "
            "by security guardrails."
        )
    }


# ============================================================
# CACHE STORE NODE
# ============================================================

def cache_store_node(state):

    query = state["query"]

    answer = state["answer"]

    print("\n")
    print("=" * 70)
    print("SEMANTIC CACHE STORE")
    print("=" * 70)

    semantic_cache.set(
        query,
        answer
    )

    print("\nCACHE STORED")

    return {}


# ============================================================
# CREATE LANGGRAPH
# ============================================================

workflow = StateGraph(ARESState)


# ============================================================
# ADD NODES
# ============================================================

workflow.add_node(
    "guardrail",
    guardrail_node
)

workflow.add_node(
    "blocked",
    blocked_node
)

workflow.add_node(
    "semantic_cache",
    semantic_cache_node
)

workflow.add_node(
    "router",
    router_node
)

workflow.add_node(
    "rag",
    rag_node
)

workflow.add_node(
    "sql",
    sql_node
)

workflow.add_node(
    "hybrid",
    hybrid_node
)

workflow.add_node(
    "answer_guardrail",
    answer_guardrail_node
)

workflow.add_node(
    "blocked_answer",
    blocked_answer_node
)

workflow.add_node(
    "cache_store",
    cache_store_node
)


# ============================================================
# START → GUARDRAIL
# ============================================================

workflow.add_edge(
    START,
    "guardrail"
)


# ============================================================
# GUARDRAIL → CACHE / BLOCKED
# ============================================================

workflow.add_conditional_edges(
    "guardrail",
    guardrail_router,
    {
        "semantic_cache": "semantic_cache",
        "blocked": "blocked"
    }
)


# ============================================================
# BLOCKED → END
# ============================================================

workflow.add_edge(
    "blocked",
    END
)


# ============================================================
# CACHE → CACHE END / ROUTER
# ============================================================

workflow.add_conditional_edges(
    "semantic_cache",
    cache_router,
    {
        "cache_end": END,
        "router": "router"
    }
)


# ============================================================
# ROUTER → AGENT
# ============================================================

workflow.add_conditional_edges(
    "router",
    agent_router,
    {
        "rag": "rag",
        "sql": "sql",
        "hybrid": "hybrid"
    }
)


# ============================================================
# AGENTS → ANSWER GUARDRAIL
# ============================================================

workflow.add_edge(
    "rag",
    "answer_guardrail"
)

workflow.add_edge(
    "sql",
    "answer_guardrail"
)

workflow.add_edge(
    "hybrid",
    "answer_guardrail"
)


# ============================================================
# ANSWER GUARDRAIL → CACHE / BLOCKED ANSWER
# ============================================================

workflow.add_conditional_edges(
    "answer_guardrail",
    answer_guardrail_router,
    {
        "cache_store": "cache_store",
        "blocked_answer": "blocked_answer"
    }
)


# ============================================================
# BLOCKED ANSWER → END
# ============================================================

workflow.add_edge(
    "blocked_answer",
    END
)


# ============================================================
# CACHE STORE → END
# ============================================================

workflow.add_edge(
    "cache_store",
    END
)


# ============================================================
# COMPILE WORKFLOW
# ============================================================

app = workflow.compile()


# ============================================================
# FUNCTION FOR EVALUATION SYSTEM
# ============================================================

def build_workflow():

    return app


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    result = app.invoke(
        {
            "query": "How many employees are there?",

            "route": "",

            "answer": "",

            "query_allowed": True,

            "answer_allowed": True,

            "guardrail_reason": "",

            "cache_hit": False
        }
    )

    print("\n")
    print("=" * 70)
    print("FINAL RESULT")
    print("=" * 70)

    print("\nRoute:")
    print(
        result.get(
            "route",
            ""
        )
    )

    print("\nAnswer:")
    print(
        result.get(
            "answer",
            ""
        )
    )

    print("\nCache Hit:")
    print(
        result.get(
            "cache_hit",
            False
        )
    )