"""
Objective 1: Static Dependency Analyzer (FaaSLight-style AST Analysis)
Parses Python source code to detect, classify, and graph dependencies:
- Indispensable (Eager / Top-level): must be loaded at cold-start
- Optional (Lazy / Deferred): loaded on-demand inside functions or conditionals
"""

import ast
import json
import os
import pathlib
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional, Set


@dataclass
class ImportDetail:
    module: str
    imported_symbols: List[str]
    line_no: int
    scope: str
    is_conditional: bool
    classification: str  # 'indispensable' or 'optional'
    reason: str


@dataclass
class FileAnalysisReport:
    file_path: str
    module_name: str
    total_imports: int
    indispensable_imports: List[str]
    optional_imports: List[str]
    details: List[ImportDetail]

    def to_dict(self) -> dict:
        return {
            "module_name": self.module_name,
            "file_path": self.file_path,
            "total_imports": self.total_imports,
            "indispensable_imports": self.indispensable_imports,
            "optional_imports": self.optional_imports,
            "details": [asdict(d) for d in self.details]
        }

    def print_summary(self):
        print("=" * 70)
        print(f"  Dependency Analysis: {self.module_name} ({self.file_path})")
        print("=" * 70)
        print(f"Total Dependencies Detected: {self.total_imports}")
        print(f"  ├── Indispensable (Eager / Cold-start) : {len(self.indispensable_imports)}")
        for dep in self.indispensable_imports:
            print(f"  │    └── {dep}")
        print(f"  └── Optional (Deferred / Lazy)        : {len(self.optional_imports)}")
        for dep in self.optional_imports:
            print(f"       └── {dep}")
        
        print("\nDetailed Import Manifest:")
        print(f"{'Line':<6} | {'Module':<32} | {'Class':<14} | {'Scope / Reason'}")
        print("-" * 70)
        for d in self.details:
            syms = f" ({', '.join(d.imported_symbols)})" if d.imported_symbols and d.imported_symbols != [d.module] else ""
            mod_str = f"{d.module}{syms}"[:32]
            print(f"{d.line_no:<6} | {mod_str:<32} | {d.classification.upper():<14} | {d.reason}")
        print("=" * 70)


class ASTDependencyVisitor(ast.NodeVisitor):
    """
    Traverses AST to identify import statements and their context/scope.
    """

    def __init__(self):
        self.details: List[ImportDetail] = []
        self.scope_stack: List[str] = ["global"]
        self.conditional_depth = 0

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.scope_stack.append(f"def {node.name}()")
        self.generic_visit(node)
        self.scope_stack.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.scope_stack.append(f"async def {node.name}()")
        self.generic_visit(node)
        self.scope_stack.pop()

    def visit_ClassDef(self, node: ast.ClassDef):
        self.scope_stack.append(f"class {node.name}")
        self.generic_visit(node)
        self.scope_stack.pop()

    def visit_If(self, node: ast.If):
        self.conditional_depth += 1
        self.generic_visit(node)
        self.conditional_depth -= 1

    def visit_Try(self, node: ast.Try):
        self.conditional_depth += 1
        self.generic_visit(node)
        self.conditional_depth -= 1

    def visit_Import(self, node: ast.Import):
        is_top = (len(self.scope_stack) == 1 and self.scope_stack[0] == "global")
        is_cond = (self.conditional_depth > 0)
        current_scope = self.scope_stack[-1]

        if is_top and not is_cond:
            classification = "indispensable"
            reason = "Top-level global scope (Eagerly required)"
        elif is_cond:
            classification = "optional"
            reason = f"Conditional block in {current_scope} (Lazy candidate)"
        else:
            classification = "optional"
            reason = f"Scoped inside {current_scope} (Deferred until call)"

        for alias in node.names:
            self.details.append(
                ImportDetail(
                    module=alias.name,
                    imported_symbols=[alias.asname or alias.name],
                    line_no=node.lineno,
                    scope=current_scope,
                    is_conditional=is_cond,
                    classification=classification,
                    reason=reason
                )
            )

    def visit_ImportFrom(self, node: ast.ImportFrom):
        is_top = (len(self.scope_stack) == 1 and self.scope_stack[0] == "global")
        is_cond = (self.conditional_depth > 0)
        current_scope = self.scope_stack[-1]

        if is_top and not is_cond:
            classification = "indispensable"
            reason = "Top-level global scope (Eagerly required)"
        elif is_cond:
            classification = "optional"
            reason = f"Conditional block in {current_scope} (Lazy candidate)"
        else:
            classification = "optional"
            reason = f"Scoped inside {current_scope} (Deferred until call)"

        module = node.module or ""
        symbols = [alias.name for alias in node.names]

        self.details.append(
            ImportDetail(
                module=module,
                imported_symbols=symbols,
                line_no=node.lineno,
                scope=current_scope,
                is_conditional=is_cond,
                classification=classification,
                reason=reason
            )
        )


class StaticDependencyAnalyzer:
    """
    Core static analysis engine for single files and directories.
    """

    @classmethod
    def analyze_file(cls, filepath: str | pathlib.Path, module_name: Optional[str] = None) -> FileAnalysisReport:
        path = pathlib.Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Source file not found: {path}")

        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))

        visitor = ASTDependencyVisitor()
        visitor.visit(tree)

        mod_name = module_name or path.stem
        indispensable: Set[str] = set()
        optional: Set[str] = set()

        for d in visitor.details:
            if d.classification == "indispensable":
                indispensable.add(d.module)
            else:
                optional.add(d.module)

        return FileAnalysisReport(
            file_path=str(path.resolve()),
            module_name=mod_name,
            total_imports=len(visitor.details),
            indispensable_imports=sorted(list(indispensable)),
            optional_imports=sorted(list(optional)),
            details=visitor.details
        )

    @classmethod
    def analyze_directory(cls, dirpath: str | pathlib.Path) -> Dict[str, FileAnalysisReport]:
        dir_path = pathlib.Path(dirpath)
        if not dir_path.exists() or not dir_path.is_dir():
            raise NotADirectoryError(f"Directory not found: {dir_path}")

        reports = {}
        for py_file in sorted(dir_path.rglob("*.py")):
            if py_file.name == "__init__.py":
                continue
            rel_parts = py_file.relative_to(dir_path).with_suffix("").parts
            dotted_rel = ".".join(rel_parts)
            
            report = cls.analyze_file(py_file, module_name=dotted_rel)
            reports[dotted_rel] = report
            # Also register stem for backwards compatibility if no collision
            if py_file.stem not in reports:
                reports[py_file.stem] = report
        return reports

    @classmethod
    def generate_ascii_graph(cls, reports: Dict[str, FileAnalysisReport]) -> str:
        lines = ["\nDependency Call Graph:"]
        for mod, rep in reports.items():
            lines.append(f"\n[{mod}]")
            if rep.indispensable_imports:
                for imp in rep.indispensable_imports:
                    lines.append(f"  ├── (indispensable) ──> {imp}")
            if rep.optional_imports:
                for imp in rep.optional_imports:
                    lines.append(f"  └── (optional / lazy) ─> {imp}")
            if not rep.indispensable_imports and not rep.optional_imports:
                lines.append("  └── (leaf module, no local imports)")
        return "\n".join(lines)
