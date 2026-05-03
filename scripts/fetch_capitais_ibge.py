import csv
import time

import requests

CAPITAIS = [
    {"nome": "Porto Velho", "code": "1100205", "uf": "RO", "regiao": "Norte"},
    {"nome": "Rio Branco", "code": "1200401", "uf": "AC", "regiao": "Norte"},
    {"nome": "Manaus", "code": "1302603", "uf": "AM", "regiao": "Norte"},
    {"nome": "Boa Vista", "code": "1400100", "uf": "RR", "regiao": "Norte"},
    {"nome": "Belém", "code": "1501402", "uf": "PA", "regiao": "Norte"},
    {"nome": "Macapá", "code": "1600303", "uf": "AP", "regiao": "Norte"},
    {"nome": "Palmas", "code": "1721000", "uf": "TO", "regiao": "Norte"},
    {"nome": "São Luís", "code": "2111300", "uf": "MA", "regiao": "Nordeste"},
    {"nome": "Teresina", "code": "2211001", "uf": "PI", "regiao": "Nordeste"},
    {"nome": "Fortaleza", "code": "2304400", "uf": "CE", "regiao": "Nordeste"},
    {"nome": "Natal", "code": "2408102", "uf": "RN", "regiao": "Nordeste"},
    {"nome": "João Pessoa", "code": "2507507", "uf": "PB", "regiao": "Nordeste"},
    {"nome": "Recife", "code": "2611606", "uf": "PE", "regiao": "Nordeste"},
    {"nome": "Maceió", "code": "2704302", "uf": "AL", "regiao": "Nordeste"},
    {"nome": "Aracaju", "code": "2800308", "uf": "SE", "regiao": "Nordeste"},
    {"nome": "Salvador", "code": "2927408", "uf": "BA", "regiao": "Nordeste"},
    {"nome": "Belo Horizonte", "code": "3106200", "uf": "MG", "regiao": "Sudeste"},
    {"nome": "Vitória", "code": "3205309", "uf": "ES", "regiao": "Sudeste"},
    {"nome": "Rio de Janeiro", "code": "3304557", "uf": "RJ", "regiao": "Sudeste"},
    {"nome": "São Paulo", "code": "3550308", "uf": "SP", "regiao": "Sudeste"},
    {"nome": "Curitiba", "code": "4106902", "uf": "PR", "regiao": "Sul"},
    {"nome": "Florianópolis", "code": "4205407", "uf": "SC", "regiao": "Sul"},
    {"nome": "Porto Alegre", "code": "4314902", "uf": "RS", "regiao": "Sul"},
    {"nome": "Campo Grande", "code": "5002704", "uf": "MS", "regiao": "Centro-Oeste"},
    {"nome": "Cuiabá", "code": "5103403", "uf": "MT", "regiao": "Centro-Oeste"},
    {"nome": "Goiânia", "code": "5208707", "uf": "GO", "regiao": "Centro-Oeste"},
    {"nome": "Brasília", "code": "5300108", "uf": "DF", "regiao": "Centro-Oeste"},
]

CODES_PIPE = "|".join(c["code"] for c in CAPITAIS)
BASE_V3 = "https://servicodados.ibge.gov.br/api/v3/agregados"
BASE_V1 = "https://servicodados.ibge.gov.br/api/v1"


def fetch_sidra(agregado, periodo, variavel, label):
    url = f"{BASE_V3}/{agregado}/periodos/{periodo}/variaveis/{variavel}?localidades=N6[{CODES_PIPE}]"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    result = {}
    for item in r.json():
        for res in item.get("resultados", []):
            for s in res.get("series", []):
                code = s["localidade"]["id"]
                val = list(s["serie"].values())[0]
                try:
                    result[code] = (
                        float(val.replace(",", "."))
                        if val not in ("-", "...", "", None)
                        else None
                    )
                except Exception:
                    result[code] = None
    print(f"  OK  {label}: {len(result)} registros")
    return result


def main():
    print("Buscando dados IBGE para as 27 capitais...\n")

    # Localidades: microrregião e mesorregião
    print("[1/7] Localidades...")
    r = requests.get(f"{BASE_V1}/localidades/municipios", timeout=30)
    r.raise_for_status()
    loc_map = {}
    for m in r.json():
        loc_map[str(m["id"])] = {
            "microrregiao": (m.get("microrregiao") or {}).get("nome", ""),
            "mesorregiao": ((m.get("microrregiao") or {}).get("mesorregiao") or {}).get(
                "nome", ""
            ),
        }
    print(f"  OK  {len(loc_map)} municípios carregados")
    time.sleep(0.4)

    print("[2/7] Área territorial km² (via localidades)...")
    area = {}
    for c in CAPITAIS:
        r2 = requests.get(
            f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{c['code']}",
            timeout=30,
        )
        r2.raise_for_status()
        data2 = r2.json()
        area[c["code"]] = (
            data2.get("area", {}).get("area")
            if isinstance(data2.get("area"), dict)
            else None
        )
        time.sleep(0.1)
    print(f"  OK  {len(area)} registros")

    print("[3/7] População residente — Censo 2022...")
    try:
        pop = fetch_sidra(9514, 2022, 93, "População")
    except Exception as e:
        print(f"  AVISO: falhou ({e}) — população será vazia")
        pop = {}
    time.sleep(0.4)

    print("[4/7] Domicílios particulares ocupados — Censo 2022...")
    try:
        dom = fetch_sidra(9514, 2022, 6318, "Domicílios")
    except Exception as e:
        print(f"  AVISO: falhou ({e}) — domicílios serão vazios")
        dom = {}
    time.sleep(0.4)

    print("[5/7] PIB total em R$ mil (2021)...")
    try:
        pib_total = fetch_sidra(5938, 2021, 513, "PIB total")
    except Exception as e:
        print(f"  AVISO: falhou ({e}) — PIB total será vazio")
        pib_total = {}
    time.sleep(0.4)

    print("[6/7] PIB per capita em R$ (2021)...")
    try:
        pib_pc = fetch_sidra(5938, 2021, 37, "PIB per capita")
    except Exception as e:
        print(f"  AVISO: falhou ({e}) — PIB per capita será vazio")
        pib_pc = {}
    time.sleep(0.4)

    print("[7/7] Taxa de mortalidade infantil (2021)...")
    try:
        mort = fetch_sidra(9152, 2021, 106, "Mortalidade infantil")
    except Exception as e:
        print(f"  AVISO: falhou ({e}) — mortalidade será vazia")
        mort = {}

    print("\nMontando CSV...")
    rows = []
    for c in CAPITAIS:
        code = c["code"]
        pop_val = pop.get(code)
        area_val = area.get(code)
        dens = round(pop_val / area_val, 2) if pop_val and area_val else None
        loc = loc_map.get(code, {})
        rows.append(
            {
                "municipio": c["nome"],
                "codigo_ibge": code,
                "uf": c["uf"],
                "regiao": c["regiao"],
                "mesorregiao": loc.get("mesorregiao", ""),
                "microrregiao": loc.get("microrregiao", ""),
                "area_km2": area_val,
                "populacao_2022": pop_val,
                "domicilios_ocupados_2022": dom.get(code),
                "densidade_hab_km2": dens,
                "pib_total_2021_RS_mil": pib_total.get(code),
                "pib_per_capita_2021_RS": pib_pc.get(code),
                "mortalidade_infantil_2021": mort.get(code),
            }
        )

    output = "capitais_ibge.csv"
    cols = list(rows[0].keys())
    with open(output, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    print(f"\nSalvo em: {output}")
    print(f"Colunas:  {', '.join(cols)}")
    print(f"Linhas:   {len(rows)}")


if __name__ == "__main__":
    main()
