from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionExtrairDadosVitima(Action):
    def name(self) -> Text:
        return "action_extrair_dados_vitima"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slots = {}

        # Obtém a lista de todas as entidades do tipo "inem" do tracker
        entities = [entity["value"] for event in tracker.events if event["event"] == "user" for entity in event["parse_data"].get("entities", []) if entity["entity"] == "inem"]

        slots["respostas"] = entities
        # Retorna os slots atualizados para o tracker
        return [SlotSet(slot, value) for slot, value in slots.items()]
    


class ActionGetAllSlots(Action):
    def name(self) -> Text:
        return "action_get_slot_values"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Obter os slots do rastreador
        slots = tracker.slots
        slots_info = []
        message = "Informações Guardadas:\n"

        for _, slot_value in slots.items():
            # Verificar se o valor do slot é None e substituir por uma string vazia
            if slot_value is None:
                slot_value = ""
            # Se o valor do slot for uma lista, converte para string
            elif isinstance(slot_value, list):
                slot_value = ", ".join(slot_value)
            slots_info.append(slot_value)
          
            message+= f"{slot_value}\n "
        # Escrever a mensagem no "cal112.txt"
        f=open("cal112.txt", "w", encoding="utf-8")
        f.write(message)

        # Enviar mensagem
        dispatcher.utter_message(text=message)

        return []
