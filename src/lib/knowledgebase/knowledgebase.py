import os.path

from pyke import knowledge_engine
import logging

from pyke.knowledge_engine import CanNotProve

from src import ROOT_DIR
from src.webapp.models.ResponseDTO import ResponseDTO, ResponseTypeEnum

SOURCE_PATH = os.path.join(ROOT_DIR, "src/resources/data/")
KB_NAME = "knowledge_base"
RB_NAME = "rules_base"


class KnowledgeBase:

    def __init__(self, source_path=SOURCE_PATH):
        self.engine = knowledge_engine.engine(source_path)
        self.engine.activate(RB_NAME)
        logging.info("Started knowledge base engine")

    def prove_1_goal(self, asked) -> ResponseDTO:
        logging.debug(f'Requested prove_1_goal: \n {asked}')

        response: ResponseDTO

        try:  # try to prove on facts base
            logging.debug("Proving on facts base...")
            self.engine.prove_1_goal(f'{KB_NAME}.{asked}')
            response = ResponseDTO(ResponseTypeEnum.PROVED)
        except SyntaxError:
            response = ResponseDTO(ResponseTypeEnum.SYNTAX_ERROR)
        except CanNotProve:
            try:  # try to prove on rules base
                logging.debug("Failed.")
                logging.debug("Proving on rules base...")
                self.engine.prove_1_goal(f'{RB_NAME}.{asked}')
                response = ResponseDTO(ResponseTypeEnum.PROVED)
            except CanNotProve:  # cannot be proven
                logging.debug("Failed. Couldn't be proven.")
                response = ResponseDTO(ResponseTypeEnum.NOT_PROVED)

        logging.debug(f'Proof: \n {response.to_dict()}')

        return response

    def prove_goal(self, asked) -> ResponseDTO:

        logging.debug(f'Requested prove_goal: \n {asked}')

        response = ResponseDTO()  # default
        bases = [KB_NAME, RB_NAME]  # list of all bases
        PROVED_ON_BASE = ""  # the name of the kb with the proof

        for base in bases:  # check if can be proved with any base
            try:
                logging.debug(f"Trying to prove on {base}")

                self.engine.prove_1_goal(f'{base}.{asked}')
                PROVED_ON_BASE = base
                response.set_response_type(ResponseTypeEnum.PROVED)

                logging.debug(f"Found a proof on {base}")

            except CanNotProve:  # try the next base
                pass

            except SyntaxError:  # malformed query
                response.set_response_type(ResponseTypeEnum.SYNTAX_ERROR)
                break

        if len(PROVED_ON_BASE) == 0:  # could not be proved on any base
            response = ResponseDTO(response_type=ResponseTypeEnum.NOT_PROVED)

        else:  # get all of the proofs
            proofs = []
            logging.debug("Getting all the bindings")
            with self.engine.prove_goal(f'{PROVED_ON_BASE}.{asked}') as it:
                for variables, plan in it:
                    proofs.append(variables)

            if not variables: #if there are no bindings do not return anything
                proofs = []

            response.set_content(proofs)

        logging.debug(f'Proofs: \n {response.to_dict()}')

        return response
