import ast
from pathlib import Path
p = Path(__file__).parent.parent / 'app' / 'states' / 'data.py'
s = p.read_text(encoding='utf-8')
mod = ast.parse(s, filename=str(p))
questions = None
for node in mod.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == 'questions':
                questions = ast.literal_eval(node.value)
                break
    if isinstance(node, ast.AnnAssign):
        target = node.target
        if isinstance(target, ast.Name) and target.id == 'questions' and node.value is not None:
            questions = ast.literal_eval(node.value)
    if questions is not None:
        break

if questions is None:
    raise SystemExit('Could not find questions in data.py')

errors = []
seen_questions = {}
for subj, qlist in questions.items():
    if not isinstance(qlist, list):
        errors.append(f'Subject {subj} does not have a list')
        continue
    for idx, q in enumerate(qlist):
        if not isinstance(q, dict):
            errors.append(f'{subj}[{idx}] is not a dict')
            continue
        for key in ('question','options','answer'):
            if key not in q:
                errors.append(f'{subj}[{idx}] missing key: {key}')
        question_text = str(q.get('question','')).strip()
        options = q.get('options')
        answer = q.get('answer')
        if not question_text:
            errors.append(f'{subj}[{idx}] empty question text')
        if not isinstance(options, list):
            errors.append(f'{subj}[{idx}] options is not a list')
        else:
            if len(options) != 4:
                errors.append(f'{subj}[{idx}] options length is {len(options)}, expected 4')
            for i,opt in enumerate(options):
                if not isinstance(opt, str) or not opt.strip():
                    errors.append(f'{subj}[{idx}] option[{i}] empty or not str')
        if not isinstance(answer, str) or not answer.strip():
            errors.append(f'{subj}[{idx}] answer empty or not str')
        else:
            # check answer in options (loose compare)
            if isinstance(options, list) and all(not (str(opt).strip()==str(answer).strip()) for opt in options):
                errors.append(f"{subj}[{idx}] answer not in options: {answer}")
        # duplicate question text
        key = (question_text)
        seen = seen_questions.setdefault(key, [])
        seen.append((subj, idx))

duplicates = {k:v for k,v in seen_questions.items() if len(v)>1}

print('subjects=', len(questions), 'total_questions=', sum(len(v) for v in questions.values()))
if errors:
    print('\nValidation ERRORS:')
    for e in errors[:200]:
        print('-', e)
else:
    print('\nNo validation errors found.')
if duplicates:
    print('\nDuplicate question texts found:', len(duplicates))
    for q,v in list(duplicates.items())[:20]:
        print('-', q, 'occurs', len(v), 'times at', v)
else:
    print('\nNo duplicate questions found.')
