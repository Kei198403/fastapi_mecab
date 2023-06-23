# -*- coding: utf-8 -*-

from typing import Literal, List, Dict

from pydantic import BaseModel

MeCabRcName = Literal["ipadict", "neologd"]


class MeCabParseResult(BaseModel):
    """MeCabの解析結果

    https://taku910.github.io/mecab/#usage-tools

    フォーマットは以下の通り。
    ```
    表層形\\t品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音
    ```
    """
    surface_form: str
    """表層形"""

    part_of_speech: str
    """品詞"""

    part_of_speech_subclass1: str
    """品詞細分類1"""

    part_of_speech_subclass2: str
    """品詞細分類2"""

    part_of_speech_subclass3: str
    """品詞細分類3"""

    conjugation_type: str
    """活用型"""

    conjugation_form: str
    """活用形"""

    original_form: str
    """原形"""

    yomi: str | None
    """読み"""

    pronunciation: str | None
    """発音"""


class MeCabRequestModel(BaseModel):
    sentence: str
    """MeCabに渡す文章"""

    use_userdic: bool = False
    """MeCabにユーザ辞書を利用するかどうか。

    * True: 利用する。
    * False: 利用しない（デフォルト）。

    利用する場合は、MECAB_USERDIC環境変数にユーザ辞書のパスを設定する必要がある。
    """

    system_dic: List[MeCabRcName] = ["ipadict", "neologd"]
    """MeCabに渡すシステム辞書の種類。

    * "ipadict": IPA辞書
    * "neologd": neologd辞書

    デフォルトは、IPA辞書とneologd辞書の両方を利用する。
    """


class MeCabResponseModel(BaseModel):
    input: MeCabRequestModel
    output: Dict[MeCabRcName, List[MeCabParseResult]]
