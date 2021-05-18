from pyke import knowledge_engine
import logging

DEFAULT_SOURCE_PATH = "../resources/data/kb/"
KB_NAME = "knowledge_base"


class KnowledgeBase:

    def __init__(self, source_path=DEFAULT_SOURCE_PATH):
        self.engine = knowledge_engine.engine(source_path)
        self.engine.activate('knowledge_base_rules')
        logging.info("Started knowledge base engine")

    def prove_1_goal(self, asked):
        logging.debug(f'Requested prove_1_goal: \n {asked}')

        proof = self.engine.prove_1_goal(f'{KB_NAME}.{asked}')

        logging.debug(f'Proof: \n {proof}')

        return proof

    def prove_goal(self, asked, custom=False):

        kb = "knowledge_base_rules" if custom else KB_NAME

        logging.debug(f'Requested prove_goal: \n {asked}')

        proofs = []

        with self.engine.prove_goal(f'{kb}.{asked}') as it:
            for variables, plan in it:
                proofs.append(variables)

        logging.debug(f'Proofs: \n {proofs}')

        return proofs


