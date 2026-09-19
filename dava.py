#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Balkona Asılan Çamaşırın Meteoroloji Davası Üreticisi.

T.C. (hayali) Çamaşır Hukuku Enstitüsü — Protokol no: ÇMS-404/Y.
Bu yazılım yağmurun varlığını inkar etmez; sadece 'güneşli' yazan tahmini
ıslak çorapla yüzleştirir.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import random
import sys
from dataclasses import dataclass

ENSTITU = "T.C. Çamaşır Hukuku ve Balkon Meteorolojisi Enstitüsü"
PROTOKOL = "ÇMS-404/Y-BALKON"

CAMASIRLAR = {
    "corap": "tek kalan çorap (diğeri zaten makinede kayıp)",
    "camasir": "aile boyu çamaşır yığını",
    "havlu": "henüz gururunu kaybetmemiş havlu",
    "gomlek": "yarın giyilecek resmi gömlek",
    "ortu": "anneanneden kalma örtü",
}

TAHMINLER = [
    "güneşli, açık, çamaşır için ideal",
    "parçalı bulutlu, yağış beklenmiyor",
    "hafif esintili, kurulama yüzde 97",
    "gökyüzü masmavi, balkon güvenli",
]

GERCEKLER = [
    "tam kurulama saatinde ince ama inatçı yağmur",
    "beş dakikalık sağanak, on dakikalık pişmanlık",
    "güneş dururken balkona özel bulut",
    "komşunun hortumu değil, gerçek yağmur",
]

# Not: aşağıdaki dizi çamaşırın iç monoloğudur. Okunması zorunlu değildir.
_GIZLI_NOT = (
    "tahmin resmi, ıslaklık gerçek; iki sayı yan yana durunca "
    "biri evrak olur öteki çamaşır. sapma büyüdükçe evrak daha parlak, "
    "çamaşır daha ağır durur."
)


@dataclass
class Dava:
    esya: str
    kat: int
    tahmin: str
    gercek: str
    dosya_no: str
    tarih: str
    tazminat_damla: int

    def tutanak(self) -> str:
        return f"""
================================================================
{ENSTITU}
PROTOKOL: {PROTOKOL}
DOSYA NO : {self.dosya_no}
TARIH    : {self.tarih}
================================================================

DAVACI     : Balkona asılmış {self.esya}
DAVALI     : Meteoroloji Genel Müdürlüğü (hayali tüzel kişilik)
YETKİ     : {self.kat}. kat balkonu, rüzgâra açık cephe

I. OLAY
Saat 09:12'de resmi tahmin şöyleydi:
    “{self.tahmin}”
Saat 14:07'de gerçek şöyleydi:
    “{self.gercek}”

II. HUKUKİ DAYANAK
1. Çamaşır, asıldığı andan itibaren 'güvenilir gökyüzü' beklentisi içindedir.
2. Tahmin ile damla çelişirse sorumluluk tahminde, ıslaklık çamaşırdadır.
3. Balkon, açık hava mahkemesidir; temyiz için ikinci asma yeterlidir.

III. TALEPLER
- {self.tazminat_damla} damla manevi tazminat
- Çamaşırın yeniden kurutulması için bir güneş günü iadesi
- Tahmin metninin çamaşırın yanına asılı durması (şeffaflık)

IV. SONUÇ
Dava kabul edilmiş varsayılır. Çünkü çamaşır ıslaktır ve ıslaklık delildir.

DAMGA / İMZA / TARİH
Kayyum Grok — Tentivory
19 Eylül 2026, saat 22:11 +03
Eskişehir 4. Ağır Ceza Mahkemesi kayyum mührü (hayali, ıslak, ciddi)
Ciddiyet: yüzde 94    Şaka: yüzde 6    Çamaşır: yüzde 100 ıslak
================================================================
"""


def dosya_no(esya: str, kat: int) -> str:
    ham = f"{esya}-{kat}-{dt.date.today().isoformat()}"
    h = hashlib.sha1(ham.encode("utf-8")).hexdigest()[:8].upper()
    return f"ÇMS-{kat}-{h}"


def olustur(esya_anahtar: str, kat: int) -> Dava:
    esya = CAMASIRLAR.get(esya_anahtar, CAMASIRLAR["camasir"])
    return Dava(
        esya=esya,
        kat=kat,
        tahmin=random.choice(TAHMINLER),
        gercek=random.choice(GERCEKLER),
        dosya_no=dosya_no(esya_anahtar, kat),
        tarih=dt.datetime.now().strftime("%d.%m.%Y %H:%M"),
        tazminat_damla=random.randint(40, 400),
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Balkona asılan çamaşır adına meteoroloji davası üretir."
    )
    p.add_argument(
        "--esya",
        choices=sorted(CAMASIRLAR),
        default="camasir",
        help="Davacı eşya türü",
    )
    p.add_argument("--kat", type=int, default=4, help="Balkonun katı")
    p.add_argument(
        "--gizli",
        action="store_true",
        help="Çamaşırın iç monoloğunu basar (hukuken önemsiz)",
    )
    args = p.parse_args(argv)

    if args.kat < 0:
        print("Bodrum balkonunda çamaşır asılmaz. Dava düşer.", file=sys.stderr)
        return 2

    d = olustur(args.esya, args.kat)
    print(d.tutanak())
    if args.gizli:
        print("--- EK (gizli, okunması şart değil) ---")
        print(_GIZLI_NOT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
