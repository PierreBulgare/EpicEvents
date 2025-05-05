from models import Client, Collaborateur, Contrat
from datetime import datetime
from utils.jwt_utils import JWTManager
from utils.utils import Utils
from messages_managers.text import TextManager
from messages_managers.error import ErrorMessage
from messages_managers.success import SuccessMessage
from messages_managers.warning import WarningMessage
from .database import DatabaseManager
from .client import ClientManager
from .user import UserManager
from app.settings import QUIT_APP_CHOICES
from utils.permission import Permission
from utils.auth import AuthManager
import uuid


class ContractManager:
    def __init__(self, db_manager: DatabaseManager, user: UserManager):
        self.db_manager = db_manager
        self.user = user

    def display_contract_data(self, contract: Contrat):
        """
        Affiche les informations d'un contrat.
        ID, client, montant total, montant restant, date de création,
        statut signé, date de signature, gestionnaire, commercial,
        date de dernière mise à jour.
        """
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

    @staticmethod
    def get_contract(session, warning=False):
        """
        Récupère un contrat à partir de son ID.
        """
        if warning:
            WarningMessage.cancel_command_info()

        while True:
            try:
                contract_id = input("ID du contrat : ").strip()
                if not contract_id:
                    ErrorMessage.id_empty()
                    continue
                try:
                    contract_uuid = uuid.UUID(contract_id, version=4)
                except ValueError:
                    ErrorMessage.invalid_id()
                    continue
                contract = session.query(Contrat
                                         ).filter_by(id=contract_uuid).first()
                if not contract:
                    ErrorMessage.data_not_found("Contrat", contract_id)
                    continue
                return contract
            except KeyboardInterrupt:
                WarningMessage.action_cancelled()
                return

    def display_contract(self, contract_id=None, success_message=None):
        """
        Affiche les informations d'un contrat avec un menu d'actions.
        Actions : Modifier, Signer, Supprimer
        """
        if not JWTManager.token_valid(self.user):
            return

        with self.db_manager.session_scope() as session:
            if not contract_id:
                contract = ContractManager.get_contract(session)
                if not contract:
                    return
            else:
                contract = session.query(Contrat).filter_by(id=contract_id).first()
            
            self.display_contract_data(contract)

            if not Permission.contract_management(self.user.role):
                return
            
            if success_message:
                success_message(contract_id)

            choices = [
                "✏️  Modifier",
                "🖊️  Signer",
                "❌ Supprimer",
                "🔙 Retour"
            ] + QUIT_APP_CHOICES

            while True:
                action = Utils.get_questionnary(choices)

                match action:
                    case "✏️  Modifier":
                        self.update_contract(contract.id)
                        break
                    case "🖊️  Signer":
                        self.sign_contract(contract.id)
                        break
                    case "❌ Supprimer":
                        self.delete_contract(contract.id)
                        break
                    case "🔙 Retour":
                        break
                    case "🔒 Déconnexion":
                        AuthManager.logout()
                    case "❌ Quitter l'application":
                        Utils.quit_app()
                    case _:
                        ErrorMessage.action_not_recognized()

    def display_all_contracts(self):
        """
        Affiche la liste de tous les contrats.
        """
        Utils.new_screen(self.user)

        if not JWTManager.token_valid(self.user):
            return

        with self.db_manager.session_scope() as session:
            contracts = session.query(Contrat
                                      ).order_by(Contrat.date_creation.desc()
                                                 ).all()
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
        """
        Crée un nouveau contrat.
        Informations obligatoires : client, montant total
        """
        WarningMessage.cancel_command_info()

        if not JWTManager.token_valid(self.user):
            return
        
        if not Permission.contract_management(self.user.role):
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
            client = ClientManager.get_client(session, warning=True)
            if not client:
                return

            contract = Contrat(
                client=client,
                montant_total=montant_total,
                montant_restant=montant_total,
                date_creation=datetime.now(),
                derniere_maj=datetime.now(),
                gestionnaire=session.query(Collaborateur
                                           ).filter_by(id=self.user.id
                                                       ).first()
            )
            session.add(contract)
            session.commit()
            self.display_contract(contract.id, SuccessMessage.create_success)

    def update_contract(self, contract_id = None):
        """
        Met à jour les informations d'un contrat existant.
        Champs modifiables :
        - Montant total
        - Montant restant dû
        """
        if not JWTManager.token_valid(self.user):
            return
        
        if not Permission.contract_management(self.user.role):
            return
        
        with self.db_manager.session_scope() as session:
            if not contract_id:
                contract = ContractManager.get_contract(session)
                if not contract:
                    return
            else:
                contract = session.query(Contrat).filter_by(id=contract_id).first()
                
            choices = [
                "Montant total",
                "Montant restant dû",
                "Retour"
            ]

            message = None

            while True:
                self.display_contract_data(contract)
                if message:
                    message()
                    message = None
                action = Utils.get_questionnary(choices, edit=True)

                match action:
                    case "Montant total":
                        message = self.update_montant_total(session, contract)
                    case "Montant restant dû":
                        message = self.update_montant_restant(session, contract)
                    case "Retour":
                        break
                    case _:
                        ErrorMessage.action_not_recognized()

    def update_montant_total(self, session, contract: Contrat):
        """
        Met à jour le montant total d'un contrat.
        """
        message = None
        current_montant_total = contract.montant_total
        while True:
            montant_total = Utils.get_input(
                "Montant total: ",
                str(contract.montant_total)
            )
            if contract.montant_total != montant_total:
                try:
                    montant_total = float(montant_total)
                    if montant_total < 0:
                        ErrorMessage.amount_negative()
                        continue
                except ValueError:
                    ErrorMessage.invalid_amount()
                    continue
                contract.montant_total = montant_total
                contract.montant_restant -= current_montant_total - montant_total
                message = SuccessMessage.update_success
                self.db_manager.update_commit(contract, session)
            return message
        
    def update_montant_restant(self, session, contract: Contrat):
        """
        Met à jour le montant restant dû d'un contrat.
        """
        message = None
        while True:
            montant_restant = Utils.get_input(
                "Montant restant dû: ",
                str(contract.montant_restant)
            )
            if contract.montant_restant != montant_restant:
                try:
                    montant_restant = float(montant_restant)
                    if montant_restant < 0:
                        ErrorMessage.amount_negative()
                        continue
                    if montant_restant > contract.montant_total:
                        ErrorMessage.remaining_gt_total()
                        continue
                except ValueError:
                    ErrorMessage.invalid_amount()
                    continue
                contract.montant_restant = montant_restant
                message = SuccessMessage.update_success
                self.db_manager.update_commit(contract, session)
            return message

    def sign_contract(self, contract_id=None):
        """
        Permet de signer un contrat.
        """
        if not JWTManager.token_valid(self.user):
            return

        with self.db_manager.session_scope() as session:
            if not contract_id:
                contract = ContractManager.get_contract(session)
                if not contract:
                    return
                client = ClientManager.get_client(session, warning=True)
                if not client:
                    return
                if contract.client != client:
                    ErrorMessage.contract_client_mismatch(contract.id, client.nom_complet)
                    return
            else:
                contract = session.query(Contrat).filter_by(id=contract_id).first()
                
            if contract.statut_signe:
                ErrorMessage.contract_already_signed(contract.id)
                return

            contract.date_signature = datetime.now()
            contract.statut_signe = True
            contract.derniere_maj = datetime.now()
            session.commit()
            self.display_contract(contract.id, SuccessMessage.sign_success)


    def delete_contract(self, contract_id=None):
        """
        Supprime un contrat.
        """
        if not JWTManager.token_valid(self.user):
            return
        
        with self.db_manager.session_scope() as session:
            if not contract_id:
                contract = ContractManager.get_contract(session)
                if not contract:
                    return
                client = ClientManager.get_client(session, warning=True)
                if not client:
                    return
                if contract.client != client:
                    ErrorMessage.contract_client_mismatch(contract.id, client.nom_complet)
                    return
            else:
                contract = session.query(Contrat).filter_by(id=contract_id).first()
            
            if not Utils.confirm_deletion():
                return

            session.delete(contract)
            session.commit()
            Utils.new_screen(self.user)
            SuccessMessage.delete_success()
