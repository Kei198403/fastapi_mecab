# -*- coding: utf-8 -*-

import os

from typing import cast, List, Dict

import MeCab

from fastapi import APIRouter, HTTPException
from routers.mecab.schema import MeCabRequestModel, MeCabResponseModel

from routers.mecab.schema import MeCabRcName, MeCabParseResult

router = APIRouter(prefix="/mecab", tags=["MeCab"])

mecabrc: Dict[MeCabRcName, str] = {
    "ipadict": "--rcfile=/app/mecabrc.ipadic",
    "neologd": "--rcfile=/app/mecabrc.neologd"
}


def parse_sentence(sentence: str, rc_name: MeCabRcName, use_userdic: bool) -> List[MeCabParseResult]:
    """MeCabに渡す文章を解析して、結果を返す

    :sentence: MeCabに渡す文章
    :rc_name: MeCabの設定ファイル名
    :use_userdic: ユーザ辞書を使用するかどうか
    """
    mecab_options = mecabrc[rc_name]

    if use_userdic:
        if user_dic := os.getenv("MECAB_USERDIC", None):
            mecab_options += f" --userdic={user_dic}"
        else:
            raise HTTPException(501, "ユーザ辞書が設定されていません")

    tagger = MeCab.Tagger(mecab_options)
    # parseToNodeではなくparseを使う
    result = cast(str, tagger.parse(sentence))

    # --nbestはデフォルトの1を前提とする
    parse_result: List[MeCabParseResult] = []

    for node in result.split("\n"):
        if node == "EOS":
            break

        # 表層形(surface)とそれ以外(feature)に分割する
        surface, feature = node.split("\t", maxsplit=2 - 1)

        # featureをカンマで分割する
        try:
            part_of_speech, part_of_speech_subclass1, part_of_speech_subclass2, part_of_speech_subclass3, \
                conjugation_type, conjugation_form, original_form, yomi, pronunciation = feature.split(",", maxsplit=9 - 1)
        except ValueError:
            part_of_speech, part_of_speech_subclass1, part_of_speech_subclass2, part_of_speech_subclass3, \
                conjugation_type, conjugation_form, original_form = feature.split(",", maxsplit=8 - 1)
            yomi = None
            pronunciation = None

        parse_result.append(MeCabParseResult(
            surface_form=surface,
            part_of_speech=part_of_speech,
            part_of_speech_subclass1=part_of_speech_subclass1,
            part_of_speech_subclass2=part_of_speech_subclass2,
            part_of_speech_subclass3=part_of_speech_subclass3,
            conjugation_type=conjugation_type,
            conjugation_form=conjugation_form,
            original_form=original_form,
            yomi=yomi,
            pronunciation=pronunciation
        ))

    return parse_result


@router.post("/", tags=["MeCab"])
async def post_process_mecab(req: MeCabRequestModel) -> MeCabResponseModel:
    output: Dict[MeCabRcName, List[MeCabParseResult]] = {}

    for rc_name in req.system_dic:
        parse_result = parse_sentence(req.sentence, rc_name, req.use_userdic)
        output[rc_name] = parse_result

    return MeCabResponseModel(input=req, output=output)


@router.get("/", tags=["MeCab"])
async def get_process_mecab(sentence: str, use_userdic: bool = False, system_dic: str = "ipadict,neologd") -> MeCabResponseModel:
    system_dic_list = []

    for rc_name in system_dic.split(","):
        if rc_name not in MeCabRcName.__args__:  # type: ignore
            raise HTTPException(400, "MeCabの設定ファイル名が不正です")
        system_dic_list.append(cast(MeCabRcName, rc_name.strip()))

    return await post_process_mecab(MeCabRequestModel(sentence=sentence, use_userdic=use_userdic, system_dic=system_dic_list))
