from cnf_helper import transform_to_cnf

def resolution(knowledge_base, query):
    clauses = transform_to_cnf(knowledge_base) + transform_to_cnf(['~' + query])
    new = []
    while True:
        for [clause1, clause2] in clauses:
            resolvents = resolve(clause1, clause2)
            if [] in resolvents:
                return True
            new += resolvents
        if new in clauses:
            return False
        clauses += new