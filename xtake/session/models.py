from django.contrib.auth.models import User
from django.db import models


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
        (0, '관리 (공공·기업, 행정·경영지원, 전문서비스, 건설·전기, 판매·고객서비스)'),
        (1, '전문 (과학, 공학, 보건·사회복지, 교육, 법률, 경영.금융, 문화·예술·스포츠)'),
        (2, '사무 (경영·회계, 금융·보험, 법률·감사, 상담·안내·통계)'),
        (3, '서비스 (경찰·소방·보안, 미용·예식·의료보조, 운송·여가, 조리·음식)'),
        (4, '판매 (영업, 매장 판매, 방문·노점·통신)'),
        (5, '농립어업 (농축산, 임업, 어업)'),
        (6, '기능원 (식품가공, 섬유·의복·가죽, 목재·가구·악기·간판, 금속성형, 운송·기계, 전기·전자, 건설·채굴, 영상·통신)'),
        (7, '기계조작 (식품가공, 섬유·신발, 화학, 금속·비금속, 기계제조, 전기·전자, 운전·운송, 상하수도·재활용, 목재·인쇄)'),
        (8, '단순노무 (건설·광업, 운송, 제조, 청소·경비, 가사·음식, 농림어업)'),
        (9, '학생'),
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

    PA_CHOICES = (
        (None, '선택해주세요'),
        (0, '매우 진보적'),
        (1, '다소 진보적'),
        (2, '중도적'),
        (3, '다소 보수적'),
        (4, '매우 보수적'),
    )

    age = models.IntegerField(choices=AGE_CHOICES, verbose_name='나이')
    gender = models.IntegerField(choices=GENDER_CHOICES, verbose_name='성별')
    occupation = models.IntegerField(choices=OCCUPATION_CHOICES, verbose_name='현재 직업')
    income = models.IntegerField(choices=INCOME_CHOICES, verbose_name='월소득')
    education = models.IntegerField(choices=EDUCATION_CHOICES, verbose_name='최종 학력')
    political_affinity = models.IntegerField(choices=PA_CHOICES, verbose_name='정치 성향')

    # csv
    answers = models.TextField()

    def __str__(self):
        return str(self.user)

    def get_answers(self):
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
