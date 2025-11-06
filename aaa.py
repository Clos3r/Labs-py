from typing import Protocol

class Document(Protocol):
    def render(self) -> str:
        ...

class Report:
    def render(self) -> str:
        return "Corporate Report: Q4 summary"

class Invoice:
    def render(self) -> str:
        return "Corporate Invoice: total 1,200"

class Contract:
    def render(self) -> str:
        return "Corporate Contract: standard terms"

class ShadowReport:
    def render(self) -> str:
        return "Shadow Report: internal id=SR-001 (alt format)"

class ShadowInvoice:
    def render(self) -> str:
        return "Shadow Invoice: alt-format, meta-only"

class ShadowContract:
    def render(self) -> str:
        return "Shadow Contract: appended service fields"

class CorpFactory:
    allowed = {
        "report": Report,
        "invoice": Invoice,
        "contract": Contract,
    }

    def create(self, doc_type: str) -> Document:
        if doc_type not in self.allowed:
            raise ValueError(f"Type not allowed: {doc_type}")
        return self.allowed[doc_type]()  

class ShadowFactory:
    allowed = {
        "report": ShadowReport,
        "invoice": ShadowInvoice,
        "contract": ShadowContract,
    }

    def create(self, doc_type: str) -> Document:
        if doc_type not in self.allowed:
            raise ValueError(f"Type not allowed (shadow): {doc_type}")
        return self.allowed[doc_type]() 


def get_factory(mode: str):
    return ShadowFactory() if mode == "shadow" else CorpFactory()


def demo(mode: str):
    f = get_factory(mode)
    print(f"\nMode: {mode.upper()}")
    for t in ["report", "invoice", "contract"]:
        doc = f.create(t)
        print(f"{t:8} -> {doc.render()}")

if __name__ == "__main__":
    demo("corp")
    demo("shadow")

    try:
        get_factory("corp").create("unknown")
    except ValueError as e:
        print("\nBlocked creation:", e)
