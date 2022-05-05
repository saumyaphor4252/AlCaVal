from flask import url_for
from flask_table import Table, Col, LinkCol


class ActionCol(Col):
    def td_contents(self, item, attr_list):
        return self.td_format(self.from_attr_list(item, attr_list), item)

    def td_format(self, content, item):
        divAction = "<div class='actions'>{mylinks}</div>"
        edit = f"<a class='cls_edit_ticket' href='/tickets/edit?prepid={content}'>Edit</a>"
        clone = f"<a class='cls_clone_ticket' href='/tickets/edit?clone={content}'>Clone</a>"
        show_relvals = f"<a class='show_relvals_{content}' href='/relvals?ticket={content}'>Show RelVals</a>"
        show_relvals = show_relvals if len(item['created_relvals']) != 0 else ""

        wf_list = f"<a class='cls_show_wf_list' href='api/tickets/relvals_workflows/{content}' title='Show list of workflows for a given ticket!'>Workflows</a>"

        matrix = f"<a href='api/tickets/run_the_matrix/{content}'>runTheMatrix.py</a>"
        jira = f"<a href='https://its.cern.ch/jira/browse/{item['jira_ticket']}' title='Go to the Jira discussion'>Jira</a>"
        create_jira = f"""<a class="cls_create_jira create_jira_{content}" onclick="create_jira('{content}')" href="javascript:void(0);">Create Jira Ticket</a> """
        jira = jira if item['jira_ticket'] != 'None' else create_jira

        delete = f"""<a class="delete_ticket delete_{content}" onclick="delete_ticket('{content}')" href="javascript:void(0);">Delete</a> """
        delete = delete if len(item['created_relvals']) == 0 else ""
        create_relval = f"""<a class="create_relval_id relval_{content}" onclick="create_alca_relval('{content}');" href="javascript:void(0);">Create Relval</a>"""
        create_relval = create_relval if item['status'] == 'new' else ""
        links = "".join([edit, clone, delete, show_relvals, wf_list, create_relval, matrix, jira])
        return divAction.format(mylinks=links)

class WFCol(Col):
    def td_format(self, content):
        workflows = ', '.join([str(a) for a in content])
        return f"<div class='bg-light'>{workflows}</div>"

class JiraCol(Col):
    def td_format(self, content):
        ticket_link = f'https://its.cern.ch/jira/browse/{content}'
        return f"<a href='{ticket_link}'>{content}</a>"

class ItemTable(Table):
    prepid = LinkCol('Prep ID', endpoint='tickets.tickets', 
                    url_kwargs=dict(prepid='prepid'), 
                    anchor_attrs={'class': 'myclass'}, attr='prepid')

    status = Col('Status')

    _id = ActionCol("Actions", td_html_attrs={'style': 'white-space: nowrap'})

    cmssw_release = LinkCol('CMSSW Release', endpoint='tickets.tickets', 
                    url_kwargs=dict(cmssw_release='cmssw_release'), 
                    anchor_attrs={}, attr='cmssw_release')

    # jira_ticket = JiraCol('Jira Ticket', td_html_attrs={'style': 'white-space: nowrap'})

    jira_ticket = LinkCol('Jira', endpoint='tickets.tickets', 
                    url_kwargs=dict(jira_ticket='jira_ticket'), 
                    anchor_attrs={}, attr='jira_ticket')

    batch_name = LinkCol('Batch Name', endpoint='tickets.tickets', 
                    url_kwargs=dict(batch_name='batch_name'), 
                    anchor_attrs={}, 
                    attr='batch_name'
                )

    cpu_cores = Col('CPU Cores')

    label = Col('Label')

    memory = Col('Memory')

    scram_arch = Col('Scram Arch')

    workflow_ids = WFCol('Workflows', td_html_attrs={'style': 'white-space: nowrap'})

    notes = Col('Notes', td_html_attrs={'style': 'white-space: nowrap'})

    allow_sort = False
    table_id = 'ticket_list'
    allow_empty = True

    #Atrributes
    html_attrs = {"style":"margin-left: 0px; width: 100%;"}
    thead_attrs = {'style': 'white-space: nowrap;'}


    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction =  'desc'
        else:
            direction = 'asc'
        return url_for('tickets.tickets', sort=col_key, direction=direction)

    def get_tr_attrs(self, item):
        return {'id': item['prepid']}
