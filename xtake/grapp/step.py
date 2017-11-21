from grapp.models import Election, Candidate, Promise


def get_related_by_order(target_promiese):
    r = target_promise.related.all()
    return r


def get_step_ctx(election_name, main_cand_name, step):
    election = Election.objects.get(name=election_name)
    if election:
        candidates = election.candidate_set.all()

        if len(candidates) != 2:
            raise Exception("This version now only supports two-party system")

        for i, cand in enumerate(candidates):
            if cand.name == main_cand_name:
                main_cand = cand
                sub_cand = list(candidates)[1-i]

        sub_promise = sub_cand.promise_set.get(pid=step)
        main_promises = get_related_by_order(sub_promise)

        return {
            'main_cand': main_cand,
            'sub_cand': sub_cand,
            'sub_promise': sub_promise,
            'main_promises': main_promises,
        }

