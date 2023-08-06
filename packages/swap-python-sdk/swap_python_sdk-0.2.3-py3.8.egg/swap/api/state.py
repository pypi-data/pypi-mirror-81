from swap.api.clients import UBLClient
from swap.api.parsers import ProgressResponseParser
from swap.common.logging import logger
from time import sleep


class State:
    def get_keys(self, input):
        return {update.message_type: update.publish_time for update in input.progress_updates}




class FinishedState(State):
    def __init__(self):
        self.name = 'finished'

    def run(self, input):
        logger.info('Entered finished state')

    def next(self, input):
        return input


class RunningState(State):
    def __init__(self):
        self.name = 'running'

    def run(self, input):
        logger.info('Entered running state')

    def next(self, input):
        keys = self.get_keys(input)

        if 'ExecutionCompletion' in keys:
            return FinishedState()

        if 'ExecutionFailure' in keys:
            return FinishedState()

        if 'ExecutionStatusUpdate' in keys:
            return RunningState()

        if 'ExecutionRequestAccept' in keys:
            return RunningState()

        raise Exception(f'No expected message types in {keys} for running state')


class WaitingState(State):
    def __init__(self):
        self.name = 'waiting'

    def run(self, input):
        logger.info('Entered waiting state')

        updates = input.progress_updates
        status_updates = [i for i in updates if i.message_type == 'ExecutionStatusUpdate']

        for update in status_updates:
            if update.exec_url != 'None':
                logger.info(f'Exec URL: {update.exec_url}')

    def next(self, input):
        keys = self.get_keys(input)

        if 'ExecutionCompletion' in keys:
            return FinishedState()

        if 'ExecutionFailure' in keys:
            return FinishedState()

        if 'ExecutionStatusUpdate' in keys:
            return RunningState()


class UnstartedState(State):
    def __init__(self):
        self.name = 'unstarted'

    def run(self, input):
        logger.info('Entered unstarted state')

    def next(self, input):
        keys = self.get_keys(input)

        if 'ExecutionRequestAccept' in keys:
            return RunningState()

        if 'ExecutionFailure' in keys:
            return FinishedState()

        raise Exception(f'No expected message types in {keys} in unstarted state')


class ProgressStateMachine:
    def __init__(self, service_chain_uuid, chain_link):
        self.chain_link = chain_link
        self.current_state = UnstartedState()
        self.data = {}
        self.parser = ProgressResponseParser()
        self.service_chain_uuid = service_chain_uuid
        self.ubl_client = UBLClient()
        self.sleep_time = 0

    def submit(self):
        url = f'/progress?service_chain_uuid={self.service_chain_uuid}'
        response = self.ubl_client.get(url)

        parsed_response = self.parser.parse(response)

        if parsed_response == 'JSONDecodeError':
            logger.info(f'The service chain uuid associated with this workflow is: {self.service_chain_uuid}')
            exit('')

        return parsed_response.chain_links[self.chain_link]

    def parse_status_updates(self, updates):
        status_updates = [i for i in updates if i.message_type == 'ExecutionStatusUpdate']

        self.data['update_messages'] = []

        for update in status_updates:
            if update.exec_status_text != 'None':
                self.data['update_messages'].append(update.exec_status_text)
            else:
                self.data['update_messages'].append('N/A')

            if update.exec_url != 'None':
                self.data['exec_url'] = update.exec_url

        self.data['update_messages'].reverse()

    def parse_execution_completion(self, updates):
        criteria = (update for update in updates if update.message_type == 'ExecutionCompletion')
        completion_update = next(criteria, None)

        if completion_update:
            self.data['status'] = 'complete'
            self.data['exec_comp_text'] = completion_update.exec_comp_text
            self.data['results_dataset'] = completion_update.results_dataset.file_uri

    def parse_execution_failure(self, updates):
        criteria = (update for update in updates if update.message_type == 'ExecutionFailure')

        failure_update = next(criteria, None)

        if failure_update:
            self.data['status'] = 'failed'
            self.data['exec_fail_text'] = failure_update.exec_fail_text

    def log_current_state(self, input):
        keys = self.current_state.get_keys(input)

        if 'ExecutionCompletion' in keys:
            logger.info(f"{keys['ExecutionCompletion']} - ExecutionCompletion")
        elif 'ExecutionFailure' in keys:
            logger.info(f"{keys['ExecutionFailure']} - ExecutionFailure")
        elif 'ExecutionStatusUpdate' in keys:
            logger.info(f"{keys['ExecutionStatusUpdate']} - ExecutionStatusUpdate")
            # FIXME KeyError
            try:
                logger.info(self.data['update_messages'][-1])
            except:
                pass
        elif 'ExecutionRequestAccept' in keys:
            logger.info(f"{keys['ExecutionRequestAccept']} - ExecutionRequestAccept")

    def update(self, response):
        updates = response.progress_updates
        self.parse_execution_completion(updates)
        self.parse_execution_failure(updates)
        self.parse_status_updates(updates)

    def run(self, input):
        while True:
            response = self.submit()
            self.current_state.run(response)
            self.update(response)
            self.log_current_state(response)

            if self.current_state.name == 'running' and input.wait:
                break

            if self.current_state.name == 'finished':
                break

            self.current_state = self.current_state.next(response)

            sleep(self.sleep_time)

        self.update(response)

        return self.data
