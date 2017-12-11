from copy import deepcopy
from django.contrib.auth.models import User
from django.db import models
from grapp.models import Election, Candidate, Promise


class BinaryQuestion(models.Model):
    num = models.IntegerField()
    choice_1 = models.TextField()
    choice_2 = models.TextField()

    def get_choices(self):
        return (
            (0, str(self.choice_1)),
            (1, str(self.choice_2)),
        )

    def get_choice(self, idx):
        return dict(self.get_choices())[int(idx)]


class UserProfile(models.Model):

    user = models.ForeignKey(User)
    completed = models.BooleanField(default=False)

    """
    [1] 박찬욱. "한국인 정치참여의 특징과 결정요인: 2004 년 조사결과 분석." (2005).
    [2] 김지범, 강정한, 김석호, 김창환, 박원호, 이윤석, 최슬기, 김솔이. (2017). 한국종합사회조사 2003-2016. 서울: 성균관대학교 출판부.
    [3] 제6차 한국표준직업분류(KSCO-6)

    """
    AGE_CHOICES = (
        (None, '선택해주세요'),
        (0, '~ 19'),
        (1, '20 ~ 29'),
        (2, '30 ~ 39'),
        (3, '40 ~ 49'),
        (4, '50 ~ 59'),
        (5, '60 ~ 69'),
        (6, '70 ~'),
    )

    GENDER_CHOICES = (
        (None, '선택해주세요'),
        (0, '남성'),
        (1, '여성'),
        (2, '그 외'),
    )

    OCCUPATION_CHOICES = (
        (None, '선택해주세요'),
        (0, '학생'),
        (1, '관리 (공공·기업, 행정·경영지원, 전문서비스, 건설·전기, 판매·고객서비스)'),
        (2, '전문 (과학, 공학, 보건·사회복지, 교육, 법률, 경영.금융, 문화·예술·스포츠)'),
        (3, '사무 (경영·회계, 금융·보험, 법률·감사, 상담·안내·통계)'),
        (4, '서비스 (경찰·소방·보안, 미용·예식·의료보조, 운송·여가, 조리·음식)'),
        (5, '판매 (영업, 매장 판매, 방문·노점·통신)'),
        (6, '농립어업 (농축산, 임업, 어업)'),
        (7, '기능원 (식품가공, 섬유·의복·가죽, 목재·가구·악기·간판, 금속성형, 운송·기계, 전기·전자, 건설·채굴, 영상·통신)'),
        (8, '기계조작 (식품가공, 섬유·신발, 화학, 금속·비금속, 기계제조, 전기·전자, 운전·운송, 상하수도·재활용, 목재·인쇄)'),
        (9, '단순노무 (건설·광업, 운송, 제조, 청소·경비, 가사·음식, 농림어업)'),
        (10, '주부'),
        (11, '군인'),
        (12, '무직 및 기타'),
    )

    INCOME_CHOICES = (
        (None, '선택해주세요'),
        (0, '0 ~ 199 만원'),
        (1, '200 ~ 449 만원'),
        (2, '450 ~ 699 만원'),
        (3, '700 ~ 949 만원'),
        (4, '950 ~ 만원'),
    )

    EDUCATION_CHOICES = (
        (None, '선택해주세요'),
        (0, '없음'),
        (1, '초등(국민)학교'),
        (2, '중학교'),
        (3, '고등학교'),
        (4, '전문대학 (2, 3년제)'),
        (5, '대학교 (4년제)'),
        (6, '대학원 (석사과정)'),
        (7, '대학원 (박사과정)'),
    )

    MARRIAGE_CHOICES = (
        (None, '선택해주세요'),
        (0, '기혼'),
        (1, '사별'),
        (2, '이혼'),
        (3, '별거'),
        (4, '미혼'),
        (5, '동거'),
    )

    POLITICAL_AFFINITY_CHOICES = (
        (None, '선택해주세요'),
        (0, '매우 진보적'),
        (1, '다소 진보적'),
        (2, '중도적'),
        (3, '다소 보수적'),
        (4, '매우 보수적'),
    )

    CHILDREN_CHOICES = (
        (None, '선택해주세요'),
        (0, '자녀가 있다'),
        (1, '자녀가 없다'),
    )

    DEPENDENT_CHOICES = (
        (None, '선택해주세요'),
        (0, '부양할 어르신이 있다'),
        (1, '부양할 어르신이 없다'),
    )

    age = models.IntegerField(choices=AGE_CHOICES, verbose_name='나이')
    gender = models.IntegerField(choices=GENDER_CHOICES, verbose_name='성별')
    occupation = models.IntegerField(choices=OCCUPATION_CHOICES, verbose_name='현재 직업')
    income = models.IntegerField(choices=INCOME_CHOICES, verbose_name='월소득')
    education = models.IntegerField(choices=EDUCATION_CHOICES, verbose_name='최종 학력')
    marriage = models.IntegerField(choices=MARRIAGE_CHOICES, verbose_name='결혼 상태')
    children = models.IntegerField(choices=CHILDREN_CHOICES, verbose_name='자녀 유무')
    dependent = models.IntegerField(choices=DEPENDENT_CHOICES, verbose_name='부양 의무')
    political_affinity = models.IntegerField(choices=POLITICAL_AFFINITY_CHOICES, verbose_name='정치 성향')

    # csv
    answers = models.TextField()

    def __str__(self):
        return str(self.user)

    def get_answers(self):
        if self.answers == '':
            return []
        else:
            return [int(x) for x in self.answers.split(",")]

    def set_answers(self, lst):
        self.answers = ",".join([str(x) for x in lst])

    def get_value(self, name):
        if name == 'answers':
            questions = BinaryQuestion.objects.all()
            answers = self.answers.split(',')
            return [(q.num, q.get_choice(a)) for (q, a) in zip(questions, answers)]
        else:
            return eval('self.get_{0}_display()'.format(name))

    def get_values(self, keys=None):
        """
        :param keys: list
        :return: list
        """
        if keys is None:
            keys = self.get_persona_dict().keys()

        answers_dict = dict(self.get_value('answers'))

        r = []
        for k in keys:
            if k.isnumeric():
                r.append(answers_dict[int(k)])
            else:
                r.append(self.get_value(k))
        return r

    def get_flatten_values(self, keys=None):
        r = []
        for e in self.get_values(keys):
            if isinstance(e, (list,)):
                r += [t[1] for t in e]
            else:
                r.append(e)
        return r

    @staticmethod
    def is_ordered_data(name):
        return name in ['age', 'income', 'education', 'political_affinity']

    def get_persona_dict(self):
        """
        :return: dictionary
        {
            'age': 5,
            'gender': 0,
            'occupation': 2,
            'income': 2,
            'education': 4,
            'marriage': 2,
            'political_affinity': 2,
            'answers': '0,0'
        }
        """
        dcpy = deepcopy(self.__dict__)
        for f in ['_state', 'id', 'user_id']:
            del dcpy[f]
        return dcpy

    def get_choices_dict(self, name: str):
        """
        :param name: string
        :return: dictionary
        {0: '~ 19', 1: '20 ~ 29', 2: '30 ~ 39', 3: '40 ~ 49', 4: '50 ~ 59', 5: '60 ~ 69', 6: '70 ~'} for 'age'
        """
        if name == 'answers':
            lst = [int(x) for x in self.answers.split(",")]
            choices_dict = dict(enumerate(lst))
        else:
            choices_dict = dict(eval('self.{0}_CHOICES'.format(name.upper())))
            del choices_dict[None]
        return choices_dict

    def get_iv_dict(self):
        """
        :return: dictionary
        {
            'age': [5],
            'gender': [1, 0, 0],
            'occupation': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'income': [2],
            'education': [4],
            'marriage': [0, 0, 1, 0, 0, 0],
            'political_affinity': [2],
            'answers': [0, 0]
        }
        """
        persona_fields = self.get_persona_dict()
        for k, v in persona_fields.items():
            if k == 'answers':
                persona_fields[k] = [int(x) for x in self.answers.split(',')]
            elif self.is_ordered_data(k):
                persona_fields[k] = [v]
            else:
                dimension = len(self.get_choices_dict(k))
                lst = [0] * dimension
                lst[v] = 1
                persona_fields[k] = lst
        return persona_fields

    def get_iv(self):
        """
        :return: list [5, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 0, 0, 1, 0, 0, 0, 2, 0, 0]
        """
        empty = []
        for lst in self.get_iv_dict().values():
            empty += lst
        return empty


class UserPostProfile(models.Model):
    user = models.ForeignKey(User)

    LIKERT_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    q1 = models.IntegerField(
        choices=LIKERT_CHOICES,
        verbose_name='설문 1',
        blank=False,
        default=0,
        help_text='세금을 내는 이상, 모든 공약의 실현에는 비용이 든다.<br/>\
                   따라서 나에게 이득이 되지 않은 공약은 나에게 손해다'
    )

    q2 = models.IntegerField(
        choices=LIKERT_CHOICES,
        verbose_name='설문 2',
        blank=False,
        default=0,
        help_text='나의 가족의 손해는 나의 손해다',
    )

    q3 = models.IntegerField(
        choices=LIKERT_CHOICES,
        verbose_name='설문 3',
        blank=False,
        default=0,
        help_text='우리 사회의 손해는 나의 손해다',
    )

    q4 = models.IntegerField(
        choices=LIKERT_CHOICES,
        verbose_name='설문 4',
        blank=False,
        default=0,
        help_text='자연의 손해는 나의 손해다',
    )
