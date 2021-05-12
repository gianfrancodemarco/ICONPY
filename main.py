from pyke import knowledge_engine

from lib.datasetcreator import create_kb

# my_engine = knowledge_engine.engine("data/kb/")
# print(my_engine.prove_1_goal('family1.son_of(frederik, $other)'))
create_kb()
my_engine = knowledge_engine.engine("data/kb/")
kbname = "knowledge_base"

while True:
    print("Ask: ", end="")
    asked = input()
    print(my_engine.prove_1_goal(f'{kbname}.{asked}'))
