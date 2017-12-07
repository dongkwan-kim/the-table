from operator import attrgetter
from prompt_responses.models import Prompt
from grapp.models import Election, Candidate, Promise
from session.models import UserProfile, BinaryQuestion
from random import shuffle
from collections import defaultdict, Counter

import json


def get_related_by_order(target_promise):
    r = target_promise.related.exclude(candidate=target_promise.candidate)
    return r


def get_elec_and_cand(election_name):
    election = Election.objects.get(name=election_name)
    if election:
        candidates = election.candidate_set.all()

        if len(candidates) != 2:
            raise Exception("This version now only supports two-party system")

        return election, list(candidates)
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
        return {'finished': True}

    (shown_cand, selected_cand) = (None, None)
    for i, cand in enumerate(candidates):
        if cand.name == selected_cand_name:
            selected_cand = cand
            shown_cand = candidates[1-i]

    shown_promise = shown_cand.promise_set.get(pid=step)
    selected_promises = get_related_by_order(shown_promise)

    return {
        'stage_info': {
            'current': int(step),
            'total': election.game_step,
        },
        'finished': False,
        'selected_cand': selected_cand,
        'shown_cand': shown_cand,
        'shown_promise': shown_promise,
        'selected_promises': selected_promises,
        'selected_promises_json': [p.json() for p in selected_promises],
    }


def get_verbose_stake(stake):
    stake = int(stake)
    if stake <= 2:
        verbose_stake = 'disadvantage'
    elif stake >= 4:
        verbose_stake = 'advantage'
    else:
        verbose_stake = 'neutral'
    return verbose_stake


def get_result_ctx(request, election_name, result_kind):

    election, candidates = get_elec_and_cand(election_name)

    user = request.user

    response_prompt = Prompt.objects.get(id=1)
    responses = response_prompt.responses.all()

    r = {}
    if result_kind == 'candidates':
        r.update(get_result_candidates_ctx(candidates, responses, user))
        r.update({'election': election, 'user': user})

    return r


def jaccard(a_counter, b_counter):
    try:
        return sum((a_counter & b_counter).values()) / sum((a_counter | b_counter).values())
    except ZeroDivisionError:
        return -1


def get_result_candidates_ctx(candidates, responses, the_user):
    """
    :param candidates:
    :param responses:
    :param the_user:
    :return:
    {
        candidates: [Candidate, Candidate],
        promises: [
            {
                promise_corr: Integer,
                list: [
                    {
                        promise: Promise,
                        advantage_personas: [String, ],
                        disadvantage_personas: [String, ],
                        persona_jaccard: Float,
                    },
                ],
            },
        ],
    }
    """
    the_profile = UserProfile.objects.get(user=the_user)

    promises2a_personas = defaultdict(list)
    promises2the_personas = defaultdict(list)
    promise_pair = []

    for res in responses:

        verbose_stake = get_verbose_stake(res.rating)

        selected_promise = Promise.objects.get(id=res.object_id)
        a_profile = UserProfile.objects.get(user=res.user)

        _response_json = json.loads(res.text)
        shown_promise_id = int(_response_json['shown_promise'][0])
        shown_promise = Promise.objects.get(id=shown_promise_id)
        demographics = _response_json['demographics']
        answers = _response_json['answers']

        persona_keys = demographics + answers
        a_personas = a_profile.get_values(persona_keys)
        the_personas = the_profile.get_values(persona_keys)

        promises2a_personas[(selected_promise, verbose_stake)] += a_personas
        promises2the_personas[selected_promise] += the_personas
        promise_pair.append(tuple(sorted([selected_promise, shown_promise], key=attrgetter('candidate'))))

    promises = []
    promise_pair = list(set(promise_pair))
    for pair in promise_pair:
        pemt_list = [{
            'promise': p,
            'advantage_personas': promises2a_personas[(p, 'advantage')],
            'disadvantage_personas': promises2a_personas[(p, 'disadvantage')],
            'the_personas': promises2the_personas[p],
            'persona_jaccard': None,
        } for p in pair]

        for e in pemt_list:
            eap = e['advantage_personas']
            diseap = e['disadvantage_personas']

            # Jaccard calculation
            adv_counter = Counter(eap)
            disadv_counter = Counter(diseap)
            the_counter = Counter(e['the_personas'])
            adv_jaccard = jaccard(adv_counter, the_counter)
            disadv_jaccard = jaccard(disadv_counter, the_counter)
            if adv_jaccard < 0 and disadv_jaccard < 0:
                e['persona_jaccard'] = None
            else:
                e['persona_jaccard'] = adv_jaccard if adv_jaccard > disadv_jaccard else -disadv_jaccard

            # Refine personas to string
            e['advantage_personas'] = ', '.join(set(eap))
            e['disadvantage_personas'] = ', '.join(set(diseap))

        promises.append(dict(promise_corr=1, list=pemt_list))

    return {
        'candidates': sorted(candidates),
        'promises': promises,
    }
