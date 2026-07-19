def enforce(decision: dict):
    '''
    decision example:
    {
        'decision': 'ALLOW',
        'reason': 'Tool is allowed'
    }
    '''

    if decision['decision'] == 'ALLOW':
        return True
    return False