"""Simulador determinístico do caminho feliz; nunca registra vendas reais."""
from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class Event:
    stage: str
    status: str
    detail: str

def simulate_happy_path():
    events = [
        Event("INT.1", "public_aggregate_signal", "Busca por banana observada em dados agregados, sem identificar usuário"),
        Event("INT.2", "public_trend_signal", "Batom em conteúdo público de influenciador; alcance ilustrativo de 1 milhão"),
        Event("offer_gate", "approved_required", "Robô seleciona apenas ofertas reais, ativas e autorizadas"),
        Event("campaign", "simulated", "Divulgação orgânica com URL rastreável; sem direcionamento individual não consentido"),
        Event("visit", "simulated", "Visitante escolhe clicar na vitrine Wero1Mercados"),
        Event("redirect", "simulated", "Clique /go/ leva à loja parceira autorizada"),
        Event("order", "simulated", "Loja parceira realiza checkout e venda"),
        Event("conversion", "simulated_partner_confirmed", "Parceiro autentica evento e confirma venda após conciliação"),
        Event("commission", "simulated_partner_approved", "Comissão aprovada conforme regras do programa"),
        Event("payout", "simulated_partner_paid", "Parceiro paga ao titular cadastrado; transferência depende do provedor"),
        Event("dashboard", "simulation_only", "Nenhum valor pode ser apresentado como saldo real"),
    ]
    return {"simulation": True, "currency": "BRL", "example_order_brl": 100.0,
            "example_commission_rate": 0.05, "example_commission_brl": 5.0,
            "real_sales_created": 0, "real_transfers_created": 0,
            "events": [asdict(e) for e in events]}
