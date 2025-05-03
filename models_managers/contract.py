from models import Client, Collaborateur, Contrat
from datetime import datetime
from utils.jwt_utils import JWTManager
from utils.utils import Utils
import questionary
from messages_managers.text import TextManager
from messages_managers.error import ErrorMessage
from messages_managers.success import SuccessMessage
from messages_managers.warning import WarningMessage
from .database import DatabaseManager
from .user import UserManager
from app.settings import QUIT_APP_CHOICES


class ContractManager:
    def __init__(self, db_manager: DatabaseManager, user: UserManager):
        self.db_manager = db_manager
        self.user = user

    def display_contract_data(self, contract: Contrat):
        Utils.new_screen(self.user)
        print(TextManager.style(TextManager.color("Informations du contrat".center(50), "blue"), "bold"))
        print(TextManager.color(f"{'Champ':<20} {'Valeur':<30}", "yellow"))
        print("-" * 50)
        print(f"{'ID':<20} {TextManager.style(contract.id, 'dim'):<30}")
        print(f"{'Client':<20} {TextManager.style(contract.client.nom_complet, 'dim'):<30}")
        print(f"{'Montant total':<20} {TextManager.style(f'{float(contract.montant_total):.2f} €', 'dim'):<30}")
        print(f"{'Montant dû':<20} {TextManager.style(f'{float(contract.montant_restant):.2f} €', 'dim'):<30}")
        print(f"{'Date de création':<20} {TextManager.style(contract.date_creation.strftime('%Y-%m-%d %H:%M'), 'dim'):<30}")
        print(f"{'Signé ?':<20} {TextManager.style('Oui' if contract.statut_signe else 'Non', 'dim'):<30}")
        if contract.statut_signe:
            print(f"{'Date de signature':<20} {TextManager.style(contract.date_signature.strftime('%Y-%m-%d %H:%M'), 'dim'):<30}")
        print(f"{'Gestionnaire':<20} {TextManager.style(contract.gestionnaire.nom, 'dim'):<30}")
        print(f"{'Commercial':<20} {TextManager.style(contract.client.commercial.nom, 'dim'):<30}")
        print(f"{'Dernière mise à jour':<20} {TextManager.style(contract.derniere_maj.strftime('%Y-%m-%d %H:%M'), 'dim'):<30}")
        print("-" * 50)

    def display_contract(self, contract_id = None, success_message = None):
        if not JWTManager.token_valid(self.user):
            return
        

        with self.db_manager.session_scope() as session:
            if not contract_id:
                try:
                    WarningMessage.cancel_command_info()
                    contract_id = input("ID du contrat à afficher : ").strip()
                    if not contract_id:
                        ErrorMessage.id_empty()
                        return
                    contract = session.query(Contrat).filter_by(id=contract_id).first()
                    if not contract:
                        ErrorMessage.data_not_found("Contrat", contract_id)
                        return
                except KeyboardInterrupt:
                    WarningMessage.action_cancelled()
                    return
            else:
                contract = session.query(Contrat).filter_by(id=contract_id).first()
            
            self.display_contract_data(contract)
            
            if success_message:
                success_message(contract_id)

            CHOICES = [
                "✏️  Modifier",
                "🖊️  Signer",
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
                        self.update_contract(contract.id)
                        break
                    case "🖊️  Signer":
                        self.sign_contract(contract.id)
                        continue
                    case "❌ Supprimer":
                        self.delete_contract(contract.id)
                        break
                    case "🔙 Retour":
                        break
                    case "❌ Quitter l'application (Sans Déconnexion)":
                        Utils.quit_app()
                    case "🔒 Quitter l'application (Avec Déconnexion)":
                        Utils.quit_app(user_logout=True)
                    case _:
                        ErrorMessage.action_not_recognized()

    def display_all_contracts(self):
        if not JWTManager.token_valid(self.user):
            return

        with self.db_manager.session_scope() as session:
            contracts = session.query(Contrat).order_by(Contrat.date_creation.desc()).all()
            if not contracts:
                WarningMessage.empty_table(Contrat.__tablename__)
                return

            width = 120
            print(TextManager.style(TextManager.color("Liste des contrats".center(width), "blue"), "bold"))
            print("-" * width)
            print(TextManager.color(f"{'ID':36} | {'Client':20} | {'Montant total':20} | {'Montant restant':20} | {'Signé ?':10}", "yellow"))
            print("-" * width)
            for contract in contracts:
                id_str = TextManager.style(contract.id, 'dim')
                client_str = TextManager.style(contract.client.nom_complet.ljust(20), 'dim')
                montant_str = TextManager.style(f"{float(contract.montant_total):,.2f} €".replace(',', ' ').ljust(20), 'dim')
                montant_restant_str = TextManager.style(f"{float(contract.montant_restant):,.2f} €".replace(',', ' ').ljust(20), 'dim')
                if contract.statut_signe:
                    statut_str = TextManager.color("Oui", 'green')
                else:
                    statut_str = TextManager.color("Non", 'red')
                print(f"{id_str:36} | {client_str} | {montant_str} | {montant_restant_str} | {statut_str:10}")
            print("-" * width)


    def create_contract(self):
        WarningMessage.cancel_command_info()

        if not JWTManager.token_valid(self.user):
            return

        while True:
            try:
                montant_total = float(input("Montant total : ").strip())
                if montant_total < 0:
                    ErrorMessage.amount_negative()
                    continue
                break
            except ValueError:
                ErrorMessage.invalid_amount()
                continue
            except KeyboardInterrupt:
                WarningMessage.action_cancelled()
                return
        
        with self.db_manager.session_scope() as session:
            while True:
                try:
                    client_email = input("Email du client : ").strip()
                    if not client_email:
                        ErrorMessage.email_empty()
                        continue
                    client = session.query(Client).filter_by(email=client_email).first()
                    if not client:
                        ErrorMessage.data_not_found("Client", client_email)
                        continue
                    break
                except KeyboardInterrupt:
                    WarningMessage.action_cancelled()
                    return

            # Création du contrat
            contract = Contrat(
                client=client,
                montant_total=montant_total,
                montant_restant=montant_total,
                date_creation=datetime.now(),
                derniere_maj=datetime.now(),
                gestionnaire=session.query(Collaborateur).filter_by(id=self.user.id).first()
            )
            session.add(contract)
            session.commit()
            self.display_contract(contract.id, SuccessMessage.create_success)

    def update_contract(self, contract_id = None):
        if not JWTManager.token_valid(self.user):
            return

        
        with self.db_manager.session_scope() as session:
            WarningMessage.cancel_command_info()
            if not contract_id:
                while True:
                    try:
                        contract_id = input("ID du contrat à modifier : ").strip()
                        if not contract_id:
                            ErrorMessage.id_empty()
                            continue
                        contract = session.query(Contrat).filter_by(id=contract_id).first()
                        if not contract:
                            print(f"Le contrat avec l'ID '{contract_id}' n'existe pas.")
                            continue
                        self.display_contract_data(contract)
                        break
                    except KeyboardInterrupt:
                        WarningMessage.action_cancelled()
                        return
            else:
                contract = session.query(Contrat).filter_by(id=contract_id).first()
                
            CHOICES = [
                "Montant total",
                "Montant restant dû",
                "Retour"
            ]

            while True:
                action = questionary.select(
                    "Que voulez-vous modifier ?",
                    choices=CHOICES,
                    use_shortcuts=True,
                    instruction=" "
                ).ask()

                match action:
                    case "Montant total":
                        current_montant_total = contract.montant_total
                        while True:
                            try:
                                montant_total = questionary.text(
                                    "Montant total : ",
                                    default=str(contract.montant_total)
                                ).ask()
                                montant_total = float(montant_total)
                                if montant_total < 0:
                                    ErrorMessage.amount_negative()
                                    continue
                                break
                            except ValueError:
                                ErrorMessage.invalid_amount()
                                continue
                        contract.montant_total = montant_total
                        # Mise à jour du montant restant dû
                        contract.montant_restant -= current_montant_total - montant_total
                    case "Montant restant dû":
                        while True:
                            try:
                                montant_restant = questionary.text(
                                    "Montant restant dû: ",
                                    default=str(contract.montant_restant)
                                ).ask()
                                montant_restant = float(montant_restant)
                                if montant_total < 0:
                                    ErrorMessage.amount_negative()
                                    continue
                                if montant_restant > contract.montant_total:
                                    ErrorMessage.remaining_gt_total()
                                    continue
                                break
                            except ValueError:
                                ErrorMessage.invalid_amount()
                                continue
                        contract.montant_restant = montant_restant
                    case "Retour":
                        break
                    case _:
                        ErrorMessage.action_not_recognized()

            contract.derniere_maj = datetime.now()

            session.commit()
            self.display_contract(contract.id, SuccessMessage.update_success)

    def sign_contract(self, contract_id = None):

        if not JWTManager.token_valid(self.user):
            return

        
        with self.db_manager.session_scope() as session:
            if not contract_id:
                WarningMessage.cancel_command_info()
                while True:
                    try:
                        contract_id = input("ID du contrat à signer : ").strip()
                        if not contract_id:
                            ErrorMessage.id_empty()
                            continue
                        contract = session.query(Contrat).filter_by(id=contract_id).first()
                        if not contract:
                            ErrorMessage.data_not_found("Contrat", contract_id)
                            continue
                        break
                    except KeyboardInterrupt:
                        WarningMessage.action_cancelled()
                        return
            else:
                contract = session.query(Contrat).filter_by(id=contract_id).first()
                
            if contract.statut_signe:
                ErrorMessage.contract_already_signed(contract.id)
                return


            # Signer le contrat
            contract.date_signature = datetime.now()
            contract.statut_signe = True
            contract.derniere_maj = datetime.now()
            session.commit()
            self.display_contract(contract.id, SuccessMessage.sign_success)


    def delete_contract(self, contract_id = None):
        if not JWTManager.token_valid(self.user):
            return
        
        with self.db_manager.session_scope() as session:
            if not contract_id:
                try:
                    WarningMessage.cancel_command_info()
                    contract_id = input("ID du contrat à supprimer : ").strip()
                    if not contract_id:
                        ErrorMessage.id_empty()
                        return
                    contract = session.query(Contrat).filter_by(id=contract_id).first()
                    if not contract:
                        ErrorMessage.data_not_found("Contrat", contract_id)
                        return
                    self.display_contract_data(contract)
                except KeyboardInterrupt:
                    WarningMessage.action_cancelled()
                    return
            else:
                contract = session.query(Contrat).filter_by(id=contract_id).first()
                
            while True:
                confirmation = questionary.select(
                    f"Êtes-vous sûr de vouloir supprimer le contrat '{contract.id}' ?",
                    choices=["Oui", "Non"],
                    use_shortcuts=True,
                    instruction=" ",
                ).ask()

                match confirmation:
                    case "Oui":
                        break
                    case "Non":
                        WarningMessage.action_cancelled()
                        return
                    case _:
                        ErrorMessage.action_not_recognized()

            # Suppression du contrat
            session.delete(contract)
            session.commit()
            Utils.new_screen(self.user)
            SuccessMessage.delete_success()
