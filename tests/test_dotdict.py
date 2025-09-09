import pytest
from comcom.playbook.template_solver.template_dict_solver import TemplateDictSolver, LoopDetectedException, MaximumResolutionDepthException, InvalidKeyException

def test_dot_dict_solve_a():
    data = {
        'first_name': "Dana",
        'last_name': "Scully",
        'name': '{first_name} {last_name}',
        'age': 32,
        'job_title': "FBI Agent",
        'Big Description': "{name} is a {stats.description}",
        'stats': {
            'description': "{age}-year old {job_title}",
            'name with title': "Dr. {name}"
        }
    }

    solved_dict = TemplateDictSolver.solve(data)
    assert solved_dict['name'] == "Dana Scully"
    assert solved_dict['stats']['description'] == '32-year old FBI Agent'
    assert solved_dict['Big Description'] == 'Dana Scully is a 32-year old FBI Agent'
    assert solved_dict['stats']['name with title'] == "Dr. Dana Scully"

def test_dot_dict_solve_b():
    data = {
        'a': '{b}',
        'b': '{c}',
        'c': '{d}',
        'd': '{a}'
    }
    with pytest.raises(LoopDetectedException, match=r".*a, b, c, d.*"):
        TemplateDictSolver.solve(data)

def test_dot_dict_solve_c():
    data = {
        'a': '{b}',
        'b': '{c}',
        'c': '{a}'
    }

    with pytest.raises(LoopDetectedException, match=r".*a, b, c.*"):
        TemplateDictSolver.solve(data)

def test_dot_dict_solve_d():
    data = {
        'a': '{b}',
        'b': '{a}'
    }
    with pytest.raises(LoopDetectedException, match=r".*a, b.*"):
        TemplateDictSolver.solve(data)

def test_dot_dict_solve_e():
    data = {
        'a': '{a}',
        'b': '{b}'
    }
    with pytest.raises(LoopDetectedException, match=r".*a, b.*"):
        TemplateDictSolver.solve(data)

def test_dot_dict_solve_f():
    data = {
        'one': "$two",
        'two': "$three",
        'three': 32
    }
    solved_dict = TemplateDictSolver.solve(data)
    assert solved_dict['one'] == 32


def test_dot_dict_with_circular_reference():
    data = {
        'description': "The {demeanor} {honorific} {full_name}",
        'honorific': "Mr.",
        'first_name': "Fox",
        'last_name': "Mulder",
        'full_name': "{first_name} {last_name}",
        'job_title': '{informal_title} FBI Agent, {full_name}',
        'informal_title': 'Spooky {honorific} {job_title}',
        'demeanor': "aloof",
        
    }

    with pytest.raises(LoopDetectedException, match=r".*job_title, informal_title.*"):
        TemplateDictSolver.solve(data)

def test_unknown_key():
    data = {
        'name': "Walter Skinner",
        'title': "Assistant Director",
        'full_title': "{honorific} {title} {name}"
    }

    with pytest.raises(InvalidKeyException, match=r"^Attempting to access unknown key \'honorific\' in template \'full_title\'.*"):
        solved_dict = TemplateDictSolver.solve(data)

def test_nested_unknown_key():
    data = {
        'name': "Walter Skinner",
        'title': "Assistant Director",
        'full_title': "{title} {name}",
        'stats': {
            'age': 32,
            'address': "1234 {stats.street_name} Street, Washington DC"
        }
    }
    
    with pytest.raises(InvalidKeyException, match=r"^Attempting to access unknown key \'street_name\' in template \'stats.address\'.*"):
        TemplateDictSolver.solve(data)

def test_cascading_a():
    data_parent = {
        'first_name': "John",
        'last_name': "Doggett",
        'name': "{first_name} {last_name}",
    }

    data_child = {
        'title': "Special Agent",
        'full title': "{title} {name}"
    }

    parent_solved = TemplateDictSolver.solve(data_parent)
    child_solved = TemplateDictSolver.solve(data_child, parent_solved)

    assert child_solved.get('full title') == "Special Agent John Doggett"

def test_solve_list():
    data = {
        'first_name': 'CGB',
        'last_name': 'Spender',
        'nemesis': "Fox",
        'children': [
            '{nemesis} Mulder',
            'Jeffrey {last_name}',
            1234,
        ]
    }

    solved = TemplateDictSolver.solve(data)
    assert solved.get('children')[0] == "Fox Mulder"
    assert solved.get('children')[1] == "Jeffrey Spender"
    assert solved.get('children')[2] == 1234

def test_solve_list_with_extra_data():
    data = {
        'first_name': 'CGB',
        'last_name': 'Spender',
        'nemesis': "Fox",
        'children': [
            '{nemesis} Mulder',
            'Jeffrey {last_name}',
            1234,
        ],
        'enemies': [
            'Dana Scully',
            'Walter Skinner'
        ]
    }

    more_data = {
        'name': "Alex Krycek",
        'works_for': [
            '{first_name} {last_name}'
        ],
        'antagonists': [
            "{enemies[0]}"
        ]

    }

    solved = TemplateDictSolver.solve(more_data, TemplateDictSolver.solve(data))
    solved['works_for'][0] == "CGB Spender"
    solved['antagonists'][0] == "Dana Scully"