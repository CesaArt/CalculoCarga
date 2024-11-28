import matplotlib.pyplot as plt
from typing import List

class UnidadTransporte:
    def __init__(self, largo: float, ancho: float, alto: float, peso_max: float):
        self.largo = largo
        self.ancho = ancho
        self.alto = alto
        self.peso_max = peso_max

    def calcular_volumen(self) -> float:
        return self.largo * self.ancho * self.alto

class Cargamento:
    def __init__(self):
        self.pallets = []

    def agregar_pallet(self, tipo: str, largo: float, ancho: float, alto: float, peso: float, estibable: bool, cantidad: int, estibas: int = 1):
        self.pallets.append({
            "Tipo": tipo,
            "Largo": largo,
            "Ancho": ancho,
            "Alto": alto,
            "Peso": peso,
            "Estibable": estibable,
            "Cantidad": cantidad,
            "Estibas": estibas
        })

    def calcular_volumen_total(self) -> float:
        total_volumen = 0
        for pallet in self.pallets:
            volumen_pallet = pallet["Largo"] * pallet["Ancho"] * pallet["Alto"] * pallet["Estibas"]
            total_volumen += volumen_pallet * pallet["Cantidad"]
        return total_volumen

    def calcular_peso_total(self) -> float:
        return sum(pallet["Peso"] * pallet["Cantidad"] for pallet in self.pallets)

def verificar_ajuste_volumen(unidad: UnidadTransporte, cargamento: Cargamento) -> bool:
    return cargamento.calcular_volumen_total() <= unidad.calcular_volumen()

def verificar_ajuste_peso(unidad: UnidadTransporte, cargamento: Cargamento) -> bool:
    return cargamento.calcular_peso_total() <= unidad.peso_max

def generar_acomodamiento(unidad: UnidadTransporte, cargamento: Cargamento) -> List[dict]:
    resultado = []
    for pallet in cargamento.pallets:
        max_cantidad = (unidad.largo // pallet["Largo"]) * (unidad.ancho // pallet["Ancho"]) * (unidad.alto // pallet["Alto"])
        cantidad_acomodada = min(pallet["Cantidad"], max_cantidad)
        cantidad_no_acomodada = pallet["Cantidad"] - cantidad_acomodada
        resultado.append({
            "Tipo": pallet["Tipo"],
            "Dimensiones (m)": f"{pallet['Largo']}x{pallet['Ancho']}x{pallet['Alto']}",
            "Peso (kg)": pallet["Peso"],
            "Estibable": pallet["Estibable"],
            "Cantidad acomodada": cantidad_acomodada,
            "Cantidad no acomodada": cantidad_no_acomodada
        })
    return resultado

def visualizar_acomodamiento(unidad: UnidadTransporte, cargamento: Cargamento, resultado: List[dict]):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, unidad.largo)
    ax.set_ylim(0, unidad.ancho)
    ax.set_title("Plan de Acomodo de la Unidad de Transporte")
    ax.set_xlabel("Largo (m)")
    ax.set_ylabel("Ancho (m)")

    colores = plt.cm.get_cmap("tab20", len(resultado))
    x, y = 0, 0

    for idx, pallet in enumerate(resultado):
        color = colores(idx)
        cantidad = pallet["Cantidad acomodada"]
        largo = float(pallet["Dimensiones (m)"].split("x")[0])
        ancho = float(pallet["Dimensiones (m)"].split("x")[1])

        for i in range(cantidad):
            if x + largo > unidad.largo:
                x = 0
                y += ancho
            if y + ancho > unidad.ancho:
                print(f"Alerta: No hay más espacio para el pallet {pallet['Tipo']}")
                break

            rect = plt.Rectangle((x, y), largo, ancho, color=color, alpha=0.6, label=pallet["Tipo"] if i == 0 else "")
            ax.add_patch(rect)
            ax.text(
                x + largo / 2, y + ancho / 2,
                f"{pallet['Tipo']}\n{largo}x{ancho}m",
                color="black", ha="center", va="center", fontsize=8
            )
            x += largo

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc="upper right", bbox_to_anchor=(1.2, 1))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.show()

# Programa principal
if __name__ == "__main__":
    largo = float(input("Ingrese el largo de la unidad (m): "))
    ancho = float(input("Ingrese el ancho de la unidad (m): "))
    alto = float(input("Ingrese el alto de la unidad (m): "))
    peso_max = float(input("Ingrese el peso máximo de la unidad (kg): "))
    unidad = UnidadTransporte(largo, ancho, alto, peso_max)

    cargamento = Cargamento()
    while True:
        tipo = input("\nIngrese el tipo de pallet: ")
        largo_p = float(input("Ingrese el largo del pallet (m): "))
        ancho_p = float(input("Ingrese el ancho del pallet (m): "))
        alto_p = float(input("Ingrese el alto del pallet (m): "))
        peso_p = float(input("Ingrese el peso del pallet (kg): "))
        estibable = input("¿Es estibable (sí/no)? ").strip().lower() == "sí"

        estibas = 1
        if estibable:
            estibas = int(input("¿Cuántas unidades pueden apilarse (estibas)? "))

        cantidad = int(input("Ingrese la cantidad de pallets de este tipo: "))
        cargamento.agregar_pallet(tipo, largo_p, ancho_p, alto_p, peso_p, estibable, cantidad, estibas)

        otra = input("¿Desea agregar otro tipo de pallet (sí/no)? ").strip().lower()
        if otra == "no":
            break

    # Verificar el ajuste y mostrar resultados
    if verificar_ajuste_volumen(unidad, cargamento) and verificar_ajuste_peso(unidad, cargamento):
        print("\nEl cargamento cabe en la unidad.")
        print("\nPlan de acomodo:")
        acomodo = generar_acomodamiento(unidad, cargamento)
        for item in acomodo:
            print(f"Tipo: {item['Tipo']}, Dimensiones: {item['Dimensiones (m)']}, Peso: {item['Peso (kg)']} kg, "
                  f"Estibable: {item['Estibable']}, Cantidad acomodada: {item['Cantidad acomodada']}, "
                  f"Cantidad no acomodada: {item['Cantidad no acomodada']}")
        visualizar_acomodamiento(unidad, cargamento, acomodo)
    else:
        print("\nEl cargamento no cabe en la unidad.")