from grapp.models import Election, Candidate, Promise
from random import shuffle


def get_related_by_order(target_promise):
    r = target_promise.related.all()
    return r


def get_candidates(election_name):
    election = Election.objects.get(name=election_name)
    if election:
        candidates = election.candidate_set.all()

        if len(candidates) != 2:
            raise Exception("This version now only supports two-party system")

        return list(candidates)
    else:
        return None


def get_choices_ctx(election_name):
    election = Election.objects.get(name=election_name)
    candidates = get_candidates(election_name)
    shuffle(candidates)
    return {
        'cand_1': candidates[0],
        'cand_2': candidates[1],
        'election': election,
    }


def get_step_ctx(election_name, main_cand_name, step):

    candidates = get_candidates(election_name)

    for i, cand in enumerate(candidates):
        if cand.name == main_cand_name:
            main_cand = cand
            sub_cand = candidates[1-i]

    sub_promise = sub_cand.promise_set.get(pid=step)
    main_promises = get_related_by_order(sub_promise)

    return {
        'main_cand': main_cand,
        'sub_cand': sub_cand,
        'sub_promise': sub_promise,
        'main_promises': main_promises,
    }

