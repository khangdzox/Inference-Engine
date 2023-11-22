from cnf_helper import transform_to_cnf

def resolution(knowledge_base : list[list[str]], query : list[str]) -> bool:
    cnf_kb = [transform_to_cnf(sentence) for sentence in knowledge_base]
    cnf_query = transform_to_cnf(query)
    clauses = cnf_kb + ['~' + cnf_query]
    new = []
    while True:
        for clause1 in clauses:
            for clause2 in clauses - clause1:
                resolvents = resolve(clause1, clause2)
                if [] in resolvents:
                    return True
                new += resolvents        
        if new in clauses:
            return False
        clauses += new