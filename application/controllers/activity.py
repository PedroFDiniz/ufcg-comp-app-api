import datetime
import threading

from application.utils.email import *
from application.utils.validation import *
from application.utils.constants import AUTH_COORDINATOR_EMAIL
from application.database.psql_database import DB_ENUM_A_METRICS, DB_ENUM_A_STATE_CREATED, DB_ENUM_A_STATE_ASSIGNED, DB_ENUM_A_STATE_APPROVED, DB_ENUM_A_STATE_REJECTED
from application.models.user import User
from application.models.activity import Activity
from application.controllers.user import User_Controller
from werkzeug.datastructures import FileStorage


class Activity_Controller:
    def register(owner_email: str, voucher: FileStorage, workload: int, kind: str, description: str, start_date: datetime.datetime, end_date: datetime.datetime):
        myAssert(owner_email, AssertionError("Email não pode ser vazio.", 400))
        myAssert(voucher, AssertionError("Documento não pode ser vazio.", 400))
        myAssert(kind, AssertionError("Tipo não pode ser vazio.", 400))
        myAssert(description, AssertionError("Descrição não pode ser vazia.", 400))

        kind_obj = {}
        for act_metric in DB_ENUM_A_METRICS:
            if kind == act_metric['kind']:
                kind_obj = act_metric
                break

        if kind_obj:
            if ('workload_unity' in kind_obj.keys()) and (kind_obj['workload_unity'] == 'meses'):
                myAssert(start_date, AssertionError("Data de início não pode ser vazia.", 400))
                myAssert(end_date, AssertionError("Data de encerramento não pode ser vazia.", 400))
            activity = Activity.register(owner_email, voucher, workload, kind, description, DB_ENUM_A_STATE_CREATED, start_date, end_date)

            return activity
        else:
            raise AssertionError("Tipo da atividade inválido.", 400)

    def find_all_subm_activities(page: int, size: int, sort: str, order: str):
        activities = Activity.find_all_subm_activities(page, size, sort, order)

        activities_list = list()
        for activity in activities:
          activities_dict = Activity_Controller.map_activity_to_dict(activity)
          activities_list.append(activities_dict)

        return activities_list

    def find_by_owner_or_state(owner_email: str, states: list, page: int, size: int, sort: str, order: str):
        activities = Activity.find_by_owner_or_state(owner_email, states, page, size, sort, order)

        activities_list = list()
        for activity in activities:
          activities_dict = Activity_Controller.map_activity_to_dict(activity)
          activities_list.append(activities_dict)

        return activities_list

    def find_by_id(activity_id: int):
        activity = Activity.find_by_owner_or_state(activity_id)

        myAssert(activity, AssertionError("Atividade não encontrada.", 404))

        activity_dict = Activity_Controller.map_activity_to_dict(activity)
        return activity_dict

    def validate(activity_id: int, reviewer_email: str, state: str, computed_credits: int, justify: str):
        myAssert(reviewer_email, AssertionError("Id do revisor não pode ser vazio.", 400))
        user = User.find_by_email(reviewer_email)
        myAssert(user, AssertionError("Revisor não encontrado.", 404))

        user = User_Controller.map_user_to_dict(user)
        myAssert(user['email'] == reviewer_email, AssertionError("Revisor inválido.", 400))

        myAssert(activity_id, AssertionError("Id da atividade não pode ser vazio.", 400))

        activity = Activity.find_by_id(activity_id)
        myAssert(activity, AssertionError("Atividade não encontrada.", 404))

        activity = Activity_Controller.map_activity_to_dict(activity)
        myAssert(activity['state'] == DB_ENUM_A_STATE_ASSIGNED, AssertionError("Atividade precisa estar como atribuida.", 400))

        myAssert(state, AssertionError("Estado da atividade não pode ser vazio.", 400))
        myAssert((computed_credits and justify) != True, AssertionError("Uma mesma atividade não pode conter justificativa e creditos computados.", 400))

        thread = threading.Thread(target=send_noreply_email_validate(activity['owner_email'], activity['description'], activity['reviewer_email']))
        thread.start()

        thread = threading.Thread(target=send_noreply_email_validate(AUTH_COORDINATOR_EMAIL, activity['description'], activity['reviewer_email']))
        thread.start()

        state = state.upper()
        if state == DB_ENUM_A_STATE_APPROVED:
            myAssert(int(computed_credits) > 0, AssertionError("Quantidade de créditos computados precisa ser maior que 0.", 400))
            Activity.validate(activity_id, state, computed_credits, None)
        elif state == DB_ENUM_A_STATE_REJECTED:
            myAssert(justify, AssertionError("Justificativa não pode ser vazia.", 400))
            Activity.validate(activity_id, state, None, justify)
        else:
            raise AssertionError("Estado inválido.", 400)

    def assign(activity_id: int, reviewer_email: str):
        user = User.find_by_email(reviewer_email)
        myAssert(user, AssertionError("Revisor não encontrado.", 404))

        user = User_Controller.map_user_to_dict(user)
        myAssert(user['email'] == reviewer_email, AssertionError("Revisor inválido.", 400))

        myAssert(activity_id, AssertionError("Id da atividade não pode ser vazio.", 400))

        activity = Activity.find_by_id(activity_id)
        myAssert(activity, AssertionError("Atividade não encontrada.", 404))

        activity = Activity_Controller.map_activity_to_dict(activity)
        myAssert(activity['state'] == DB_ENUM_A_STATE_CREATED, AssertionError("Atividade precisa estar como criada.", 400))

        thread = threading.Thread(target=send_noreply_email_assign(reviewer_email))
        thread.start()

        Activity.assign(activity_id, reviewer_email, DB_ENUM_A_STATE_ASSIGNED)

    def count_by_owner_or_state(owner_email: str, states: list):
        count = Activity.count_by_owner_or_state(owner_email, states)
        return count

    def compute_credits(owner_email: str):
        myAssert(owner_email, AssertionError("Email não pode ser vazio.", 400))

        activities = Activity.find_by_owner_or_state(owner_email, [DB_ENUM_A_STATE_APPROVED], None, None, None, None)

        computed_credits = 0
        missing_credits = 22
        for activity in activities:
            computed_credits += activity[10] 
        
        if computed_credits > missing_credits:
            missing_credits = 0
        else:
            missing_credits -= computed_credits

        return {
            'computed_credits': computed_credits,
            'missing_credits': missing_credits
        }

    def get_metrics():
        metrics = Activity.get_metrics()
    
        metrics_list = list()
        for m in metrics:
          metric_dict = Activity_Controller.map_matrics_to_dict(m)
          metrics_list.append(metric_dict)

        return metrics_list

    def map_matrics_to_dict(metric):
        return {
            'kind': metric[0],
            'credits_limit': metric[1],
            'workload_unity': metric[2],
        }

    def map_activity_to_dict(activity: tuple):
        return {
            'id': activity[0],
            'owner_email': activity[1],
            'reviewer_email': activity[2],
            'kind': activity[3],
            'workload': activity[4],
            'start_date': activity[5],
            'end_date': activity[6],
            'state': activity[7],
            'description': activity[8],
            'voucher_path': activity[9],
            'computed_credits': activity[10],
            'justify': activity[11],
            'creation_time': activity[12],
            'updated_time': activity[13],
            'workload_unity': activity[14]
            # 'full_period': activity[4] + ' ' + activity[14]
        }
