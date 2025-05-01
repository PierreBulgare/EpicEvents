from models import Evenement, Client, Collaborateur, Contrat
from datetime import datetime
from jwt_utils import token_valid
import questionary
from .text import TextManager
from .message import MessageManager
from .database import DatabaseManager
from .user import UserManager
import utils
from settings import QUIT_APP_CHOICES

class EventManager:
    def __init__(self, db_manager: DatabaseManager, user: UserManager):
        self.db_manager = db_manager
        self.user = user

    def display_event_data(self, event: Evenement):
        width = 70
        print(TextManager.style(TextManager.color("Informations de l'évènement".center(width), "blue"), "bold"))
        print(TextManager.color(f"{'Champ':<30} {'Valeur':<30}", "yellow"))
        print("-" * width)
        print(f"{'ID':<30} {TextManager.style(str(event.id), 'dim'):<30}")
        print(f"{'Nom':<30} {TextManager.style(event.nom, 'dim'):<30}")
        print(f"{'Client':<30} {TextManager.style(event.contrat.client.nom_complet, 'dim'):<30}")
        print(f"{'Contrat':<30} {TextManager.style(str(event.contrat.id), 'dim'):<30}")
        print(f"{'Date de début':<30} {TextManager.style(event.date_debut.strftime('%d-%m-%Y'), 'dim'):<30}")
        print(f"{'Date de fin':<30} {TextManager.style(event.date_fin.strftime('%d-%m-%Y'), 'dim'):<30}")
        print(f"{'Lieu':<30} {TextManager.style(event.lieu, 'dim'):<30}")
        print(f"{'Nombre de participants':<30} {TextManager.style(event.nombre_participants, 'dim'):<30}")
        print(f"{'Notes':<30} {TextManager.style(event.notes, 'dim'):<30}")
        print(f"{'Commercial':<30} {TextManager.style(event.commercial.nom, 'dim'):<30}")
        print(f"{'Contact Support':<30} {TextManager.style(event.support.nom if event.support else 'Aucun', 'dim'):<30}")
        print(f"{'Date de création':<30} {TextManager.style(event.date_creation.strftime('%d-%m-%Y %H:%M'), 'dim'):<30}")
        print(f"{'Dernière mise à jour':<30} {TextManager.style(event.derniere_maj.strftime('%d-%m-%Y %H:%M'), 'dim'):<30}")
        print("-" * width)

    def display_event(self, event: Evenement = None):
        if not token_valid(self.user):
            return

        with self.db_manager.session_scope() as session:
            if not event:
                try:
                    MessageManager.cancel_command_info()
                    event_id = input("ID de l'évènement à afficher : ").strip()
                    event = session.query(Evenement).filter_by(id=event_id).first()
                    if not event:
                        MessageManager.data_not_found("Evenement", event_id)
                        return
                except KeyboardInterrupt:
                    MessageManager.action_cancelled()
                    return
            else:
                event = session.merge(event)
            
            self.display_event_data(event)

            CHOICES = [
                "✏️  Modifier",
                "❌ Supprimer",
                "🔙 Retour"
            ] + QUIT_APP_CHOICES
            while True:
                action = questionary.select(
                    "Que voulez-vous faire ?",
                    choices=CHOICES,
                    use_shortcuts=True,
                    instruction=" ",
                ).ask()

                match action:
                    case "✏️  Modifier":
                        self.update_event(event)
                        break
                    case "❌ Supprimer":
                        self.delete_event(event)
                        break
                    case "🔙 Retour":
                        break
                    case "❌ Quitter l'application (Sans Déconnexion)":
                        utils.quit_app()
                    case "🔒 Quitter l'application (Avec Déconnexion)":
                        utils.quit_app(user_logout=True)
                    case _:
                        MessageManager.action_not_recognized()

    def display_all_events(self):
        if not token_valid(self.user):
            return

        with self.db_manager.session_scope() as session:
            events = session.query(Evenement).order_by(Evenement.date_debut.asc()).all()
            if not events:
                MessageManager.empty_table(Evenement.__tablename__)
                return

            width = 120
            print(TextManager.style(TextManager.color("Liste des évènements".center(width), "blue"), "bold"))
            print("-" * width)
            print(TextManager.color(f"{'ID':36} | {'Nom':20} | {'Client':20} | {'Date de début':20} | {'Date de fin':20}", "yellow"))
            print("-" * width)
            for event in events:
                id_str = TextManager.style(event.id, 'dim')
                nom = TextManager.style(event.nom.ljust(20), 'dim')
                client = TextManager.style(event.contrat.client.nom_complet.ljust(20), 'dim')
                date_debut = TextManager.style(event.date_debut.strftime("%d-%m-%Y").ljust(20), 'dim')
                date_fin = TextManager.style(event.date_fin.strftime("%d-%m-%Y").ljust(20), 'dim')
                print(f"{id_str:36} | {nom} | {client} | {date_debut} | {date_fin}")
            print("-" * width)

    def create_event(self):
        MessageManager.cancel_command_info()

        if not token_valid(self.user):
            return

        try:
            nom = input("Nom de l'événement : ")
            date_debut = input("Date de début l'événement (JJ-MM-AAAA) : ")
            date_fin = input("Date de fin de l'événement (JJ-MM-AAAA) : ")
            lieu = input("Lieu de l'événement : ")
            attendees = input("Nombre de participants : ")
        except KeyboardInterrupt:
            MessageManager.action_cancelled()
            return

        
        with self.db_manager.session_scope() as session:
            while True:
                try:
                    contract_id = input("ID du contrat : ")
                    client_email = input("Email du client : ")
                    contract = session.query(Contrat).filter_by(id=contract_id).first()
                    client = session.query(Client).filter_by(email=client_email).first()
                    if not client:
                        MessageManager.data_not_found("Client", client_email)
                        return
                    if not contract:
                        MessageManager.data_not_found("Contrat", contract_id)
                        return
                    if contract.client_id != client.id:
                        MessageManager.contract_client_mismatch(contract_id, client)
                        return
                    break
                except KeyboardInterrupt:
                    MessageManager.action_cancelled()
                    return

            # Création de l'événement
            event = Evenement(
                nom=nom,
                date_debut=datetime.strptime(date_debut, "%d-%m-%Y"),
                date_fin=datetime.strptime(date_fin, "%d-%m-%Y"),
                lieu=lieu,
                nombre_participants=attendees,
                contrat=contract,
                date_creation=datetime.now(),
                derniere_maj=datetime.now(),
                commercial = session.query(Collaborateur).filter_by(id=self.user.id).first(),
            )
            session.add(event)
            session.commit()
            MessageManager.create_success()
            self.display_event(event)