from datetime import datetime
import questionary
from models import Evenement, Collaborateur
from utils.jwt_utils import JWTManager
from utils.utils import Utils
from utils.auth import AuthManager
from utils.permission import Permission
from messages_managers.text import TextManager
from messages_managers.error import ErrorMessage
from messages_managers.success import SuccessMessage
from messages_managers.warning import WarningMessage
from .database import DatabaseManager
from .contract import ContractManager
from .client import ClientManager
from .user import UserManager
from .collab import CollaborateurManager
from app.settings import QUIT_APP_CHOICES
import uuid


class EventManager:
    def __init__(self, db_manager: DatabaseManager, user: UserManager):
        self.db_manager = db_manager
        self.user = user

    def display_event_data(self, event: Evenement):
        """
        Affiche les informations détaillées d'un évènement.
        """
        Utils.new_screen(self.user)

        width = 70
        print(
            TextManager.style(
                TextManager.color(
                    "Informations de l'évènement".center(width), "blue"
                ),
                "bold",
            )
        )
        print(TextManager.color(f"{'Champ':<30} {'Valeur':<30}", "yellow"))
        print("-" * width)
        print(f"{'ID':<30} {TextManager.style(str(event.id), 'dim'):<30}")
        print(f"{'Nom':<30} {TextManager.style(event.nom, 'dim'):<30}")
        print(
            f"{'Client':<30} "
            f"{TextManager.style(event.contrat.client, 'dim'):<30}"
        )
        print(
            f"{'Contrat':<30} "
            f"{TextManager.style(str(event.contrat), 'dim'):<30}"
        )
        print(
            f"{'Date de début':<30} "
            f"{TextManager.style(
                event.date_debut.strftime('%d-%m-%Y'), 'dim'):<30}"
        )
        print(
            f"{'Date de fin':<30} "
            f"{TextManager.style(
                event.date_fin.strftime('%d-%m-%Y'), 'dim'):<30}"
        )
        print(f"{'Lieu':<30} {TextManager.style(event.lieu, 'dim'):<30}")
        print(
            f"{'Nombre de participants':<30} "
            f"{TextManager.style(event.nombre_participants, 'dim'):<30}"
        )
        notes = EventManager.format_notes(event.notes)
        if isinstance(notes, str):
            print(f"{'Notes':<30} {TextManager.style(notes, 'dim'):<30}")
        else:
            print(f"{'Notes':<30} {TextManager.style('', 'dim'):<30}")
            for note in notes:
                print(f"{TextManager.style(note, 'dim'):<60}")
        print(
            f"{'Commercial':<30} "
            f"{TextManager.style(event.commercial, 'dim'):<30}"
        )
        print(
            f"{'Contact Support':<30} "
            f"{TextManager.style(event.support or 'Aucun', 'dim'):<30}"
        )
        print(
            f"{'Date de création':<30} "
            f"{TextManager.style(
                event.date_creation.strftime('%d-%m-%Y %H:%M'), 'dim'):<30}"
        )
        print(
            f"{'Dernière mise à jour':<30} "
            f"{TextManager.style(
                event.derniere_maj.strftime('%d-%m-%Y %H:%M'), 'dim'):<30}"
        )
        print("-" * width)

    @staticmethod
    def format_notes(notes):
        """
        Formate les notes d'un évènement pour l'affichage.
        """
        if not notes:
            return ""
        if "[NewLine]" in notes:
            formatted_notes = notes.split("[NewLine]")
            formatted_notes = [note.strip() for note in formatted_notes]
            return formatted_notes
        else:
            return notes

    @staticmethod
    def get_event(session, warning=False):
        """
        Récupère un évènement à partir de son ID.
        """
        if warning:
            WarningMessage.cancel_command_info()

        while True:
            try:
                event_id = input("ID de l'évènement : ").strip()
                if not event_id:
                    ErrorMessage.id_empty()
                    continue
                try:
                    event_uuid = uuid.UUID(event_id, version=4)
                except ValueError:
                    ErrorMessage.invalid_id()
                    continue
                event = session.query(Evenement
                                      ).filter_by(id=event_uuid).first()
                if not event:
                    ErrorMessage.data_not_found("Evenement", event_id)
                    continue
                return event
            except KeyboardInterrupt:
                WarningMessage.action_cancelled()
                return

    def display_event(self, event_id=None, success_message=None):
        """
        Affiche les informations d'un évènement avec un menu d'actions.
        Actions : Modifier, Supprimer
        """
        if not JWTManager.token_valid(self.user):
            return

        with self.db_manager.session_scope() as session:
            if not event_id:
                event = self.get_event(session)
            else:
                event = session.query(Evenement).filter_by(id=event_id).first()

            self.display_event_data(event)

            if success_message:
                success_message()

            choices = ["🔙 Retour"] + QUIT_APP_CHOICES

            i = 0

            if Permission.update_event(self.user.role):
                choices.insert(i, "✏️  Modifier")
                i += 1
                choices.insert(i, "🗒️  Ajouter une note")
                i += 1

            if Permission.assign_event(self.user.role):
                choices.insert(i, "🔧 Assigner")
                i += 1

            if Permission.delete_event(self.user.role):
                choices.insert(i, "❌ Supprimer")
                i += 1

            while True:
                action = Utils.get_questionnary(choices, edit=True)

                match action:
                    case "🔧 Assigner":
                        self.assign_event(event.id)
                    case "✏️  Modifier":
                        self.update_event(event.id)
                        break
                    case "🗒️  Ajouter une note":
                        self.add_note(event.id)
                        break
                    case "❌ Supprimer":
                        self.delete_event(event.id)
                        break
                    case "🔙 Retour":
                        break
                    case "🔒 Déconnexion":
                        AuthManager.logout()
                    case "❌ Quitter l'application":
                        Utils.quit_app()
                    case _:
                        ErrorMessage.action_not_recognized()

    def display_all_events_menu(self):
        """
        Affiche le menu des évènements.
        """
        if not JWTManager.token_valid(self.user):
            return

        if self.user.role != "Support":
            self.display_all_events()
            return

        choices = [
            "📜 Afficher mes Évènements",
            "📜 Afficher tous les évènements",
            "🔙 Retour"
        ] + QUIT_APP_CHOICES

        while True:
            action = Utils.get_questionnary(choices)

            match action:
                case "📜 Afficher mes Évènements":
                    self.display_all_events(filter="my_events")
                    break
                case "📜 Afficher tous les évènements":
                    self.display_all_events()
                    break
                case "🔙 Retour":
                    break
                case "🔒 Déconnexion":
                    AuthManager.logout()
                case "❌ Quitter l'application":
                    Utils.quit_app()
                case _:
                    ErrorMessage.action_not_recognized()

    def display_all_events(self, filter=None):
        """
        Affiche la liste de tous les évènements.
        """
        Utils.new_screen(self.user)

        if not JWTManager.token_valid(self.user):
            return

        with self.db_manager.session_scope() as session:
            query = session.query(Evenement).order_by(
                Evenement.date_debut.asc()
            )
            title = "Liste des évènements"
            if filter == "my_events":
                query = query.filter(Evenement.support.has(id=self.user.id))
                title = "Mes évènements"

            events = query.all()

            width = 120
            print(
                TextManager.style(
                    TextManager.color(title.center(width), "blue"),
                    "bold",
                )
            )
            print("-" * width)
            print(
                TextManager.color(
                    f"{'ID':36} | {'Nom':20} | {'Client':20} | "
                    f"{'Date de début':20} | {'Date de fin':20}",
                    "yellow",
                )
            )
            print("-" * width)
            if not events:
                print(TextManager.style("Aucun évènement trouvé.", "dim"))
                return
            for event in events:
                id_str = TextManager.style(event.id, "dim")
                nom = TextManager.style(event.nom.ljust(20), "dim")
                client = TextManager.style(
                    event.contrat.client.nom_complet.ljust(20), "dim"
                )
                date_debut = TextManager.style(
                    event.date_debut.strftime("%d-%m-%Y").ljust(20), "dim"
                )
                date_fin = TextManager.style(
                    event.date_fin.strftime("%d-%m-%Y").ljust(20), "dim"
                )
                print(
                    f"{id_str:36} | {nom} | "
                    f"{client} | {date_debut} | {date_fin}")
            print("-" * width)

    def create_event(self):
        """
        Crée un nouvel évènement.
        Informations obligatoires :
        - Nom
        - Date de début
        - Date de fin
        - Lieu
        - Nombre de participants
        - ID du contrat
        - Email du client
        """

        if not JWTManager.token_valid(self.user):
            return

        if not Permission.create_event(self.user.role):
            return

        with self.db_manager.session_scope() as session:
            while True:
                contract = ContractManager.get_contract(session, warning=True)
                if not contract:
                    return
                if str(contract.client.commercial.id) != str(self.user.id):
                    ErrorMessage.contract_not_assigned_to_user_to_create_evt()
                    continue
                if not contract.statut_signe:
                    ErrorMessage.contract_not_signed_for_event()
                    continue
                existing_event = session.query(Evenement
                                               ).filter_by(contrat=contract
                                                           ).first()
                if existing_event:
                    ErrorMessage.contract_already_linked(existing_event)
                    continue
                break
            while True:
                client = ClientManager.get_client(session)
                if not client:
                    return
                if contract.client != client:
                    ErrorMessage.contract_client_mismatch()
                    return
                break

            try:
                while True:
                    nom = input("Nom de l'évènement : ").strip()
                    if not nom:
                        ErrorMessage.event_name_empty()
                        continue
                    break
                while True:
                    date_debut = input("Date de début (JJ-MM-AAAA) : ").strip()
                    if not date_debut:
                        ErrorMessage.event_start_date_empty()
                        continue
                    if not Utils.date_is_valid(date_debut):
                        ErrorMessage.invalid_date_format()
                        continue
                    date_debut = datetime.strptime(date_debut, "%d-%m-%Y")
                    if date_debut < datetime.now():
                        ErrorMessage.start_date_before_today()
                        continue
                    break
                while True:
                    date_fin = input("Date de fin (JJ-MM-AAAA) : ").strip()
                    if not date_fin:
                        ErrorMessage.event_end_date_empty()
                        continue
                    if not Utils.date_is_valid(date_fin):
                        ErrorMessage.invalid_date_format()
                        continue
                    date_fin = datetime.strptime(date_fin, "%d-%m-%Y")
                    if date_fin < date_debut:
                        ErrorMessage.end_date_before_start_date()
                        continue
                    break
                while True:
                    lieu = input("Lieu : ").strip()
                    if not lieu:
                        ErrorMessage.event_location_empty()
                        continue
                    break
                while True:
                    attendees = input("Nombre de participants : ").strip()
                    if not attendees:
                        ErrorMessage.event_attendees_empty()
                        continue
                    try:
                        attendees = int(attendees)
                        if attendees <= 0:
                            ErrorMessage.invalid_attendees_number()
                            continue
                    except ValueError:
                        ErrorMessage.invalid_attendees_number()
                        continue
                    break
            except KeyboardInterrupt:
                WarningMessage.action_cancelled()
                return

            event = Evenement(
                nom=nom,
                date_debut=date_debut,
                date_fin=date_fin,
                lieu=lieu,
                nombre_participants=attendees,
                contrat=contract,
                date_creation=datetime.now(),
                derniere_maj=datetime.now(),
                commercial=session.query(Collaborateur
                                         ).filter_by(id=self.user.id).first(),
            )
            session.add(event)
            session.commit()
            self.display_event(event.id, SuccessMessage.create_success)

    def assign_event(self, event_id=None, edit=False):
        """
        Assigne un collaborateur support à un évènement.
        """
        if not JWTManager.token_valid(self.user):
            return

        if not Permission.assign_event(self.user.role):
            return

        with self.db_manager.session_scope() as session:
            if not event_id:
                event = self.get_event(session, warning=True)
            else:
                event = session.query(Evenement
                                      ).filter_by(id=event_id).first()

            if event.support and not edit:
                while True:
                    action = questionary.select(
                        f"L'évènement a déjà un contact support assigné : "
                        f"{event.support}\n"
                        f"Voulez-vous changer ?",
                        choices=["Oui", "Non"],
                        use_shortcuts=True,
                        instruction=" ",
                    ).ask()

                    match action:
                        case "Oui":
                            break
                        case "Non":
                            WarningMessage.action_cancelled()
                            return
                        case _:
                            ErrorMessage.action_not_recognized()

            while True:
                try:
                    support = CollaborateurManager.get_collaborateur(
                        session, warning=True)
                    if not support:
                        return
                    if support.role.nom != "Support":
                        ErrorMessage.collab_role_mismatch(
                            support.nom, "Support")
                        continue
                    break
                except KeyboardInterrupt:
                    WarningMessage.action_cancelled()
                    return

            event.support = support
            session.commit()
            self.display_event(
                event.id, lambda: SuccessMessage.assign_success(
                    event, support))

    def add_note(self, event_id=None):
        """
        Ajoute une note à un évènement.
        """
        if not JWTManager.token_valid(self.user):
            return

        if not Permission.update_event(self.user.role):
            return

        with self.db_manager.session_scope() as session:
            if not event_id:
                event = self.get_event(session, warning=True)
                if not event:
                    return
            else:
                event = session.query(Evenement
                                      ).filter_by(id=event_id).first()

            while True:
                note = Utils.get_input("Note :")
                if not note:
                    ErrorMessage.event_note_empty()
                    continue
                break

            if event.notes:
                event.notes += "[NewLine]" + note
            else:
                event.notes = note
            event.derniere_maj = datetime.now()
            session.commit()
            self.display_event(event.id, SuccessMessage.event_note_success)

    def update_event(self, event_id=None):
        """
        Met à jour un évènement.
        Champs modifiables :
        - Nom
        - Date de début
        - Date de fin
        - Lieu
        - Nombre de participants
        - Contact Support
        """
        if not JWTManager.token_valid(self.user):
            return

        if not Permission.update_event(self.user.role):
            return

        with self.db_manager.session_scope() as session:
            if not event_id:
                event = self.get_event(session, warning=True)
                if not event:
                    return
            else:
                event = session.query(Evenement
                                      ).filter_by(id=event_id).first()

            choices = [
                "Nom",
                "Date de début",
                "Date de fin",
                "Lieu",
                "Nombre de participants",
                "Tout modifier",
                "Retour"
            ]

            message = None

            while True:
                self.display_event_data(event)
                if message:
                    message()
                    message = None
                action = Utils.get_questionnary(choices, edit=True)

                match action:
                    case "Nom":
                        message = self.update_nom(session, event)
                    case "Date de début":
                        message = self.update_date_debut(session, event)
                    case "Date de fin":
                        message = self.update_date_fin(session, event)
                    case "Lieu":
                        message = self.update_lieu(session, event)
                    case "Nombre de participants":
                        message = self.update_nombre_participants(
                            session, event)
                    case "Tout modifier":
                        messages = [
                            self.update_nom(session, event),
                            self.update_date_debut(session, event),
                            self.update_date_fin(session, event),
                            self.update_lieu(session, event),
                            self.update_nombre_participants(session, event),
                        ]
                        for msg in messages:
                            if msg:
                                message = msg
                                break
                    case "Retour":
                        break
                    case _:
                        ErrorMessage.action_not_recognized()
                        continue

    def update_nom(self, session, event):
        """
        Met à jour le nom d'un évènement.
        """
        message = None
        while True:
            nom = Utils.get_input("Nom :", event.nom)
            if event.nom != nom:
                if not nom:
                    ErrorMessage.event_name_empty()
                    continue
                event.nom = nom
                message = SuccessMessage.update_success
                event.derniere_maj = datetime.now()
                self.db_manager.update_commit(event, session)
            return message

    def update_date_debut(self, session, event):
        """
        Met à jour la date de début d'un évènement.
        """
        message = None
        while True:
            date_debut = Utils.get_input(
                "Date de début (JJ-MM-AAAA) :",
                event.date_debut.strftime("%d-%m-%Y"),
            )
            if event.date_debut != date_debut:
                if not date_debut:
                    ErrorMessage.event_start_date_empty()
                    continue
                if not Utils.date_is_valid(date_debut):
                    ErrorMessage.invalid_date_format()
                    continue
                date_debut = datetime.strptime(date_debut, "%d-%m-%Y")
                if date_debut < datetime.now():
                    ErrorMessage.start_date_before_today()
                    continue
                if date_debut > event.date_fin:
                    ErrorMessage.start_date_after_end_date()
                    continue
                event.date_debut = date_debut
                message = SuccessMessage.update_success
                event.derniere_maj = datetime.now()
                self.db_manager.update_commit(event, session)
            return message

    def update_date_fin(self, session, event):
        """
        Met à jour la date de fin d'un évènement.
        """
        message = None
        while True:
            date_fin = Utils.get_input(
                "Date de fin (JJ-MM-AAAA) :",
                event.date_fin.strftime("%d-%m-%Y"),
            )
            if event.date_fin != date_fin:
                if not date_fin:
                    ErrorMessage.event_end_date_empty()
                    continue
                if not Utils.date_is_valid(date_fin):
                    ErrorMessage.invalid_date_format()
                    continue
                date_fin = datetime.strptime(date_fin, "%d-%m-%Y")
                if date_fin < event.date_debut:
                    ErrorMessage.end_date_before_start_date()
                    continue
                event.date_fin = date_fin
                message = SuccessMessage.update_success
                event.derniere_maj = datetime.now()
                self.db_manager.update_commit(event, session)
            return message

    def update_lieu(self, session, event):
        """
        Met à jour le lieu d'un évènement.
        """
        message = None
        while True:
            lieu = Utils.get_input("Lieu :", event.lieu)
            if event.lieu != lieu:
                if not lieu:
                    ErrorMessage.event_location_empty()
                    continue
                event.lieu = lieu
                message = SuccessMessage.update_success
                event.derniere_maj = datetime.now()
                self.db_manager.update_commit(event, session)
            return message

    def update_nombre_participants(self, session, event):
        """
        Met à jour le nombre de participants d'un évènement.
        """
        message = None
        while True:
            nombre_participants = Utils.get_input(
                "Nombre de participants :",
                str(event.nombre_participants),
            )
            if event.nombre_participants != nombre_participants:
                if not nombre_participants:
                    ErrorMessage.event_attendees_empty()
                    continue
                try:
                    nombre_participants = int(nombre_participants)
                    if nombre_participants <= 0:
                        ErrorMessage.invalid_attendees_number()
                        continue
                except ValueError:
                    ErrorMessage.invalid_attendees_number()
                    continue
                event.nombre_participants = nombre_participants
                message = SuccessMessage.update_success
                event.derniere_maj = datetime.now()
                self.db_manager.update_commit(event, session)
            return message

    def delete_event(self, event_id=None):
        """
        Supprime un évènement.
        """
        if not JWTManager.token_valid(self.user):
            return

        if not Permission.delete_event(self.user.role):
            return

        with self.db_manager.session_scope() as session:
            if not event_id:
                event = self.get_event(session, warning=True)
                if not event:
                    return
            else:
                event = session.query(Evenement
                                      ).filter_by(id=event_id).first()

            if not Utils.confirm_deletion():
                return

            session.delete(event)
            session.commit()
            Utils.new_screen(self.user)
            SuccessMessage.delete_success()
