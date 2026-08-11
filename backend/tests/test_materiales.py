from app.core.materiales import pn_limite, PN_POR_DEFECTO_BAR, PN_DESCONOCIDO_BAR


def test_pn_conocida_prevalece_sobre_el_valor_por_defecto():
    assert pn_limite("pvc", 16) == 16


def test_sin_pn_usa_la_clase_minima_del_material():
    for material, esperado in PN_POR_DEFECTO_BAR.items():
        assert pn_limite(material, None) == esperado


def test_material_desconocido_usa_el_limite_mas_restrictivo():
    assert pn_limite(None, None) == PN_DESCONOCIDO_BAR
    assert pn_limite("acero", None) == PN_DESCONOCIDO_BAR


def test_pn_cero_se_trata_como_no_documentada():
    # pn=0 no tiene sentido físico; no debe usarse como límite real.
    assert pn_limite("pvc", 0) == PN_POR_DEFECTO_BAR["pvc"]
