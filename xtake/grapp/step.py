from grapp.models import Election, Candidate, Promise
from random import shuffle


def get_related_by_order(target_promise):
    r = target_promise.related.all()
    return r


def get_elec_and_cand(election_name):
    election = Election.objects.get(name=election_name)
    if election:
        candidates = election.candidate_set.all()

        if len(candidates) != 2:
            raise Exception("This version now only supports two-party system")

        return (election, list(candidates))
    else:
        return None


def get_choices_ctx(election_name):
    election, candidates = get_elec_and_cand(election_name)
    shuffle(candidates)
    return {
        'cand_1': candidates[0],
        'cand_2': candidates[1],
        'election': election,
    }


def get_step_ctx(election_name, selected_cand_name, step):

    election, candidates = get_elec_and_cand(election_name)

    if int(step) > election.game_step:
        return { 'finished': True }

    for i, cand in enumerate(candidates):
        if cand.name == selected_cand_name:
            selected_cand = cand
            shown_cand = candidates[1-i]

    shown_promise = shown_cand.promise_set.get(pid=step)
    selected_promises = get_related_by_order(shown_promise)

    return {
        'finished': False,
        'selected_cand': selected_cand,
        'shown_cand': shown_cand,
        'shown_promise': shown_promise,
        'selected_promises': selected_promises,
        'selected_promises_json': [p.json() for p in selected_promises],
    }

