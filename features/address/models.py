from django.db import models
from core.validators import validate_postal_code


class Address(models.Model):
    postal_code = models.CharField(
        "CEP", max_length=9, validators=[validate_postal_code]
    )
    street = models.CharField("Rua", max_length=160)
    district = models.CharField("Bairro", max_length=160)
    city = models.CharField("Cidade", max_length=160)

    STATE_RONDONIA = "RO"
    STATE_ACRE = "AC"
    STATE_AMAZONAS = "AM"
    STATE_RORAIMA = "RR"
    STATE_PARA = "PA"
    STATE_AMAPA = "AP"
    STATE_TOCANTINS = "TO"
    STATE_MARANHAO = "MA"
    STATE_PIAUI = "PI"
    STATE_CEARA = "CE"
    STATE_RIO_GRANDE_NORTE = "RN"
    STATE_PARAIBA = "PB"
    STATE_PERNAMBUCO = "PE"
    STATE_ALAGOAS = "AL"
    STATE_SERGIPE = "SE"
    STATE_BAHIA = "BA"
    STATE_MINAS_GERAIS = "MG"
    STATE_ESPIRITO_SANTO = "ES"
    STATE_RIO_JANEIRO = "RJ"
    STATE_SAO_PAULO = "SP"
    STATE_PARANA = "PR"
    STATE_SANTA_CATARINA = "SC"
    STATE_RIO_GRANDE_SUL = "RS"
    STATE_MATO_GROSSO_SUL = "MS"
    STATE_MATO_GROSSO = "MT"
    STATE_GOIAS = "GO"
    STATE_DISTRITO_FEDERAL = "DF"
    STATES = (
        (STATE_RONDONIA, STATE_RONDONIA),
        (STATE_ACRE, STATE_ACRE),
        (STATE_AMAZONAS, STATE_AMAZONAS),
        (STATE_RORAIMA, STATE_RORAIMA),
        (STATE_PARA, STATE_PARA),
        (STATE_AMAPA, STATE_AMAPA),
        (STATE_TOCANTINS, STATE_TOCANTINS),
        (STATE_MARANHAO, STATE_MARANHAO),
        (STATE_PIAUI, STATE_PIAUI),
        (STATE_CEARA, STATE_CEARA),
        (STATE_RIO_GRANDE_NORTE, STATE_RIO_GRANDE_NORTE),
        (STATE_PARAIBA, STATE_PARAIBA),
        (STATE_PERNAMBUCO, STATE_PERNAMBUCO),
        (STATE_ALAGOAS, STATE_ALAGOAS),
        (STATE_SERGIPE, STATE_SERGIPE),
        (STATE_BAHIA, STATE_BAHIA),
        (STATE_MINAS_GERAIS, STATE_MINAS_GERAIS),
        (STATE_ESPIRITO_SANTO, STATE_ESPIRITO_SANTO),
        (STATE_RIO_JANEIRO, STATE_RIO_JANEIRO),
        (STATE_SAO_PAULO, STATE_SAO_PAULO),
        (STATE_PARANA, STATE_PARANA),
        (STATE_SANTA_CATARINA, STATE_SANTA_CATARINA),
        (STATE_RIO_GRANDE_SUL, STATE_RIO_GRANDE_SUL),
        (STATE_MATO_GROSSO_SUL, STATE_MATO_GROSSO_SUL),
        (STATE_MATO_GROSSO, STATE_MATO_GROSSO),
        (STATE_GOIAS, STATE_GOIAS),
        (STATE_DISTRITO_FEDERAL, STATE_DISTRITO_FEDERAL),
    )

    state = models.CharField("UF", max_length=2, choices=STATES)
    number = models.CharField(
        "Número", max_length=30, blank=True, null=True, default=""
    )
    complement = models.CharField(
        "Complemento", max_length=160, blank=True, null=True, default=""
    )

    def __str__(self):
        return (
            "%(street)s, %(district)s, %(city)s - %(state)s, CEP %(postal_code)s, %(number)s"
            % {**self.__dict__, "number": self.number or "S/N"}
        )

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"
