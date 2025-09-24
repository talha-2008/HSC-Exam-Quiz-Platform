import ast
from pathlib import Path
p = Path(__file__).parent.parent / 'app' / 'states' / 'data.py'
s = p.read_text(encoding='utf-8')
mod = ast.parse(s, filename=str(p))
for node in mod.body:
    # Handle plain assignment (Assign) and annotated assignment (AnnAssign)
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == 'questions':
                try:
                    questions = ast.literal_eval(node.value)
                except Exception as e:
                    print('ERROR: could not evaluate questions literal:', e)
                    raise
                subjects = len(questions)
                total = sum(len(v) for v in questions.values())
                print('subjects=', subjects)
                print('total_questions=', total)
                raise SystemExit(0)
    if isinstance(node, ast.AnnAssign):
        # Annotated assignment like: questions: dict[...] = {...}
        target = node.target
        if isinstance(target, ast.Name) and target.id == 'questions' and node.value is not None:
            try:
                questions = ast.literal_eval(node.value)
            except Exception as e:
                print('ERROR: could not evaluate questions literal (AnnAssign):', e)
                raise
            subjects = len(questions)
            total = sum(len(v) for v in questions.values())
            print('subjects=', subjects)
            print('total_questions=', total)
            raise SystemExit(0)
print('questions not found')
