import pprint
import copy


class Algorithm:
    def get_algorithm_steps(self, tiles, variables, words):
        pass


class ExampleAlgorithm(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):
        pprint.pprint(tiles)
        moves_list = [['0h', 0], ['0v', 2], ['1v', 1], ['2h', 1], ['4h', None],
                      ['2h', None], ['1v', None], [
                          '0v', 3], ['1v', 1], ['2h', 1],
                      ['4h', 4], ['5v', 5]]
        domains = {var: [word for word in words] for var in variables}
        solution = []
        for move in moves_list:
            solution.append([move[0], move[1], domains])
        pprint.pprint(solution)
        return solution


class BacktrackingAlgorithm(Algorithm):
    def parseVariable(var: str, matrix: list) -> tuple[int, int, bool]:
        # print(var, matrix)

        field: int = int(var[:-1])
        horizontal: bool
        if var[-1] == 'h':
            horizontal = True
        elif var[-1] == 'v':
            horizontal = False

        rowlen: int = len(matrix[0])
        row: int = field // rowlen
        col: int = field % rowlen

        # print(row, col, horizontal)
        return row, col, horizontal

    def write_to_matrix(v, val, matrix):
        row, col, dir = BacktrackingAlgorithm.parseVariable(v, matrix)
        i: int = 0
        while i < len(val) and (col if dir else row) + i < len(matrix[row] if dir else matrix):
            matrix[row + (0 if dir else i)][col + (i if dir else 0)] = val[i]
            i += 1

    def is_consistent_assignment(v, val, vars, domains, matrix):
        row, col, dir = BacktrackingAlgorithm.parseVariable(v, matrix)
        i: int = 0

        while (i < len(val)
               and (col if dir else row) + i < len(matrix[row] if dir else matrix)
               and matrix[row + (0 if dir else i)][col + (i if dir else 0)] != '+'):
            if matrix[row + (0 if dir else i)][col + (i if dir else 0)] != '_' and val[i] != matrix[row + (0 if dir else i)][col + (i if dir else 0)]:
                # print(matrix[row + (0 if dir else i)][col + (i if dir else 0)], val[i])
                # print('returning false 1...', v, val, matrix)
                return False
            i += 1

        if not (i == len(val)
                and ((col if dir else row) + i == len(matrix[row] if dir else matrix)
                or matrix[row + (0 if dir else i)][col + (i if dir else 0)] == '+')):
            # print('returning false 2...', v, val, i == len(val), (col if dir else row) + i == len(matrix[row] if dir else matrix), matrix[row + (0 if dir else i)][col + (i if dir else 0)] == '+', i, len(val), matrix)
            # print("Conditions...", i < len(val), (col if dir else row) + i < len(matrix[row] if dir else matrix), matrix[row + (0 if dir else i)][col + (i if dir else 0)] != '+', row, col)
            return False

        # print('RETURNING TRUE...', v, val, matrix)
        return True

    def forward_check(self, v, val, new_dom, varmap, matrix):
        return True
    
    def arc_consistency(self, domains, varmap, matrix):
        return True

    def no_empty_domain(domains) -> bool:
        for var in domains:
            if len(domains[var]) == 0:
                return False
        return True

    def backtrack_search(self, vars, domains, matrix, solution, lvl, varmap) -> bool:
        if lvl == len(vars):
            return True
        v = vars[lvl]
        for index, val in list(enumerate(domains[v])):
            if BacktrackingAlgorithm.is_consistent_assignment(v, val, vars, domains, matrix):

                # if not BacktrackingAlgorithm.no_empty_domain(domains):
                #     solution.append([v, None, domains])
                #     return False

                new_mat = copy.deepcopy(matrix)
                BacktrackingAlgorithm.write_to_matrix(v, val, new_mat)
                new_dom = copy.deepcopy(domains)
                new_dom[v] = [val]

                # print('BEFORE')
                # pprint.pprint(new_dom)
                # comment out the if and continue if using no_empty_domain
                if not self.forward_check(v, val, new_dom, varmap, matrix):
                    continue

                if not self.arc_consistency(new_dom, varmap, matrix):
                    continue
                # print('nope', new_dom)
                # print('AFTER')
                # pprint.pprint(new_dom)

                solution.append([v, index, domains])

                # print(v, val, new_mat)
                if self.backtrack_search(vars, new_dom, new_mat, solution, lvl + 1, varmap):
                    return True
        solution.append([v, None, domains])
        return False

    def resolve_unary_constraints(variables: dict, domains: dict):
        for var in domains:
            domains[var] = [word for word in domains[var]
                            if len(word) == variables[var]]

    def get_algorithm_steps(self, tiles, variables, words):
        matrix = [['+' if tile else '_' for tile in row] for row in tiles]
        # pprint.pprint(matrix)
        # pprint.pprint(variables)

        # moves_list = [['0h', 0], ['0v', 2], ['1v', 1], ['2h', 1], ['4h', None],
        #               ['2h', None], ['1v', None], [
        #     '0v', 3], ['1v', 1], ['2h', 1],
        #     ['4h', 4], ['5v', 5]]

        domains = {var: [word for word in words] for var in variables}
        # pprint.pprint(domains)
        BacktrackingAlgorithm.resolve_unary_constraints(variables, domains)
        # pprint.pprint(domains)
        solution = []
        # for move in moves_list:
        #     solution.append([move[0], move[1], domains])
        self.backtrack_search(vars=[var for var in variables], domains=domains,
                              solution=solution, matrix=matrix, lvl=0, varmap=variables)
        # pprint.pprint(solution)
        return solution


class ForwardCheckingAlgorithm(BacktrackingAlgorithm):
    def find_intersection(v1, v2, varmap, matrix) -> tuple[int, int]:
        r1, c1, d1 = BacktrackingAlgorithm.parseVariable(v1, matrix)
        r2, c2, d2 = BacktrackingAlgorithm.parseVariable(v2, matrix)
        if d1 != d2:
            if d1 and c1 <= c2 < c1 + varmap[v1] and r2 <= r1 < r2 + varmap[v2]:
                # print('intersection words 1', v1, v2, r1, c2)
                return r1, c2
            if d2 and c2 <= c1 < c2 + varmap[v2] and r1 <= r2 < r1 + varmap[v1]:
                # print('intersection words 2', v1, v2, r2, c1)
                return r2, c1
        return -1, -1

    def are_constrained(v1, v2, varmap, matrix):
        r, c = ForwardCheckingAlgorithm.find_intersection(
            v1, v2, varmap, matrix)
        if r != -1 and c != -1:
            return True
        return False

    def update_domain(domains, cvar, cvalue, var, varmap, matrix):
        r1, c1, d1 = BacktrackingAlgorithm.parseVariable(cvar, matrix)
        r2, c2, d2 = BacktrackingAlgorithm.parseVariable(var, matrix)
        r, c = ForwardCheckingAlgorithm.find_intersection(
            cvar, var, varmap, matrix)
        to_erase = []
        if d1 and not d2:
            # print(cvalue, c, c1)
            char = cvalue[c - c1]
            for word in domains[var]:
                # print(word, r, r2)
                if char != word[r - r2]:
                    # print('want to erase ', word)
                    to_erase.append(word)
        elif not d1 and d2:
            # print(cvalue, r, r1)
            char = cvalue[r - r1]
            for word in domains[var]:
                # print(word, c, c2)
                if char != word[c - c2]:
                    # print('want to erase ', word)
                    to_erase.append(word)
        # pprint.pprint(domains[var])
        domains[var] = [word for word in domains[var] if word not in to_erase]
        # pprint.pprint(domains[var])

    def forward_check(self, v, val, new_dom, varmap, matrix):
        for var in varmap:
            if var != v and ForwardCheckingAlgorithm.are_constrained(v, var, varmap, matrix):
                ForwardCheckingAlgorithm.update_domain(
                    new_dom, v, val, var, varmap, matrix)
                if len(new_dom[var]) == 0:
                    return False
        return True


class ArcConsistencyAlgorithm(ForwardCheckingAlgorithm):

    def __init__(self) -> None:
        super().__init__()
        self.all_arcs = None

    def get_all_arcs(self, varmap, matrix):
        if self.all_arcs == None:
            self.all_arcs = []
            for v1 in varmap :
                # print(v1)
                for v2 in varmap :
                    # print(v2)
                    if (ForwardCheckingAlgorithm.are_constrained(v1, v2, varmap, matrix)):
                        self.all_arcs.append((v1, v2))

        return copy.deepcopy(self.all_arcs)

    def satisfies_constraint(val_x, val_y, x, y, domains, varmap, matrix):
        r1, c1, d1 = BacktrackingAlgorithm.parseVariable(x, matrix)
        r2, c2, d2 = BacktrackingAlgorithm.parseVariable(y, matrix)
        r, c = ForwardCheckingAlgorithm.find_intersection(x, y, varmap, matrix)

        if ((d1 and not d2 and val_x[c - c1] != val_y[r - r2]) or (not d1 and d2 and val_x[r - r1] != val_y[c - c2])
            or not BacktrackingAlgorithm.is_consistent_assignment(x, val_x, None, domains, matrix)
            or not BacktrackingAlgorithm.is_consistent_assignment(x, val_x, None, domains, matrix)):
            return False
        return True
            

    def arc_consistency(self, domains, varmap, matrix):

        arc_list = self.get_all_arcs(varmap, matrix)
        while arc_list:
            x, y = arc_list.pop(0)
            x_vals_to_del = []
            for val_x in domains[x]:
                y_no_val = True
                for val_y in domains[y]:
                    if ArcConsistencyAlgorithm.satisfies_constraint(val_x, val_y, x, y, domains, varmap, matrix):
                        y_no_val = False
                        break
                if y_no_val:
                    x_vals_to_del.append(val_x)
            if x_vals_to_del:
                domains[x] = [v for v in domains[x] if v not in x_vals_to_del]
                if not domains[x]:
                    return False
                for v in varmap:
                    if v != x and ForwardCheckingAlgorithm.are_constrained(v, x, varmap, matrix):
                        arc_list.append((v, x))
        return True
